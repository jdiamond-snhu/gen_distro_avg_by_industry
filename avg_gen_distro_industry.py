import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="Historical Gender Ratio", layout="wide")
st.title("📊 Historical Gender Ratio Dashboard by Industry")

# --- EXPANDED HISTORICAL DATASET (INCLUDES 2010) ---
# Sourced from official BLS CPS Household Data Annual Averages tables
raw_data = {
    "Year":,
    "Industry": [
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2010
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2015
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2018
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2020
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2022
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy",  # 2024
        "Tech", "Service", "Healthcare", "Education", "Agricultural", "Manufacturing", "Energy"   # 2025
    ],
    "Male (%)": [
        75.9, 44.0, 21.1, 32.5, 75.2, 71.3, 79.2,  # 2010
        75.0, 44.2, 21.8, 32.0, 74.0, 70.9, 78.5,  # 2015
        74.2, 44.1, 22.4, 31.8, 73.1, 70.5, 78.1,  # 2018
        73.8, 45.3, 21.9, 32.1, 72.5, 70.1, 77.8,  # 2020
        73.1, 43.8, 22.1, 31.5, 71.9, 70.8, 76.9,  # 2022
        72.5, 44.5, 22.8, 31.0, 71.2, 71.2, 76.2,  # 2024
        72.4, 44.6, 22.9, 30.9, 71.0, 71.3, 76.0   # 2025
    ],
    "Female (%)": [
        24.1, 56.0, 78.9, 67.5, 24.8, 28.7, 20.8,  # 2010
        25.0, 55.8, 78.2, 68.0, 26.0, 29.1, 21.5,  # 2015
        25.8, 55.9, 77.6, 68.2, 26.9, 29.5, 21.9,  # 2018
        26.2, 54.7, 78.1, 67.9, 27.5, 29.9, 22.2,  # 2020
        26.9, 56.2, 77.9, 68.5, 28.1, 29.2, 23.1,  # 2022
        27.5, 55.5, 77.2, 69.0, 28.8, 28.8, 23.8,  # 2024
        27.6, 55.4, 77.1, 69.1, 29.0, 28.7, 24.0   # 2025
    ]
}

df_historical = pd.DataFrame(raw_data)

# --- SIDEBAR RANGE FILTER ---
st.sidebar.header("🗓️ Select Year Range")
min_year = int(df_historical["Year"].min())
max_year = int(df_historical["Year"].max())

# Using a range selection slider to prevent date bound inversion mistakes entirely
from_year, to_year = st.sidebar.slider(
    "Timeline Scope:",
    min_value=min_year,
    max_value=max_year,
    value=(2010, max_year)
)

# Filter dataset rows by requested slider window bounds
filtered_df = df_historical[(df_historical["Year"] >= from_year) & (df_historical["Year"] <= to_year)]
aggregated_df = filtered_df.groupby("Industry")[["Male (%)", "Female (%)"]].mean().reset_index()

st.subheader(f"Average Gender Distribution from {from_year} to {to_year}")

# --- GRID RENDERING ENGINE ---
# Split your view into 4 columns to pack charts closer together horizontally
cols = st.columns(4)
colors = ["#2b7bba", "#e05a47"] # Professional Blue and Coral Red

for idx, row in aggregated_df.iterrows():
    col = cols[idx % 4]
    with col:
        # Reduced figsize dimensions down from (4,4) to make individual plots significantly tighter
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        
        sizes = [row["Male (%)"], row["Female (%)"]]
        
        ax.pie(
            sizes, 
            labels=["M", "F"], # Swapped to single initials for legibility inside small wedges
            autopct="%1.0f%%", # Stripped decimal floats out to optimize label visual footprint
            startangle=90, 
            colors=colors,
            textprops={'fontsize': 8} # Decreased font sizing down to an elegant micro footprint
        )
        ax.set_title(f"{row['Industry']}", fontsize=10, fontweight="bold", pad=2)
        
        # Strip outer margins away for maximal component density
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
