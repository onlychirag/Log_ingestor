
# Log Ingestor and Search Project

## Project Overview

This Django project is designed to ingest log data and provide a full-text search functionality with various filters. Currently, the search functionality is under active development and will soon support efficient and comprehensive querying capabilities. It uses Elasticsearch for indexing and searching logs, Celery for asynchronous task processing, and PostgreSQL as the database backend.

## Features

- Ingestion of log data into Elasticsearch.
- Full-text search across logs with filters such as log level, message, resourceId, timestamp, traceId, spanId, commit, and metadata.parentResourceId (Under Development).
- Asynchronous task processing with Celery.
- Efficient and quick search results.
- Robust data storage with PostgreSQL.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Elasticsearch 7.x
- PostgreSQL
- Celery
- RabbitMQ (or another Celery broker)

### Setup

1. **Clone the Repository**
   ```
   git clone [repository-url]
   cd log_ingestor
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Configure Elasticsearch**
   - Ensure Elasticsearch is installed and running on your system.
   - Update `log_ingestor/log_ingestor/elasticsearch_conf.py` with your Elasticsearch configuration.

4. **Configure PostgreSQL**
   - Set up a PostgreSQL database.
   - Update the `DATABASES` setting in `log_ingestor/log_ingestor/settings.py` with your PostgreSQL database credentials.

5. **Configure Celery**
   - Ensure RabbitMQ or your chosen broker is set up and running.
   - Update the Celery configuration in `log_ingestor/log_ingestor/celery.py`.

6. **Database Migrations**
   ```
   python manage.py migrate
   ```

7. **Running the Application**
   ```
   python manage.py runserver
   ```

8. **Running Celery Worker**
   ```
   celery -A log_ingestor worker --loglevel=info
   ```

## Usage

1. **Accessing the Application**
   - Open a web browser and navigate to `http://localhost:8000/`.

2. **Log Ingestion**
   - Use the provided endpoints to ingest log data into the system.

3. **Searching Logs (Under Development)**
   - The full-text search functionality with various filters is currently in progress. Once completed, it will be accessible at `http://localhost:8000/search/`.
   - Users will be able to enter search criteria and filters to find specific log entries efficiently.

## Contributing

Contributions to this project are welcome. Please follow the standard procedures for contributing to open-source projects:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).
