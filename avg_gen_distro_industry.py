import streamlit as st
import pandas as pd
import os

# 1. Cache the function so the cloud server doesn't hit the BLS API on every single click
@st.cache_data
def load_live_data():
    csv_filename = "gender_by_industry.csv"
    
    # Check if the CSV file exists on the Streamlit server instance
    if not os.path.exists(csv_filename):
        st.info("🔄 First-time setup: Fetching live data from the BLS API...")
        
        # This imports your fetch_data.py file and runs its main function
        import fetch_data
        fetch_data.fetch_bls_data()
        
    return pd.read_csv(csv_filename)

# 2. Call the function to populate your dashboard variables
df_historical = load_live_data()
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
