# CLI client

-------------------------------------------

## CONTENTS:

- ### [Command Line Interface (CLI)](#command-line-interface-cli-1)
- ### [Set-up](#set-up-1)
- ### [Usage](#usage-1)
- ### [Validation module](#validation-module-1)
- ### [Commands and REST/API calls](#commands-and-res-api-calls-1)
- ### [Public commands](#public-commands-1)
- ### [User commands](#user-commands-1)
- ### [Admin command](#admin-command-1)
- ### [Usefull comments](#usefull-commends-1)
- ### [CLI unit tests](#cli-unit-tests-1)

-------------------------------------------

## Command Line Interface (CLI):

This is a Command Line Interface tool we 
developed for some basic functions of our 
site. Each command requires one of the three 
user authorization levels (none, basic, admin).

-------------------------------------------

## Set-up:

After you have downloaded all the folders
and successfully run your server (See back-end 
README.md), open a command line prompt
and change to the folder containing the CLI 
files (cli-client). If you have created a 
virtual environment, make sure to activate 
it before you set up the CLI tool, because 
it is going to install complementary Python libraries.

Now, install the CLI tool using the command:

```pip install --editable .```

The setup.py then will install all modules
needed for the CLI tool to run as well as
create the CLI tool named **ev_group50.**

Now, open the file paths.py and fill the
"folder" variable in eith an existing path
in your system.

```folder='C:/Users/example/cli-client/'```

In this folder the CLI tool
will save the token file when a user logs in
as well as any temporary file needed.

You are all set! You can use our CLI tool!

-------------------------------------------

## Usage:

```ev_group50 [options] COMMAND [options]```

Some options are required and some are 
optional.

Type:

```ev_group50 --help```

to see all available commands and options.

or:

```ev_group50 COMMAND --help```

to see all command's available options.

-------------------------------------------

## Validation module:

Inside the cli-client folder there is a file
named validation.py. Inside this file
there are all the validation functions of 
the Command Line tool. The validation module
is imported into the main py file and anywhere
else validation of typed data is needed 
(usernames, passwards, keys etc)

-------------------------------------------

## Commands and REST/API calls:

>> admin                ---> System Administration
>> 
>> healthcheck          ---> REST API call: /healthcheck
>> 
>> login                ---> REST API call: /login
>> 
>> logout               ---> REST API call: /logout
>> 
>> resetsessions        ---> REST API call: /resetsessions
>> 
>> sessionsperev        ---> REST API call: /SessionsPerEV
>> 
>> sessionsperpoint     ---> REST API call: /SessionsPerPoint
>> 
>> sessionsperprovider  ---> REST API call: /SessionsPerProvider
>> 
>> sessionsperstation   ---> REST API call: /SessionsPerStation

-------------------------------------------

## Public commands:

- healthcheck

This command executes a sytem health ckeck.

User authorization level: **None**

REST API call: /healthckeck

>> NOTE: The function returns the system's
health status ("OK" on success / "failed"
on failure).

- resetsessions 

This command resets all charging sessions.

User authorization level: **None**

REST API call: /resetsessions

>> WARNING: After this call, all records of
charging sessions will be erased.

-------------------------------------------

## User commands:

- login

User log in command.

User authorization level: **None**

REST API call: /login

>> NOTE: If you are logged in with another
user account, you have to logout before
you can log in again.

- logout

User log out command.

User authorization level: **Connected user**

REST API call: /logout

>> NOTE: If you are not logged in, you cannot
logout (OBVIOUSLY!). Don't try to trick us!

- sessionsperpoint

This command displays all charging sessions
at a specific point, during the givven 
period of time.

User authorization level: **Connected user**

REST API call: /SessionsPerPoint

>> NOTE: Date options must be chronologically
correct. (--datefrom = starting date ,
--dateto = ending date)

- sessionsperstation

This command displays all charging sessions
at a specific station, during the givven 
period of time.

User authorization level: **Connected user**

REST API call: /SessionsPerStation

>> NOTE: Date options must be chronologically
correct. (--datefrom = starting date ,
--dateto = ending date)

- sessionsperev

This command displays all charging sessions
of a vehicle, during the givven period of
time.

User authorization level: **Connected user**

REST API call: /SessionsPerEV

>> NOTE: Date options must be chronologically
correct. (--datefrom = starting date ,
--dateto = ending date)

- sessionsperprovider

This command displays all charging sessions
from an energy provider, during the givven
period of time.

User authorization level: **Connected user**

REST API call: /SessionsPerProvider

>> NOTE: Date options must be chronologically
correct. (--datefrom = starting date ,
--dateto = ending date)


>> REMINDER: You can see all the required and
optional arguments of each command by typing:

```ev_group50 COMMAND --help```

-------------------------------------------

## Admin command:

System Administration Command

User authorization level: **Administrator**

- Options Usage

```sh --usermod --username username --passw password```
Using this parameter the administrator can
create a new user or update an existing
user's password. If the username exists,
then the passw argument will be the new
password of the user. If not, then a new
user with the username and password 
arguments will be created.
There is an optional parameter --role, where
you can declare the role of a new user.


```--healthcheck```
Using this parameter the administrator can
execute a system health check. The function
returns the system's health status ("OK" on
succes / "failed" on failure).


```--resetsessions```
Using this parameter the administrator can
reset all charging sessions as well as
initialize the default admin user (username:
admin, password: petrol4ever).
>> NOTE: The reset is final and after the 
execution of the function, all charging 
records will be
deleted.


```--users username```
Using this parameter the administrator can
see the information of a user.


```--sessionsupd --source filename```
Using this parameter the administrator can
"upload" a CSV file with charging sessions
data. The name of the file is stated in the
--source argument and the file itself must
be in multipart/from-data encoding.


>> NOTE: You can call multible function by 
entering more than one option parameters. The
options do not have to be in order.


>> NOTE: If more than one options are entered,
/healthcheck (if called) will be executed
first and /resetsessions (if called) last.

>> NOTE: Options resetsessions and sessionsupd
cannot be executed in the same command.

-------------------------------------------

## Usefull comments:

- Options ```--format``` and ```--apikey``` are required in all commands. The format of the request response can be "json" or "csv" and the apikey in
XXXX-XXXX-XXXX format.

- The available valid apikeys are listed in the text file apikeys.txt inside the folder.

- You can see all the required and optional arguments of each command by typing: ```ev_group50 COMMAND --help```


-------------------------------------------

## CLI unit tests

The functionality of the CLI commands was tested thoroughly. More specifically, we tested:

- Multiple logins from different role users
- Both json and csv format request in all formats
- All possible apikey errors
- All possible parameter skips, both optional(execution was continued) and required(exception was raised)
- Unauthorized requests
- Bad parameter entering
- All possible login-logout compinations (e.g. login while logged in)
- User entry
- Pasword change
- All **sessionsper** commands in deifferent periods of time and for multiple point/station/ev/provider
- Sessions update with local CSV file
- Updating existing sessions (so nothing happened)
- Reseting sessions data and updating it again

As most commands required a token file, we could not perform unit tests in all of them. In the **Unit-tests** folder the ```test_cli.py``` file contains some test for **healthcheck** and **login** commands. We can run a pytest by typing:

```pytest -v ```

In these cases, we test possible outcomes (e.g. Status: OK) or error messages due to exceptions (\nError: {'Not Authorized: Invalid API key'}\n)



