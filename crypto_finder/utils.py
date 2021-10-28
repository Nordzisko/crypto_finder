import os
import importlib.util
from pathlib import Path


def get_package_contents(package_name: str) -> set:
    """
    Given a package name ('crypto_finder.models') will return all the modules in that package
    Source: https://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package
    """
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()

    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith("__"):
                continue
            current = ".".join((package_name, entry.name.partition(".")[0]))
            if entry.is_file():
                if entry.name.endswith(".py"):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= get_package_contents(current)

    return ret
