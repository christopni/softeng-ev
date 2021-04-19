import click
import os.path
import os
import paths


def letnumcount(str):
    cnt=0
    for ch in str:
        if ((ch.isdigit()) or (ch.isalpha())): cnt = cnt + 1
    return cnt


def spacecount(str):
    return (sum(ch.isspace() for ch in str))


def numcount(str):
    return (sum(ch.isdigit() for ch in str))


def letcount(str):
    return (sum(ch.isalpha() for ch in str))
                

def valid(key):
    if (len(key)!=14):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 key+ ". (valid format: XXXX-XXXX-XXXX, X = letter or number)",
                                param=key, param_hint="'--apikey'")
    if ((key[4]!="-") or (key[9]!="-")):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 key+ ". (valid format: XXXX-XXXX-XXXX, X = letter or number)",
                                param=key, param_hint="'--apikey'")
    if (letnumcount(key)!=12):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 key+ ". (valid format: XXXX-XXXX-XXXX, X = letter or number)",
                                param=key, param_hint="'--apikey'")


def usercheck(username):
    if (letnumcount(username)!=len(username)):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 username+ ". (username must contain letters and numbers only)",
                                param=username, param_hint="'--username'")


def namecheck(name):
    if (letcount(name)!=len(name)):
        click.echo()
        click.echo("Error: invalid format: (name must contain letters only)")
        return True
    return False


def passwcheck(password):
    if (spacecount(password)>0):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 password+ ". (password cannot contain spaces)",
                                param=password, param_hint="'--passw'")


def fdatecheck(date):
    if(numcount(date)!=8):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 date+ ". (valid format: YYYYMMDD)",
                                param=date, param_hint="'--datefrom'")
    if(len(date)!=8):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 date+ ". (valid format: YYYYMMDD)",
                                param=date, param_hint="'--datefrom'")


def tdatecheck(date):
    if(numcount(date)!=8):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 date+ ". (valid format: YYYYMMDD)",
                                param=date, param_hint="'--dateto'")
        

    if(len(date)!=8):
        click.echo()
        raise click.BadParameter("invalid format: "+
                                 date+ ". (valid format: YYYYMMDD)",
                                param=date, param_hint="'--dateto'")


def chronological(date1,date2):
    if (int(date1[:4])<int(date2[:4])):
        return
    if (int(date1[:4])==int(date2[:4])):
        if (int(date1[4:6])<int(date2[4:6])):
            return
        if (int(date1[4:6])==int(date2[4:6])):
            if (int(date1[6:8])<int(date2[6:8])):
                return
    click.echo()
    raise click.BadParameter("invalid values: "+
                                 date1+", "+date2+ ". (dates must be chronologically correct)",
                                param=date1, param_hint="'--datefrom' and '--dateto'")


def validusermod(usermod,username,password):
    if (usermod==False):
        if (username!=None):
            click.echo()
            raise click.NoSuchOption(username, "Admin() got an unexpected argument '--username' ('admin --help' for usage help)")
        if (password!=None):
            click.echo()
            raise click.NoSuchOption(password, "Admin() got an unexpected argument '--passw' ('admin --help' for usage help)")
    else:
        if (username==None):
            click.echo()
            raise click.BadOptionUsage(username, "Missing option '--username'")
        if (password==None):
            click.echo()
            raise click.BadOptionUsage(password, "Missing option '--passw'")
        usercheck(username)
        passwcheck(password)
    if usermod: 
        return True
    return False


def validsessionsupd(upd,source):
    if (upd==False):
        if (source!=None):
            click.echo()
            raise click.NoSuchOption(username, "Admin() got an unexpected argument '--source' (Try 'admin --help' for usage help)")
    else:
        if (source==None):
            click.echo()
            raise click.BadOptionUsage(source, "Missing option '--source'")
    if upd: 
        return True
    return False


def user():
    if (not(os.path.isfile(paths.token_path))):
        click.echo()
        raise click.ClickException("You have to login in order to use this command.")


def nand(a,b):
    if a and b:
        click.echo()
        raise click.ClickException("Requests --resetsessions and --sessionsupd cannot be executed in the same command")

