from getpass import getpass
import json
import requests
import pandas as pd

r = requests.get(
    'https://registration.pep-dortmund.org/events/4/participants',
    headers={'accept': 'application/json'},
    auth=(input('Username: '), getpass())
)
# make sure request was successfull
r.raise_for_status()

data = r.json()


def get_data(p):
    data = p['data'].copy()
    del data['name']
    del data['email']

    return data

participants = [get_data(p) for p in data['participants']]

with open('data/toolbox2020.json', 'w') as f:
    json.dump(participants, f, indent=2)


keys = ['os', 'installieren', 'toolbox', 'latex']
df = pd.DataFrame([{k: p[k] for k in keys} for p in participants])

for part in ('installieren', 'toolbox', 'latex'):
    print('\n')
    print(part, '\t\t', df[df[part]]['os'].value_counts().sum())
    print(df[df[part]]['os'].value_counts())
