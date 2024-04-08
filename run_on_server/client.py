from pathlib import Path

import paramiko as ssh

SSH_DIR = Path("~/.ssh/").expanduser().resolve()


def local_conf() -> ssh.SSHConfig:
  return ssh.SSHConfig.from_path(str(SSH_DIR / "config"))


def init_client(server_name: str) -> ssh.SSHClient:
  conf = local_conf()
  server_info = conf.lookup(server_name)

  assert "user" in server_info and "port" in server_info

  client = ssh.SSHClient()
  client.set_missing_host_key_policy(ssh.AutoAddPolicy())
  client.load_system_host_keys()
  client.connect(
      hostname=server_info["hostname"],
      port=int(server_info["port"]),
      username=server_info["user"],
  )

  return client
