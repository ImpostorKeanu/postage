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
from sys import exit

if __name__ == '__main__':

    # ===============
    # BUILD INTERFACE
    # ===============

    parser = argparse.ArgumentParser(
        'Postage: Send them emails',
        description='''Use a module to send one or more emails. Select one of the following
        subcommands for additional information.
        ''',
    )
    sp = subparsers = parser.add_subparsers()

    # ========================
    # DEFINE GENERIC ARGUMENTS
    # ========================

    module_argument = Argument('--module','-m',
        choices=modules.handles.keys(),
        required=True,
        help='''Module to use.
        '''
    )
    module_arguments = Argument('--module-arguments-file','-maf',
        required=False,
        help='''A file containing additional argument that will be
        passed to the sender module. This is useful in situations
        where credentials need to be supplied and you would like to
        avoid writing them to the console window.
        ''')

    # =====================
    # SEND INDIVIDUAL EMAIL
    # =====================

    single_parser = sp.add_parser('single',
        description='''Send a single email.
        ''')
    module_argument.add(single_parser)
    module_arguments.add(single_parser)
    single_parser.add_argument('--from-address','-f',
        required=True,
        help='''Address from which the email will originate.
        '''
    )

    single_parser.add_argument('--to-addresses','-t',
        required=True,
        nargs='+',
        help='''One or more of the following space delimited values: 
        individual email addresses, file containing email addresses.
        '''
    )

    single_parser.add_argument('--subject','-s',
        required=True,
        help='''Subject of the email being sent.
        '''
    )

    single_parser.add_argument('--content','-c',
        required=True,
        help='''String or input file for email body
        ''')
    single_parser.set_defaults(cmd='single')

    # ====================
    # LIST MODULES COMMAND
    # ====================

    list_parser = sp.add_parser('list',
        description='''List available modules.
        ''')
    list_parser.set_defaults(cmd='list')

    # ==================
    # SEND FROM CSV FILE
    # ==================

    csv_parser = sp.add_parser('csv',
        description='''Send emails from csv. Fields are extracted from the
        header file of the CSV and are used to update content in the email
        and subject. Fields are designated using the following case-sensitive
        syntax: <<<:FIELD_NAME:>>>. FIELD_NAME is mapped back to the header
        of each column in the CSV. If a random value is required, use this
        tag: <<<:RANDOM:>>>.
        ''')

    csv_gen = csv_parser.add_argument_group('General Arguments',
        '''Use the following parameters to configure general
        capabilities.
        ''')

    module_argument.add(csv_gen)
    module_arguments.add(csv_gen)

    csv_gen.add_argument('--csv-file','-cf',
        required=True,
        help='''CSV file containing records to send. Must have a column
        for each update field within the template file. The following
        columns are required: from_address, to_address.
        '''
    )

    csv_gen.add_argument('--log-file','-lf',
        default='postage.log',
        help='''Log file to receive full content. Useful when random
        values are generated.'''
    )

    email_group = eg = csv_parser.add_argument_group('Email Configuration',
        '''Configure how each email will be formatted. See the description
        of this subcommand for information on how formatting works.
        '''
    )

    eg.add_argument('--body-template','-bt',
        required=True,
        help='''File containing email body. Supports update fields; see 
        the description of this subcommand for more information on this
        capability.
        '''
    )

    eg.add_argument('--subject-template','-st',
        required=False,
        help='''Template for all subjects. Update fields can be applied here.
         See the description of this subcommand for more information.
        '''
    )

    jitter_group = jg = csv_parser.add_argument_group('Jitter Parameters',
        '''Configure sleep time between sending emails. Integer values
        supported only. Suffix a multiplier to the end of an integer to determine
        a multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.
        ''')
    jg.add_argument('--jitter-minimum','-jmin',
        default='1s',
        help='''Minimium time to sleep between sending emails.
        '''
    )
    jg.add_argument('--jitter-maximum','-jmax',
        default='1s',
        help='''Maximum time to sleep between sending emails.
        '''
    )
    csv_parser.set_defaults(cmd='csv')

    args = parser.parse_args()

    if args.cmd == 'list':
        pp('Printing module list:')
        print('\n- '+'\n- '.join(modules.handles.keys()))
        exit()

    module = modules.handles[args.module].Module

    if args.cmd == 'single':

        args.to_addresses = misc.expand_value(*args.to_addresses)
        args.content = misc.expand_and_join(args.content,delimiter='\n')
        sender = module(from_address=args.from_address,
            to_addresses=args.to_addresses,
            subject=args.subject,
            content=args.content,
            arguments_file=args.module_arguments_file)
        response, error = sender.send()

    elif args.cmd == 'csv':

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

        body_template = misc.expand_and_join(
            args.body_template
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

            body = record.update_content(body_template)

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
                content=body,
                arguments_file=args.module_arguments_file,
            ).send()

            # =====================
            # LOG THE EMAIL TO DISK
            # =====================

            if error: status = 'FAILED'
            else: status = 'SUCCESS'
    
            log_record = '\n\n========[RECORD DELIMITER]========\n\n' \
                f'status:{status}\n' \
                f'from_address:{record.from_address}\n' \
                f'to_address:{record.to_address}\n' \
                f'subject:{subject}\n' \
                f'content:\n\n{body}\n'
    
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
