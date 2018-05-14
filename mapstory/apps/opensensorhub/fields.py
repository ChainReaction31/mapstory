from django.db import models

class ArrayField(models.Field)

	description = "A container for data to be used as arrays"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		return name, path, args, kwargs

	def from_db_value(self, value, expression, connection):
		pass

	def to_python(self, value):
		pass

	class Meta:
		abstract = True

class RgbField(ArrayField)

	description = "An array containing the integer values for RGB color definition"

	def __init__(self, *, **kwargs):
		kwargs['max_length'] = 3
		kwargs['db_name'] = "rgb_color"
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs['max_length']
		del kwargs['db_name']
		return name, path, args, kwargs

	def db_type(self, connection)
		return "RgbField"


	def from_db_value(self, value, expression, connection):

		if value is None:
			return value

		rgbValues = [int(x) for x in value.split(",")]

		return rgbValues

	def to_python(self, value):

		if value is None:
			return value

		if isinstance(value, list):
			return value
		
		rgbValues = [int(x) for x in value.split(",")]


		return rgbValues

	def get_prep_value(self, value):

		if len(value) != 3:
			raise ValidationError("Invalid RGB value: length=" + len(value))
		
		return ''.join(json.dumps(values, separator(','))

class ThresholdField(ArrayField)

	description = "Container for value pairs as (min, max)"
	
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 2
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs['max_length']
		return name, path, args, kwargs

	def db_type(self, connection)
		return "ThresholdField"

	def from_db_value(self, value, expression, connection):
		pass

	def to_python(self, value):
		pass

	class Meta:
		abstract = True

class IntThresholdField(ThresholdField)

	description = "Container for integer value pairs as (min, max)"
	
	def __init__(self, *args, **kwargs):		
		kwargs['db_name'] = "threshold_as_int"
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs['db_name']
		return name, path, args, kwargs

	def db_type(self, connection)
		return "IntThresholdField"

	def from_db_value(self, value, expression, connection):

		if value is None:
			return value

		rangeValues = [int(x) for x in value.split(",")]

		return rangeValues

	def to_python(self, value):

		if value is None:
			return value

		if isinstance(value, list):
			return value
		
		rangeValues = [int(x) for x in value.split(",")]


		return rangeValues

	def get_prep_value(self, value):

		if len(value) != 2:
			raise ValidationError("Invalid Threshold value: length=" + len(value))
		
		return ''.join(json.dumps(value, separator(','))

class FloatThresholdField(ThresholdField)

	description = "Container for floating point precision value pairs as (min, max)"
	
	def __init__(self, *args, **kwargs):	
		kwargs['db_name'] = "threshold_as_float"
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs['db_name']
		return name, path, args, kwargs

	def db_type(self, connection)
		return "DoubleThresholdField"

	def from_db_value(self, value, expression, connection):

		if value is None:
			return value

		rangeValues = [int(x) for x in value.split(",")]

		return rangeValues

	def to_python(self, value):

		if value is None:
			return value

		if isinstance(value, list):
			return value
		
		rangeValues = [float(x) for x in value.split(",")]


		return rangeValues

	def get_prep_value(self, value):

		if len(value) != 2:
			raise ValidationError("Invalid Threshold value: length=" + len(value))
		
		return ''.join(json.dumps(value, separator(','))

class ThresholdArrayField(ArrayField)

	description = "An array containing threshold values"

	def __init__(self, *, **kwargs):
		kwargs['db_name'] = "thresholds"
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs['db_name']
		return name, path, args, kwargs

	def db_type(self, connection)
		return "ThresholdArrayField"

	def from_db_value(self, value, expression, connection):

		if value is None:
			return value

		rangeValues = [int(x) for x in value.split(",")]

		return rangeValues

	def to_python(self, value):

		if value is None:
			return value

		if isinstance(value, list):
			return value
		
		# TODO: Need to implement

		return None

	def get_prep_value(self, value):

		if len(value) == 0:
			raise ValidationError("Invalid Threshold value: length=" + len(value))

		# TODO: Need to implement

		return None

