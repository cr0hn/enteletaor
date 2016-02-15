# -*- coding: utf-8 -*-

import six

from wtforms import (Form as Model,
                     DateTimeField,
                     StringField as _StringField,
                     IntegerField as _IntegerField,
                     FloatField as _FloatField,
                     BooleanField as _BooleanField,
                     DecimalField, validators)
from wtforms.fields.core import Field as _Field, Label as _Label
from wtforms.utils import unset_value


# --------------------------------------------------------------------------
# Monkey patch fo wftorm to add:
# - Enforce type checking
# - Change default str(..) actcion
# ----------------------------------------------------------------------
# Validate
def new_module_validate(self):
    for name, func in six.iteritems(self._fields):
        if hasattr(func, "validator"):
            if func.validator() is False:
                self._errors = {name: "Data type incorrect"}
                return False

    return self.old_validate()

if not hasattr(Model, "old_validate"):
    Model.old_validate = Model.validate
    Model.validate = new_module_validate


# --------------------------------------------------------------------------
# Field Monkey path
# --------------------------------------------------------------------------
def new_field_str(self):
    return str(self.data)

_Field.__str__ = new_field_str
_Field.__repr__ = new_field_str


# --------------------------------------------------------------------------
# Label Monkey path
# --------------------------------------------------------------------------
def new_label_str(self):
    return self.text

_Label.__str__ = new_label_str

# --------------------------------------------------------------------------
# Base rename
# --------------------------------------------------------------------------
BaseField = _Field


# --------------------------------------------------------------------------
# New types:
#
# We must add new validator because WTForms don't check input types and
# doesn't raise exception when they doesn't matches.
# --------------------------------------------------------------------------
def _validator(self):
    to_check = self.data
    if to_check is None:
        to_check = self.default
    return isinstance(to_check, self.__type__)


# --------------------------------------------------------------------------
class StringField(_StringField):
    """Improved String data that checks types"""
    __type__ = str
StringField.validator = _validator


# ----------------------------------------------------------------------
class IntegerField(_IntegerField):
    """Improved Integer data that checks types"""
    __type__ = int
IntegerField.validator = _validator


# ----------------------------------------------------------------------
class IncrementalIntegerField(IntegerField):
    """Special Int indicates their value can be handler by increments, not by assigns"""
    __type__ = int
IncrementalIntegerField.validator = _validator


# ----------------------------------------------------------------------
class FloatField(_FloatField):
    """Improved fload data that checks types"""
    __type__ = float
FloatField.validator = _validator


# ----------------------------------------------------------------------
class BoolField(_FloatField):
    """Improved bool data that checks types"""
    __type__ = bool
BoolField.validator = _validator
