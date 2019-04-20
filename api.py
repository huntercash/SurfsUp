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
        f"<center>"
        f"<b>Available Routes:</b><br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"</br>"
        f"Date Format yyyy-mm-dd</br>"
        f"/api/dates/start<br/>"
        f"/api/dates/start/end<br/>"
        f"</center>"
    )


#################################################
# Precipitation
#################################################

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

#################################################
# Stations
#################################################

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


#################################################
# Temperature
#################################################

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


#################################################
# Dates TMIN, TAVG, TMAX
#################################################

# Defines the start date function
def start_summary(start_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
# Defines the start/end function
def end_summary(start_date,end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


@app.route("/api/dates/")
@app.route("/api/dates/<start>/")
def start_temps(start='2016-08-23'):
    start_list = start_summary(start)
    start_dict = {"START DATE":start, "TMIN":start_list[0][0], "TAVG":start_list[0][1], "TMAX":start_list[0][2]}
    return jsonify(start_dict)
@app.route("/api/dates/<start>/<end>")
def end_temps(start,end):
    end_list = end_summary(start,end)
    end_dict = {"START DATE":start, "END DATE":end, "TMIN":end_list[0][0], "TAVG":end_list[0][1], "TMAX":end_list[0][2]}
    return jsonify(end_dict)

if __name__ == '__main__':
    app.run(debug=True)