from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from string import ascii_lowercase, ascii_uppercase, digits

symbol = '!@$%%_'
charTypes = [ascii_lowercase, ascii_uppercase, digits, symbol]

class UpperLowerNumSymValidator:
    def validate(self, password, user=None):
        for charType in charTypes:
            if not any(x in charType for x in password):
                raise ValidationError(
                    _("This password must contain at least one of " + charType),
                    code ='password_missing_character',
                    params={'Needs': charType},
                    )

    def get_help_text(self):
        return _("This password must contain at least one Upper and lowercase letter, number, and symbol")