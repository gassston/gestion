# Inventory & Branch Management API

**Version:** 1.0.0

## Description

This API powers a multi-branch inventory management system.

## Features

* 🔐 User authentication with roles (admin, user)
* 📦 CRUD operations for products and real-time stock management
* 🧍 CRUD operations for clients
* 🔁 Stock transfers between branches
* 🌐 Multi-branch visibility and control

## API Endpoints

The API provides the following endpoints:

### Health Check

* `GET /health`: Checks the health status of the API.

### Authentication (`/auth`)

* `POST /auth/login`: Logs in a user and returns access/refresh tokens.
* `POST /auth/logout`: Logs out the current user (requires valid token).
* `POST /auth/refresh`: Refreshes the access token using a valid refresh token (sent via cookie).

### Products (`/products`)

* `GET /products`: Lists all products.
* `POST /products`: Creates a new product.
* `GET /products/{product_id}`: Retrieves a specific product by ID.
* `PUT /products/{product_id}`: Updates a specific product by ID.
* `DELETE /products/{product_id}`: Deletes a specific product by ID.

### Stock (`/stock`)

* `GET /stock`: Retrieves stock information, optionally filtered by branch.
* `POST /stock`: Adds initial stock for a product in a branch.
* `PUT /stock/{stock_id}`: Updates the quantity of a specific stock item by ID.
* `DELETE /stock/{stock_id}`: Deletes a specific stock item by ID.

### Users (`/users`)

* `GET /users`: Lists all users (requires appropriate permissions).
* `POST /users`: Creates a new user.
* `GET /users/{user_id}`: Retrieves a specific user by ID.
* `PUT /users/{user_id}`: Updates a specific user by ID.
* `DELETE /users/{user_id}`: Deletes a specific user by ID.

### Clients (`/clients`)

* `GET /clients`: Lists all clients.
* `POST /clients`: Creates a new client.
* `PUT /clients/{client_id}`: Updates a specific client by ID.
* `DELETE /clients/{client_id}`: Deletes a specific client by ID.

### Movements (`/movements`)

* `GET /movements`: Lists all stock movements (transfers) between branches.
* `POST /movements`: Creates a new stock movement record (transfer).

### Branches (`/branches`)

* `GET /branches`: Lists all branches.
* `POST /branches`: Creates a new branch.
* `GET /branches/{branch_id}`: Retrieves a specific branch by ID.
* `PUT /branches/{branch_id}`: Updates a specific branch by ID.
* `DELETE /branches/{branch_id}`: Deletes a specific branch by ID.

## Getting Started

*(This section is a placeholder. You should add instructions specific to your project setup)*

1.  **Prerequisites:** List any software needed (e.g., Python version, Node.js version, Docker).
2.  **Installation:** Provide steps to clone the repository and install dependencies.
    ```bash
    git clone https://github.com/gassston/gestion.git
    cd gestion
    docker compose up --build
    ```
3.  **Configuration:** .
4.  **Running the API:** Show how to start the server.
    ```bash
    docker compose up --build
    ```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

* **Name:** J&T
* **Website:** [https://ourdomain.com/](https://ourdomain.com/)
* **Email:** support@ourdomain.com