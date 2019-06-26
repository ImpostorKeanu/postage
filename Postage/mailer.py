#!/usr/bin/env python3

from Postage.decorators import mailer_init
from Postage.argument import *

class Mailer:
    '''Simple mailer class that which all future mailers should inherit. The
    interface will use methods defined here to send emails.
    '''

    REQUIRED_ATTRIBUTES = ['from_address','to_addresses','subject',
        'content']

    def __init__(self,from_address,to_addresses,subject,content,
            *args, **kwargs):
        '''
        - from - string value - from email
        - to - list of strings - list of email recipients
        - subject - string - email subject
        - content - string - email body
        '''

        # =============================
        # INITIALIZE INSTANCE VARIABLES
        # =============================

        self.from_address = from_address 
        self.subject = subject 
        self.content = content

        # ====================================
        # TO SHOULD BE AN ITERABLE IF PROVIDED
        # ====================================
        
        if to_addresses and not hasattr(to_addresses,'__iter__'):
            # Non-list value; make a list
            self.to_addresses = [to_addresses]
        elif to_addresses:
            # Just set the list
            self.to_addresses = to_addresses
        else:
            # Set to_addresses an empty list
            self.to_addresses = []

        self.validated = False
        self.validated_successfully = False

    def send(self,*args,**kwargs):
        '''This should be overriden by child classes.
        '''

        raise Exception(
            'This method should be overridden by child classes'
        )

    def validate(self):
        '''Assure that all required attributes are provided.
        '''
        
        missing = [r for r in Mailer.REQUIRED_ATTRIBUTES if not hasattr(self,r)]
        
        validated = True

        if missing:
            assert not missing, (
                f'Mailer object variables are missing: ", ".join(missing)'
            )
        else:
            self.validated_successfully = True



