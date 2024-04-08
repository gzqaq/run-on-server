# run-on-server

Run experiments on a SSH server.

- Supports executing necessary commands before running experiments.
- Supports transferring saved data from the server to the local host by `rsync`.

## Usage

``` text
Usage: run-on-server [OPTIONS] SERVER SCRIPT [ARGS]...

  Run SCRIPT with arguments ARGS on the SSH server named SERVER.

Options:
  --conda-prefix TEXT    Conda prefix on the server. Can also be passed by
                         SSH_CONDA_PREFIX.  [required]
  -c, --pre-comm TEXT    Command to be executed before running the script.
  -s, --sync             Whether to transfer saved data from the server.
  -p, --re-pattern TEXT  Regex pattern to extract the path to be transferred
                         from server.
  -t, --target PATH      Local location to save the transferred data.
  -h, --help             Show this message and exit.
```

## Installation
Build with `poetry`:

``` shell
poetry install
```
