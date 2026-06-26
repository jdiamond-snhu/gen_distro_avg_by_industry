import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set up page configuration
st.set_page_config(page_title="Historical Gender Ratio", layout="wide")
st.title("📊 Historical Gender Ratio Dashboard by Industry")

# --- DYNAMIC LIVE DATASET LOADER ---
@st.cache_data
def load_live_data():
    csv_filename = "gender_by_industry.csv"
    
    if not os.path.exists(csv_filename):
        st.info("🔄 First-time setup: Fetching live data from the BLS API...")
        import fetch_data
        fetch_data.fetch_bls_data()
        
    return pd.read_csv(csv_filename)

# Load data into memory safely
df_historical = load_live_data()

# --- SIDEBAR YEAR FILTERS ---
st.sidebar.header("🗓️ Select Year Range")

min_year = int(df_historical["Year"].min())
max_year = int(df_historical["Year"].max())

from_year = st.sidebar.number_input("From Year:", min_value=min_year, max_value=max_year, value=min_year)
to_year = st.sidebar.number_input("To Year:", min_value=min_year, max_value=max_year, value=max_year)

if from_year > to_year:
    st.error("Error: 'From Year' cannot be greater than 'To Year'. Please fix your range.")
else:
    filtered_df = df_historical[(df_historical["Year"] >= from_year) & (df_historical["Year"] <= to_year)]
    aggregated_df = filtered_df.groupby("Industry")[["Male (%)", "Female (%)"]].mean().reset_index()

    st.subheader(f"Average Gender Distribution from {from_year} to {to_year}")
    
    cols = st.columns(3)
    colors = ["#2b7bba", "#e05a47"]
    
    for idx, row in aggregated_df.iterrows():
        col = cols[idx % 3]
        with col:
            male_val = row["Male (%)"]
            female_val = row["Female (%)"]
            
            # CRITICAL PIE CHART VALUE SAFETY CHECK
            if male_val <= 0 and female_val <= 0:
                st.warning(f"⚠️ No data found for {row['Industry']}.")
                continue
                
            fig, ax = plt.subplots(figsize=(4, 4))
            
            # Ensure no tiny rounding errors result in values lower than 0
            sizes = [max(0, male_val), max(0, female_val)]
            
            ax.pie(
                sizes, 
                labels=["Male", "Female"], 
                autopct="%1.1f%%", 
                startangle=90, 
                colors=colors
            )
            ax.set_title(f"{row['Industry']} Sector (Avg)", fontsize=13, fontweight="bold")
            st.pyplot(fig)
            plt.close(fig)
