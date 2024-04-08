import re


def extract_path(output: str, pattern: str) -> str:
  res = re.search(pattern, output)

  if res is None:
    raise ValueError(f"No {pattern} in\n{output}")

  return res.groups()[-1]
