import click
import paths
import os.path
import os
import requests
import validation
import json
import csv
import time
import public_commands



@click.group()
def cli():

    """\b
       -------------------------------------------
       Hello we are team 50. Welcome to our CLI!
       -------------------------------------------

       \b
       This is a Command Line tool we developed
       for some basic functions of our site. Each
       command requires one of the three user
       authorization levels (none, basic, admin).

       \b
       For more information about each command
       use the --help option:
       ev_group50 [COMMAND] --help

       \b
       -------------------------------------------
       TEAM MEMBERS:
       Ageridis Georgios
       Christodoulea Effrosyni
       Christopoulos Nikolaos
       Giannakopoulou Kalliopi-Eleftheria
       Glytsos Marios
       Kritharoula Anastasia
       -------------------------------------------
       """

    pass


#healthcheck

@cli.command(short_help='REST API call: /healthcheck')
@click.option('--format', type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
@click.pass_context
def healthcheck(ctx, format, apikey):

    """\b
       -------------------------------------------
       This command executes a sytem health ckeck.
       -------------------------------------------

       User authorization level: None

       REST API call: /healthckeck

       \b
       -------------------------------------------
       NOTE: The function returns the system's
       health status ("OK" on success / "failed"
       on failure).
       -------------------------------------------
       """

    validation.valid(apikey)
    ctx.invoke(public_commands.healthcheck, format=format, apikey=apikey)


#resetsessions

@cli.command(short_help='REST API call: /resetsessions')
@click.option('--format', type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
@click.pass_context
def resetsessions(ctx, format, apikey):

    """\b
       -------------------------------------------
       This command resets all charging sessions.
       -------------------------------------------

       User authorization level: None

       REST API call: /resetsessions

       \b
       -------------------------------------------
       WARNING: After this call, all records of
       charging sessions will be erased.
       -------------------------------------------
       """

    ctx.invoke(public_commands.resetsessions, format=format, apikey=apikey)


#login

@cli.command(short_help='REST API call: /login')
@click.option('--username', required=True,
               help='Enter username', metavar='<username>')
@click.option('--passw', required=True, hide_input=True,
                help='Enter password', metavar='<password>')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def login(username, passw, format, apikey):

    """\b
       -------------------------------------------
       User log in command.
       -------------------------------------------

       User authorization level: None

       REST API call: /login

       \b
       -------------------------------------------
       NOTE: If you are logged in with another
       user account, you have to logout before
       you can log in again.
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.usercheck(username)
    validation.passwcheck(passw)

    if (os.path.isfile(paths.token_path)):
        click.echo('A user is already logged in!')
    else:
        p = {'username': username , 'password': passw, 'format': format, 'apikey': apikey}
        service = 'login'
        click.echo()
        click.echo(click.style('Logging in...', fg='cyan'))
        click.echo()
        response = requests.post(url=f'{paths.baseURL}/{service}/', params=p)
        if response.status_code == 200:
            if format == 'json':
                res = json.loads(response.text)
                f = open(paths.token_path, "w")
                f.write(res['token'])
                click.echo(click.style('Login successful!', fg='green'))
                f.close()
            else:
                #f is a temporary
                f = open(paths.temporary_path, 'w')
                f.write(response.text)
                f.close()
                #now f is the token file
                f = open(paths.token_path, "w")
                with open(paths.temporary_path) as temp:
                    res = csv.DictReader(temp)
                    for rows in res:
                        f.write(str(rows['token']))
                click.echo(click.style('Login successful!', fg='green'))
                f.close()
        else:
            if format == 'json':
                click.echo()
                raise click.ClickException(response.text[2:(len(response.text))-2])
            else:
                click.echo()
                raise click.ClickException(response.text[4:(len(response.text))-2])


#logout

@cli.command(short_help='REST API call: /logout')
@click.option('--format', type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def logout(format, apikey):

    """\b
       -------------------------------------------
       User log out command.
       -------------------------------------------

       User authorization level: Connected user

       REST API call: /logout

       \b
       -------------------------------------------
       NOTE: If you are not logged in, you cannot
       logout (OBVIOUSLY!). Don't try to trick us!
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.user()

    click.echo('You are about to log out.')
    click.echo('Continue? '+click.style('[y/n]',fg='cyan'), nl=False)
    c = click.getchar()
    click.echo()
    if c=='y':
        f = open(paths.token_path, "r")
        token = f.readline()
        f.close()
        p = {'format': format, 'apikey': apikey}
        h = {'Authorization':'Token '+token}
        service = 'logout'
        click.echo()
        click.echo(click.style('Logging out...', fg='cyan'))
        click.echo()
        response = requests.post(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
        if response.status_code == 200:
            os.remove(paths.token_path)
            click.echo(click.style('Logout complete!', fg='green'))
        else:
            if format == 'json':
                click.echo()
                raise click.ClickException(response.text[2:(len(response.text))-2])
            else:
                click.echo()
                raise click.ClickException(response.text[4:(len(response.text))-2])
    elif c=='n':
        click.echo()
        click.echo(click.style('Abort...', fg='cyan'))
        click.echo()
        time.sleep(1)
        click.echo('You are still logged in.')
    else:
        click.echo()
        click.echo('Error: Invalid input.')


#sessionsperpoint

@cli.command(short_help='REST API call: /SessionsPerPoint')
@click.option('--point', required=False,
               help='Enter Point ID', metavar='<Point_ID>')
@click.option('--datefrom', required=True,
                help='Starting date', metavar='[YYYYMMDD]')
@click.option('--dateto', required=True,
                help='Ending date', metavar='[YYYYMMDD]')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def SessionsPerPoint(point, datefrom, dateto, format, apikey):

    """\b
       -------------------------------------------
       This command displays all charging sessions
       at a specific point, during the givven pe-
       riod of time.
       -------------------------------------------

       User authorization level: Connected user

       REST API call: /SessionsPerPoint

       \b
       -------------------------------------------
       NOTE: Date options must be chronologically
       correct. (--datefrom = starting date ,
       --dateto = ending date)
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.fdatecheck(datefrom)
    validation.tdatecheck(dateto)
    validation.chronological(datefrom, dateto)
    validation.user()

    click.echo()
    click.echo(click.style("Loading...", fg='cyan'))
    f = open(paths.token_path, "r")
    token = f.readline()
    f.close()
    p = {'format': format, 'apikey': apikey}
    h = {'Authorization':'Token '+token}
    service = 'SessionsPerPoint/'+ point+ '/'+ datefrom+ '/'+ dateto
    response = requests.get(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
    if response.status_code == 200 or response.status_code == 402:
        with click.progressbar([1, 2, 3, 4]) as bar:
            for x in bar:
                time.sleep(0.4)
        if format == 'json':
            res = json.loads(response.text)
            click.echo()
            click.echo('Point: '+ str(res['Point']))
            click.echo('Point operator: '+ str(res['PointOperator']))
            click.echo('Request Timestamp: '+ str(res['RequestTimestamp']))
            click.echo('Period from: '+ str(res['PeriodFrom']))
            click.echo('Period to: '+ str(res['PeriodTo']))
            click.echo('Number of charging sessions: '+ str(res['NumberOfChargingSessions']))
            if response.status_code == 200:
                click.echo()
                click.echo(click.style('Charging Sessions:', fg='cyan'))
                for session in res['ChargingSessionsList']:
                    click.echo()
                    #click.echo('Session index: '+ str(session['SessionIndex']))
                    click.echo('Session ID: '+ str(session['SessionID']))
                    click.echo('Started on: '+ str(session['StartedOn']))
                    click.echo('Finished on: '+ str(session['FinishedOn']))
                    click.echo('Protocol: '+ str(session['Protocol']))
                    click.echo('Energy delivered: '+ str(session['EnergyDelivered'])+ ' kWh')
                    click.echo('Payment: '+ str(session['Payment']))
                    click.echo('Vehicle type: '+ str(session['VehicleType']))
            else:
                click.echo()
                click.echo(click.style('Charging Sessions:', fg='cyan') + 'No data')
        else:
            f = open(paths.temporary_path, 'w')
            f.write(response.text)
            f.close()
            with open(paths.temporary_path) as temp:
                res = csv.DictReader(temp)
                for rows in res:
                    click.echo()
                    click.echo('Point: '+ str(rows['Point']))
                    click.echo('Point operator: '+ str(rows['PointOperator']))
                    click.echo('Request timestamp: '+ str(rows['RequestTimestamp']))
                    click.echo('Period from: '+ str(rows['PeriodFrom']))
                    click.echo('Period to: '+ str(rows['PeriodTo']))
                    session_count = rows['NumberOfChargingSessions']
                    session_count = int(session_count)
                    click.echo('Number of charging sessions: '+ str(session_count))
                    if response.status_code == 200:  
                        click.echo()
                        click.echo(click.style('Charging Sessions:', fg='cyan'))
                        for i in range(0,session_count):
                            click.echo()
                            click.echo('Session ID: '+ str(rows['ChargingSessionsList.'+str(i)+'.SessionID']))
                            click.echo('Started on: '+ str(rows['ChargingSessionsList.'+str(i)+'.StartedOn']))
                            click.echo('Finished on: '+ str(rows['ChargingSessionsList.'+str(i)+'.FinishedOn']))
                            click.echo('Energy delivered: '+ str(rows['ChargingSessionsList.'+str(i)+'.EnergyDelivered'])+ ' kWh')
                            click.echo('Payment: '+ str(rows['ChargingSessionsList.'+str(i)+'.Payment']))
                            click.echo('Vehicle type: '+ str(rows['ChargingSessionsList.'+str(i)+'.VehicleType']))
                    else:
                        click.echo()
                        click.echo(click.style('Charging Sessions: ', fg='cyan') + 'No data')
            os.remove(paths.temporary_path)
    else:
        if format == 'json':
            click.echo()
            raise click.ClickException(response.text[2:(len(response.text))-2])
        else:
            click.echo()
            raise click.ClickException(response.text[4:(len(response.text))-2])


#sessionsperstation

@cli.command(short_help='REST API call: /SessionsPerStation')
@click.option('--station', required=True,
               help='Enter Station ID', metavar='<Station_ID>')
@click.option('--datefrom', required=True,
                help='Starting date', metavar='[YYYYMMDD]')
@click.option('--dateto', required=True,
                help='Ending date', metavar='[YYYYMMDD]')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def SessionsPerStation(station, datefrom, dateto, format, apikey):

    """\b
       -------------------------------------------
       This command displays all charging sessions
       at a specific station, during the givven pe-
       riod of time.
       -------------------------------------------

       User authorization level: Connected user

       REST API call: /SessionsPerStation

       \b
       -------------------------------------------
       NOTE: Date options must be chronologically
       correct. (--datefrom = starting date ,
       --dateto = ending date)
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.fdatecheck(datefrom)
    validation.tdatecheck(dateto)
    validation.chronological(datefrom, dateto)
    validation.user()

    click.echo()
    click.echo(click.style("Loading...", fg='cyan'))
    f = open(paths.token_path, "r")
    token = f.readline()
    f.close()
    p = {'format': format, 'apikey': apikey}
    h = {'Authorization':'Token '+token}
    service = 'SessionsPerStation/'+ station+ '/'+ datefrom+ '/'+ dateto
    response = requests.get(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
    if response.status_code == 200 or response.status_code == 402:
        with click.progressbar([1, 2, 3]) as bar:
                for x in bar:
                    time.sleep(0.5)
        if format == 'json':
            res = json.loads(response.text)
            click.echo()
            click.echo('Station ID: '+ str(res['StationID']))
            click.echo('Station operator: '+ str(res['Operator']))
            click.echo('Request Timestamp: '+ str(res['RequestTimestamp']))
            click.echo('Period from: '+ str(res['PeriodFrom']))
            click.echo('Period to: '+ str(res['PeriodTo']))
            click.echo('Total energy delivered: '+ str(res['TotalEnergyDelivered'])+ ' kWh')
            click.echo('Number of charging sessions: '+ str(res['NumberOfChargingSessions']))
            click.echo('Number of active points: '+ str(res['NumberOfActivePoints']))
            if response.status_code == 200:
                click.echo()
                click.echo(click.style('Sessions Summary:', fg='cyan'))
                for session in res['SessionsSummaryList']:
                    click.echo()
                    click.echo('Point ID: '+ str(session['PointID']))
                    click.echo('Point sessions: '+ str(session['PointSessions']))
                    click.echo('Energy delivered: '+ str(session['EnergyDelivered'])+ ' kWh')
            else:
                click.echo()
                click.echo(click.style('Sessions Summary: ', fg='cyan') + 'No data')
        else:
            f = open(paths.temporary_path, 'w')
            f.write(response.text)
            f.close()
            with open(paths.temporary_path) as temp:
                res = csv.DictReader(temp)
                for rows in res:
                    click.echo()
                    click.echo('Station ID: '+ str(rows['StationID']))
                    click.echo('Station operator: '+ str(rows['Operator']))
                    click.echo('Request timestamp: '+ str(rows['RequestTimestamp']))
                    click.echo('Period from: '+ str(rows['PeriodFrom']))
                    click.echo('Period to: '+ str(rows['PeriodTo']))
                    click.echo('Total energy delivered: '+ str(rows['TotalEnergyDelivered'])+ ' kWh')
                    click.echo('Number of charging sessions: '+ str(rows['NumberOfChargingSessions']))
                    points_count = rows['NumberOfActivePoints']
                    points_count = int(points_count)
                    click.echo('Number of active points: '+ str(points_count))
                    if response.status_code == 200:
                        click.echo()
                        click.echo(click.style('Sessions Summary: ', fg='cyan'))
                        for i in range(0,points_count):
                            click.echo()
                            click.echo('Point ID: '+ str(rows['SessionsSummaryList.'+str(i)+'.PointID']))
                            click.echo('Point sessions: '+ str(rows['SessionsSummaryList.'+str(i)+'.PointSessions']))
                            click.echo('Energy delivered: '+ str(rows['SessionsSummaryList.'+str(i)+'.EnergyDelivered'])+ ' kWh')
                    else:
                        click.echo()
                        click.echo(click.style('Sessions Summary: ', fg='cyan') + 'No data')
            os.remove(paths.temporary_path)
    else:
        if format == 'json':
            click.echo()
            raise click.ClickException(response.text[2:(len(response.text))-2])
        else:
            click.echo()
            raise click.ClickException(response.text[4:(len(response.text))-2])


#sessionsperev

@cli.command(short_help='REST API call: /SessionsPerEV')
@click.option('--ev', required=True,
               help='Enter Vehicle ID', metavar='<Vehicle_ID>')
@click.option('--datefrom', required=True,
                help='Starting date', metavar='[YYYYMMDD]')
@click.option('--dateto', required=True,
                help='Ending date', metavar='[YYYYMMDD]')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def SessionsPerEV(ev, datefrom, dateto, format, apikey):

    """\b
       -------------------------------------------
       This command displays all charging sessions
       of a vehicle, during the givven period of
       time.
       -------------------------------------------

       User authorization level: Connected user

       REST API call: /SessionsPerEV

       \b
       -------------------------------------------
       NOTE: Date options must be chronologically
       correct. (--datefrom = starting date ,
       --dateto = ending date)
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.fdatecheck(datefrom)
    validation.tdatecheck(dateto)
    validation.chronological(datefrom, dateto)
    validation.user()

    click.echo()
    click.echo(click.style("Loading...", fg='cyan'))
    f = open(paths.token_path, "r")
    token = f.readline()
    f.close()
    p = {'format': format, 'apikey': apikey}
    h = {'Authorization':'Token '+token}
    service = 'SessionsPerEV/'+ ev+ '/'+ datefrom+ '/'+ dateto
    response = requests.get(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
    if response.status_code == 200 or response.status_code == 402:
        with click.progressbar([1, 2, 3]) as bar:
                for x in bar:
                    time.sleep(0.5)
        if format == 'json':
            res = json.loads(response.text)
            click.echo()
            click.echo('Vehicle ID: '+ str(res['VehicleID']))
            click.echo('Request Timestamp: '+ str(res['RequestTimestamp']))
            click.echo('Period from: '+ str(res['PeriodFrom']))
            click.echo('Period to: '+ str(res['PeriodTo']))
            click.echo('Total energy consumed: '+ str(res['TotalEnergyConsumed'])+ ' kWh')
            click.echo('Number of visited points: '+ str(res['NumberOfVisitedPoints']))
            click.echo('Number of vehicle charging sessions: '+ str(res['NumberOfVehicleChargingSessions']))
            if response.status_code == 200:
                click.echo()
                click.echo(click.style('Vehicle Charging Sessions:', fg='cyan'))
                for session in res['VehicleChargingSessionsList']:
                    click.echo()
                    click.echo('Session index: '+ str(session['SessionIndex']))
                    click.echo('Session ID: '+ str(session['SessionID']))
                    click.echo('Energy provider: '+ str(session['EnergyProvider']))
                    click.echo('Started on: '+ str(session['StartedOn']))
                    click.echo('Finished on: '+ str(session['FinishedOn']))
                    click.echo('Energy delivered: '+ str(session['EnergyDelivered'])+ ' kWh')
                    click.echo('Price policy reform: '+ str(session['PricePolicyRef']))
                    click.echo('Cost per kWh: '+ str(session['CostPerKWh'])+ '$')
                    click.echo('Session cost: '+ str(session['SessionCost'])+ '$')
            else:
                click.echo()
                click.echo(click.style('Vehicle Charging Sessions:', fg='cyan') + 'No data')

        else:
            f = open(paths.temporary_path, 'w')
            f.write(response.text)
            f.close()
            with open(paths.temporary_path) as temp:
                res = csv.DictReader(temp)
                for rows in res:
                    click.echo()
                    click.echo('Vehicle ID: '+ str(rows['VehicleID']))
                    click.echo('Request timestamp: '+ str(rows['RequestTimestamp']))
                    click.echo('Period from: '+ str(rows['PeriodFrom']))
                    click.echo('Period to: '+ str(rows['PeriodTo']))
                    click.echo('Total energy consumed: '+ str(rows['TotalEnergyConsumed'])+ ' kWh')
                    click.echo('Number of visited points: '+ str(rows['NumberOfVisitedPoints']))
                    sessions_count = rows['NumberOfVehicleChargingSessions']
                    sessions_count = int(sessions_count)
                    click.echo('Number of vehicle charging sessions: '+ str(sessions_count))
                    if response.status_code == 200:
                        click.echo()
                        click.echo(click.style('Vehicle Charging Sessions: ', fg='cyan'))
                        for i in range(0,sessions_count):
                            click.echo()
                            click.echo('Session index: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.SessionIndex']))
                            click.echo('Session ID: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.SessionID']))
                            click.echo('Energy provider: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.EnergyProvider']))
                            click.echo('Started on: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.StartedOn']))
                            click.echo('Finished on: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.FinishedOn']))
                            click.echo('Energy delivered: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.EnergyDelivered'])+ ' kWh')
                            click.echo('Price policy reform: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.PricePolicyRef']))
                            click.echo('Cost per kWh: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.CostPerKWh'])+ ' $')
                            click.echo('Session cost: '+ str(rows['VehicleChargingSessionsList.'+str(i)+'.SessionCost'])+ ' $')
                    else:
                        click.echo()
                        click.echo(click.style('Vehicle Charging Sessions: ', fg='cyan') + 'No data')
            os.remove(paths.temporary_path)
    else:
        if format == 'json':
            click.echo()
            raise click.ClickException(response.text[2:(len(response.text))-2])
        else:
            click.echo()
            raise click.ClickException(response.text[4:(len(response.text))-2])


#sessionsperprovider

@cli.command(short_help='REST API call: /SessionsPerProvider')
@click.option('--provider', required=True,
               help='Enter provider name', metavar='<provider name>')
@click.option('--datefrom', required=True,
                help='Starting date', metavar='[YYYYMMDD]')
@click.option('--dateto', required=True,
                help='Ending date', metavar='[YYYYMMDD]')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def SessionsPerProvider(provider, datefrom, dateto, format, apikey):

    """\b
       -------------------------------------------
       This command displays all charging sessions
       from an energy provider, during the givven
       period of time.
       -------------------------------------------

       User authorization level: Connected user

       REST API call: /SessionsPerProvider

       \b
       -------------------------------------------
       NOTE: Date options must be chronologically
       correct. (--datefrom = starting date ,
       --dateto = ending date)
       -------------------------------------------
       """

    validation.valid(apikey)
    validation.fdatecheck(datefrom)
    validation.tdatecheck(dateto)
    validation.chronological(datefrom, dateto)
    validation.user()

    click.echo()
    click.echo(click.style("Loading...", fg='cyan'))
    f = open(paths.token_path, "r")
    token = f.readline()
    f.close()
    p = {'format': format, 'apikey': apikey}
    h = {'Authorization':'Token '+token}
    service = 'SessionsPerProvider/'+ provider+ '/'+ datefrom+ '/'+ dateto
    with requests.get(url=f'{paths.baseURL}/{service}/', headers=h, params=p, stream=True) as response:    
        if response.status_code == 200 or response.status_code == 402:
            with click.progressbar([1, 2, 3]) as bar:
                for x in bar:
                    time.sleep(0.5)
            if format == 'json':
                res = json.loads(response.text)
                click.echo()
                click.echo('Provider ID: '+ str(res['ProviderID']))
                click.echo('Provider name: '+ str(res['ProviderName']))
                click.echo('Number of provider charging sessions: '+ str(res['NumberOfProviderChargingSessions']))
                if response.status_code == 200:
                    click.echo()
                    click.echo(click.style('Provider Charging Sessions:', fg='cyan'))
                    for session in res['ProviderChargingSessionsList']:
                        click.echo()
                        click.echo('Station ID: '+ str(session['StationID']))
                        click.echo('Session ID: '+ str(session['SessionID']))
                        click.echo('Vehicle ID: '+ str(session['VehicleID']))
                        click.echo('Started on: '+ str(session['StartedOn']))
                        click.echo('Finished on: '+ str(session['FinishedOn']))
                        click.echo('Energy delivered: '+ str(session['EnergyDelivered'])+ ' kWh')
                        click.echo('Price policy reform: '+ str(session['PricePolicyRef']))
                        click.echo('Cost per kWh: '+ str(session['CostPerKWh']))
                        click.echo('Total cost: '+ str(session['TotalCost']))
                else:
                    click.echo()
                    click.echo(click.style('Provider Charging Sessions:', fg='cyan')+ 'No data')
            else:
                f = open(paths.temporary_path, 'w')
                f.write(response.text)
                f.close()
                with open(paths.temporary_path) as temp:
                    res = csv.DictReader(temp)
                    for rows in res:
                        click.echo()
                        click.echo('Provider ID: '+ str(rows['ProviderID']))
                        click.echo('Provider name: '+ str(rows['ProviderName']))
                        sessions_count = rows['NumberOfProviderChargingSessions']
                        sessions_count = int(sessions_count)
                        click.echo('Number of provider charging sessions: '+ str(sessions_count))
                        if response.status_code == 200:
                            click.echo()
                            click.echo(click.style('Provider Charging Sessions: ', fg='cyan'))
                            for i in range(0,sessions_count):
                                click.echo()
                                click.echo('Station ID: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.StationID']))
                                click.echo('Session ID: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.SessionID']))
                                click.echo('Vehicle ID: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.VehicleID']))
                                click.echo('Started on: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.StartedOn']))
                                click.echo('Finished on: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.FinishedOn']))
                                click.echo('Energy delivered: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.EnergyDelivered'])+ ' kWh')
                                click.echo('Price policy reform: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.PricePolicyRef']))
                                click.echo('Cost per kWh: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.CostPerKWh'])+ ' $')
                                click.echo('Total cost: '+ str(rows['ProviderChargingSessionsList.'+str(i)+'.TotalCost'])+ ' $')
                        else:
                            click.echo()
                            click.echo(click.style('Provider Charging Sessions: ', fg='cyan')+ 'No data')
                os.remove(paths.temporary_path)
        else:
            if format == 'json':
                click.echo()
                raise click.ClickException(response.text[2:(len(response.text))-2])
            else:
                click.echo()
                raise click.ClickException(response.text[4:(len(response.text))-2])


#admin

@cli.command(short_help='System Administration')
@click.option('--usermod', required=False, is_flag=True,
               help="Enter new user/Change user's password", metavar='--username username --passw password')
@click.option('--username', required=False,
               help='Enter username  [required in --usermod]', metavar='<username>')
@click.option('--passw', required=False, hide_input=True,
                help='Enter password  [required in --usermod]', metavar='<password>')
@click.option('--healthcheck', required=False, is_flag=True,
                help='Execute system health check', metavar='')
@click.option('--resetsessions', required=False, is_flag=True,
                help='Reset charging sessions', metavar='')
@click.option('--users', required=False,
                help="Display user's info", metavar='<username>')
@click.option('--sessionsupd', required=False, is_flag=True,
                help="Upload a session's update CSV file", metavar='')
@click.option('--source', required=False,
                help="Upload a session's update CSV file  [required in --sessionupd]", metavar='<filename>')
@click.option('--format',type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--role',type=click.Choice(['CarOwner', 'EnergyProvider','Municipality', 'ParkingOwner', 'Admin'],
               case_sensitive=False), default='CarOwner', help='Usermod role', 
               metavar='[CarOwner|EnergyProvider|Municipality|ParkingOwner|Admin]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
@click.pass_context
def Admin(ctx, usermod, username, passw, healthcheck, resetsessions, users, sessionsupd, source, format, apikey, role):

    """\b
       -------------------------------------------
       System Administration Command
       -------------------------------------------

       User authorization level: Administrator

       \b
       -------------------------------------------
       Options Usage:
       -------------------------------------------

       \b
       --usermod --username username --passw password
       Using this parameter the administrator can
       create a new user or update an existing
       user's password. If the username exists,
       then the passw argument will be the new
       password of the user. If not, then a new
       user with the username and password argu-
       ments will be created.
       There is an optional parameter --role, where
       you can declare the role of a new user.


       \b
       --healthcheck
       Using this parameter the administrator can
       execute a system health check. The function
       returns the system's health status ("OK" on
       succes / "failed" on failure).


       \b
       --resetsessions
       Using this parameter the administrator can
       reset all charging sessions as well as ini-
       tialize the default admin user (username:
       admin, password: petrol4ever). NOTE: The
       reset is final and after the execution of
       the function, all charging records will be
       deleted.


       \b
       --users username
       Using this parameter the administrator can
       see the information of a user.

       \b
       --sessionsupd --source filename
       Using this parameter the administrator can
       "upload" a CSV file with charging sessions
       data. The name of the file is stated in the
       --source argument and the file itself must
       be in multipart/from-data encoding.

       \b
       -------------------------------------------
       NOTE: You can call multible function by en-
       tering more than one option parameters. The
       options do not have to be in order.

       \b
       NOTE: If more than one options are entered,
       /healthcheck (if called) will be executed
       first and /resetsessions (if called) last.

       \b
       NOTE: Options resetsessions and sessionsupd
       cannot be executed in the same command.

       -------------------------------------------
       """

    upd = validation.validsessionsupd(sessionsupd, source)
    umod = validation.validusermod(usermod, username, passw)
    validation.valid(apikey)
    validation.nand(upd,resetsessions)


    #Health check

    if healthcheck:
        ctx.invoke(public_commands.healthcheck, format=format, apikey=apikey)


    #User info

    if users!=None:
        validation.user()
        click.echo()
        click.echo(click.style("Loading user's information...", fg='cyan'))
        f = open(paths.token_path, "r")
        token = f.readline()
        f.close()
        p = {'format': format, 'apikey': apikey}
        h = {'Authorization':'Token '+token}
        service = 'admin/users/'+ users
        response = requests.get(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
        if response.status_code == 200:
            with click.progressbar([1, 2, 3, 4]) as bar:
                for x in bar:
                    time.sleep(0.4)
            if format == 'json':
                res = json.loads(response.text)
                click.echo()
                click.echo('User ID: '+ str(res['ID']))
                click.echo('Username: '+ str(res['Username']))
                click.echo('First name: '+ str(res['FirstName']))
                click.echo('Last name: '+ str(res['LastName']))
                click.echo('Role: '+ str(res['Role']))
                click.echo('Date joined: '+ str(res['DateJoined']))
                click.echo('Last login: '+ str(res['LastLogin']))
            else:
                f = open(paths.temporary_path, 'w')
                f.write(response.text)
                f.close()
                with open(paths.temporary_path) as temp:
                    res = csv.DictReader(temp)
                    for rows in res:
                        click.echo()
                        click.echo('User ID: '+ str(rows['ID']))
                        click.echo('Username: '+ str(rows['Username']))
                        click.echo('First name: '+ str(rows['FirstName']))
                        click.echo('Last name: '+ str(rows['LastName']))
                        click.echo('Role: '+ str(rows['Role']))
                        click.echo('Date joined: '+ str(rows['DateJoined']))
                        click.echo('Last login: '+ str(rows['LastLogin']))
                os.remove(paths.temporary_path)
        else:
            if format == 'json':
                click.echo()
                raise click.ClickException(response.text[2:(len(response.text))-2])
            else:
                click.echo()
                raise click.ClickException(response.text[4:(len(response.text))-2])


    #Password change / New user

    if umod:
        f = open(paths.token_path, "r")
        token = f.readline()
        f.close()
        firstname = str(username)
        lastname = str(username)
        email = str(username) + '@evmail.com'
        click.echo('Is this a new user? If so, you may want to enter first name, last name and email. If you'
                    +' do not enter these info they will be automatically filled in. If this is an existing'
                    +' user, then no more changes than password will be applied.')
        click.echo("Do you want to enter user's info? " + click.style('[y/n]', fg='cyan'), nl=False)
        c = click.getchar()
        if c=='y':
            click.echo()
            flag = True
            while flag:
                firstname = click.prompt('First name')
                flag = validation.namecheck(firstname)
            flag = True
            while flag:
                lastname = click.prompt('Last name')
                flag = validation.namecheck(lastname)
            email = click.prompt('E-mail')
        click.echo()
        click.echo()
        click.echo(click.style("Processing...", fg='cyan'))
        p = {'format': format,  'role': role, 'firstname': firstname, 'lastname': lastname, 'email': email, 'apikey': apikey}
        h = {'Authorization':'Token '+token}
        service = 'admin/usermod/'+ str(username)+ '/'+ str(passw)
        response = requests.post(url=f'{paths.baseURL}/{service}/', headers=h, params=p)
        if response.status_code != 401:
            if format == 'json':
                res = json.loads(response.text)
                with click.progressbar([1, 2, 3]) as bar:
                    for x in bar:
                        time.sleep(0.5)
                if response.status_code == 200:
                    click.echo()
                    click.echo("Usermod status: " + click.style(res['status'], fg='green'))
                else:
                    click.echo()
                    click.echo("Usermod status: " + click.style(res['status'], fg='red'))
            else:
                f = open(paths.temporary_path, 'w')
                f.write(response.text)
                f.close()
                with open(paths.temporary_path) as temp:
                    res = csv.DictReader(temp)
                    for rows in res: 
                        if response.status_code == 200:
                            click.echo()
                            click.echo("Status: " + click.style(rows['status'], fg='green'))
                        else:
                            click.echo()
                            click.echo("Status: " + click.style(rows['status'], fg='red'))
                os.remove(paths.temporary_path)
        else:
            if format == 'json':
                click.echo()
                raise click.ClickException(response.text[2:(len(response.text))-2])
            else:
                click.echo()
                raise click.ClickException(response.text[4:(len(response.text))-2])


    #Sessions update

    if upd:
        click.echo()
        click.echo(click.style("Uploading CSV file...", fg='cyan'))
        ff = open(paths.token_path, "r")
        token = ff.readline()
        ff.close()
        p = {'format': format, 'apikey': apikey}
        h = {'Authorization':'Token '+token}
        f = {'file': open(source,'r')}
        service = 'admin/system/sessionsupd'
        response = requests.post(url=f'{paths.baseURL}/{service}/', files=f, headers=h, params=p)
        if response.status_code == 200:
            if format == 'json':
                res = json.loads(response.text)
                with click.progressbar([1, 2, 3, 4, 5]) as bar:
                    for x in bar:
                        time.sleep(0.3)
                click.echo()
                click.echo('Sessions in uploaded file: ' + str(res['SessionsInUploadedFile']))
                click.echo('Sessions imported: '+ str(res['SessionsImported']))
                click.echo('Total sessions in database: '+ str(res['TotalSessionsInDatabase']))
            else:
                f = open(paths.temporary_path, 'w')
                f.write(response.text)
                f.close()
                with open(paths.temporary_path) as temp:
                    res = csv.DictReader(temp)
                    for rows in res:
                        click.echo()
                        click.echo('Sessions in uploaded file: '+ str(rows['SessionsInUploadedFile']))
                        click.echo('Sessions imported: '+ str(rows['SessionsImported']))
                        click.echo('Total sessions in database: '+ str(rows['TotalSessionsInDatabase']))
                os.remove(paths.temporary_path)
        else:
            click.echo()
            if response.status_code == 401:
                if format == 'json':
                    click.echo()
                    raise click.ClickException('Error: Update ' + response.text[2:(len(response.text))-2])
                else:
                    click.echo()
                    raise click.ClickException('Error: Update ' + response.text[4:(len(response.text))-2])
            else:
               if format == 'json':
                    click.echo()
                    raise click.ClickException(response.text[2:(len(response.text))-2])
               else:
                    click.echo()
                    raise click.ClickException(response.text[4:(len(response.text))-2]) 


    #Reset sessions

    if resetsessions:
        ctx.invoke(public_commands.resetsessions, format=format, apikey=apikey)

if __name__ == "__cli__":
   cli()