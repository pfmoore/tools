import sys
import requests
from wheel.install import WheelFile
import xml.etree.ElementTree

def pypi_candidates(package):
    req = requests.get('https://pypi.python.org/pypi/{}/json'.format(package))
    if req.status_code != requests.codes.ok:
        return "", ""
    data = req.json()
    ver = data['info']['version']
    wheels = [u['filename'] for u in data['urls'] if u['packagetype'] =='bdist_wheel']
    sdists = [u['filename'] for u in data['urls'] if u['packagetype'] =='sdist']
    wheels = [w for w in wheels if WheelFile(w).compatible]
    return ver, wheels[0] if wheels else sdists[0]

def binstar_candidates(package, ver=None):
    req = requests.get('https://pypi.binstar.org/pmoore/simple/{}/'.format(package))
    if req.status_code != requests.codes.ok:
        return False, "", ""

    p = xml.etree.ElementTree.fromstring(req.text)
    candidates = []
    for el in p.iterfind('.//a'):
        try:
            wheel = WheelFile(el.text)
        except BadWheelFile:
            continue
        if wheel.compatible:
            candidates.append(wheel)

    if not candidates:
        return False, "", ""

    if ver:
        # First, try for a match
        for wheel in candidates:
            wheel_ver = wheel.parsed_filename.group('ver')
            if wheel_ver == ver:
                return True, wheel_ver, wheel.filename

    # No exact match, just get the first (should probably get latest version,
    # save that for another day...)
    wheel = candidates[0]
    return False, wheel.parsed_filename.group('ver'), wheel.filename

if __name__ == '__main__':
    pypi_ver, pypi_file = pypi_candidates(sys.argv[1])
    messages = []
    if not pypi_ver:
        messages.append("Project does not exist")
    if pypi_file.endswith('.whl'):
        messages.append("PyPI has a wheel")
    matches, binstar_ver, binstar_file = binstar_candidates(sys.argv[1], pypi_ver)
    if not matches:
        messages.append("Binstar does not have the PyPI version")

    print("Source   Version       Filename")
    print("-------  ------------  ------------------------------")
    print("PyPI     {:<12}  {}".format(pypi_ver, pypi_file))
    print("Binstar  {:<12}  {}".format(binstar_ver, binstar_file))

    if messages:
        print("\n" + "\n".join(messages))
