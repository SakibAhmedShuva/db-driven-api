# 🚀 Database-Driven API

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Backend-Supabase-green.svg)](https://supabase.io/)

*A generic, database-driven REST API backend built with Python, Flask, and Supabase*

[Features](#-features) • [Getting Started](#-getting-started) • [API Documentation](#-api-endpoint-documentation) • [Database Schema](#-database-schema)

</div>

---

## 📖 Overview

A robust and scalable REST API template that demonstrates the **database-driven architecture** approach. This project serves as a production-ready foundation for building APIs where endpoints primarily query and serve data from a well-defined database schema.

> **Example Use Case:** Marine Business Directory - A comprehensive platform for discovering marine businesses, marinas, and boat services.

### 💡 Core Concept

The **database-driven approach** means your application's structure and capabilities are fundamentally shaped by the database schema. Instead of complex business logic scattered across the application layer, the API acts as a clean, efficient interface to your data - making it easier to manage, scale, and maintain.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **[Flask](https://flask.palletsprojects.com/)** | Lightweight Python web framework |
| **[Supabase](https://supabase.io/)** | PostgreSQL database with built-in APIs |
| **[supabase-py](https://github.com/supabase-community/supabase-py)** | Official Python client |
| **[python-dotenv](https://github.com/theskumar/python-dotenv)** | Environment variable management |
| **[Flask-CORS](https://flask-cors.readthedocs.io/)** | Cross-Origin Resource Sharing support |

---

## ✨ Features

- 🔌 **RESTful API** - Clean, well-defined endpoints following REST principles
- 🗄️ **Database-First Design** - Comprehensive SQL schema drives application structure
- 🔐 **Token-Based Authentication** - Secure endpoints using Bearer Token authorization
- ⚙️ **Environment Configuration** - Sensitive data managed via `.env` files
- 🌐 **CORS Enabled** - API accessible from different domains
- 💚 **Health Check Endpoint** - Monitor service status and database connectivity
- 📈 **Scalable Architecture** - Built on Supabase for robust, enterprise-grade infrastructure
- 📊 **Analytics Ready** - Built-in tracking for search queries and user interactions

---

## 📡 API Endpoint Documentation

> **Authentication:** All protected endpoints require an `Authorization: Bearer {{api_token}}` header.

### Public Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/health` | Health check for API and database | `200 OK` with status |

### Protected Endpoints

#### 📂 Reference Data

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/categories` | Get all business categories (ID: Name mapping) |
| `GET` | `/api/locations` | Get all available locations (ID: Name mapping) |
| `GET` | `/api/stats` | Get system statistics (table counts) |

#### 🔍 Search & Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/search` | Search companies by category, location, and term |
| `GET` | `/api/user/status` | Get user subscription status and query limits |

---

### 🔎 Detailed Endpoint Specifications

#### `GET /api/search`

Search for companies with filtering options.

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `category_id` | `integer` | Category ID to filter by |
| `location_id` | `integer` | Location ID to filter by |

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search_term` | `string` | Filter by company name, description, or keywords |

**Example Request:**
```http
GET /api/search?category_id=1&location_id=1&search_term=luxury
Authorization: Bearer your_api_token_here
```

---

#### `GET /api/user/status`

Retrieve user subscription information and query limits.

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `phone_number` | `string` | User's phone number with country code |

**Example Request:**
```http
GET /api/user/status?phone_number=+6591234567
Authorization: Bearer your_api_token_here
```

---

## 🗃️ Database Schema

The comprehensive database schema (`SQL.txt`) includes:

| Table | Purpose |
|-------|---------|
| `users` | User profiles, subscription tiers, query limits |
| `companies` | Business listings with details and contact info |
| `categories` | Business classification (Marinas, Repair, etc.) |
| `locations` | Geographic location management |
| `conversations` | User interaction logs |
| `search_queries` | Search analytics and patterns |
| `feedback` | User feedback and ratings |
| `api_logs` | API usage tracking |

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ [Supabase](https://supabase.com/) account (free tier available)
- ✅ [Git](https://git-scm.com/) installed

---

### Step 1: Set Up Supabase

#### 1.1 Create a Project

1. Navigate to your [Supabase Dashboard](https://app.supabase.io/)
2. Click **"New Project"**
3. Fill in project details and create
4. Save your **Project URL** and **Service Role Key** (found in Project Settings → API)

#### 1.2 Initialize Database Schema

1. Open the **SQL Editor** in your Supabase dashboard
2. Copy the contents of `SQL.txt` from this repository
3. Paste and execute the SQL to create tables and functions
4. **(Optional)** Run `SQL_Mock Data.txt` to populate with sample data

---

### Step 2: Local Setup

#### 2.1 Clone the Repository

```bash
git clone https://github.com/your-username/db-driven-api.git
cd db-driven-api
```

#### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.4 Configure Environment Variables

Create a `.env` file in the project root:

```env
# Supabase Configuration
SUPABASE_URL="https://your-project-ref.supabase.co"
SUPABASE_SERVICE_KEY="your-supabase-service-role-key"

# API Security
API_TOKEN="your_secure_token_here"
```

> ⚠️ **Security Note:** Keep your `.env` file private and never commit it to version control!

---

### Step 3: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output similar to:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

🎉 **Success!** Your API is now running at `http://localhost:5000`

---

## 🧪 Usage & Testing

### Testing with Postman

The easiest way to test your API is using the included Postman collection.

#### 1. Import Collection

- Open Postman
- Click **Import** → **File**
- Select `postman_collection.json` from this repository

#### 2. Configure Variables

In the imported collection:

1. Go to **Variables** tab
2. Set `baseUrl` to `http://localhost:5000`
3. Set `api_token` to your token from `.env`

#### 3. Start Testing

- Begin with **Public → Health Check** to verify the server
- Explore protected endpoints with pre-configured requests
- Modify parameters to test different scenarios

### Testing with cURL

```bash
# Health Check
curl http://localhost:5000/health

# Search Companies (requires authentication)
curl -H "Authorization: Bearer your_api_token_here" \
  "http://localhost:5000/api/search?category_id=1&location_id=1"
```

---

## 📁 Project Structure

```
db-driven-api/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── SQL.txt                   # Database schema
├── SQL_Mock Data.txt         # Sample data
├── postman_collection.json   # API testing collection
├── README.md                 # This file
└── LICENSE                   # MIT License
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [Supabase](https://supabase.io/)
- Inspired by database-driven architecture principles

---

<div align="center">

**[⬆ Back to Top](#-database-driven-api)**

Made with ❤️ by developers, for developers

</div>
