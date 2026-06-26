import json
import pandas as pd
import requests

# Dictionary mapping your industries to official BLS Survey Series IDs
BLS_SERIES_MAP = {
    "Agriculture, forestry, fishing, and hunting": "LNU02032213",
    "Mining, quarrying, and oil and gas extraction": "LNU02032214", 
    "Manufacturing": "LNU02032216",
    "Education and health services": "LNU02032224", 
    "Professional and business services": "LNU02032223", 
    "Other services": "LNU02032227" 
}

def fetch_bls_data(start_year=2015, end_year=2025):
    """Fetches data directly from the official BLS API."""
    url = "https://bls.gov"
    headers = {"Content-type": "application/json"}
    
    series_ids = list(BLS_SERIES_MAP.values())
    payload = json.dumps({
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year)
    })
    
    print(f"🔄 Contacting BLS API for historical range {start_year}-{end_year}...")
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error: API request failed with status code {response.status_code}")
        return None
        
    json_data = response.json()
    id_to_name = {v: k for k, v in BLS_SERIES_MAP.items()}
    records = []
    
    for series in json_data.get("Results", {}).get("series", []):
        series_id = series.get("seriesID")
        industry_name = id_to_name.get(series_id, "Unknown")
        
        for item in series.get("data", []):
            year = int(item.get("year"))
            period = item.get("period") 
            female_percent = float(item.get("value"))
            male_percent = round(100.0 - female_percent, 1)
            
            records.append({
                "Year": year,
                "Period": period,
                "Industry": industry_name,
                "Male (%)": male_percent,
                "Female (%)": female_percent
            })
            
    df = pd.DataFrame(records)
    
    # Standardize names to your requested list
    rename_dict = {
        "Professional and business services": "Tech",
        "Education and health services": "Healthcare & Education",
        "Other services": "Service",
        "Agriculture, forestry, fishing, and hunting": "Agricultural",
        "Mining, quarrying, and oil and gas extraction": "Energy",
        "Manufacturing": "Manufacturing"
    }
    df["Industry"] = df["Industry"].replace(rename_dict)
    
    # Create clean annual averages
    final_df = df.groupby(["Year", "Industry"])[["Male (%)", "Female (%)"]].mean().reset_index()
    final_df = final_df.round(1)
    
    final_df.to_csv("gender_by_industry.csv", index=False)
    print("✅ Success! 'gender_by_industry.csv' generated.")
    return final_df

if __name__ == "__main__":
    fetch_bls_data()
