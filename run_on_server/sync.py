from pathlib import Path

import subprocess as sp


def rsync(server_name: str, src: str | Path, tgt: str | Path) -> bool:
  subp = sp.Popen(
      args=["/usr/bin/rsync", "-az", f"{server_name}:{src}",
            str(tgt)],
      stdout=sp.PIPE,
      stderr=sp.PIPE,
  )
  _, stderr = subp.communicate()

  if subp.returncode != 0:
    raise ChildProcessError(stderr.decode())

  return True
