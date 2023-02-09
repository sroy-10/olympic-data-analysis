import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# import seaborn as sns
import streamlit as st
from PIL import Image

import helper
from preprocessor import preprocess

event_df = pd.read_csv("dataset/athlete_events.csv")
region_df = pd.read_csv("dataset/noc_regions.csv")

st.sidebar.markdown(
    '<div style="text-align: center;"><h1>Olympic Analysis</h1></div>',
    unsafe_allow_html=True,
)
st.sidebar.image(Image.open("olympic_logo.png"))

user_menu = st.sidebar.radio(
    "Select an Option",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete wise Analysis",
    ),
)

event_df, region_df = preprocess(event_df, region_df)

if user_menu == "Medal Tally":
    st.sidebar.subheader("Medal Tally")

    # fetch the country and year for selection
    years, country = helper.get_country_year_list(event_df)

    user_year = st.sidebar.selectbox(
        "Year-wise",
        years,
    )

    user_country = st.sidebar.selectbox(
        "Country-wise",
        country,
    )

    # fetch the data as per the selection data
    medal_tally, title = helper.fetch_medal_tally(
        event_df, region_df, user_year, user_country
    )

    st.title(title)
    st.table(medal_tally)

elif user_menu == "Overall Analysis":
    st.title("Top Statistics")
    overall_performance = {
        # no of editions; 1906 Olympic is not considered
        "Year": (event_df["Year"].unique().shape[0] - 1),
        # no of city
        "City": (event_df["City"].unique().shape[0]),
        # no of sports
        "Sports": (event_df["Sport"].unique().shape[0]),
        # no of events
        "Events": (event_df["Event"].unique().shape[0]),
        # no of athelets
        "Athelets": (event_df["Name"].unique().shape[0]),
        # no of participating nation
        "Nation": (event_df["region"].unique().shape[0]),
    }
    col = st.columns(len(overall_performance), gap="large")
    for idx, d_val in enumerate(overall_performance.items()):
        with col[idx]:
            st.header(d_val[0])
            st.title(d_val[1])

    # Display Chart :: Year vs No. of Participating Country
    st.subheader("Participating Nations over the Years")
    nation_over_time = helper.get_data_over_time(event_df, "region")
    fig = px.line(
        nation_over_time,
        x="Edition",
        y="region",
        labels={"region": "No. of Participating Country"},
    )
    st.plotly_chart(fig)

    # Display Chart :: Year vs Number of Events
    st.subheader("Events over the Years")
    event_over_time = helper.get_data_over_time(event_df, "Event")
    fig = px.line(
        event_over_time,
        x="Edition",
        y="Event",
        labels={"Event": "No. of Events"},
    )
    st.plotly_chart(fig)

    # Display Chart :: Year vs Number of Athlete
    st.subheader("Athlete over the Years")
    athlete_over_time = helper.get_data_over_time(event_df, "Name")
    fig = px.line(
        athlete_over_time,
        x="Edition",
        y="Name",
        labels={"Event": "No. of Athlete Participated"},
    )
    st.plotly_chart(fig)

    # heatmap for Number of Events over time
    # st.subheader("No of Events over time (Every Sport)")
    # fig, ax = plt.subplots(figsize=(20, 20))
    # x = event_df.drop_duplicates(["Year", "Sport", "Event"])
    # plt.figure(figsize=(20, 20))
    # ax = sns.heatmap(
    #     x.pivot_table(
    #         index="Sport",
    #         columns="Year",
    #         values="Event",
    #         aggfunc="count",
    #     )
    #     .fillna(0)
    #     .astype(int),
    #     annot=True,
    # )
    # st.pyplot(fig)


elif user_menu == "Country-wise Analysis":
    # fetch the country and year for selection
    years, country = helper.get_country_year_list(
        event_df, overall_flag=""
    )
    user_country = st.sidebar.selectbox(
        "Select a Country",
        country,
    )
    country_df = helper.get_yearwise_medal_tally(event_df, user_country)
    st.title(f"{user_country}: Medal Tally over the years")
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    # construct a heatmap which showcase in which sports the country excels

elif user_menu == "Athlete wise Analysis":
    pass
