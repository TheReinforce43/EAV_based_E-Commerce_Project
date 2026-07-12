
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



user_type = (
    ('customer', 'Customer'),
    ('vendor', 'Vendor'),
    ('admin', 'Admin'),
    
)



def validate_bd_phone_number(value):
    """
    Validates Bangladeshi phone numbers.
    Accepts:
        01636021298        (11 digits, local format)
        +8801636021298      (with country code)
        8801636021298       (country code, no +)
    """
    # Normalize: strip spaces, dashes
    cleaned = re.sub(r'[\s\-]', '', value)

    # Extract the local 11-digit part regardless of prefix
    match = re.fullmatch(r'(?:\+?88)?(01[3-9]\d{8})', cleaned)

    if not match:
        raise ValidationError(
            _("Enter a valid Bangladeshi phone number.")
        )

    return match.group(1)  # returns normalized 11-digit local number