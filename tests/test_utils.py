import pytest

from run_on_server.utils import extract_path


def test_extract_path() -> None:
  output = "Data saved to /home/zqgong/empty-dir!"

  with pytest.raises(ValueError):
    extract_path(output, r"saved to (.*)\.")

  path = extract_path(output, r"saved to (.*)\!")

  assert path == "/home/zqgong/empty-dir"
