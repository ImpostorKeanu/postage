# Postage: a modularized email sender

More documentation coming eventually.

# Sending a Single Email

```
# ./postage single --help

usage: Postage: Send them emails single [-h] --module {sendgrid_api}
                                        [--module-arguments-file MODULE_ARGUMENTS_FILE]
                                        --from-address FROM_ADDRESS
                                        --to-addresses TO_ADDRESSES
                                        [TO_ADDRESSES ...] --subject SUBJECT
                                        --content CONTENT

Send a single email.

optional arguments:
  -h, --help            show this help message and exit
  --module {sendgrid_api}, -m {sendgrid_api}
                        Module to use.
  --module-arguments-file MODULE_ARGUMENTS_FILE, -maf MODULE_ARGUMENTS_FILE
                        A file containing additional argument that will be
                        passed to the sender module. This is useful in
                        situations where credentials need to be supplied and
                        you would like to avoid writing them to the console
                        window.
  --from-address FROM_ADDRESS, -f FROM_ADDRESS
                        Address from which the email will originate.
  --to-addresses TO_ADDRESSES [TO_ADDRESSES ...], -t TO_ADDRESSES [TO_ADDRESSES ...]
                        One or more of the following space delimited values:
                        individual email addresses, file containing email
                        addresses.
  --subject SUBJECT, -s SUBJECT
                        Subject of the email being sent.
  --content CONTENT, -c CONTENT
                        String or input file for email body

```

# Sending Emails from a CSV

```
# ./postage csv --help

usage: Postage: Send them emails csv [-h] --module {sendgrid_api}
                                     [--module-arguments-file MODULE_ARGUMENTS_FILE]
                                     --csv-file CSV_FILE [--log-file LOG_FILE]
                                     --body-template BODY_TEMPLATE
                                     [--subject-template SUBJECT_TEMPLATE]
                                     [--jitter-minimum JITTER_MINIMUM]
                                     [--jitter-maximum JITTER_MAXIMUM]

Send emails from csv. Fields are extracted from the header file of the CSV and
are used to update content in the email and subject. Fields are designated
using the following case-sensitive syntax: <<<:FIELD_NAME:>>>. FIELD_NAME is
mapped back to the header of each column in the CSV. If a random value is
required, use this tag: <<<:RANDOM:>>>.

optional arguments:
  -h, --help            show this help message and exit

General Arguments:
  Use the following parameters to configure general capabilities.

  --module {sendgrid_api}, -m {sendgrid_api}
                        Module to use.
  --module-arguments-file MODULE_ARGUMENTS_FILE, -maf MODULE_ARGUMENTS_FILE
                        A file containing additional argument that will be
                        passed to the sender module. This is useful in
                        situations where credentials need to be supplied and
                        you would like to avoid writing them to the console
                        window.
  --csv-file CSV_FILE, -cf CSV_FILE
                        CSV file containing records to send. Must have a
                        column for each update field within the template file.
                        The following columns are required: from_address,
                        to_address.
  --log-file LOG_FILE, -lf LOG_FILE
                        Log file to receive full content. Useful when random
                        values are generated.

Email Configuration:
  Configure how each email will be formatted. See the description of this
  subcommand for information on how formatting works.

  --body-template BODY_TEMPLATE, -bt BODY_TEMPLATE
                        File containing email body. Supports update fields;
                        see the description of this subcommand for more
                        information on this capability.
  --subject-template SUBJECT_TEMPLATE, -st SUBJECT_TEMPLATE
                        Template for all subjects. Update fields can be
                        applied here. See the description of this subcommand
                        for more information.

Jitter Parameters:
  Configure sleep time between sending emails. Integer values supported
  only. Suffix a multiplier to the end of an integer to determine a
  multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.

  --jitter-minimum JITTER_MINIMUM, -jmin JITTER_MINIMUM
                        Minimium time to sleep between sending emails.
  --jitter-maximum JITTER_MAXIMUM, -jmax JITTER_MAXIMUM
                        Maximum time to sleep between sending emails.

```
