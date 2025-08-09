# E-commerce Backend API

## Description

This project is a complete e-commerce backend built with Django and Django REST Framework (DRF). It provides a full-featured API for managing products, a shopping cart, orders, and user authentication. The application is containerized using Docker Compose for easy setup and deployment.

## Features

### E-commerce Functionality
* **Product Catalog:** Browse a list of all active products.
* **Shopping Cart:** A user can add products to a session-based or logged-in user's cart.
* **Secure Checkout:** The cart is converted into a permanent order record in the database during checkout.
* **Order History:** Users can view a complete history of their past orders.
* **Inventory Management:** Product stock is atomically decremented when an order is placed, preventing race conditions.

### API Functionality (DRF & JWT)
* **JWT Authentication:** User registration, login, and token refresh are handled via a secure API using JWT.
* **Protected Endpoints:** All critical API endpoints are protected and require a valid JWT for access.
* **API for Cart Management:** Programmatically add, update, or remove items from the shopping cart.
* **API for Orders:** Place new orders and view past order history via API calls.

## Getting Started

These instructions will get a copy of the project up and running on your local machine.

### Prerequisites
You need to have **Docker** and **Docker Compose** installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Build and run the containers:**
    ```bash
    docker compose up --build -d
    ```
    This will build the Docker images and start the application and database containers in detached mode.

3.  **Run migrations and set up the database:**
    Access the running container to run initial commands.
    ```bash
    docker compose exec app python manage.py migrate
    docker compose exec app python manage.py createsuperuser
    ```
    Follow the prompts to create an admin user.

The application should now be running. You can access it at `http://127.0.0.1:8000/`.

## API Endpoints

The API is accessible under the `/api/` path. You can use a tool like Postman or `curl` to interact with it.

| Endpoint                                      | Method | Description                                                               | Permissions      |
| --------------------------------------------- | ------ | ------------------------------------------------------------------------- | ---------------- |
| `/api/register/`                              | `POST` | Creates a new user account.                                               | `AllowAny`       |
| `/api/token/`                                 | `POST` | Retrieves a new access token and refresh token.                           | `AllowAny`       |
| `/api/token/refresh/`                         | `POST` | Refreshes an expired access token using a refresh token.                  | `AllowAny`       |
| `/api/products/`                              | `GET`  | Lists all available products.                                             | `IsAuthenticated`|
| `/orders/api/cart/`                           | `GET`  | Retrieves the current user's active cart.                                 | `IsAuthenticated`|
| `/orders/api/cart/add/`                       | `POST` | Adds a product to the cart.                                               | `IsAuthenticated`|
| `/orders/api/cart/update/<int:item_id>/`      | `PUT`  | Updates the quantity of a cart item.                                      | `IsAuthenticated`|
| `/orders/api/cart/update/<int:item_id>/`      | `DELETE`| Deletes a cart item.                                                      | `IsAuthenticated`|
| `/orders/api/checkout/`                       | `POST` | Creates a new order from the user's active cart.                          | `IsAuthenticated`|
| `/orders/api/history/`                        | `GET`  | Lists the user's past orders.                                             | `IsAuthenticated`|

## Technology Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Authentication:** JWT (JSON Web Tokens)
* **Containerization:** Docker, Docker Compose
