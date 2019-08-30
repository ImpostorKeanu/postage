#!/usr/bin/env python3

from Postage.decorators import mailer_init
from Postage.argument import *

class Mailer:
    '''Simple mailer class that which all future mailers should inherit. The
    interface will use methods defined here to send emails.
    '''

    REQUIRED_ATTRIBUTES = ['from_address','to_addresses','subject',
        'html_content','text_content']


    tg = template_group = ArgumentGroup(
        title='Template Arguments',
        description='These arguments define the values that will build '\
        'the body and subject of outbound emails. Body values '\
        'in text and HTML formats are provided as file names, '\
        'where the subject is provided as a single string.')

    tg.append(Argument('--body-text-template','-btt',
        required=True,
        help='''File containing email body. Supports update fields; see 
        the description of this subcommand for more information on this
        capability. Required: %(required)s
        '''
    ))

    tg.append(Argument('--body-html-template','-bht',
        required=True,
        help='''File containing the HTML email body. Supports update fields; see 
        the description of this subcommand for more information on this
        capability. Required: %(required)s
        '''
    ))
    
    tg.append(Argument('--subject-template','-st',
        required=True,
        help='''Template string for all subjects. Update fields can be applied here.
         See the description of this subcommand for more information. Required: %(required)s
        '''
    ))


    jitter_group = jg = ArgumentGroup(title='Jitter Parameters',
        description='''Configure sleep time between sending emails. Integer values
        supported only. Suffix a multiplier to the end of an integer to determine
        a multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.
        ''')

    jg.append(Argument('--jitter-minimum','-jmin',
        default='1s',
        help='''Minimium time to sleep between sending emails. Default: %(default)s
        '''
    ))
    jg.append(Argument('--jitter-maximum','-jmax',
        default='1s',
        help='''Maximum time to sleep between sending emails. Default: %(default)s
        '''
    ))

    iog = io_group = ArgumentGroup(title='I/O Parameters',
        description='Set input/output configurations for the CSV and log files')
    iog.append(Argument('--log-file','-lf',
        default='postage.log',
        help='''Log file to receive full content. Useful when random
        values are generated. Default: %(default)s''')
    ),
    iog.append(Argument('--csv-file','-cf',
        required=True,
        help='''File containing CSV records. Fields are extracted from the
        header file of the CSV and are used to update content in the email
        and subject. Fields are designated using the following case-sensitive
        syntax: <<<:FIELD_NAME:>>>. FIELD_NAME is mapped back to the header
        of each column in the CSV. If a random value is required, use this
        tag: <<<:RANDOM:>>>. REQUIRED FIELDS: to_address, from_address.
        Required: %(required)s''')
    )

    DEFAULT_ARGUMENTS = [
        tg,
        jg,
        iog
    ]

    def __init__(self,from_address,to_addresses,subject,html_content,
            text_content,*args, **kwargs):
        '''
        - from - string value - from email
        - to - list of strings - list of email recipients
        - subject - string - email subject
        - content - string - email body
        - text_content - string - email body (text)
        '''

        # =============================
        # INITIALIZE INSTANCE VARIABLES
        # =============================

        self.from_address = from_address 
        self.subject = subject 
        self.html_content = html_content
        self.text_content = text_content

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
                f'Mailer object variables are missing: {", ".join(missing)}'
            )
        else:
            self.validated_successfully = True



