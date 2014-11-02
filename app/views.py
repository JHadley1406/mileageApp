from flask import render_template, request
from app import app, db
from forms import AddVehicle, AddFillup
from models import Vehicle, Fillup
from datetime import datetime


@app.route('/')
def index():
    vehicles = Vehicle.query.all()
    if vehicles:
        fillups = Fillup.query.all()
        return render_template('index.html',
                                vehicles=vehicles,
                                fillups=fillups)
    form = AddVehicle()
    return render_template('add_vehicle.html', form=form)


@app.route('/addVehicle', methods=['GET', 'POST'])
def add_vehicle():
    form = AddVehicle()
    if request.method == 'POST':
        vehicle = Vehicle(vehicleName=form.vehicleName.data,
                          startingMileage=form.startingMileage.data,
                          currentMileage=form.startingMileage.data,
                          averageMpg=0.00,
                          createdOn=datetime.now(),
                          lastUpdated=datetime.now())
        db.session.add(vehicle)
        db.session.commit()
        return render_template("index.html",
                               vehicles=Vehicle.query.all(),
                               fillups=Fillup.query.all())
    return render_template("add_vehicle.html", form=form)


@app.route('/addFillup/<vehicleId>', methods=['GET', 'POST'])
def add_fillup(vehicleId):
    vehicle = Vehicle.query.get(vehicleId)
    form = AddFillup()
    if request.method == 'POST':
        fillup = Fillup(vehicleId=vehicle.id,
                        fillupMileage=form.currentMileage.data,
                        fuelGallons=form.fuelGallons.data,
                        fuelPrice=form.fuelPrice.data,
                        createdOn=datetime.now())
        fillup.fillupMpg = (fillup.fillupMileage-vehicle.currentMileage)/fillup.fuelGallons

        #get count of fillups for this vehicle
        fillup_count = db.session.query(Fillup).filter_by(vehicleId=vehicle.id).count()
        if fillup_count > 0:
            new_avg_mpg = ((float(vehicle.averageMpg) * (fillup_count))+float(fillup.fillupMpg))/(fillup_count+1)
        else:
            new_avg_mpg=fillup.fillupMpg
        db.session.add(fillup)
        db.session.query(Vehicle).filter_by(id=vehicle.id).update({'currentMileage' : fillup.fillupMileage,
                                                                    'averageMpg': new_avg_mpg,
                                                                    'lastUpdated' : datetime.now()})
        db.session.commit()
        return render_template("index.html",
                               vehicles=Vehicle.query.all(),
                               fillups=Fillup.query.all())
    return render_template("add_fillup.html", vehicleId=vehicle.id, form=form)

def delete_vehicle(vehicleId):
    db.session.query(Vehicle.filter_by(id=vehicleId).delete())