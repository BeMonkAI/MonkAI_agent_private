import logging
import functools

def validate(validation_func):
    def decorator_validate(func):
        @functools.wraps(func)
        def wrapper_validate(authority, *args, **kwargs):
            if validation_func(authority):
                logging.info("User is valid")
                return func(authority, *args, **kwargs)
            else:
                logging.warning("User is not validated for this functionality. Do not perform the action.")
                return "User is not validated for this functionality. Do not perform the action."
        
        return wrapper_validate
    return decorator_validate



