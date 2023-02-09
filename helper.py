def get_medal_tally(event_df, region_df, filter=dict()):
    medal_tally = event_df.drop_duplicates(
        subset=[
            "Team",
            "NOC",
            "Games",
            "Year",
            "City",
            "Sport",
            "Event",
            "Medal",
        ]
    )

    # applying filter (if any)
    if len(filter) != 0:
        for key, val in filter.items():
            medal_tally = medal_tally[medal_tally[key] == val]

    # grouping & finding the value
    medal_tally = (
        medal_tally.groupby("region")
        .sum(numeric_only=True)[["Gold", "Silver", "Bronze"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )
    medal_tally.rename(columns={"region": "Region"}, inplace=True)
    medal_tally["Total"] = (
        medal_tally["Gold"]
        + medal_tally["Silver"]
        + medal_tally["Bronze"]
    )
    return medal_tally


def get_country_year_list(df, overall_flag="X"):
    years = df["Year"].dropna().unique().tolist()
    years.sort(reverse=True)
    if overall_flag == "X":
        years.insert(0, "Overall")

    country = df["region"].dropna().unique().tolist()
    country.sort()
    if overall_flag == "X":
        country.insert(0, "Overall")

    return years, country


def fetch_medal_tally(event_df, region_df, year, country):
    filter = dict()
    title = ""

    if year == "Overall" and country == "Overall":
        title = "Overall Performance"

    elif year == "Overall" and country != "Overall":
        title = f"{country}'s Overall Performance"
        filter = {"region": country}

    elif year != "Overall" and country == "Overall":
        title = f"Overall Performance in {year}"
        filter = {"Year": year}

    elif year != "Overall" and country != "Overall":
        title = f"{country}'s Performance in {year}"
        filter = {"region": country, "Year": year}

    medal_tally = get_medal_tally(event_df, region_df, filter)
    return medal_tally, title


def get_nation_over_time(df):
    nation_over_time = (
        df.drop_duplicates(["Year", "region"])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("index")
    )
    nation_over_time = nation_over_time.rename(
        columns={"index": "Edition", "Year": "No. of Countries"}
    )
    return nation_over_time


def get_data_over_time(df, col):
    data_over_time = (
        df.drop_duplicates(["Year", col])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("index")
    )
    data_over_time = data_over_time.rename(
        columns={"index": "Edition", "Year": col}
    )
    return data_over_time


def get_yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(
        subset=[
            "Team",
            "NOC",
            "Games",
            "Year",
            "City",
            "Sport",
            "Event",
            "Medal",
        ],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]
    new_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return new_df
