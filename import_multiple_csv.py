import pandas as pd
import glob


def concat_more_file(df):
    path = './users2'
    all_files = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()

    csv_list = []
    for csv_file in all_files:
        df = pd.read_csv(csv_file, index_col=None)
        csv_list.append(df)

    frame = pd.concat(csv_list)
    frame.drop_duplicates(inplace=True)
    return frame


def concat_users(df):
    df1 = pd.read_csv('users2/users1.csv', keep_default_na=False)
    df2 = pd.read_csv('users2/users2.csv', keep_default_na=False)

    df = pd.concat([df1, df2])
    df.drop_duplicates(inplace=True)
    df.to_csv('users2/users.csv', index=False)
    return df
