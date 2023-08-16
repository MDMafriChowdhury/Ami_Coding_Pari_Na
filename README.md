# Ami Coding Pari Na

"Ami Coding Pari Na" is a web application developed using the Django framework. It provides user authentication, a search feature, and an API endpoint to retrieve input values.

## Features

- User Registration and Login: Users can register and log in to the application.
- Khoj Search: Users can input comma-separated integers and a search value. The application will store the input values, sort them, and check if the search value exists.
- API Endpoint: An API endpoint allows users to retrieve all their previously entered input values within a specific date range.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python (>= 3.6)
- Django (>= 3.0)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/amicodingparina_project.git
   cd amicodingparina_project

2. Create a virtual environment (optional but recommended):

      ```sh
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
## Usage
1. Apply migrations:

      ```sh
      python manage.py migrate
2. Run the development server:
      ```sh
      python manage.py runserver
3. Access the application in your browser at http://127.0.0.1:8000/.

## API Endpoint

- To access the API endpoint for retrieving input values, use the following URL:
   http://127.0.0.1:8000/api/get-all-input-values/
- Provide query parameters start_datetime, end_datetime, and user_id to specify the date range and user.
