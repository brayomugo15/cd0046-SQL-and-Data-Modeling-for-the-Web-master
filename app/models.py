from datetime import datetime
from app import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = "show"
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  start_time = db.Column(db.DateTime, nullable=False)
  venue = db.relationship('Venue', backref=db.backref('artists', lazy=True))
  artist = db.relationship('Artist', backref=db.backref('venues', lazy=True))

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(), nullable=False)
    seeking_talent = db.Column(db.Boolean(), nullable=False)
    seeking_description = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.address}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(250), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state}>'

