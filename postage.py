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
from Postage.exceptions import MalformedMessageRecordException
from Postage.jitter import *
from pathlib import Path
from types import ModuleType
from Postage.csv import CSV,Record
from datetime import datetime
from sys import exit
import pdb

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

        sub = subparsers.add_parser(
                handle,
                description=module.description,
            )
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
    module = modules.handles[args.module](args)

    # Perform any additional module initializations
    if 'module_init' in module.__dict__:
        module.module_init(args)

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
    # PARSE THE CSV FILE
    # ==================

    pp(f'Parsing: {args.csv_file}')

    c = CSV(args.csv_file)

    pp(f'Sending emails')

    for record in c.records:

        # ====================
        # SEND EMAIL AND SLEEP
        # ====================

        status = 'SUCCESS'
        try:
            message_attributes = ma = \
                    module.send(record=record)
        except MalformedMessageRecordException as e:
            status = 'FAILED'
            print(f"Invalid CSV record: {e}")
            continue
        except Exception as e:
            pp("Unhandled exception occurred:\n\n\n")
            raise e

        # =====================
        # LOG THE EMAIL TO DISK
        # =====================

        log.write('\n\n========[ RECORD DELIMITER ]========\n\n' \
            f'time_sent:{datetime.now()}\n' \
            f'status:{status}\n' \
            f'from_address:{ma["sender_address"]}\n' \
            f'to_address:{ma["recipient_address"]}\n' \
            f'subject:{ma["subject"]}\n' \
            f'content:\n\n{ma["body"]}\n')

        print(
            fix(
                f'Sent: {ma["sender_address"]} > ' \
                f'{ma["recipient_address"]} [{ma["subject"]}]',
                prefix='-'
            )
        )
        
        jitter.sleep()
    
    pp('Finished!')
    ep('Exiting')
