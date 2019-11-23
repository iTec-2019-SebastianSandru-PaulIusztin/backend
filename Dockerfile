FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

# Copy only Pipfiles in order to cache dependency installation steps
COPY Pipfile /app/
COPY Pipfile.lock /app/
WORKDIR /app

# Install project dependencies
RUN set -xe \
    && pip install pipenv \
    && pipenv install --system --deploy

# Install GDAL library
RUN set -xe \
    && apt-get update \
    && apt-get install -y gdal-bin

# Copy all the source code
COPY . /app

# Launching app
EXPOSE 80
CMD ["/app/scripts/entrypoint.sh"]
