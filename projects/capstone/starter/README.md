## Casting Agency
        Motivation: Casting Agency is the final project of Udacity’s Full Stack Nanodegree, this project is the final step to finish my Nanodegree, the agency in the project models a company that is responsible for creating movies, managing and assigning actors to those movies.


# Getting Started
### Pre-requisites and Local Development:

1. **Python 3.8** - Developers using this project should already have Python3, pip and node installed on their local machines.
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Enviornment** - its recommended working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages selected within the `requirements.txt` file.

4. **Key Dependencies**
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

### Database Setup
With Postgres running, run the following commands with a database user of your choice:

dropdb casting_agency_db
createdb casting_agency_db

dropdb casting_agency_test
createdb casting_agency_test

### Running the server

To run the application cd to the project `./starter` directory and run the following commands:

export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload

The `--reload` flag will detect file changes and restart the server automatically.

•	These commands put the application in development and directs our application to use the app.py file in our starter folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If you are running locally on Windows, look for the commands in the Flask documentation.
•	The application is run on http://127.0.0.1:5000/ by default 

## Endpoints
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

GET /actors
- Fetches a dictionary of actors in which the keys are the id, name, age and gender
- Request Arguments: None
- Returns: An object with a success, current_actors and actors_total_number keys, where success is True, current_actors is a list of up to 10 formated actor objects per page and actors_total_number is the total number of actors

{
    'success': True,
    'current_actors': [
        {
            'id': 1,
            'name': 'John',
            'age': 26,
            'gender': 'Male'
        },
        ...
    ],
    'actors_total_number': 13
}

GET /movies
- Fetches a dictionary of movies in which the keys are the id, title and release_date
- Request Arguments: None
- Returns: An object with a success, current_movies and movies_total_number keys, where success is True, current_movies is a list of up to 10 formated movie objects per page and movies_total_number is the total number of movies

{
    'success': True,
    'current_movies': [
        {
            'id': 1,
            'title': 'the cool kids',
            'release_date': '1/1/2020 12:00'
        },
        ...
    ],
    'movies_total_number': 11
}

POST /actors
- Fetches: None
- Request Arguments: a json object with name(String), age(Integer) and gender(String) keys and their correct values
{
    'name': 'Smith',
    'age': 40,
    'gender': 'Male'
}

- Returns: An object with a success and new_actor keys, where success is True and new_actor is the newly added actor as a formatted json object

{
    'success': True,
    'new_actor': {
            'id': 12,
            'name': 'Smith',
            'age': 40,
            'gender': 'Male'
        }
}

POST /movies
- Fetches: None
- Request Arguments: a json object with title(String) and release_date(Datetime) keys and their correct values
{
    'title': 'the cool kids',
    'release_date': '2023-1-2T11:00:00'
}

- Returns: An object with a success and new_movie keys, where success is True and new_movie is the newly added movie as a formatted json object

{
    'success': True,
    'new_movie': {
            'id': 15,
            'title': 'these kids aren't cool anymore',
            'release_date': '1/2/2023 11:00'
        }
}


PATCH /actors/12
- Fetches: the actor with the specified id in the url 
- Request Arguments: a json object with name(String) and/or age(Integer) and/or gender(String) keys and their correct values
{
    'name': 'Smithern',
    'age': 34
}

- Returns: An object with a success and actor keys, where success is True and actor is the updated actor as a formatted json object

{
    'success': True,
    'actor': {
            'id': 12,
            'name': 'Smithern',
            'age': 34,
            'gender': 'Male'
        }
}

PATCH /movies/15
- Fetches: the movie with the specified id in the url
- Request Arguments: a json object with title(String) and/or release_date(Datetime) keys and their correct values
{
    'title': 'The cool kids are cool again',
    'release_date': '2022-4-2T12:00:00'
}

- Returns: An object with a success and movie keys, where success is True and movie is the updated movie as a formatted json object

{
    'success': True,
    'movie': {
            'id': 15,
            'title': 'The cool kids are cool again',
            'release_date': '4/2/2022 12:00'
        }
}


DELETE /actors/12
- Fetches: the actor with the specified id in the url
- Request Arguments: None
- Returns: An object with a success and deleted keys, where success is True and deleted is id of the deleted actor

{
    'success': True,
    'deleted': 12
}

DELETE /movies/15
- Fetches: the movie with the specified id in the url
- Request Arguments: None
- Returns: An object with a success and deleted keys, where success is True and deleted is id of the deleted movie

{
    'success': True,
    'deleted': 15
}
