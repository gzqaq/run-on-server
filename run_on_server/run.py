import click
import paramiko as ssh


def exec_comm(client: ssh.SSHClient, comm: str, pwd: str | None = None) -> str:
  if pwd is not None:
    comm = f"cd {pwd}; {comm}"

  _, stdout, stderr = client.exec_command(comm)
  outp = stdout.read()
  err_msg = stderr.read().decode().strip()

  if len(err_msg) > 0:
    click.echo(f"stderr output of {comm}:\n{err_msg}\n")

  return outp.decode()


def exec_script(client: ssh.SSHClient,
                conda_prefix: str,
                py_file: str,
                args: list[str],
                pwd: str | None = None,
                envvars: str | None = None) -> str:
  py_exec = f"{conda_prefix}/bin/python3"

  if envvars is not None:
    comm = " ".join(envvars.split(",") + [py_exec, py_file] + args)
  else:
    comm = " ".join([py_exec, py_file] + args)

  return exec_comm(client, comm, pwd)
