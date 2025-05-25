# NYC Taxi Trip Data Batch Processing Pipeline

## Overview
This project implements a batch processing pipeline for NYC Taxi trip data using Apache Spark, MongoDB, and Flask. The pipeline processes a large dataset (12.7 million rows) of taxi trips, aggregates the data by pickup hour, stores the results in MongoDB, and serves the data via a Flask API.

### Project Structure
- **src/**: Contains the application code.
  - `main.py`: Orchestrates the pipeline, running it once (previously scheduled every 10 seconds).
  - `ingest.py`: Ingests data from a CSV file into a Spark DataFrame with a defined schema.
  - `process.py`: Processes the data by extracting the pickup hour and aggregating trip counts.
  - `store.py`: Stores the processed data in MongoDB, overwriting the collection to avoid duplicates.
  - `api.py`: Flask API to serve the processed data with endpoints `/api/taxi_data` and `/api/taxi_data/<hour>`.
- **config/**: Contains configuration files.
  - `Dockerfile`: Defines the Docker image for both `api` and `pipeline` services.
  - `requirements.txt`: Lists Python dependencies (shared across services).
- **docker-compose.yml**: Defines the services (`mongo`, `api`, `pipeline`) and their configurations.

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd nyc-taxi-prediction
   ```
2. **Prepare the Dataset**:
   - Place `nyc_taxi_data.csv` (12.7 million rows) in the project directory.
3. **Run the Pipeline**:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```
   - The `pipeline` service runs once, processes the data, and exits.
   - The `api` and `mongo` services continue running.
4. **Access the API**:
   - Get all data: `curl -H "X-API-Key: your-secret-key" http://localhost:5000/api/taxi_data`
   - Get data for a specific hour: `curl -H "X-API-Key: your-secret-key" http://localhost:5000/api/taxi_data/19`
