# -*- coding: utf-8 -*-

import six


from wtforms import (Form as Model,
                     DateTimeField,
                     StringField as _StringField,
                     IntegerField as _IntegerField,
                     FloatField as _FloatField,
                     BooleanField as _BooleanField,
                     SelectField as _SelectField,
                     DecimalField, validators)

from wtforms.utils import unset_value

from wtforms.fields.core import Field as _Field, Label as _Label, UnboundField as _UnboundField


# --------------------------------------------------------------------------
# Monkey patch fo Field to add:
# - New parameter: required
# --------------------------------------------------------------------------
def new_field__init__(self, label=None, validators=None, filters=tuple(),
                      description='', id=None, default=None, widget=None,
                      render_kw=None, _form=None, _name=None, _prefix='',
                      _translations=None, _meta=None, required=False):

    self.required = required

    self.__old___init__(label=label, validators=validators, filters=filters,
                        description=description, id=id, default=default, widget=widget,
                        render_kw=render_kw, _form=_form, _name=_name, _prefix=_prefix,
                        _translations=_translations, _meta=_meta)

if not hasattr(_Field, "__old___init__"):
    _Field.__old___init__ = _Field.__init__
    _Field.__init__ = new_field__init__

BaseField = _Field


# --------------------------------------------------------------------------
# Monkey patch fo wftorm to add:
# - Enforce type checking
# - Change default str(..) actcion
# --------------------------------------------------------------------------
# Validate
def new_module_validate(self):
    """
    This function add the feature that checks data type in fields
    """
    for name, func in six.iteritems(self._fields):
        if hasattr(func, "validator"):
            if func.validator() is False:
                self._errors = {}

                if type(self._fields[name].data) is type(self._fields[name].__type__):
                    self._errors[name] = ("Data type incorrect or not default value "
                                          "provided. Got %s. Expected: %s" % (
                                              type(self._fields[name].data),
                                              self._fields[name].__type__))

                    return False

        # Checks required if object is an instance
        if type(self) is type:
            if self._fields[name].required is True:
                if self._fields[name].data is None and self._fields[name].default is None:
                    self._errors = {name: "Field '%s' is required" % name}
                    return False

    return self.old_validate()

if not hasattr(Model, "old_validate"):
    Model.old_validate = Model.validate
    Model.validate = new_module_validate


# --------------------------------------------------------------------------
# Field Monkey path
# --------------------------------------------------------------------------
def new_field_str(self):
    if self.__type__ is str:
        return str(self.data)
    else:
        return self.data


def new_file_repr(self):
    return str(self.data)

_Field.__str__ = new_field_str
_Field.__repr__ = new_file_repr


# --------------------------------------------------------------------------
# Label Monkey path
# --------------------------------------------------------------------------
def new_label_str(self):
    return str(self.text)

_Label.__str__ = new_label_str


# --------------------------------------------------------------------------
# New types:
#
# We must add new validator because WTForms don't check input types and
# doesn't raise exception when they doesn't matches.
# --------------------------------------------------------------------------
def _validator(self):
    to_check = self.data
    if to_check is None:
        if self.data is None:
            return True
        else:
            # to_check = self.default
            return False
    else:
        if not isinstance(to_check, self.__type__):
            return False
        else:
            return True


# --------------------------------------------------------------------------
class StringField(_StringField):
    """Improved String data that checks types"""
    __type__ = str
StringField.validator = _validator


# ----------------------------------------------------------------------
class IntegerField(_IntegerField):
    """Improved Integer data that checks types"""
    __type__ = six.integer_types
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
class BoolField(_BooleanField):
    """Improved bool data that checks types"""
    __type__ = bool
BoolField.validator = _validator


# --------------------------------------------------------------------------
# Especial fields
# --------------------------------------------------------------------------
# ----------------------------------------------------------------------
class SelectField(_SelectField):
    """Improved bool data that checks types"""
    __type__ = six.text_type
SelectField.validator = _validator
