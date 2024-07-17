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

- Endpoint: `/relations/api/send_friend_requests/{uuid}`
- Method: `POST`
- This API endpoint allows a user to send a friend request.

#### Accept a Friend request

- Endpoint: `/relations/api/accept_friend_requests/{uuid}`
- Method: `POST`
- This API endpoint allows a user to accept a friend request.

#### Cancel a Friend request

- Endpoint: `/relations/api/cancel_friend_requests/{uuid}`
- Method: `DELETE`
- This API endpoint allows a user to cancel a sent friend request.


#### Reject a Friend request

- Endpoint: `/relations/api/reject_friend_requests/{uuid}`
- Method: `POST`
- This API endpoint allows a user to reject a friend request.

#### Unfriend a user 

- Endpoint: `/relations/api/unfriend/{uuid}`
- Method: `POST`
- This API endpoint allows a user to unfriend a user who is already a friend.

### 3. Friend Recommendations

The application provides friend recommendations, which are generally friends of friends. 

These recommendations are pre-calculated daily and stored in a `Redis` cache.

#### Get Friend Recommendations

- Endpoint: `/relations/api/unfriend/{uuid}`
- Method: `POST`
- This API endpoint allows a user to unfriend a user who is already a friend.
























## 🚀 Usage

Make sure you have [npx](https://www.npmjs.com/package/npx) installed (`npx` is shipped by default since npm `5.2.0`)

Just run the following command at the root of your project and answer questions:

```sh
npx readme-md-generator
```

Or use default values for all questions (`-y`):

```sh
npx readme-md-generator -y
```

Use your own `ejs` README template (`-p`):

```sh
npx readme-md-generator -p path/to/my/own/template.md
```

You can find [ejs README template examples here](https://github.com/kefranabg/readme-md-generator/tree/master/templates).

## Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/kefranabg/readme-md-generator/graphs/contributors"><img src="https://opencollective.com/readme-md-generator/contributors.svg?width=890&button=false" /></a>

## Financial Contributors

Become a financial contributor and help us sustain our community. [[Contribute](https://opencollective.com/readme-md-generator/contribute)]

### Individuals

<a href="https://opencollective.com/readme-md-generator"><img src="https://opencollective.com/readme-md-generator/individuals.svg?width=890"></a>

### Organizations

Support this project with your organization. Your logo will show up here with a link to your website. [[Contribute](https://opencollective.com/readme-md-generator/contribute)]
<a href="https://opencollective.com/readme-md-generator/organization/0/website"><img src="https://opencollective.com/readme-md-generator/organization/0/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/1/website"><img src="https://opencollective.com/readme-md-generator/organization/1/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/2/website"><img src="https://opencollective.com/readme-md-generator/organization/2/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/3/website"><img src="https://opencollective.com/readme-md-generator/organization/3/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/4/website"><img src="https://opencollective.com/readme-md-generator/organization/4/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/5/website"><img src="https://opencollective.com/readme-md-generator/organization/5/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/6/website"><img src="https://opencollective.com/readme-md-generator/organization/6/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/7/website"><img src="https://opencollective.com/readme-md-generator/organization/7/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/8/website"><img src="https://opencollective.com/readme-md-generator/organization/8/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/9/website"><img src="https://opencollective.com/readme-md-generator/organization/9/avatar.svg"></a>

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/kefranabg/readme-md-generator/issues) if you want to contribute.<br />
[Check the contributing guide](./CONTRIBUTING.md).<br />

## Author

👤 **Franck Abgrall**

- Twitter: [@FranckAbgrall](https://twitter.com/FranckAbgrall)
- Github: [@kefranabg](https://github.com/kefranabg)

## Show your support

Please ⭐️ this repository if this project helped you!

<a href="https://www.patreon.com/FranckAbgrall">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## 📝 License

Copyright © 2019 [Franck Abgrall](https://github.com/kefranabg).<br />
This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
