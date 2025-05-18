from flask import Flask, jsonify, request, abort
  from pymongo import MongoClient
  import logging
  
  logger = logging.getLogger(__name__)
  app = Flask(__name__)
  API_KEY = "your-secret-key"  # Replace with a secure key in production
  
  def require_api_key(func):
      def wrapper(*args, **kwargs):
          api_key = request.headers.get('X-API-Key')
          if api_key and api_key == API_KEY:
              return func(*args, **kwargs)
          else:
              abort(401, description="Unauthorized: Missing or invalid API key")
      wrapper.__name__ = func.__name__
      return wrapper
  
  def get_mongo_collection():
      try:
          client = MongoClient("mongodb://mongo:27017/")
          db = client["taxi_db"]
          return db["processed_data"], client
      except Exception as e:
          logger.error("Error connecting to MongoDB: %s", e, exc_info=True)
          raise
  
  @app.route("/api/taxi_data", methods=["GET"])
  @require_api_key
  def get_taxi_data():
      try:
          collection, client = get_mongo_collection()
          data = list(collection.find({}, {"_id": 0}))
          client.close()
          if not data:
              return jsonify({"error": "No data found"}), 404
          return jsonify(data)
      except Exception as e:
          logger.error("Error fetching data: %s", e, exc_info=True)
          return jsonify({"error": str(e)}), 500
  
  @app.route("/api/taxi_data/<int:hour>", methods=["GET"])
  @require_api_key
  def get_taxi_data_by_hour(hour):
      if hour < 0 or hour > 23:
          return jsonify({"error": "Hour must be between 0 and 23"}), 400
      try:
          collection, client = get_mongo_collection()
          data = collection.find_one({"pickup_hour": hour}, {"_id": 0})
          client.close()
          if not data:
              return jsonify({"error": f"No data found for hour {hour}"}), 404
          return jsonify(data)
      except Exception as e:
          logger.error("Error fetching data for hour %d: %s", hour, e, exc_info=True)
          return jsonify({"error": str(e)}), 500
  
  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=5000, debug=False)
