# user-management-service
This service should create new users, authenticate them, manage created users and allow login. 

This project works using docker-containers, using docker-compose we're going to run each service accordingly.

To run this service using docker-compose, type-in the following command in your terminal inside the root directory:

# RUN SERVICE
`docker-compose up --build`

** INFO: the project is going to run on portal :8002

# CREATE a Django SUPERUSER inside the docker-container:
`docker-compose run user_manage_api python manage.py createsuperuser`

-> user_manage_api is the name of the container

# MAKEMIGRATION and MIGRATE

`docker-compose run user_manage_api python manage.py makemigrations`
`docker-compose run user_manage_api python manage.py migrate`

