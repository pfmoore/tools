import webbrowser
import argparse
import requests
import sys

parser = argparse.ArgumentParser(description="Open a PyPI project's webpage")
parser.add_argument('name', help="The name of the project")
parser.add_argument('--pypi', action='store_true',
        help="Get PyPI page rather than homepage")

args = parser.parse_args()

url = 'https://pypi.python.org/pypi/' + args.name
if not args.pypi:
    req = requests.get(url + "/json")
    data = req.json()
    url = data['info'].get('home_page', url)

webbrowser.open_new_tab(url)
