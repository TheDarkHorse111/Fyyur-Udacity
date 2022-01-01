from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import true
from database_models.models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

NUM_PER_PAGE = 10

def paginate_selections(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * NUM_PER_PAGE
    end = start + NUM_PER_PAGE
    
    if len(selection) == 0:
      abort(404)

    results = [result.format() for result in selection]
    current_results = results[start:end]

    
    return current_results


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def index():
    return "it works i guess"


  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.order_by(Actor.id).all()
    current_actors = paginate_selections(request, actors)
    
    if len(current_actors) == 0:
      abort(404)
    
    return jsonify(
      {
        "current_actors": current_actors,
        "actors_total_number": len(actors),
        "success": True
      }
    )

    

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):
    movies = Movie.query.order_by(Movie.id).all()
    current_movies = paginate_selections(request, movies)

    if len(current_movies) == 0:
      abort(404)

    return jsonify(
      {
        "current_movies": current_movies,
        "movies_total_number": len(movies),
        "success": True
      }
    )
 


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
    body = request.get_json()

    if 'name' and 'age' and 'gender' not in body:
      abort(400)

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    

    if new_name is None or new_age is None or new_gender is None:
      abort(404)

    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()
      return jsonify({
        'success': True,
        'new_actor': actor.format()
      })
    except:
      abort(422)   


  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(jwt):
    body = request.get_json()
    
    if 'title' not in body or 'release_date' not in body:
      abort(400)
    
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if new_title is None or new_release_date is None:
      abort(404)

    try:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()
      return jsonify(
        {
          'success':True,
          "new_movie": movie.format()
        }
      )
    except:
      abort(422)

  
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt,id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor is None:
        abort(404)
      actor.delete()
      return jsonify({
        'success':True,
        'deleted':id
      })
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt,id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie is None:
        abort(404)
      
      movie.delete()
      return jsonify({
        'success':True,
        'deleted':id
      })
    except:
      abort(422)


  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt,id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor is None:
        abort(404)
      body = request.get_json()
      if "name" in body:
        name = body.get('name')
        actor.name = name

      if "age" in body:
        age = body.get('age')
        actor.age = age
      
      if "gender" in body:
        gender = body.get('gender')
        actor.gender = gender

      
      actor.update()
      return jsonify({
        'success':True,
        'actor':actor.format()
      })
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt,id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie is None:
        abort(404)
      body = request.get_json()
      if "title" in body:
        title = body.get('title')
        movie.title = title

      if "release_date" in body:
        release_date = body.get('release_date')
        movie.release_date = release_date
      
      
      movie.update()
      return jsonify({
        'success':True,
        'movie':movie.format()
      })
    except:
      abort(422)


  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "resource not found"}),
          404,
      )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422,
      )

  @app.errorhandler(400)
  def bad_request(error):
      return( 
          jsonify({"success": False, "error": 400, "message": "bad request"}),
          400,
      )

  @app.errorhandler(405)
  def not_allowed(error):
      return (
          jsonify({"success": False, "error": 405, "message": "method not allowed"}),
          405,
      )
  
  @app.errorhandler(500)
  def server_error(error):
      return (
          jsonify({"success": False, "error": 500, "message": "internal server error"}),
          500,
      )

  @app.errorhandler(401)
  def token_error(error):
      return (
          jsonify({"success": False, "error": 401, "message": "unauthorized"}),
          401,
      )

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)