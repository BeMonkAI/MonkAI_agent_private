import logging
import functools

def validate(validation_func):
    def decorator_validate(func):
        @functools.wraps(func)
        def wrapper_validate(authority, *args, **kwargs):
            if validation_func(authority):
                logging.info("User is validated")
                return func(authority, *args, **kwargs)
            else:
                logging.warning("User is not validated for this functionality")
                return "User is not validated for this functionality"
        
        return wrapper_validate
    return decorator_validate

# Example usage
def is_user_valid(user):
    if user=="valid_user":
        return True
    else:
        return False

@validate(is_user_valid)
def some_protected_function(user):
    return f"Access granted to {user} "

