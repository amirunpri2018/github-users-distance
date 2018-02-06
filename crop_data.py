import pandas as pd

df = pd.read_csv('filter/neo4jdata/follows2013_07.csv',
                 usecols=[':START_ID', ':END_ID'])


def user_data(df):
    users = list(set(df[':START_ID']) | set(df[':END_ID']))
    df = pd.DataFrame(users, columns=['userId:ID'])
    df[':LABEL'] = 'User'
    return df


def follow_data(df):
    df = df[df['type'] == 'FollowEvent']
    df['type'] = 'FOLLOW'
    df = df[['actor_login', 'payload', 'type']]
    df.columns = [':START_ID', ':END_ID', ':TYPE']
    df.drop_duplicates(inplace=True)
    df = df.dropna(axis=0, how='any')
    return df


df = user_data(df)
df.to_csv('filter/neo4jdata/users2013_07.csv', index=False)
