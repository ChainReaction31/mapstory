from django.db import models


class ArrayField(models.Field):
    description = "A container for data to be used as arrays"

    def __init__(self, *args, **kwargs):
        super(ArrayField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        pass

    def to_python(self, value):
        pass

    class Meta:
        abstract = True


class RgbField(ArrayField):
    description = "An array containing the integer values for RGB color definition"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 3
        super(RgbField, self).__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    @staticmethod
    def db_type(self, connection):
        return "RgbField"

    def from_db_value(self, value, expression, connection):

        if value is None:
            return value

        rgb_values = [int(x) for x in value.split(",")]

        return rgb_values

    def to_python(self, value):

        if value is None:
            return value

        if isinstance(value, list):
            return value

        rgb_values = [int(x) for x in value.split(",")]

        return rgb_values

    @staticmethod
    def get_prep_value(self, value):

        if len(value) != 3:
            raise ValidationError("Invalid RGB value: length=" + len(value))

        return ''.join(json.dumps(value, separator(',')))


class ThresholdField(ArrayField):
    description = "Container for value pairs as (min, max)"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        super(ThresholdField, self).__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    @staticmethod
    def db_type(self, connection):
        return "ThresholdField"

    def from_db_value(self, value, expression, connection):
        pass

    def to_python(self, value):
        pass

    class Meta:
        abstract = True


class IntThresholdField(ThresholdField):
    description = "Container for integer value pairs as (min, max)"

    def __init__(self, *args, **kwargs):
        super(IntThresholdField, self).__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        return name, path, args, kwargs

    def db_type(self, connection):
        return "IntThresholdField"

    def from_db_value(self, value, expression, connection):

        if value is None:
            return value

        range_values = [int(x) for x in value.split(",")]

        return range_values

    def to_python(self, value):

        if value is None:
            return value

        if isinstance(value, list):
            return value

        range_values = [int(x) for x in value.split(",")]

        return range_values

    @staticmethod
    def get_prep_value(self, value):

        if len(value) != 2:
            raise ValidationError("Invalid Threshold value: length=" + len(value))

        return ''.join(json.dumps(value, separator(',')))


class FloatThresholdField(ThresholdField):
    description = "Container for floating point precision value pairs as (min, max)"

    def __init__(self, *args, **kwargs):
        super(FloatThresholdField, self).__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        return name, path, args, kwargs

    @staticmethod
    def db_type(self, connection):
        return "DoubleThresholdField"

    def from_db_value(self, value, expression, connection):

        if value is None:
            return value

        range_values = [float(x) for x in value.split(",")]

        return range_values

    def to_python(self, value):

        if value is None:
            return value

        if isinstance(value, list):
            return value

        range_values = [float(x) for x in value.split(",")]

        return range_values

    @staticmethod
    def get_prep_value(self, value):

        if len(value) != 2:
            raise ValidationError("Invalid Threshold value: length=" + len(value))

        return ''.join(json.dumps(value, separator(',')))


class ThresholdArrayField(ArrayField):
    description = "An array containing threshold values"

    def __init__(self, array_field, *args, **kwargs):
        super(ThresholdArrayField, self).__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ChildB, self).deconstruct()
        return name, path, args, kwargs

    @staticmethod
    def db_type(self, connection):
        return "ThresholdArrayField"

    def from_db_value(self, value, expression, connection):

        if value is None:
            return value

        range_values = [int(x) for x in value.split(",")]

        return range_values

    def to_python(self, value):

        if value is None:
            return value

        if isinstance(value, list):
            return value

        # TODO: Need to implement

        return None

    @staticmethod
    def get_prep_value(self, value):

        if len(value) == 0:
            raise ValidationError("Invalid Threshold value: length=" + len(value))

        # TODO: Need to implement

        return None
