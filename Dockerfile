FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /user-management-service
COPY requirements.txt /user-management-service/requirements.txt
RUN pip install -r requirements.txt
COPY . /user-management-service
#RUN python manage.py makemigrations
#RUN python manage.py migrate
#CMD python manage.py runserver 0.0.0.0:8000