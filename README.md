# Catalog - "МЕЧТА"

## Project Description

An online store project that will be finalized in each lesson throughout the course.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/PaulBitHub/Catalog_DjPr]
cd Catalog_DjPr
```
### 2. Copy the env.example file to .env:

Open.env and replace the values of the variables with your own

```bash
cp .env.example .env
```

### 3. Install Dependencies
The project uses Poetry for dependency management. Ensure Poetry is installed, then run the following command to install all dependencies:
```bash
poetry shell
poetry install
```
### 4. Start Migrations
To start migrations, use the following command:
```bash
python3 manage.py migrate
```

### 5. Load Fixture
Loading test fixtures for the database:
```bash
python3 manage.py load_fixtures
```

### 6. Create Superuser
Enter the command in the terminal:
```bash
python3 manage.py csu
```
or
```bash
python manage.py csu --email=example@example.com --password=SuperSecretPassword123
```

### 6. Run Server
To run server, use the following command:
```bash
python3 manage.py runserver
```
The server will be available at http://127.0.0.1:8000
