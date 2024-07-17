<h1 align="center">Welcome to Simple Social 👋</h1>

> This project is a `backend API` for a `social media` mock-up built with `Django REST Framework`. It provides functionalities for `user authentication`, `post management`, `friend management`, and `post reactions`, offering a rich foundation for building a social media platform.

## ✨ Setup Instructions

Download and install [Docker](https://docs.docker.com/engine/install/) Engine.

Change directory and go to `simple_social`

```sh
cd simple_social
```

Run docker compose build command to build the Docker images for the services defined in the docker-compose file.
```sh
docker compose -f docker-compose.yml build
```

Run docker compose up command to start and run the containers for the services defined in the docker-compose.yml file.
```sh
docker compose -f docker-compose.yml up
```

You backend should be up and accessible from [here](http://localhost:8000/api/schema/swagger-ui/#/).

# Social Media Mockup Backend

## Features

### 1. User Authentication

#### JWT Authentication

- Uses JWT for secure authentication.
- Endpoint to refresh JWT access token by sending a refresh token is available.

#### Sign Up

- Endpoint: `/account/api/signup/`
- Method: `POST`
- This API endpoint allows a new user to sign up. 
- Request Body:
  ```json
  {
  "username": "Zve",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "country_code": "string",
  "phone_number": "string",
  "password": "string",
  "confirm_password": "string"
  }
  ```

#### Signin

- Endpoint: `/account/api/signin/`
- Method: `POST`
- This API endpoint allows a user to log in.
- Request Body:
  ```json
  {
  "username": "string",
  "password": "string"
  }
  ```

#### Refresh JWT Token

- Endpoint: `/account/api/signin/refresh/`
- Method: `POST`
- This API endpoint allows a user to refresh their JWT access token by sending a refresh token.
- Request Body:
  ```json
  {
  "token": "string"
  }
  ```

### 2. Posts Management

#### Create a Post

- Endpoint: `/post/api/create/`
- Method: `POST`
- This API endpoint allows a user to create a new post. 
- Request Body:
  ```json
  {
  "images": [
    {
      "image": "string"
    }
  ],
  "tags": [
    {
      "tag": "string",
      "type": "HASHTAG"
    }
  ],
  "text_content": "string",
  "share_with": "PUBLIC",
  "is_active": true
  }
  ```

#### Get, update and delete a Post

- Endpoint: `/post/api/{uuid}/`
- Method: `GET` `PUT` `PATCH` `DELETE`
- This API endpoint allows a user to retrieve a specific post using the `GET` method, allows a user to update a post using `PUT` or `PATCH` methods and allows a user to delete a post using the `DELETE` method.

#### Post Reactions

- Endpoint: `/post/api/{uuid}/react/`
- Method: `POST`
- The application supports reactions to posts such as LIKE, WOW, SAD, ANGRY, LOVE, and HAHA.
- Reactions are processed in batches every 10 seconds.
- - Request Body:
  ```json
  {
  "type": "LIKE"
  }
  ```

### 3. Friendship Management

The application manages friendships using a `Neo4J` database.

#### Send a Friend request

- Endpoint: `/relations/api/send_friend_requests/{uuid}/`
- Method: `POST`
- This API endpoint allows a user to send a friend request.

#### Accept a Friend request

- Endpoint: `/relations/api/accept_friend_requests/{uuid}`
- Method: `POST`
- This API endpoint allows a user to accept a friend request.

#### Cancel a Friend request

- Endpoint: `/relations/api/cancel_friend_requests/{uuid}/`
- Method: `DELETE`
- This API endpoint allows a user to cancel a sent friend request.


#### Reject a Friend request

- Endpoint: `/relations/api/reject_friend_requests/{uuid}/`
- Method: `POST`
- This API endpoint allows a user to reject a friend request.

#### Unfriend a user 

- Endpoint: `/relations/api/unfriend/{uuid}/`
- Method: `POST`
- This API endpoint allows a user to unfriend a user who is already a friend.

#### Get Sent Friend Requests

- Endpoint: `/relations/api/friend_requests_sent`
- Method: `GET`
- This API endpoint allows a user to retrieve the friend requests they have sent.

#### Get Received Friend Requests

- Endpoint: `/relations/api/friend_requests_received/`
- Method: `GET`
- This API endpoint allows a user to retrieve the friend requests they have received.

### 4. Friend Recommendations

The application provides friend recommendations, which are generally friends of friends. 

These recommendations are pre-calculated daily and stored in a `Redis` cache.

#### Get Friend Recommendations

- Endpoint: `/relations/api/friend_recommendations/`
- Method: `GET`
- This API endpoint allows a user to retrieve friend recommendations.

### 5. Timeline

The user's timeline is generated and calculated daily, then stored in a Redis cache.

#### Get User Timeline

- Endpoint: `/retrieve-post/api/timeline/`
- Method: `GET`
- This API endpoint allows a user to retrieve their timeline.

#### Get User's Posts

- Endpoint: `/retrieve-post/api/post_by_user/{uuid}/`
- Method: `GET`
- This API endpoint allows a user to retrieve the posts of a specific user.

## 💻 Tech Stack

Backend: `Python` `Django` `Django REST Framework`

Authentication: `JWT`

Database: `PostgreSQL`

Graph Database: `Neo4J`

Cache: `Redis`

Async Processing: `Celery`

## 🚀 Usage

Detailed API documentationis provided via a dedicated API documentation tool `Swagger`. 

Refer to the documentation for specific endpoint details, request parameters, and response formats [here](http://localhost:8000/api/schema/swagger-ui/#/).

You can use tools like curl or Postman to interact with the APIs.

## 🔥 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## 👨🏻‍💻 Author

👤 **Prashant Mishra**

- LinkedIn: [@prashant-manoj-mishra](https://www.linkedin.com/in/prashant-manoj-mishra/)
- Github: [@mishraprashant1](https://github.com/mishraprashant1)
- Twitter: [@iamjunooo](https://twitter.com/iamjunooo)
