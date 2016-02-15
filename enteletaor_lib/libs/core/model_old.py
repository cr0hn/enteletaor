# -*- coding: utf-8 -*-
from schematics.exceptions import ConversionError, ValidationError
from schematics.models import Model as _Model
from schematics.types import BaseType as _BaseType, utf8_decode, unicode
from schematics.types import (StringType, IntType, FloatType, DateTimeType, IPv4Type,
                              URLType, EmailType, NumberType, LongType, DecimalType,
                              HashType, SHA1Type, BooleanType, DateType, UUIDType)
from schematics.types.compound import ListType


# region Monkey Patch


# --------------------------------------------------------------------------
# Monkey patch fo Schematics to add:
# - New property for types: "description"
# - Constructor of models without dicts, using instead **kwargs
# --------------------------------------------------------------------------
def __str__(self):
    return self.description


# ----------------------------------------------------------------------
def new_init(self, required=False, default=None, serialized_name=None,
             choices=None, validators=None, deserialize_from=None,
             serialize_when_none=None, messages=None,

             # Custom parameters
             description="Field description", is_file_results=False):

    # Call original constructor
    _BaseType.old__init__(self, required, default, serialized_name, choices, validators, deserialize_from,
                          serialize_when_none, messages)
    if not isinstance(description, str):
        raise TypeError("Expected str, got '%s' instead" % type(description))
    if not isinstance(is_file_results, bool):
        raise TypeError("Expected bool, got '%s' instead" % type(is_file_results))

    self.description = description
    self.is_file_results = is_file_results


# Monkey patch!
_BaseType.old__init__ = _BaseType.__init__
_BaseType.__init__ = new_init
# _BaseType.__str__ = __str__


# endregion
        

# --------------------------------------------------------------------------
# New type
# --------------------------------------------------------------------------
class FileType(_BaseType):
    allow_casts = (int, str)

    MESSAGES = {
        'convert'   : u"Couldn't interpret '{0}' as string.",
        'max_length': u"String value is too long.",
        'min_length': u"String value is too short."
    }

    def __init__(self, name=None, file_type=None, path=None, max_length=None, min_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.file_type = file_type
        self.path = path

        super(FileType, self).__init__(**kwargs)

    def to_native(self, value, context=None):
        if value is None:
            return None

        if not isinstance(value, unicode):
            if isinstance(value, self.allow_casts):
                if not isinstance(value, str):
                    value = str(value)
                value = utf8_decode(value)  # unicode(value, 'utf-8')
            else:
                raise ConversionError(self.messages['convert'].format(value))

        return value

    def validate_length(self, value):
        len_of_value = len(value) if value else 0

        if self.max_length is not None and len_of_value > self.max_length:
            raise ValidationError(self.messages['max_length'])

        if self.min_length is not None and len_of_value < self.min_length:
            raise ValidationError(self.messages['min_length'])


# --------------------------------------------------------------------------
# STB Model class
# --------------------------------------------------------------------------
class Model(_Model):
    MESSAGES = {
        "label": "Console label"
    }

    BASIC_REVERSE = {
        "IntType"     : "int",
        "URLType"     : "str",
        "IPv4Type"    : "str",
        "DateType"    : "str",
        "HashType"    : "str",
        "SHA1Type"    : "str",
        "FileType"    : "str",
        "LongType"    : "int",
        "EmailType"   : "str",
        "FloatType"   : "float",
        "NumberType"  : "int",
        "StringType"  : "str",
        "DecimalType" : "float",
        "BooleanType" : "bool",
        "DateTimeType": "str",
    }

    def __init__(self, raw_data=None, deserialize_mapping=None, strict=True, **kwargs):
        super(Model, self).__init__(raw_data=raw_data, deserialize_mapping=deserialize_mapping, strict=strict)

        for k, v in kwargs.items():
            if k in self.keys():
                setattr(self, k, v)


    # ----------------------------------------------------------------------
    def get_basic_types(self):
        """
		Get a dict with basic types
		"""
        results = {}
        for name, _type in self._fields.items():
            try:
                results[name] = self.BASIC_REVERSE[_type.__class__.__name__]
            except KeyError:
                pass
        return results

    # ----------------------------------------------------------------------
    def get_field_results(self):
        """
        Return the name of property that will contains the file results

        :return: a string with the name of field of file results
        :rtype: str

        """
        for name, _type in self._fields.items():
            if _type.is_file_results:
                return name

        return None


if __name__ == '__main__':
    class Testing(Model):
        p1 = FileType(is_file_results=True)

    m1 = Testing()

    print(m1.get_field_results())