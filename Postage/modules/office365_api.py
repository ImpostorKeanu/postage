#!/usr/bin/env python3

from Postage.mailer import Mailer,DEFAULT_ARGUMENTS
from Postage.argument import *
import O365 as O
from sys import exit
import warnings

warnings.filterwarnings('ignore')

class Module(Mailer):

    # ======================================
    # DEFINE REQUIRED CSV FIELDS FOR MESSAGE
    # ======================================

    MESSAGE_ATTRIBUTES=["sender_name","sender_address","recipient_name",
            "recipient_address","subject","html_body"]


    # ============================================================
    # DEFINE A USEFUL HELP MESSAGE ESTABLISHING MESSAGE ATTRIBUTES
    # ============================================================

    description=f'''Send emails using Office 365 via Azure application. Requires
    a username and password. The following attributes are required for
    each CSV record in order for this module to function: 

    {", ".join(MESSAGE_ATTRIBUTES)}
    '''

    # =======================
    # DEFINE MODULE ARGUMENTS
    # =======================

    args=[a for a in DEFAULT_ARGUMENTS if '-btt' not in a.pargs]+[
            Argument('--client-id','-ci',
                required=True,
                help='''Client id issued while registering the Azure
                application.
                '''
            ),
            Argument('--client-secret','-cs',
                required=True,
                help='''Client secret issued while registering the
                Azure application.
                '''
           )
    ]

    def __init__(self, args):
        '''Initialize the module.
        '''

        self.account = O.Account((args.client_id, args.client_secret))

        # Attempt authentication with necessary scopes
        if not self.account.authenticate(scopes=["message_all",
            "message_send","message_send_shared","message_all_shared"]):
            print("Authentication failed")
            exit()

    def send(self, record, *args, **kwargs):
        '''Validate the current configuration and send the email.
        '''

        self.validateRecord(record)

        # Initialie a new message
        message = m = self.account.mailbox().new_message()

        # Set the message attributes
        m.subject = record.subject
        m.sender.name = record.sender_name
        m.sender.address = record.sender_address
        m.to.add([(record.recipient_name,record.recipient_address)])
        m.body = record.html_body

        # Send the message
        m.send()
        return self.buildMessageAttributes(
                record.sender_address,
                record.recipient_address,
                record.subject,
                record.html_body)
