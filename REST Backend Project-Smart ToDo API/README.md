# Smart ToDo API

Smart ToDo API is a RESTful backend application for managing tasks with secure user authentication.  
It is built using **FastAPI**, **MongoDB Atlas**, and **JWT authentication**.

## Features

- User Registration and Login
- JWT-based Authentication
- Secure password hashing using bcrypt
- Create, Read, Update, and Delete (CRUD) operations for tasks
- MongoDB Atlas (NoSQL database)
- Interactive API documentation using Swagger (OpenAPI)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Smart-ToDo-API.git
cd Smart-ToDo-API

# Install Dependencies
pip install -r requirements.txt

Create a .env file in the project root directory and add the following:
MONGO_URI=mongodb+srv://todo_admin:Anshu%4003@cluster0.l1cqewp.mongodb.net/?appName=Cluster0

# Run the Application
python -m uvicorn main:app --reload

Once the server is running, open the following URL in your browser:
http://127.0.0.1:8000/docs


#How Authentication Works

User registers using /register

User logs in using /login and receives a JWT token

The token is passed in the Authorization header as:
Bearer <token>

Authorized users can access protected task endpoints