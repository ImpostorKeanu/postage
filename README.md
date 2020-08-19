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

# Input Expectations

## Credentials

Credentials are handled individually by modules. For instance, the `office365_api`
module expects values for the `--client-id` and `--client-secret` flags to support
authentication. Use the `--help` flag for each module to identify required arguments.

## Email Addresses, Subject, Body, etc.

The postage interface expects that a single CSV file containing all messages to
be provided, one for each row. The header file will be used to map back to the
message attributes defined in the module per the `--help` flag.

I know this sounds painful but consider using a tool like
[Parsuite](https://github.com/arch4ngel/parsuite) and the `templatizer`
module to generate the input file.

Let's say we have a CSV file (`inputs.csv`) that we'd like to translate
to a CSV file for Postage:

```
first_name,last_name,email
Bob,Green,bgreen@yahoo.com
Alice,Orange,aorange@yahoo.com
```

And here are the templates defined for use with the `templatizer` module
in Parsuite.

```
export subject_template="<<<:first_name:>>>, you should unquestionably click this link!"
export html_template='<p>Hello <<<:first_name:>>>, click this link! https://www.evil.com?uid=<<<:RAND1:>>></p>'
```

This command would compile the CSV file required for Postage:

```
python3.8 parsuite.py templatizer --csv-file inputs.csv \
    -tts "<<<:RAND1:>>>" "<<<:first_name:>>>" \
    "<<<:last_name:>>>" "<<<:email:>>>" \
    "Evil Bill" "sender@evil.com" \
    "$subject_template" "$html_template"
```
And the output would be:

```
b3a2652sK9,Bob,Green,bgreen@yahoo.com,"Bob, you should unquestionably click this link!","<p>Hello Bob, click this link! https://www.evil.com?uid=b3a2652sK9</p>"
y0gdPUvr9h,Alice,Orange,aorange@yahoo.com,"Alice, you should unquestionably click this link!","<p>Hello Alice, click this link! https://www.evil.com?uid=y0gdPUvr9h</p>"
```

Now we add a header to the file to make sure it can be used with
the desired module. Let's say we're using the O365 module, which
requires the following components: sender_name, sender_address,
recipient_name, recipient_address, subject, html_body

```
id,recipient_name,recipient_last_name,recipient_address,subject,html_body,sender_name,sender_address
b3a2652sK9,Bob,Green,bgreen@yahoo.com,Evil Bill,"Bob, you should unquestionably click this link!","<p>Hello Bob, click this link! https://www.evil.com?uid=b3a2652sK9</p>"
y0gdPUvr9h,Alice,Orange,aorange@yahoo.com,"Alice, you should unquestionably click this link!","<p>Hello Alice, click this link! https://www.evil.com?uid=y0gdPUvr9h</p>"
```

Now the `sender_name` and `sender_address` fields need to be added
to the records. Assuming the same are being used for each target,
then sed could be used. Assuming output from the previous command
was dumped to `output.csv`:

```
sed -i -r -e 's/.$/,"Evil Bob",bob@evil.com/' output.csv
```

Now the CSV fils is Postage ready!

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
