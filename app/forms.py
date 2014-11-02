from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import Required

class AddVehicle(Form):
	vehicleName = StringField('Vehicle Name', validators = [Required()])
	startingMileage = IntegerField('Starting Mileage', validators = [Required()])
				
class AddFillup(Form):
	currentMileage = IntegerField('Current Mileage', validators = [Required()])
	fuelGallons = DecimalField('Gallons of Fuel', validators = [Required()], places = 2)
	fuelPrice = DecimalField('Price Per Gallon', validators = [Required()], places = 2)