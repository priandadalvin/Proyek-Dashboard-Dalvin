import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

sns.set_style("whitegrid")

df = pd.read_csv("main_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

# Mapping label
df["weather_label"] = df["weathersit"].map({
    1: "Clear",
    2: "Mist",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Ice"
})

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.header("Filter Data")
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

filtered_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

st.title("🚲 Bike Sharing Dashboard")

total = filtered_df["cnt"].sum()
st.metric("Total Rentals", f"{total:,}")

st.subheader("Daily Rentals Trend")

daily_df = filtered_df.groupby("dteday")["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    daily_df["dteday"],
    daily_df["cnt"],
    marker="o",
    linewidth=2
)

# Format tanggal
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)

ax.set_title("Daily Rentals")
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")

# Grid
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

st.subheader("Rentals by Weather Condition")

weather_df = filtered_df.groupby("weather_label")["cnt"].sum() \
                        .sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x="weather_label",
    y="cnt",
    data=weather_df,
    ax=ax
)

# Tambahkan label angka di atas bar
for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"{int(x):,}" for x in container.datavalues],
        padding=3
    )

ax.set_title("Total Rentals by Weather")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Total Rentals")

st.pyplot(fig)

st.caption("Bike Sharing Dashboard - Streamlit App")