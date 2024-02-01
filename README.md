# Catalyst-count Django Project

## Overview

Catalyst-count is a Django project designed to manage user data and interactions with a PostgreSQL database hosted on AWS RDS. The project includes functionality for adding users, uploading data to the PostgreSQL server, a query builder to execute database queries, and a user login system using Django authentication.

## Setup

### 1. PostgreSQL Setup on AWS RDS

- Install PostgreSQL server on AWS RDS.
- Use a tool like DBeaver to connect to the AWS RDS server.
- Create a database named `catdb`.
- Create a table named `company` for the Catalyst-count project.

### 2. Local Django Project Setup

- Create a Django project on your local system named `catalyst_count`.
- Create an app inside the project named `catapp`.

### 3. Project Features

- **Add User:**
  - Implement views, templates, and URLs to facilitate user registration.
  - Users can input their details, which are then stored users-data of the admin panel.

- **Upload Data to PostgreSQL:**
  - Design functionality to upload data to the PostgreSQL server.
  - Ensure data is correctly stored in the `company` table.

- **Query Builder:**
  - Develop a query builder to execute custom queries on the `catdb` database.

- **Display Users:**
  - Create views and templates to display available users.
  - Users can view a list of registered users on the "Display Users" page.

- **User Login:**
  - Implement Django authentication for user login.
  - Users can securely log in and access specific features based on their roles.

## Usage

1. Install the required dependencies using:
  - using the requiremnet.txt (present in the project directory)
    -  pip install -r requirements.txt
2. Run the Django development server:
  - python manage.py runserver

3. Access the application at `http://localhost:8000/`.

## Contributors

- [Amish Khatu]

Feel free to contribute or report issues by creating a pull request or raising an issue in the repository.

