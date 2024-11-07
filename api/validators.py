from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_identification_num(value):
    if len(value) != 13:
        raise ValidationError(_("%(value)s is supposed to be 13 digits"))

def validate_phone_num(value):
    if len(value) != 10:
        raise ValidationError(_("%(value)s is supposed to be 10 digits"))