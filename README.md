# Log Finder
A HTTP API for querying JSON logs on a local machine.

## Environment Variables
- SERVER_HOST: Host of the log finder API (default 0.0.0.0).
- SERVER_PORT: Port of the log finder API (default 4321).
- LOGS: A CSV in the format `<name>:<regex_of_files>:<index>`.
- MONGO_HOST: Host of MongoDB for caching (default localhost).
- MONGO_PORT: Port of MongoDB (default 27017).
- MONGO_DATABASE: Database to use for cache (default log_finder).

## Push to ECR

1. `docker build -t nexmo-chatapp-log-finder .`

2. `docker tag nexmo-chatapp-log-finder:latest 564623767830.dkr.ecr.eu-west-1.amazonaws.com/nexmo-chatapp-log-finder:latest`

3. `docker push 564623767830.dkr.ecr.eu-west-1.amazonaws.com/nexmo-chatapp-log-finder:latest`


## Running Locally

1. Start MongoDB instance: `docker run -p 27017:27017 --name log-finder-mongo -d mongo:latest`

1. `pipenv install`

2. `pipenv run python main.py`
