import re


def validate_email(email):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    is_valid = bool(re.match(email_validate_pattern, email))
    return is_valid
