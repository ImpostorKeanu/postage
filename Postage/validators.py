#!/usr/bin/env python3

def module(m):
    '''Validate that a module has a `Module` class.
    '''

    dct = m.__dict__()
    assert 'Module' in dct, (
        'modules must have a Module class'
    )

    return dct['Module']
