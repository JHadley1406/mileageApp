from app import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicleName = db.Column(db.String(128))
    startingMileage = db.Column(db.Integer)
    currentMileage = db.Column(db.Integer)
    averageMpg = db.Column(db.Float)
    createdOn = db.Column(db.DateTime)
    lastUpdated = db.Column(db.DateTime)

    def __repr__(self):
        return self.id

class Fillup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicleId = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    fillupMileage = db.Column(db.Integer)
    fillupMpg = db.Column(db.Float)
    fuelGallons = db.Column(db.Float)
    fuelPrice = db.Column(db.Float)
    createdOn = db.Column(db.DateTime)

    def __repr__(self):
        return 'Fillup On %r' % (self.createdOn.__str__())