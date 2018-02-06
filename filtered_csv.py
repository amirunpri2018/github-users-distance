import pandas as pd
import json
from io import StringIO

df = pd.read_csv('data/2012_05_06.csv')
nan_index = df[(df['type'] == 'MemberEvent') & df.isnull().any(axis=1)].index
df = df.drop(nan_index)


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def filter_data(row):
    event_type, payload, actor_login, repo_url = row
    data = json.load(StringIO(payload))

    if event_type == 'FollowEvent':
        actor = actor_login
        target = data['target']['login']
        action = None
    else:
        action = data['action']
        if 'repo' in data:
            target = data['member']
            actor = data['repo']
        else:
            target = data['member']['login']
            actor = remove_prefix(repo_url, "https://github.com/")

    row = [event_type, target, actor, action]
    return row


df = df.apply(filter_data, axis=1)
print("\n Writing to CSV file...")
df.to_csv('filter/2012_05_06.csv', sep='\t')
print("\n Done!")
