import paramiko as ssh


def exec_comm(client: ssh.SSHClient, comm: str) -> str:
  _, stdout, stderr = client.exec_command(comm)
  outp = stdout.read()
  err_msg = stderr.read()

  if len(err_msg) > 0:
    raise ChildProcessError(err_msg.decode())

  return outp.decode()


def exec_script(client: ssh.SSHClient, conda_prefix: str, py_file: str,
                args: list[str]) -> str:
  py_exec = f"{conda_prefix}/bin/python3"
  comm = " ".join([py_exec, py_file] + args)

  return exec_comm(client, comm)
