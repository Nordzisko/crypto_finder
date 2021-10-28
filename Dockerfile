FROM python:3.8-alpine

ARG DB_HOST="postgres"
ARG DB_PORT=5432
ARG DB_USER="admin"
ARG DB_NAME="cryptofinder_db"
ARG DB_SCHEMA="public"
ARG DB_PASSWORD=password

RUN mkdir /app
WORKDIR /app

# Install system-wide dependencies
RUN apk add --update --no-cache \
    build-base \
    libffi-dev \
    python3-dev \
    make \
    postgresql-dev

# Make sure pip is up-to date
RUN pip install --upgrade pip

# Copy the application code
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/

ARG package_version
ENV PACKAGE_VERSION=$package_version
RUN pip install -e .

# Configure the postgresql secrets file
# Format:
#   hostname:port:database:username:password
RUN touch ~/.pgpass
RUN echo "$DB_HOST:$DB_PORT:$DB_NAME:$DB_USER:$DB_PASSWORD" >> ~/.pgpass
RUN chmod 600 ~/.pgpass

# Setup environment and run application
ENV SERVER_HOST $SERVER_HOST
ENV SERVER_PORT $SERVER_PORT
ENV DB_HOST $DB_HOST
ENV DB_PORT $DB_PORT
ENV DB_NAME $DB_NAME
ENV DB_USER $DB_USER

CMD [ "gunicorn", "crypto_finder.app:create_app_async", "--config", "gunicorn_config.py" ]
EXPOSE 8899
LABEL name=crypto_finder version=dev
