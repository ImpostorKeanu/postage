#!/usr/bin/env python3

import importlib
import argparse
import Postage
import re
from Postage.argument import *
from Postage import modules
from Postage.string_fix import *
from Postage import validators
from Postage import misc
from Postage.jitter import *
from pathlib import Path
from types import ModuleType
from Postage.csv import CSV,Record
from datetime import datetime
from sys import exit

def add_args(dst_obj,args):
    '''Add arguments to a parser object. Useful when initializing
    an argument group.
    '''

    for arg in args:
        dst_obj.add_argument(*arg.pargs, **arg.kwargs)

if __name__ == '__main__':

    # ===============
    # BUILD INTERFACE
    # ===============

    parser = argparse.ArgumentParser(
        description='''Send emails using one of multiple modules, which are
        generallye associated with a specific email service, such as SendGrid or
        Office365. Inputs for these messages are received via CSV file and each
        field within the CSV file is accessible during templating as each email
        is constructed and sent.
        ''',
    )
    sp = subparsers = parser.add_subparsers(help='Module selection.')
    sp.required=True
    sp.dest='module'

    for handle,module in modules.handles.items():

        sub = subparsers.add_parser(handle,help=module.help)
        for arg in module.args:

            if arg.__class__ == ArgumentGroup:
                group = sub.add_argument_group(*arg.pargs,**arg.kwargs)
                add_args(group,arg)
            elif arg.__class__ == MutuallyExclusiveArgumentGroup:
                group = sub.add_mutually_exclusive_group(
                        *arg.pargs,**arg.kwargs
                )
                add_args(group,arg)
            else:
                sub.add_argument(*arg.pargs,**arg.kwargs)

    # ========================
    # DEFINE GENERIC ARGUMENTS
    # ========================


    args = parser.parse_args()
    module = modules.handles[args.module]

    # ====================
    # PREPARE THE LOG FILE
    # ====================

    lp = Path(args.log_file)

    if lp.exists(): log = open(lp.__str__(),'a')
    else: log = open(lp.__str__(),'w')

    # ==================
    # PREPARE THE JITTER
    # ==================

    jitter = Jitter(
        args.jitter_minimum,
        args.jitter_maximum
    ) 

    # ==================
    # GET THE EMAIL BODY
    # ==================

    body_html_template = misc.expand_and_join(
        args.body_html_template
    )

    body_text_template = misc.expand_and_join(
        args.body_text_template
    )

    # ==================
    # PARSE THE CSV FILE
    # ==================

    pp(f'Parsing: {args.csv_file}')

    c = CSV(args.csv_file)

    if not 'from_address' in c.headers or not 'to_address' in c.headers:

        raise Exception(
            'CSV header must have "from_address" and "to_address"'
        )

    elif not args.subject_template and not 'subject' in c.headers:

        raise Exception(
            '''"subject" field must be set in CSV or using the
            subject_template commandline argument.
            '''
        )

    pp(f'Sending emails')

    for record in c.records:
    
        # ===========================
        # UPDATE SUBJECT/BODY CONTENT
        # ===========================

        html_body = record.update_content(body_html_template)
        text_body = record.update_content(body_text_template)

        if args.subject_template:

            subject = record.update_content(
                args.subject_template
            )

        else:

            subject = record.update_content(
                record.subject
            )

        # ====================
        # SEND EMAIL AND SLEEP
        # ====================

        response, error = module(
            from_address=record.from_address,
            to_addresses=[record.to_address],
            subject=subject,
            html_content=html_body,
            text_content=text_body,
            args=args
        ).send()

        # =====================
        # LOG THE EMAIL TO DISK
        # =====================

        if error: status = 'FAILED'
        else: status = 'SUCCESS'

        log_record = '\n\n========[RECORD DELIMITER]========\n\n' \
            f'time_sent:{datetime.now()}\n' \
            f'status:{status}\n' \
            f'from_address:{record.from_address}\n' \
            f'to_address:{record.to_address}\n' \
            f'subject:{subject}\n' \
            f'content:\n\n{text_body}\n'

        log.write(log_record)                

        if not error:

            print(
                fix(
                    f'Sent: {record.from_address} > {record.to_address} [{subject}]',
                    prefix='-')
                )
    
        else:

            ep(f'FAILED: {record.from_address} > {record.to_address} ({error})')
        
        jitter.sleep()
    
    pp('Finished!')
    ep('Exiting')
