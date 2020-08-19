#!/usr/bin/env python3

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from Postage.mailer import Mailer, DEFAULT_ARGUMENTS
from Postage.argument import *
import json

class Module(Mailer):

    # ======================================
    # DEFINE REQUIRED CSV FIELDS FOR MESSAGE
    # ======================================

    MESSAGE_ATTRIBUTES=["from_email","to_address","subject",
            "html_content","plain_text_content"]


    description=f'''Send emails using the sendgrid API. Requires an API
    key. The following attributes are required for each record in
    the CSV file:

    {", ".join(MESSAGE_ATTRIBUTES)}
    '''

    # =======================
    # DEFINE MODULE ARGUMENTS
    # =======================

    args=DEFAULT_ARGUMENTS+[
            Argument('--api-key','-ak',
                required=True,
                help='SendGrid API key'
            )
    ]

    def __init__(self, args):
        '''Initialize the module.
        '''

        # Set the client from the api key
        self.client = SendGridAPIClient(args.api_key)

    def send(self):
        '''Validate the current configuration and send the email.
        '''

        self.validateRecord(record)

        # Send the email
        response = self.client.send(
            Mail(
                from_email=record.from_email,
                to_emails=[record.to_address],
                subject=record.subject,
                html_content=record.html_content,
                plain_text_content=record.plain_text_content
            )
        )

        # Return the expected dictionary output for logging
        return self.buildMessageAttributes(
                record.from_email,
                record.to_address,
                record.subject,
                record.text_body
            )
