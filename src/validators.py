import re

def is_valid_email(email):
    if not isinstance(email, str):
        return False
    if not email:
        return False
    pattern = r"^[\w\.\+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def is_valid_password(password):
    if not isinstance(password, str):
        return {"valid": False, "errors": ["invalid_type"]}
    if not password:
        return {"valid": False, "errors": ["empty_password"]}
    
    errors = []
    if len(password) < 8:
        errors.append("too_short")
    if not re.search(r"[A-Z]", password):
        errors.append("missing_uppercase")
    if not re.search(r"[a-z]", password):
        errors.append("missing_lowercase")
    if not re.search(r"\d", password):
        errors.append("missing_digit")
    if not re.search(r"[!@#\$%\^&\*]", password):
        errors.append("missing_special")
        
    return {"valid": len(errors) == 0, "errors": errors}

def is_valid_age(age):
    if isinstance(age, bool):
        return False
    if isinstance(age, (int, float)):
        if isinstance(age, float) and not age.is_integer():
            return False
        return 0 <= age <= 150
    return False
