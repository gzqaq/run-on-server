from run_on_server.sync import rsync


def test_rsync() -> None:
  synced = rsync("gpu2", "~/.empty", "/tmp/")

  assert synced
