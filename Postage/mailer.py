#!/usr/bin/env python3

from Postage.decorators import mailer_init
from Postage.argument import *

jitter_group = jg = ArgumentGroup(title='Jitter Parameters',
    description='''Configure sleep time between sending emails. Integer values
    supported only. Suffix a multiplier to the end of an integer to determine
    a multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.
    '''
)

jg.append(Argument('--jitter-minimum','-jmin',
    default='1s',
    help='''Minimium time to sleep between sending emails. Default: %(default)s
    '''
    )
)

jg.append(Argument('--jitter-maximum','-jmax',
    default='1s',
    help='''Maximum time to sleep between sending emails. Default: %(default)s
    '''
    )
)

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
        and subject.
        '''
    )
)

DEFAULT_ARGUMENTS = [
    jg,
    iog
]

class Mailer:
    '''Simple mailer class that which all future mailers should inherit. The
    interface will use methods defined here to send emails.
    '''

    def scanRecordAttributes(self,r):
        '''Return a list of any attributes missing from the
        email record.
        '''

        return [
                a for a in self.__class__.MESSAGE_ATTRIBUTES
                if not hasattr(r,a)
            ]

    def validateRecord(self,r):

        missing = self.scanRecordAttributes(r)

        if missing:
            raise Exception(
                f"Message record missing attributes: {','.join(missing)}"
            )

    def send(self, record, *args, **kwargs):
        '''This should be overriden by child classes.
        '''

        raise Exception(
            'This method should be overridden by child classes'
        )

    def buildMessageAttributes(self,sender_address,recipient_address,
            subject,body):

        return {
                "sender_address":sender_address,
                "recipient_address":recipient_address,
                "subject":subject,
                "body":body
            }
