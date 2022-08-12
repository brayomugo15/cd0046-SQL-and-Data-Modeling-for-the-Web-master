from flask import render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from app.forms import *
from app import app, db
from app.models import Artist, Venue, Show
import dateutil.parser
import babel


    #----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
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

  artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()

  return render_template('/pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  results = Venue.query.group_by('city','state','name','id').all()
  
  return render_template('pages/venues.html', areas=results)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')

  data = Venue.query
  data = data.filter(Venue.name.ilike('%' + search_term + '%'))
  response = data.order_by(Venue.id).all()
  venuecount  = data.count()

  return render_template('pages/search_venues.html', results=response, search_term=search_term, venuecount=venuecount)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)

  upcoming_show_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time > datetime.utcnow()).all()
  upcoming_shows = []

  for show in upcoming_show_query:
    upcoming_shows.append(show)
  
  past_show_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time < datetime.utcnow()).all()
  past_shows = []

  for show in past_show_query:
    past_shows.append(show)

  return render_template('pages/show_venue.html',upcoming_shows=upcoming_shows, past_shows=past_shows, venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  form = VenueForm()

  if form.validate_on_submit():
    error = False
    try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_talent = form.seeking_talent.data
      seeking_description = form.seeking_description.data

      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, 
      image_link=image_link, facebook_link=facebook_link, website_link=website_link, 
      seeking_talent=seeking_talent, seeking_description=seeking_description)

      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
      if error:
        # on successful db insert, flash success
        flash('Error encountered while saving Venue ' + form.name.data + '!')
      else:
        flash('Venue ' + form.name.data + ' was successfully saved!')
  else:
    flash('Internal Server Error. Please Contact Admins!')

  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      flash("Failed to delete")
    else:
      flash("Deletion Successful")
  
  return render_template('/venues')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.order_by('id').all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term', '')

  data = Artist.query
  data = data.filter(Artist.name.ilike('%' + search_term + '%'))
  response = data.all()
  artistcount = data.count()

  return render_template('pages/search_artists.html', results=response, search_term=search_term, artistcount=artistcount)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  data = Artist.query.get(artist_id)

  upcoming_show_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time > datetime.utcnow()).all()
  upcoming_shows = []

  for show in upcoming_show_query:
    upcoming_shows.append(show)
  
  past_show_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time < datetime.utcnow()).all()
  past_shows = []

  for show in past_show_query:
    past_shows.append(show)
  
  return render_template('pages/show_artist.html', upcoming_shows=upcoming_shows, past_shows=past_shows, artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  form = ArtistForm()

  if form.validate_on_submit():
    error = False
    try:
      artist = Artist.query.get(artist_id)

      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = request.form.getlist('genres')
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.commit()
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
      if error:
        flash("Encountered a problem while saving "+ form.name.data +" update!")
      else:
        flash(form.name.data + " has been updated successfully!")
  else:
    flash("Internal Server error: Please Contact Admins!")

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  if request.method == 'POST':

    error = False
    form = VenueForm()
    try:
      venue = Venue.query.get(venue_id)

      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.commit()
    except:
      error = True
      db.session.commit()
    finally:
      db.session.close()
      if error:
        flash("Encountered a problem while saving "+ form.name.data +" update!")
      else:
        flash(form.name.data + " has been updated successfully!")
  else:
    flash("Internal Server error: Please Contact Admins!")

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
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  form = ArtistForm()

  if request.method == "POST":
    error = False
    try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres = form.genres.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data

      artist = Artist(name=name, city=city, state=state, phone=phone, 
      genres=genres, image_link=image_link, facebook_link=facebook_link, 
      website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
      if error:
        flash('Error encountered while saving Artist ' + form.name.data + '!')
      else:
        flash('Artist ' + form.name.data + ' was successfully saved!')
    
  else:
    flash('Internal Server Error. Please Contact Admins!')

  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  
  data = Show.query.all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  form = ShowForm()

  if request.method == "POST":
      error = False
      try:
        artist_id = form.artist_id.data
        venue_id = form.venue_id.data
        start_time = form.start_time.data

        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()
        if error:
          flash('Error encountered while saving Show !')
        else:
          flash('Show  was successfully saved!')

  else:
    flash('Internal Server Error. Please Contact Admins!')
  

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html', form=form)

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