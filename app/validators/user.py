import re


def validate_register_schema(data):
    email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    required_params = {"name", "email", "password"}
    missing_params = check_missing_params(required_params, data)

    if missing_params:
        return -1, f"Some required params are missing: {missing_params}"

    if len(data.get('name')) > 30:
        return -1, "Name is not valid"

    if not re.search(email_regex, data.get("email")) or len(data.get("email")) > 30:
        return -1, "Email is not valid"

    if not re.search(password_regex, data.get("password")) or len(data.get("password")) > 30:
        return -1, "Password is invalid"

    return 1, "ok"


def validate_update_schema(data):
    email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    if 'name' in data and len(data.get('name')) > 30:
        return -1, "Name is not valid"

    if 'email' in data and (not re.search(email_regex, data.get("email")) or len(data.get("email")) > 30):
        return -1, "Email is not valid"

    if 'password' in data and (not re.search(password_regex, data.get("password")) or len(data.get("password")) > 30):
        return -1, "Password is invalid"

    return 1, "ok"


def check_missing_params(required_params, request_data):
    request_params = set(request_data.keys())
    return required_params - request_params
