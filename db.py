import pandas as pd

# pandas to mongodb
def pd_to_dic(df: pd.DataFrame):
    return df.to_dict('records')

# mongodb to pandas
def dic_to_pd(dic):
    return pd.DataFrame.from_records(dic)
