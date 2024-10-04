# Inventory Management System

This project implements a backend API for an Inventory Management System using Django Rest Framework (DRF). The API provides secure access to manage inventory items, using JWT-based authentication to protect endpoints. The system is designed to handle CRUD operations (Create, Read, Update, Delete) for items, with Redis caching integrated for performance optimization. The project also includes unit tests to verify the functionality and a logging system for monitoring and debugging.


## Features

- **User Authentication**: JWT-based user authentication using Django Rest Framework’s Simple JWT.
Endpoints for registering users and logging in to obtain JWT tokens.

- **CRUD Operations on Inventory Items**: Create, Read, Update, and Delete operations for items in the inventory.
Proper error handling and response codes for each operation.

- **Redis Caching**: Caching of frequently accessed items on the Read Item endpoint.
Cached items are stored in Redis for a specified timeout to improve performance.

- **Logging**: Integrated logging system that tracks API usage, errors, and important events.
Logs are written to both the console and a log file.

- **Unit Testing**: Comprehensive unit tests for all endpoints, covering both success and failure scenarios.
Tests include authentication, CRUD operations, caching behavior, and error handling.



# Tech Stack
- **Backend**:  Django, Django Rest Framework
- **Authentication**: JWT (JSON Web Token) using djangorestframework-simplejwt
- **Database**: PostgreSQL or MySQL
- **Caching**: Redis
- **Testing**: Django’s built-in test framework
- **Logging**: Python's built-in logging module



# Setup Instructions
**1. Clone the Repository**
```
git clone https://github.com/Sajal-techie/Inventory-System
```

**2. Create and Activate a Virtual Environment**
```
python -m venv venv
source venv/bin/activate  
# For Windows use: venv\Scripts\activate
```

**3. Install Dependencies**
```
pip install -r requirements.txt
```

**4. Setup Database**
 - Configure the PostgreSQL database in your settings.py:
create new data base in Postgres and add credentials in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory_db', 
        'USER': '<your-db-user>',
        'PASSWORD': '<your-db-password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
- Run database migrations:
```
python manage.py migrate
```


**5. Redis Setup**
Ensure Redis is installed and running. You can install Redis on your local machine. Update the CACHES setting in settings.py as follows:

```
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**6. Run the Server**
```
python manage.py runserver
```



# API Endpoints
**Authentication Endpoints**
- POST /register/: User registration
- POST /login/: User login and token retrieval (JWT)

**Item Management Endpoints**
- POST /items/: Create a new inventory item.
- GET /items/{item_id}/: Retrieve details of an item.
- PUT /items/{item_id}/: Update an existing item’s details.
- DELETE /items/{item_id}/: Delete an item from the inventory.


 [API documentation] (https://documenter.getpostman.com/view/33970118/2sAXxMesbE) 

