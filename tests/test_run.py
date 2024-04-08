import paramiko as ssh

from run_on_server.run import run_on_server
from tests.test_client import example_client


def test_run_on_server(example_client: ssh.SSHClient) -> None:
  output = run_on_server(
      client=example_client,
      conda_prefix="/home/zqgong/miniforge3",
      py_file="/home/zqgong/test-script.py",
      args=["1"],
  )

  assert output.strip() == "Slept for 1 seconds."
