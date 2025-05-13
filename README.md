# NYC Taxi Trip Data Batch Processing Pipeline

## Overview
This project implements a batch processing pipeline for NYC taxi trip data using Docker microservices. The pipeline ingests Yellow Taxi trip data, extracts the pickup hour, aggregates trip counts by hour, and stores the results in MongoDB. A Flask API (`/api/taxi_data`) provides access to the aggregated data. The system is deployed locally for development, ensuring reproducibility and demonstrating core data processing capabilities.

## Project Structure
- `config/`: Contains `Dockerfile` and `requirements.txt`.
- `src/`: Contains the pipeline code (`pipeline.py`).
- `nyc_taxi_data.csv`: Full dataset (12.7 million rows, not included in repo due to size).
- `nyc_taxi_data_small.csv`: Smaller dataset for testing (10,000 rows, not included in repo due to size).
- `docker-compose.yml`: Docker Compose configuration for microservices.
- `github_link.txt`: Contains the GitHub repository link for submission.

## Setup Instructions
### Prerequisites
- Docker Desktop installed on your machine.
- Git installed to clone the repository.
- NYC taxi trip dataset (`nyc_taxi_data.csv`) downloaded and placed in the project root directory.

### Steps to Run
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/EkashreeK/nyc-taxi-pipeline.git
   cd nyc-taxi-pipeline
   ```
2. **Download the Dataset**:
   - Download the NYC Yellow Taxi trip data (e.g., from NYC Open Data) and place it as `nyc_taxi_data.csv` in the project root directory.
   - Alternatively, create a smaller dataset for testing:
     ```cmd
     powershell -Command "Get-Content nyc_taxi_data.csv -TotalCount 10001 | Set-Content nyc_taxi_data_small.csv"
     ```
3. **Configure the Dataset**:
   - For the smaller dataset, ensure `pipeline.py` has `DATA_PATH = "./nyc_taxi_data_small.csv"` and `docker-compose.yml` mounts this file.
   - For the full dataset, update `pipeline.py` to `DATA_PATH = "./nyc_taxi_data.csv"` and ensure `docker-compose.yml` mounts this file.
4. **Build and Run the Docker Containers**:
   ```cmd
   docker-compose up --build
   ```
5. **Query the API**:
   - Wait for the pipeline to process the data, then query the API:
     ```cmd
     curl http://localhost:5000/api/taxi_data
     ```
6. **Verify Data in MongoDB**:
   - Connect to the MongoDB container:
     ```cmd
     docker exec -it nyc-taxi-prediction-mongo-1 mongosh
     ```
   - Query the data:
     ```
     use taxi_db
     db.processed_data.find()
     ```

## Results
The pipeline was tested with the smaller dataset (`nyc_taxi_data_small.csv`, 10,000 rows). The API (`/api/taxi_data`) returned the following aggregated trip counts by pickup hour:
```json
[
    {"pickup_hour": 12, "trip_count": 499},
    {"pickup_hour": 22, "trip_count": 411},
    {"pickup_hour": 1, "trip_count": 285},
    {"pickup_hour": 13, "trip_count": 406},
    {"pickup_hour": 16, "trip_count": 465},
    {"pickup_hour": 6, "trip_count": 177},
    {"pickup_hour": 3, "trip_count": 65},
    {"pickup_hour": 20, "trip_count": 588},
    {"pickup_hour": 5, "trip_count": 66},
    {"pickup_hour": 19, "trip_count": 868},
    {"pickup_hour": 15, "trip_count": 406},
    {"pickup_hour": 9, "trip_count": 467},
    {"pickup_hour": 17, "trip_count": 577},
    {"pickup_hour": 4, "trip_count": 44},
    {"pickup_hour": 8, "trip_count": 391},
    {"pickup_hour": 23, "trip_count": 651},
    {"pickup_hour": 7, "trip_count": 479},
    {"pickup_hour": 10, "trip_count": 502},
    {"pickup_hour": 21, "trip_count": 756},
    {"pickup_hour": 11, "trip_count": 236},
    {"pickup_hour": 14, "trip_count": 568},
    {"pickup_hour": 2, "trip_count": 88},
    {"pickup_hour": 0, "trip_count": 518},
    {"pickup_hour": 18, "trip_count": 487}
]
```
The total trip count (10,000) matches the dataset size, confirming correct aggregation. The pipeline has been prepared to scale to the full dataset (12.7 million rows).

## System Qualities
- **Reliability**: Error handling and logging are implemented throughout the pipeline.
- **Scalability**: Spark partitioning (`spark.sql.shuffle.partitions=400`) ensures scalability for large datasets.
- **Maintainability**: Dockerized microservices and a modular code structure enhance maintainability.
- **Data Security**: Local deployment minimizes exposure; future enhancements could include authentication.
- **Governance**: Code is version-controlled in Git, with clear documentation.
- **Protection**: No sensitive data is exposed in the current setup.

## Future Improvements
- Add authentication for the API and MongoDB.
- Optimize Spark memory settings for the full dataset.
- Implement data validation before ingestion.
- Deploy to a cloud environment for production use.
