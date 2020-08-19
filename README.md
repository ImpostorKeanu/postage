# Postage: a modularized email sender

## Description

Postage is a modularized email sender to support phishing campaigns. Simple modules
are stored in the `Postage/modules` directory that detail the required arguments
for a given module to run. Generally speaking, a single module is written for one
service, e.g. the office365_api module details the arguments and provides logic to
send emails via O365.

## Why?

Because juggling tools and reinventing the wheel gets a bit old and this approach
provides a central interface to carpet bomb target email addresses.

# Installation

```
git clone https://github.com/arch4ngel/postage
cd postage
python3.8 -m pip install -r requirements.txt
```

# Supported Services

The following services are currently supported by Postage

- Office365, via the [O365 package](https://pypi.org/project/O365/)
- Sendgrid, via the [sendgrid-python package](https://github.com/sendgrid/sendgrid-python)

# Basic Usage

Listing modules: `python3.8 postage.py --help`

```
usage: postage.py [-h] {office365_api,sendgrid_api} ...

Send emails using one of multiple modules, which are generallye associated with a specific email service, such as SendGrid or Office365. Inputs for these messages are received via CSV file and each field within the CSV file is accessible during templating as each email is constructed and sent.

positional arguments:
  {office365_api,sendgrid_api}
                        Module selection.

optional arguments:
  -h, --help            show this help message and exit
  ```
  
  Getting module help: `python3.8 postage.py <module> --help`
  
  ```
  usage: postage.py office365_api [-h] [--jitter-minimum JITTER_MINIMUM] [--jitter-maximum JITTER_MAXIMUM] [--log-file LOG_FILE] --csv-file CSV_FILE --client-id CLIENT_ID --client-secret CLIENT_SECRET

Send emails using Office 365 via Azure application. Requires a username and password. The following attributes are required for each CSV record in order for this module to function: sender_name, sender_address, recipient_name, recipient_address, subject, html_body

optional arguments:
  -h, --help            show this help message and exit
  --client-id CLIENT_ID, -ci CLIENT_ID
                        Client id issued while registering the Azure application.
  --client-secret CLIENT_SECRET, -cs CLIENT_SECRET
                        Client secret issued while registering the Azure application.

Jitter Parameters:
  Configure sleep time between sending emails. Integer values supported only. Suffix a multiplier to the end of an integer to determine a multiplier: s,m,h. Example: 33m indicates a time of thirty-three minutes.

  --jitter-minimum JITTER_MINIMUM, -jmin JITTER_MINIMUM
                        Minimium time to sleep between sending emails. Default: 1s
  --jitter-maximum JITTER_MAXIMUM, -jmax JITTER_MAXIMUM
                        Maximum time to sleep between sending emails. Default: 1s

I/O Parameters:
  Set input/output configurations for the CSV and log files

  --log-file LOG_FILE, -lf LOG_FILE
                        Log file to receive full content. Useful when random values are generated. Default: postage.log
  --csv-file CSV_FILE, -cf CSV_FILE
                        File containing CSV records. Fields are extracted from the header file of the CSV and are used to update content in the email and subject.
```
