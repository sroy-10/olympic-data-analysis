import pandas as pd


def preprocess(event_df, region_df):
    event_df = event_df[event_df["Season"] == "Summer"]
    event_df = event_df.merge(region_df, how="left", on="NOC")
    event_df.drop_duplicates(inplace=True)
    event_df = pd.concat(
        [event_df, pd.get_dummies(event_df["Medal"])], axis=1
    )
    return event_df, region_df
