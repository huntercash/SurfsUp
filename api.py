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

# @app.route("/api/v1.0/justice-league")
# def justice_league():
#     """Return the justice league data as json"""

#     return jsonify(justice_league_members)


@app.route("/api/stations")
def station():
    """Returns All of The Stations in Hawaii"""
    statn = session.query(Station.station)
    station_list = []
    for station in statn:
        station_dict = {}
        station_dict['station'] = station
        station_list.append(station_dict)
    return jsonify(station_list)




@app.route("/api/temperature")
def tobs():
    """Return a list of temperatures for prior year"""
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
# Return the json representation of your dictionary.
    temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).\
        order_by(Measurement.date).all()
# Create a list of dicts with `date` and `tobs` as the keys and values
    tobs_summary = []
    for date, tobs in temp:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_summary.append(tobs_dict)

    return jsonify(tobs_summary)




# /api/<start> and /api/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# Hint: You may want to look into how to create a defualt value for your route variable.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

if __name__ == '__main__':
    app.run(debug=True)