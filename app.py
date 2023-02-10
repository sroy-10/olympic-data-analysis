import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import streamlit as st
from PIL import Image

import helper
from preprocessor import preprocess

# from sessionState import _get_state
# state = _get_state()
# state.page_config =
st.set_page_config(layout="wide")

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
    st.subheader("No of Events over time (Every Sport)")
    x = event_df.drop_duplicates(["Year", "Sport", "Event"])
    fig = plt.figure(figsize=(20, 20))
    ax = sns.heatmap(
        x.pivot_table(
            index="Sport",
            columns="Year",
            values="Event",
            aggfunc="count",
        )
        .fillna(0)
        .astype(int),
        annot=True,
        linewidth=0.5,
        cmap="crest",
    )
    st.pyplot(fig)

    # Most Successful Athletes
    st.subheader("Most Successful Athletes")

    sports_list = event_df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    selected_sports = st.selectbox("Select a Sports", sports_list)

    # # CSS to inject contained in a string
    # hide_table_row_index = """
    #         <style>
    #         thead tr th:first-child {display:none}
    #         tbody th {display:none}
    #         </style>
    #         """

    # # Inject CSS with Markdown
    # st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Displaying table
    st.table(
        helper.get_most_successful_athlete(event_df, selected_sports)
    )

elif user_menu == "Country-wise Analysis":
    # fetch the country and year for selection
    # years, country = helper.get_country_year_list(
    #     event_df, overall_flag=""
    # )
    country_list = (
        event_df.dropna(subset=["region"])["region"].unique().tolist()
    )
    country_list.sort()
    selected_country = st.sidebar.selectbox(
        "Select a Country",
        country_list,
    )
    country_df = helper.get_yearwise_medal_tally(
        event_df, selected_country
    )
    st.title(f"{selected_country}'s Medal Tally over the years")
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    # construct a heatmap which showcase in which sports the country excels
    pivot = helper.get_country_event_heatmap(event_df, selected_country)
    if len(pivot) != 0:
        st.subheader(
            f"{selected_country} excels in the following Sports"
        )
        fig = plt.figure(figsize=(10, 15))
        ax = sns.heatmap(
            pivot,
            annot=True,
            linewidths=0.5,
            cmap="YlOrBr",
        )
        st.pyplot(fig)

    # top successful athelets of the country
    st.subheader(f"Most Successful Athletes of {selected_country}")
    st.table(
        helper.get_most_successful_athlete(
            df=event_df, country=selected_country, top=10
        )
    )

elif user_menu == "Athlete wise Analysis":
    st.subheader("Distribution of Age")
    athlete_df = event_df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        [
            "Overall Age",
            "Gold Medalist",
            "Silver Medalist",
            "Bronze Medalist",
        ],
        show_hist=False,
        show_rug=False,
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = [
        "Basketball",
        "Judo",
        "Football",
        "Tug-Of-War",
        "Athletics",
        "Swimming",
        "Badminton",
        "Sailing",
        "Gymnastics",
        "Art Competitions",
        "Handball",
        "Weightlifting",
        "Wrestling",
        "Water Polo",
        "Hockey",
        "Rowing",
        "Fencing",
        "Shooting",
        "Boxing",
        "Taekwondo",
        "Cycling",
        "Diving",
        "Canoeing",
        "Tennis",
        "Golf",
        "Softball",
        "Archery",
        "Volleyball",
        "Synchronized Swimming",
        "Table Tennis",
        "Baseball",
        "Rhythmic Gymnastics",
        "Rugby Sevens",
        "Beach Volleyball",
        "Triathlon",
        "Rugby",
        "Polo",
        "Ice Hockey",
    ]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)
    fig = ff.create_distplot(
        x,
        name,
        show_hist=False,
        show_rug=False,
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = event_df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    st.subheader("Height vs Weight")
    selected_sports = st.selectbox("Select a Sports", sport_list)
    temp_df = helper.get_weight_v_height(event_df, selected_sports)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(
        x=temp_df["Weight"],
        y=temp_df["Height"],
        hue=temp_df["Medal"],
        style=temp_df["Sex"],
        s=60,
    )
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.get_men_vs_women(event_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
