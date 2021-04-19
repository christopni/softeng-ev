from click.testing import CliRunner
from ev_group50 import cli

def test_healthcheck1_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck','--format','json','--apikey','1234-1234-1234'])
	assert 'Status: OK' or 'Status: failed' in result.output
	assert result.exit_code == 0

def test_healthcheck2_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck','--format','csv','--apikey','1234-1234-1234'])
	assert 'Status: OK' or 'Status: failed' in result.output
	assert result.exit_code == 0

def test_healthcheck3_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck'])
	assert """Usage: cli healthcheck [OPTIONS]\nTry 'cli healthcheck --help' for help.\n\nError: Missing option '--format'.  Choose from:\n\tcsv,\n\tjson.\n""" in result.output
	

def test_healthcheck4_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck','--apikey','1234-1234-1234'])
	assert """Usage: cli healthcheck [OPTIONS]\nTry 'cli healthcheck --help' for help.\n\nError: Missing option '--format'.  Choose from:\n\tcsv,\n\tjson.\n""" in result.output

def test_healthcheck5_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck','--format','csv','--apikey','1234-1234-1235'])
	assert "\nError: {'Not Authorized: Invalid API key'}\n" in result.output

def test_healthcheck6_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['healthcheck','--format','csv'])
	assert """Usage: cli healthcheck [OPTIONS]\nTry 'cli healthcheck --help' for help.\n\nError: Missing option '--apikey'.\n""" in result.output

def test_login1_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['login','--format','csv','--apikey','1234-1234-1234','--username','example'])
	assert """Usage: cli login [OPTIONS]\nTry 'cli login --help' for help.\n\nError: Missing option '--passw'.\n""" in result.output

def test_login2_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['login','--format','csv','--apikey','1234-1234-1234','--passw','example'])
	assert """Usage: cli login [OPTIONS]\nTry 'cli login --help' for help.\n\nError: Missing option '--username'.\n""" in result.output

def test_login3_in_cli():
	runner = CliRunner()
	result = runner.invoke(cli,['login','--format','json','--apikey','1234-1234-123','--username','example','--passw','example'])
	assert """\nUsage: cli login [OPTIONS]\n\nError: Invalid value for '--apikey': invalid format: 1234-1234-123. (valid format: XXXX-XXXX-XXXX, X = letter or number)\n""" in result.output