#!/usr/bin/env python3

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from Postage.mailer import Mailer
import json

class Module(Mailer):

    def __init__(self,arguments_file,*args,**kwargs):
        '''Initialize the module.
        '''


        self.parse_module_arguments(arguments_file)
        super().__init__(*args,**kwargs)

    @staticmethod
    def build_message(from_address, to_addresses, subject, content):
        '''Build the message before sending. Made as a static method
        to allow any other module to call it should it found to be
        useful.
        '''

        return Mail(
            from_email=from_address,
            to_emails=','.join(to_addresses),
            subject=subject,
            html_content=content
        )
    
    def send(self):
        '''Validate the current configuration and send the email.
        '''

        # Validate the configuration
        self.validate()

        # Initialize output variables
        response = None
        e = None

        # Send the email
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(Module.build_message(self.from_address,
                self.to_addresses, self.subject, self.content))
        except Exception as ex:
            e = ex

        return response,e

    def parse_module_arguments(self,infile):
        '''Extract an API key from the supplied input file.
        '''

        try:

            with open(infile) as infile:
                self.api_key = json.loads(infile.read())['API_KEY']          

        except Exception as e:

            print('Failed to load arguments file for the sendgrid module')
            raise e
