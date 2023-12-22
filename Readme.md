# Employee Backend

A simple microservice for an HR company that populates the employee search directory.

## Installation

### Docker installation:

`docker-compose up -d`

### Local installation:

Install dependencies:

`pip install -r ./requirements.txt`

Migrate the database:

`python manage.py migrate`

Run the app:

`python manage.py runserver`

I also provided some utility scripts for data seeding.

Generate some data:

`python manage.py runscripts seed_data`

Clear data:

`python manage.py runscripts clear_data`

Run unit tests:

`python manage.py test`

## Usage

The application runs with default port 8000. The swagger page can be accessed at http://localhost:8000/swagger/