docker exec -ti 4305d0390fe5 /bin/bash

docker compose up --build -d --remove-orphans

docker compose logs
docker exec -ti -u root 0b7b9a9a3667 /bin/bash
docker network inspect bridge

docker-compose run user_manage_api python manage.py makemigrations

docker-compose config