# Project Name: IMDB Movies ETL Pipeline with Airflow and Docker

This project is an ETL (Extract, Transform, Load) pipeline that extracts data about movies from IMDB, transforms it into a structured format, and loads it into a PostgreSQL database using Airflow and Docker. The project is implemented using Python, Airflow, and several libraries such as BeautifulSoup, Pandas, Requests, and psycopg2.

## Data Source
The data is extracted from the IMDB website using web scraping techniques.

## Extract
The data is extracted from IMDB using the Requests library in Python to send HTTP requests to the IMDB website and the BeautifulSoup library to parse the HTML content of the website and extract the relevant data.

## Transform
The extracted data is transformed into a structured format using the Pandas library in Python. The data is cleaned, filtered, and transformed as required to prepare it for loading into the database.

## Load
The transformed data is loaded into a PostgreSQL database using the psycopg2 library in Python.

## Airflow
The pipeline is orchestrated and scheduled using Apache Airflow. The DAG (Directed Acyclic Graph) file defines the tasks and their dependencies. The tasks include extracting, transforming.

## Docker
The pipeline is run using Docker containers. The Dockerfile defines the image used to run the pipeline. The docker-compose.yml file defines the services used, including the Airflow web server, scheduler, and worker, as well as the PostgreSQL database.

## Dependencies
- Python
- BeautifulSoup
- Pandas
- Requests
- psycopg2
- Apache Airflow
- Docker
- PostgreSQL

## Usage
1. Clone the project repository
2. Install Docker and Docker Compose
3. Run the `docker-compose up` command to start the services
4. Access the Airflow web server at http://localhost:8081
5. Enable the DAG
