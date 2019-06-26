#!/usr/bin/env python3

from Postage import validators
from pathlib import Path

def mailer_init(func):
    '''Assure that the class subclassing Mailer subclass
    provides all instance variables for assignment.
    '''

    def wrapper(*args,**kwargs):

        missing = validators.mailer_init(**kwargs)

        assert not missing, (
            'Mailer is missing the following keyword arguments: ' \
            ','.join(missing)
        )

        return func(*args, **kwargs)

    return wrapper

def expand_value(func):

    def wrapper(*values,**kwargs):
        
        ivals = []
        for v in values:

            path = Path(v)

            if path.exists() and path.is_dir():
                raise Exception(
                    f'Value is a directory, which is invalid: {v}'
                )
            elif path.exists() and path.is_file():
                with open(path.__str__()) as infile:
                    for line in infile: ivals.append(line.strip())
            else: ivals.append(v)

        return func(*ivals,**kwargs)

    return wrapper
