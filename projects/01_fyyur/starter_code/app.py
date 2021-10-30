#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from operator import le
import re
import sys
import dateutil.parser
import babel
from flask import(
  Flask,
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
  )
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from jinja2.nodes import Not
from forms import *
from flask_migrate import Migrate, current, show
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
from models import Venue, Artist, Shows, db
db.init_app(app)


# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 
  locals = []
  venues = Venue.query.all()

  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
      locals.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
              'num_upcoming_shows': len([show for show in venue.shows if show.Start_time > datetime.now()])
          } for venue in venues if
              venue.city == place.city and venue.state == place.state]
      })
  return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchTerm = request.form.get('search_term', '')

  searchedVenues = Venue.query.filter(Venue.name.ilike('%'+ searchTerm+'%'))
  data = []
  for venue in searchedVenues:
    venue.num_upcoming_shows = db.session.query(Shows).filter(Shows.Venue_id == venue.id,Shows.Start_time > datetime.today()).count()
    data.append({
      "id" : venue.id,
      "name" :venue.name,
      "num_upcoming_shows": venue.num_upcoming_shows
    })
  response={
    "count": searchedVenues.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  
  venue = Venue.query.get_or_404(venue_id)

  pastShows = []
  upcomingShows = []

  for show in venue.shows:
      temp_show = {
          'artist_id': show.artist.id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': show.Start_time.strftime("%m/%d/%Y, %H:%M")
      }
      if show.Start_time <= datetime.now():
          pastShows.append(temp_show)
      else:
          upcomingShows.append(temp_show)


  

  
 
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.strip("{}").split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link":venue.image_link,
    "past_shows": pastShows,
    "upcoming_shows": upcomingShows,
    "past_shows_count": len(pastShows),
    "upcoming_shows_count": len(upcomingShows),
  }
  
 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  error = False
  try:
    venue = Venue()
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    if form.seeking_talent.data == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False
    venue.seeking_description = form.seeking_description.data
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
        
  

  # on successful db insert, flash success
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occured. Venue ' + request.form['name'] + ' Could not be listed!')
    
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  venue.delete()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id":artist.id,
      "name":artist.name
    })

  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  searchTerm = request.form['search_term']
  searchedArtists = Artist.query.filter(Artist.name.ilike('%'+ searchTerm+'%'))
  data = []
  for artist in searchedArtists:
    num_upcoming_shows = Shows.query.filter(Shows.Artist_id == artist.id and Shows.Start_time > datetime.today()).count()
    data.append({
      "id" : artist.id,
      "name" :artist.name,
      "num_upcoming_shows": num_upcoming_shows
    })
  response={
    "count": searchedArtists.count(),
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  pastShows =[]
  upcomingShows = []
  shows = Shows.query.filter_by(Artist_id = artist_id).all()
  
  for show in shows:
    print(show)
    venue = Venue.query.get(show.Venue_id)
    print(venue)
    if show.Start_time <= datetime.today():
      pastShows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": str(show.Start_time)
      })
    else:
      upcomingShows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": str(show.Start_time)
      })
  
  artist = Artist.query.get(artist_id)
 
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.strip("{}").split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website":artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": pastShows,
    "upcoming_shows": upcomingShows,
    "past_shows_count": len(pastShows),
    "upcoming_shows_count": len(upcomingShows)
  }
  print(len(pastShows))
 
  
 
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  currentArtist = Artist.query.get(artist_id)
  artist={
    "id": currentArtist.id,
    "name": currentArtist.name,
    "genres": currentArtist.genres,
    "city": currentArtist.city,
    "state": currentArtist.state,
    "phone": currentArtist.phone,
    "website_link": currentArtist.website_link,
    "facebook_link": currentArtist.facebook_link,
    "seeking_venue": currentArtist.seeking_venue,
    "seeking_description": currentArtist.seeking_description,
    "image_link": currentArtist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  try:
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
   
    artist.genres = form.genres.data
    artist.website_link = form.website_link.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    if form.seeking_venue.data == "y":
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  myVenue = Venue.query.get(venue_id)
  venue={
    "id": myVenue.id,
    "name": myVenue.name,
    "genres": myVenue.genres,
    "address": myVenue.address,
    "city": myVenue.city,
    "state": myVenue.state,
    "phone": myVenue.phone,
    "website": myVenue.website_link,
    "facebook_link": myVenue.facebook_link,
    "seeking_talent": myVenue.seeking_talent,
    "seeking_description": myVenue.seeking_description,
    "image_link": myVenue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  try:
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    if form.seeking_talent.data == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  form = ArtistForm(request.form)
  try:
    name = form.name.data
    print(request.form.get('name'))
    city = form.city.data
    print(request.form['city'])
    state = form.state.data
    print(request.form['state'])
    phone = form.phone.data
    print(request.form['phone'])
    
    genres = form.genres.data
    print(genres)
    website_link = form.website_link.data
    print(request.form['website_link'])
    image_link = form.image_link.data
    print(request.form['image_link'])
    facebook_link = form.facebook_link.data
    print(request.form['facebook_link'])
    print(request.form['seeking_venue'])
    if form.seeking_venue.data == 'y':
      seeking_venue = True
    else:
      seeking_venue = False
    
    seeking_description = form.seeking_description.data
    print(request.form['seeking_description'])
    myArtist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,website_link=website_link,
    image_link=image_link,facebook_link=facebook_link,seeking_venue=seeking_venue,seeking_description=seeking_description)
    db.session.add(myArtist)
    db.session.commit()   
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()  
   
  # on successful db insert, flash success
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occured. Artist ' + request.form['name'] + ' Could not be created!')

  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  shows = Shows.query.all()
  for show in shows:
    venue = Venue.query.get(show.Venue_id)
    artist = Artist.query.get(show.Artist_id)
    
    data.append(
      {
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.Start_time)
      }
    )
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error=True
  try:
    artistID =request.form['artist_id']
    print(request.form['artist_id'])
    venueID =request.form['venue_id']
    print(request.form['venue_id'])
    myArtist = Artist.query.get(artistID)
    myVenue = Venue.query.get(venueID)

    
    Start_Time = request.form['start_time']
    show = Shows(Artist_id=artistID, Venue_id = venueID, Start_time = Start_Time)
    show.artist = myArtist
    myVenue.shows.append(show)
  
    print(request.form['start_time'])
    db.session.add(show)
    db.session.commit()
  except:
    error=False
    db.session.rollback()
  finally:
    db.session.close()

  # on successful db insert, flash success
  if error:
    flash('Show was successfully listed!')
  else:
    flash('Show was not listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
