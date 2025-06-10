# Restaurant Recommendation System - Backend

This directory contains the backend services for the Restaurant Recommendation System. It is a Python-based Flask application that serves a REST API to the frontend, handles business logic, and interacts with the MongoDB database.

## 🎯 Backend Overview

The backend is responsible for:
-   **API Endpoints**: Providing data to the frontend for restaurants, user preferences, and recommendations.
-   **Recommendation Engine**: Running the core machine learning logic to generate personalized restaurant suggestions.
-   **Database Interaction**: Managing all communication with the MongoDB database, including storing and retrieving user data, restaurant information, and user ratings.
-   **User Management**: Handling user creation, preference storage, and profile updates.

## 🛠️ Tech Stack

-   **Framework**: [Flask](https://flask.palletsprojects.com/)
-   **Database**: [MongoDB](https://www.mongodb.com/) (accessed via [PyMongo](https://pymongo.readthedocs.io/))
-   **Machine Learning**: [scikit-learn](https://scikit-learn.org/stable/)
-   **Data Manipulation**: [NumPy](https://numpy.org/) & [Pandas](https://pandas.pydata.org/)
-   **Environment Management**: `venv`

## 🚀 Getting Started

These instructions assume you are in the `backend` directory.

### 1. Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root of the project (`res-rec-system/`) by copying the example file. The backend will read its configuration from there.
```bash
cp ../env.example ../.env
```
Ensure the variables like `MONGODB_URI` and `DATABASE_NAME` are correctly set.

### 4. Run the Server
```bash
flask run
```
The backend API will now be running, typically at `http://127.0.0.1:5000`.

## 📁 Project Structure
