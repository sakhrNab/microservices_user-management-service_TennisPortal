# Before RUNNING this Service, please do the follwoing:

1. Run the Review-Service inside this repository: [Review-Service](https://github.com/blitz-de/review_service)  

2. Run the Frontend-Service inside this repository: [Frontend-Service](https://github.com/blitz-de/frontend-service)

3. Run the User-Management-Service :)


# Inside the User-Management-Service

## Makefile

There is a file called makefile, inside of it are various commands to run different containers within the service, for example:

### To run the service
`make run user-service`

### To create a superuser inside the User-Management-Service Database
`make superuser`

*** The Admin Panel for this service is
`http:localhost:8080/superuser/`

### To run the makemigration command inside the container
`make makemigration`

### To run the migrate command inside the container
`make migrate`

### To run the test coverage
`make test`

# The available Endpoints using swagger UI
`http:localhost:8080/users/api/swagger/`


# Link to the User-Management-Service Travis-CI Dashboard
`https://app.travis-ci.com/github/blitz-de/user-management-service/builds`


