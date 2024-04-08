from pathlib import Path

import click

from run_on_server.client import init_client
from run_on_server.run import exec_comm, exec_script
from run_on_server.sync import rsync
from run_on_server.utils import extract_path


@click.command(
    "run-on-server", context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("server", type=click.STRING)
@click.argument("script", type=click.STRING)
@click.argument("args", nargs=-1, type=click.STRING)
@click.option(
    "--conda-prefix",
    type=click.STRING,
    required=True,
    envvar="SSH_CONDA_PREFIX",
    help="Conda prefix on the server. Can also be passed by SSH_CONDA_PREFIX.")
@click.option(
    "--pwd",
    type=click.STRING,
    envvar="SSH_PWD",
    help="PWD for running the script (and pre-command). "
    "Can be passed by SSH_PWD.")
@click.option(
    "--envvars",
    type=click.STRING,
    envvar="SSH_ENV_VARS",
    help="[key=val,...] Environment variables when running the script. "
    "Can be passed by SSH_ENV_VARS.")
@click.option(
    "-c",
    "--pre-comm",
    help="Command to be executed before running the script.")
@click.option(
    "-s",
    "--sync",
    is_flag=True,
    help="Whether to transfer saved data from the server.")
@click.option(
    "-p",
    "--re-pattern",
    type=click.STRING,
    help="Regex pattern to extract the path to be transferred from server.")
@click.option(
    "-t",
    "--target",
    type=click.Path(resolve_path=True),
    help="Local location to save the transferred data.")
def main(
    server: str,
    script: str,
    args: tuple[str, ...],
    conda_prefix: str,
    pwd: str | None,
    envvars: str | None,
    pre_comm: str | None,
    sync: bool,
    re_pattern: str | None,
    target: Path | None,
) -> None:
  """Run SCRIPT with arguments ARGS on the SSH server named SERVER."""
  if sync and (re_pattern is None or target is None):
    click.echo("--re-pattern and --target must be specified with --sync on!")
    exit(1)

  client = init_client(server)

  if pre_comm is not None:
    output = exec_comm(client=client, comm=pre_comm, pwd=pwd)
    click.echo(f"Pre-command output: \n{output}")

  output = exec_script(
      client=client,
      conda_prefix=conda_prefix,
      py_file=script,
      args=list(args),
      pwd=pwd,
      envvars=envvars,
  )
  click.echo(f"Script output:\n{output}")

  if sync:
    assert re_pattern is not None and target is not None

    data_pth = extract_path(output, re_pattern)

    assert rsync(server_name=server, src=data_pth, tgt=target)

    target = Path(target)
    if target.is_dir():
      target /= Path(data_pth).name

    click.echo(f"Data saved to {target}.")
