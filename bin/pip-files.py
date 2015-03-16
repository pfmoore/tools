from distutils.version import LooseVersion
import webbrowser
import argparse
import requests
import sys

parser = argparse.ArgumentParser(description="List files for a PyPI project")
parser.add_argument('name', help="The name of the project")
parser.add_argument('--all', action='store_true', help="List all versions (default: latest)")

args = parser.parse_args()

url = 'https://pypi.python.org/pypi/' + args.name
req = requests.get(url + "/json")
data = req.json()
if args.all:
    rels = sorted(data['releases'].keys(), key=LooseVersion)
    for rel in rels:
        files = data['releases'][rel]
        print(rel, ('\n ' + (' '*len(rel))).join(f['filename'] for f in files))
else:
    rel = data['info']['version']
    files = data['urls']
    print(rel, ('\n ' + (' '*len(rel))).join(f['filename'] for f in files))
