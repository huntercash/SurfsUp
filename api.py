import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"/api/start<br/>"
        f"/api/start-end<br/>"
    )


@app.route("/api/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""
# Query for the dates and precipitation observations from the last year.
# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the json representation of your dictionary.

    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    precipitation_list = []
    for date, prcp in data:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)



# @app.route("/api/stations")
#     return jsonify(all_passengers)

# @app.route("/api/temperature")
#     return jsonify()

# @app.route("/api/<start>")
#     return jsonify()

# @app.route("/api/start-end")
#     return jsonify()
if __name__ == '__main__':
    app.run(debug=True)