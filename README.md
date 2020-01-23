# ubiwhere-challenge

A REST API for managing occurrences in an urban environment, implemented using Django with a SQLite database, for Ubiwhere's challenge.
The description of the endpoints of the API is available at its root (api/) once it is running.

Note: The server time is set to be according to the UTC time zone.

**Running the API with Docker**

To run the API using Docker simply use the following command.

```
docker-compose up
```

The API will then be ready to receive requests.

**Running the API using the command line**

To run the API using the command line we need to first install the necessary Python packages using these commands.

```
pip3 install Django
pip3 install djangorestframework
```

With all the requirements met, the following commands must be run.

```
cd challenge
python3 manage.py makemigrations api
python3 manage.py migrate
```

If the goal is to run the implemented set of tests, then the command to use is the following.

```
python3 manage.py test api
```

If the goal is to run the API, then the next command will start the server.

```
python3 manage.py runserver
```

The API will then be available to receive requests.