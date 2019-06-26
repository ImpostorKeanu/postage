#!/usr/bin/env python3

def fix(s,prefix=None,suffix=None,end='\n',file=None,*args,**kwargs):
    '''Suffix/prefix the `s` string.
    '''

    prefix = prefix or ''
    suffix = suffix or ''
    end = end or '\n'
    file = file

    return f'{prefix} {s} {suffix}'

def pos_print(s,prefix='[+]',suffix=None,*args,**kwargs):
    '''Print with the positive char
    '''

    print(fix(s,prefix,suffix),*args,**kwargs)

def neg_print(s,prefix='[-]',suffix=None,*args,**kwargs):
    '''Print with the negative char
    '''

    print(fix(s,prefix,suffix),*args,**kwargs)

def exc_print(s,prefix='[!]',suffix=None,*args,**kwargs):
    '''Print with the excalamation char
    '''

    print(fix(s,prefix,suffix),*args,**kwargs)

pp = pos_print
np = neg_print
ep = exc_print
