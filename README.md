# Postage: a modularized email sender

More documentation coming soon.

# Usage

First, select a module. List modules by running the script and passing `--help` as an argument:

```
./postage --help
```

Then you can get a comprehensive list of arguments:

```
./postage.py sendgrid_api --help
usage: postage.py sendgrid_api [-h] --body-text-template BODY_TEXT_TEMPLATE
                               --body-html-template BODY_HTML_TEMPLATE
                               --subject-template SUBJECT_TEMPLATE
                               [--jitter-minimum JITTER_MINIMUM]
                               [--jitter-maximum JITTER_MAXIMUM]
                               [--log-file LOG_FILE] --csv-file CSV_FILE
                               --api-key API_KEY

optional arguments:
  -h, --help            show this help message and exit
  --api-key API_KEY, -ak API_KEY
                        SendGrid API key

Template Arguments:
  These arguments define the values that will build the body and subject of
  outbound emails. Body values in text and HTML formats are provided as file
  names, where the subject is provided as a single string.

  --body-text-template BODY_TEXT_TEMPLATE, -btt BODY_TEXT_TEMPLATE
                        File containing email body. Supports update fields;
                        see the description of this subcommand for more
                        information on this capability. Required: True
  --body-html-template BODY_HTML_TEMPLATE, -bht BODY_HTML_TEMPLATE
                        File containing the HTML email body. Supports update
                        fields; see the description of this subcommand for
                        more information on this capability. Required: True
  --subject-template SUBJECT_TEMPLATE, -st SUBJECT_TEMPLATE
                        Template string for all subjects. Update fields can be
                        applied here. See the description of this subcommand
                        for more information. Required: True

Jitter Parameters:
  Configure sleep time between sending emails. Integer values supported
  only. Suffix a multiplier to the end of an integer to determine a
  multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.

  --jitter-minimum JITTER_MINIMUM, -jmin JITTER_MINIMUM
                        Minimium time to sleep between sending emails.
                        Default: 1s
  --jitter-maximum JITTER_MAXIMUM, -jmax JITTER_MAXIMUM
                        Maximum time to sleep between sending emails. Default:
                        1s

I/O Parameters:
  Set input/output configurations for the CSV and log files

  --log-file LOG_FILE, -lf LOG_FILE
                        Log file to receive full content. Useful when random
                        values are generated. Default: postage.log
  --csv-file CSV_FILE, -cf CSV_FILE
                        File containing CSV records. Fields are extracted from
                        the header file of the CSV and are used to update
                        content in the email and subject. Fields are
                        designated using the following case-sensitive syntax:
                        <<<:FIELD_NAME:>>>. FIELD_NAME is mapped back to the
                        header of each column in the CSV. If a random value is
                        required, use this tag: <<<:RANDOM:>>>. REQUIRED
                        FIELDS: to_address, from_address. Required: True
```
