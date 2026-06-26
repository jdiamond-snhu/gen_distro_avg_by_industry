import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="Historical Gender Ratio", layout="wide")
st.title("📊 Historical Gender Ratio Dashboard by Industry")

# --- MOCK HISTORICAL DATASET ---
# In a real app, you would load this directly from your scraped CSV or database.
historical_data = {
    "Year": [2018, 2018, 2019, 2019, 2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024, 2025, 2025],
    "Industry": ["Tech", "Healthcare", "Tech", "Healthcare", "Tech", "Healthcare", "Tech", "Healthcare", 
                 "Tech", "Healthcare", "Tech", "Healthcare", "Tech", "Healthcare", "Tech", "Healthcare"],
    "Male (%)": [75, 22, 74, 21, 73, 23, 72, 24, 71, 25, 70, 24, 69, 23, 68, 22],
    "Female (%)": [25, 78, 26, 79, 27, 77, 28, 76, 29, 75, 30, 76, 31, 77, 32, 78]
}
df_historical = pd.DataFrame(historical_data)

# --- SIDEBAR YEAR FILTERS ---
st.sidebar.header("🗓️ Select Year Range")

# Determine data boundaries dynamically
min_year = int(df_historical["Year"].min())
max_year = int(df_historical["Year"].max())

# Creating the 'From' and 'To' inputs
from_year = st.sidebar.number_input("From Year:", min_value=min_year, max_value=max_year, value=2020)
to_year = st.sidebar.number_input("To Year:", min_value=min_year, max_value=max_year, value=2024)

# Error validation handling for date bounds
if from_year > to_year:
    st.error("Error: 'From Year' cannot be greater than 'To Year'. Please fix your range.")
else:
    # Filter dataset using pandas boolean masking based on user input
    filtered_df = df_historical[(df_historical["Year"] >= from_year) & (df_historical["Year"] <= to_year)]
    
    # Aggregate data by calculating the mean across the chosen span
    aggregated_df = filtered_df.groupby("Industry")[["Male (%)", "Female (%)"]].mean().reset_index()

    st.subheader(f"Average Gender Distribution from {from_year} to {to_year}")
    
    # Display the processed charts
    cols = st.columns(2)
    colors = ["#2b7bba", "#e05a47"]
    
    for idx, row in aggregated_df.iterrows():
        col = cols[idx % 2]
        with col:
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(
                [row["Male (%)"], row["Female (%)"]], 
                labels=["Male", "Female"], 
                autopct="%1.1f%%", 
                startangle=90, 
                colors=colors
            )
            ax.set_title(f"{row['Industry']} Sector (Avg)", fontsize=13, fontweight="bold")
            st.pyplot(fig)
            plt.close(fig)
