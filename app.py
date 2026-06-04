import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv("word_count_data.csv")

##

st.title("Who Gets to Speak? Gendered Dialogue in Best Picture Winners")

####
st.sidebar.header("Filters")
min_year, max_year = int(df["Year Won"].min()), int(df["Year Won"].max())

year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df[
    (df["Year Won"] >= year_range[0]) &
    (df["Year Won"] <= year_range[1])
]

####



fig = px.scatter(
    filtered_df,
    x="Year Won",
    y="Percent Female Word Count",
    hover_name="Movie",
    trendline="lowess",
    size= "Total Word Count",

    hover_data={
        # "Percent Female Word Count": ':.1f',
        "Female Word Count": True,
        "Male Word Count": True,
        "Year Won": False,
        "Total Word Count": False
    },
    labels={
        "Year Won": "Oscar Year",
        "Percent Female Word Count": "% Female"
    },
    title="% Female Over Time (Word Count)",

)
fig.update_yaxes(ticksuffix="%")
fig.update_xaxes(
    type="linear",   # forces true numeric spacing
    dtick=5          # optional: tick every 5 years
)

###


col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### About this project

    This project explores the gender imbalance in films over time by analyzing the movie scripts of Oscar Best Picture winners. 

    Unfortunately, this dataset remains incomplete, as this project has faced significant difficulty analyzing a number of screenplays, particularly from the early twentieth century.
    """)
with col2:


    st.markdown("### Key insights")

    avg = filtered_df["Percent Female Word Count"].mean()
    # highest = filtered_df.loc[filtered_df["Percent Female Word Count"].idxmax()]
    # lowest = filtered_df.loc[filtered_df["Percent Female Word Count"].idxmin()]

    max_value = filtered_df["Percent Female Word Count"].max()
    highest = filtered_df[
        filtered_df["Percent Female Word Count"] == max_value
        ]
    highest_text = ", ".join(
        f"{row['Movie']} ({row['Percent Female Word Count']:.1f}%)"
        for _, row in highest.iterrows()
    )


    min_value = filtered_df["Percent Female Word Count"].min()
    lowest = filtered_df[
        filtered_df["Percent Female Word Count"] == min_value]
    lowest_text = ", ".join(
        f"{row['Movie']} ({row['Percent Female Word Count']:.1f}%)"
        for _, row in lowest.iterrows()
    )

    st.markdown(f"""
    - Average female dialogue: **{avg:.1f}%**
    - Highest: **{highest_text}**
    - Lowest: **{lowest_text}**
    """)

###

st.plotly_chart(fig, width="stretch")



# st.markdown("## Heighest & Lowest Movies")



top_10 = df.sort_values(
    "Percent Female Word Count",
    ascending=False
).head(10)

bottom_10 = df.sort_values(
    "Percent Female Word Count",
    ascending=True
).head(10)

bottom_10 = bottom_10.sort_values(
    "Percent Female Word Count",
    ascending=False
)


top_10["Group"] = "Top 10"
bottom_10["Group"] = "Bottom 10"

separator = pd.DataFrame({
    "Movie": ["⋯"],
    "Percent Female Word Count": [None],
    "Group": ["Break"]
})

combined = pd.concat([top_10, separator, bottom_10])
y_order = list(top_10["Movie"]) + ["⋯"] + list(bottom_10["Movie"])

fig = px.bar(
    combined,
    x="Percent Female Word Count",
    y="Movie",
    color="Group",
    orientation="h",
    # hover_data={
    #     "Percent Female Word Count": "% Female",
    #     "Movie": True,
    #     "Group": False,
    # },
    category_orders={"Movie": y_order},
    text="Percent Female Word Count",
    title="Top 10 vs Bottom 10 Movies by Female Dialogue",
    color_discrete_map={
        "Top 10": "#FC0FC0",
        "Bottom 10": "#0B54FE",
        "Break": "#bdbdbd"
    }
)
fig.update_traces(
    selector=dict(name="Break"),
    marker_color="lightgray",
    opacity=0.4
)
fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_traces(
    hovertemplate=
        "<b>%{y}</b><br>" +
        "% Female: %{x:.1f}%<br>" +
        "<extra></extra>"
)
fig.update_layout(height=650)


st.plotly_chart(fig, use_container_width=True)

##


st.subheader("Dataset")
st.markdown("Click on header to sort by that column.")


colors = ['#0B54FE', '#FFFFFF', '#FC0FC0']
cmap_name = 'blue_to_pink'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors)

st.dataframe(
    filtered_df[[
        "Movie",
        "Year Won",
        "Percent Female Word Count",
        "Female Word Count",
        "Male Word Count",
        "Total Word Count"
    ]].rename(columns={
        "Percent Female Word Count": "% Female",
        "Female Word Count": "Total Female",
        "Male Word Count": "Total Male",
        "Total Word Count": "Total Word Count"
        }).style.format({
    "% Female": "{:.1f}%",
    "Total Female": "{:,.0f}",
    "Total Male": "{:,.0f}",
    "Total Word Count": "{:,.0f}"
}).background_gradient(
    subset=["% Female"],
    # cmap="RdYlGn"
    cmap=custom_cmap
),
    use_container_width=True
)

search = st.text_input("Search for a movie")

df_plot = filtered_df.copy()

match_df = df_plot.iloc[0:0]  # empty fallback

if search:
    match_df = df_plot[
        df_plot["Movie"].str.contains(search, case=False, na=False)
    ]

main_df = df_plot


if not match_df.empty:

    st.dataframe(
        match_df[[
            "Movie",
            "Year Won",
            "Percent Female Word Count",
            "Female Word Count",
            "Male Word Count",
            "Total Word Count"
        ]].rename(columns={
        "Percent Female Word Count": "% Female",
        "Female Word Count": "Total Female",
        "Male Word Count": "Total Male",
        "Total Word Count": "Total Word Count"
        }),
        use_container_width=True
    )

###
