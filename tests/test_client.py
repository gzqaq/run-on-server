import pytest

import paramiko as ssh

from run_on_server.client import init_client


def test_init_client() -> None:
  client = init_client("gpu2")
  _, stdout, _ = client.exec_command("echo hello")

  assert stdout.read().decode().strip() == "hello"


@pytest.fixture(scope="module")
def example_client() -> ssh.SSHClient:
  return init_client("gpu2")
