from pathlib import Path

import click

from run_on_server.client import init_client
from run_on_server.run import exec_comm, exec_script
from run_on_server.sync import rsync
from run_on_server.utils import extract_path


@click.command("run-on-server")
@click.argument("server", type=click.STRING)
@click.argument("script", type=click.STRING)
@click.argument("args", nargs=-1, type=click.STRING)
@click.option(
    "--conda-prefix",
    type=click.STRING,
    required=True,
    envvar="SSH_CONDA_PREFIX",
    help="conda prefix on the server")
@click.option(
    "--pre-comm", help="command to be executed before running the script")
@click.option(
    "--sync",
    is_flag=True,
    help="whether to transfer saved data from the server")
@click.option(
    "-p",
    "--re-pattern",
    type=click.STRING,
    help="regex pattern to extract the path to be transferred from server")
@click.option(
    "-t",
    "--target",
    type=click.Path(resolve_path=True),
    help="local path to save the transferred data")
def main(
    server: str,
    script: str,
    args: tuple[str, ...],
    conda_prefix: str,
    pre_comm: str | None,
    sync: bool,
    re_pattern: str | None,
    target: Path | None,
) -> None:
  if sync and (re_pattern is None or target is None):
    click.echo("--re-pattern and --target must be specified with --sync on!")
    exit(1)

  client = init_client(server)

  if pre_comm is not None:
    click.echo(exec_comm(client=client, comm=pre_comm))

  output = exec_script(
      client=client,
      conda_prefix=conda_prefix,
      py_file=script,
      args=list(args),
  )
  click.echo(output)

  if sync:
    assert re_pattern is not None and target is not None

    data_pth = extract_path(output, re_pattern)

    assert rsync(server_name=server, src=data_pth, tgt=target)

    click.echo(f"Data saved to {target}.")
