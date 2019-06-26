#!/usr/bin/env python3

from Postage import decorators

@decorators.expand_value
def expand_value(*v):
    '''Determine if a value is a file. If so, return the lines
    from that file in a list. Return the value as is otherwise.
    '''

    return v

@decorators.expand_value
def expand_and_join(*v,delimiter='\n'):
    '''Functions just as `expand_value`, except values are joined
    on a common delimiter.
    '''

    return delimiter.join(v)
