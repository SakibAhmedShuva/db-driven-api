# db-driven-api

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Backend-Supabase-green.svg)](https://supabase.io/)

A generic, database-driven REST API backend built with Python, Flask, and Supabase. This project serves as a robust template for creating a service where the API endpoints are primarily responsible for querying and serving data from a pre-defined database schema. It includes authentication, environment configuration, and a clear structure for easy extension.

The example business case used in this repository is a **Marine Business Directory**.

---

## Table of Contents

- [Core Concept](#core-concept)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [API Endpoint Documentation](#api-endpoint-documentation)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Set Up Supabase](#1-set-up-supabase)
  - [2. Local Setup](#2-local-setup)
  - [3. Run the Application](#3-run-the-application)
- [Usage & Testing](#usage--testing)
- [License](#license)

---

## Core Concept

The "database-driven" approach means that the application's logic, structure, and capabilities are fundamentally shaped by the database schema. Instead of having complex business logic in the application layer, the API acts as a clean and efficient interface to the data, making it easy to manage and scale.

This repository demonstrates this concept by building an API on top of a comprehensive Supabase PostgreSQL schema.

## Technology Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
- **Database**: [Supabase](https://supabase.io/) (PostgreSQL)
- **Python Libraries**:
  - `supabase-py`: Official Python client for Supabase.
  - `python-dotenv`: For managing environment variables.
  - `Flask-Cors`: For handling Cross-Origin Resource Sharing (CORS).
- **Development Tool**: [Postman](https://www.postman.com/) for API testing.

## Features

-   **RESTful API**: Clean, well-defined endpoints for interacting with data.
-   **Database-First Design**: A comprehensive SQL schema that defines the application's structure.
-   **Token-Based Authentication**: Secure endpoints using a Bearer Token.
-   **Environment Configuration**: All sensitive keys and settings are managed via a `.env` file.
-   **CORS Enabled**: Allows the API to be accessed from different domains.
-   **Health Check**: A public `/health` endpoint for monitoring service status.
-   **Scalable Architecture**: Built on Supabase for robust, scalable backend infrastructure.

---

## API Endpoint Documentation

All protected endpoints require an `Authorization: Bearer {{api_token}}` header.

### Public Endpoints

| Method | Endpoint      | Description                                                                                             |
| :----- | :------------ | :------------------------------------------------------------------------------------------------------ |
| `GET`  | `/health`     | Checks the health of the API and its database connection. Returns a `200 OK` with status `healthy`.       |

### Protected API Endpoints

| Method | Endpoint             | Description                                                                    |
| :----- | :------------------- | :----------------------------------------------------------------------------- |
| `GET`  | `/api/categories`    | Retrieves a list of all available company categories as an `ID: Name` mapping. |
| `GET`  | `/api/locations`     | Retrieves a list of all available locations as an `ID: Name` mapping.        |
| `GET`  | `/api/search`        | Searches for companies based on query parameters.                              |
| `GET`  | `/api/user/status`   | Retrieves the subscription status and query limits for a given user.           |
| `GET`  | `/api/stats`         | Retrieves internal system statistics (total counts for tables).                |

#### `GET /api/search`

Search for companies with the required `category_id` and `location_id`.

**Query Parameters:**

| Parameter     | Type      | Required | Description                                                                 |
| :------------ | :-------- | :------- | :-------------------------------------------------------------------------- |
| `category_id` | `integer` | **Yes**  | The ID of the category to search within.                                    |
| `location_id` | `integer` | **Yes**  | The ID of the location to search within.                                    |
| `search_term` | `string`  | No       | An optional term to filter results by company name, description, or keywords. |

**Example:**
`{{baseUrl}}/api/search?category_id=1&location_id=1&search_term=luxury`

#### `GET /api/user/status`

Retrieves the subscription status for a user.

**Query Parameters:**

| Parameter      | Type     | Required | Description                                     |
| :------------- | :------- | :------- | :---------------------------------------------- |
| `phone_number` | `string` | **Yes**  | The user's phone number, including country code. |

**Example:**
`{{baseUrl}}/api/user/status?phone_number=+6591234567`

---

## Database Schema

The database schema is defined in `SQL.txt` and includes tables for managing:

-   `users`: User profiles, subscription tiers, and query limits.
-   `companies`: Business listings with details, locations, and categories.
-   `categories`: Business categories (e.g., Marinas, Boat Repair).
-   `locations`: Geographical locations.
-   `conversations`: Logs of user interactions.
-   `search_queries`: Analytics on user search behavior.
-   ...and more for logging, feedback, and metrics.

---

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

-   Python 3.8+ and Pip
-   A free [Supabase](https://supabase.com/) account
-   [Git](https://git-scm.com/)

### 1. Set Up Supabase

1.  **Create a Supabase Project**:
    -   Go to your [Supabase Dashboard](https://app.supabase.io/) and create a new project.
    -   Save your **Project URL** and **`service_role` Key**.

2.  **Set Up the Database Schema**:
    -   Navigate to the **SQL Editor** in your Supabase project.
    -   Open the `SQL.txt` file from this repository, copy its content, and run it in the SQL Editor to create the tables and functions.
    -   (Optional) For testing, open `SQL_Mock Data.txt`, copy its content, and run it to populate your database with sample data.

### 2. Local Setup

1.  **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/db-driven-api.git
    cd db-driven-api
    ```

2.  **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    -   Create a file named `.env` in the root of the project.
    -   Copy the following content into it and replace the placeholder values with your Supabase credentials and a secure API token of your choice.

    ```env
    # Supabase credentials from your project's "API" settings
    SUPABASE_URL="https://your-project-ref.supabase.co"
    SUPABASE_SERVICE_KEY="your-supabase-service-role-key"

    # A secure, custom token for your API
    API_TOKEN="ssg_secure_token_2025"
    ```

### 3. Run the Application

Start the Flask development server with the following command:

```sh
python app.py
