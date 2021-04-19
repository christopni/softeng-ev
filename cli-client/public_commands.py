import click
import paths
import os.path
import os
import requests
import validation
import json
import csv
import time


@click.command(short_help='REST API call: /healthcheck')
@click.option('--format', type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def healthcheck(format, apikey):

    click.echo('Ready for system health check.')
    click.pause()  
    click.echo()
    click.secho(click.style("Gathering information about system's health...", fg='cyan'))
    p = {'format': format, 'apikey': apikey}
    service = 'healthcheck'
    response = requests.get(url=f'{paths.baseURL}/{service}/', params=p)
    with click.progressbar([1, 2, 3, 4, 5]) as bar:
        for x in bar:
            time.sleep(0.4)
    if response.status_code == 200 or response.status_code == 500:
        if format == 'json':
            res = json.loads(response.text)
            if response.status_code == 200:
                click.echo()
                click.echo("Status: " + click.style(res['status'], fg='green'))
            else:
                click.echo()
                click.echo("Status: " + click.style(res['status'], fg='red'))
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





@click.command(short_help='REST API call: /resetsessions/')
@click.option('--format', type=click.Choice(['csv', 'json'], case_sensitive=False), required=True,
               help='CLI format', metavar='[csv|json]')
@click.option('--apikey', required=True,
               help='API key', metavar='[XXXX-XXXX-XXXX]')
def resetsessions(format, apikey):

    click.echo('WARNING: You are about to delete all charging records.')
    click.echo('Continue? ' + click.style('[y/n]', fg='cyan'), nl=False)
    c = click.getchar()
    if c == 'y':
        click.echo()
        click.echo()
        click.echo(click.style('Reseting charging data...', fg='cyan'))
        p = {'format': format, 'apikey': apikey}
        service = 'admin/resetsessions'
        response = requests.post(url=f'{paths.baseURL}/{service}/', params=p)
        with click.progressbar([1, 2, 3, 4, 5, 6]) as bar:
            for x in bar:
                time.sleep(0.3)
        if response.status_code == 200 or response.status_code == 500:
            if format == 'json':
                if response.status_code == 200:
                    click.echo()
                    click.echo("Status: " + click.style(res['status'], fg='green'))
                else:
                    click.echo()
                    click.echo("Status: " + click.style(res['status'], fg='red'))
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
    elif c == 'n':
        click.echo()
        click.echo(click.style('Abort...', fg='cyan')) 
        time.sleep(1)
    else:
        click.echo()
        raise click.ClickException("Invalid input.")