#!/usr/bin/env python3

class Argument:
    '''Generic argument object which will pass args and kwargs to
    argparse.parser.add_argument.
    '''

    def __init__(self, *args, **kwargs):

        self.pargs = args
        self.kwargs = kwargs

    def add(self,target):

        target.add_argument(*self.pargs,**self.kwargs)

class ArgumentGroup(Argument,list):
    '''A list of arguments that will be added to an argument group.
    '''

    def __init__(self, arguments=[], *args, **kwargs):
        '''`arguments` is a list of Argument objects
        '''
        Argument.__init__(self,*args,**kwargs)
        
        # Validate and append arguments
        if arguments:
            for arg in arguments: self.append(arg)
        

    def append(self,arg):
        '''Append an argument to the list.
        '''

        self.validate_arg(arg)
        super().append(arg)

    def validate_arg(self,arg):
        '''Assure that the argument is of type Argument
        '''

        if arg.__class__ != Argument:
            raise TypeError('ArgumentGroup expects an type of Argument')

class MutuallyExclusiveArgumentGroup(ArgumentGroup):
    pass
