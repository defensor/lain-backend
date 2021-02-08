import re
from typing import List

import requests


def read_and_filter(file) -> List[str]:
    addrs = []
    for _row in file:
        row = _row.strip()
        if row:
            addrs.append(row)

    addrs = list(dict.fromkeys(addrs))

    return addrs


def filter_addrs(addrs: List[str], exclude: List[str]) -> List[str]:
    for _pat in exclude:
        pat = re.compile(_pat)
        addrs = [addr for addr in addrs if not pat.match(addr)]

    return addrs


def make_http_https(addrs: List[str]) -> List[str]:
    sites = []
    for addr in addrs:
        sites.append(f"http://{addr}")
        sites.append(f"https://{addr}")

    return sites


def site_up(site: str) -> bool:
    try:
        resp = requests.get(site, verify=False, timeout=3)
        resp.status_code
    except requests.exceptions.RequestException:
        return False

    return True


def filter_up(sites: List[str]) -> List[str]:
    active_sites = list(filter(lambda site: site_up(site), sites))

    return active_sites


if __name__ == "__main__":
    import os
    from pathlib import Path

    file_path = Path(os.path.dirname(__file__)) / ".." / "inputs" / "sites_raw"

    file = open(file_path.as_posix(), "r")

    addrs_all = read_and_filter(file)

    addrs = filter_addrs(addrs_all, exclude=["^ns\\.*"])

    sites = make_http_https(addrs)

    active_sites = filter_up(sites)

    print(f"addrs_all   : {len(addrs_all)}")
    print(f"addrs       : {len(addrs)}")
    print(f"sites       : {len(sites)}")
    print(f"active_sites: {len(active_sites)}")

    with open("out_sites", "w") as out_file:
        for site in active_sites:
            out_file.write(f"{site}\n")
