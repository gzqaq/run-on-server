import paramiko as ssh

from run_on_server.run import exec_comm, exec_script
from tests.test_client import example_client


def test_exec_comm(example_client: ssh.SSHClient) -> None:
  output = exec_comm(
      client=example_client,
      comm="echo hello",
  )

  assert output.strip() == "hello"


def test_exec_script(example_client: ssh.SSHClient) -> None:
  output = exec_script(
      client=example_client,
      conda_prefix="/home/zqgong/miniforge3",
      py_file="/home/zqgong/test-script.py",
      args=["1"],
  )

  assert output.strip() == "Slept for 1 seconds."
