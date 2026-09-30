import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(
    page_title="Airbnb Booking Analysis",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Airbnb Booking Analysis")
st.subheader("Exploratory Data Analysis Dashboard")
st.write(
    "This interactive dashboard explores Airbnb listing patterns "
    "using room type, price, neighbourhood, reviews, availability, "
    "and correlation analysis."
)

df = pd.read_csv("AB_India_2019.csv")
st.sidebar.title("🔍 Filters")

room_types = df["room_type"].unique()

selected_room = st.sidebar.multiselect(
    "Select Room Type",
    room_types,
    default=room_types
)

filtered_df = df[df["room_type"].isin(selected_room)]

st.write("Dataset loaded successfully!")

st.write("Number of rows:", df.shape[0])
st.write("Number of columns:", df.shape[1])
st.divider()

total_listings = len(filtered_df)
average_price = filtered_df["price"].mean()
total_hosts = filtered_df["host_id"].nunique()
average_reviews = filtered_df["number_of_reviews"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏠 Total Listings", f"{total_listings:,}")
col2.metric("💰 Average Price", f"${average_price:,.2f}")
col3.metric("👤 Total Hosts", f"{total_hosts:,}")
col4.metric("⭐ Average Reviews", f"{average_reviews:.1f}")
st.divider()

st.header("📊 Room Type Analysis")

room_counts = filtered_df["room_type"].value_counts()

st.bar_chart(room_counts)
st.divider()

st.header("💰 Price Analysis")

price_data = filtered_df[(filtered_df["price"] > 0) & (filtered_df["price"] <= 500)]

st.line_chart(price_data["price"].value_counts().sort_index())
st.divider()

st.header("📍 Neighbourhood Analysis")

neighbourhood_counts = filtered_df["neighbourhood"].value_counts().head(10)

st.bar_chart(neighbourhood_counts)
st.divider()

st.header("💬 Price vs Number of Reviews")

price_reviews = filtered_df[
    (filtered_df["price"] > 0) &
    (filtered_df["price"] <= 500)
].copy()

st.scatter_chart(
    price_reviews,
    x="price",
    y="number_of_reviews"
)
st.divider()

st.header("📅 Availability Analysis")

st.bar_chart(
    filtered_df["availability_365"].value_counts().sort_index()
)
st.divider()

st.header("🔗 Correlation Analysis")

numeric_cols = [
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365"
]

corr_matrix = filtered_df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax
)

st.pyplot(fig)
st.divider()

st.header("💡 Key Insights")

st.markdown("""
- 🏠 **Entire home/apt** is the most common room type in the dataset.
- 💰 Listing prices are **right-skewed**, with some high-price outliers.
- 📍 Listing counts vary across the different neighbourhoods.
- 💬 **Price and number of reviews** have a very weak linear relationship.
- ⭐ **Number of reviews and reviews per month** show a moderate positive relationship.
- 📅 Availability varies considerably across listings, with many listings having very low availability.
""")
st.divider()

st.header("📌 Dataset Disclaimer")

st.info("""
This project uses a Bengaluru-themed adapted version of the original
NYC Airbnb dataset for educational Exploratory Data Analysis.

The neighbourhood names and geographic information have been adapted
to represent Bengaluru for this project, while several numerical
variables are retained from the source dataset.

Therefore, the results should not be interpreted as actual Bengaluru
Airbnb market statistics.
""")
st.divider()

st.caption("Airbnb Booking Analysis | Exploratory Data Analysis Project")
st.caption("Built using Python, Pandas, Matplotlib, Seaborn and Streamlit")