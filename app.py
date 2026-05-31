import pandas as pd
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Tourist Recommender", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    
    # Clean column names (avoid KeyError)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    
    return df

df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🔎 Search Preferences")

place_type = st.sidebar.selectbox(
    "Select Place Type", sorted(df["Type"].dropna().unique())
)

season = st.sidebar.selectbox(
    "Select Best Season", sorted(df["Best_Season"].dropna().unique())
)

budget = st.sidebar.selectbox(
    "Select Budget", sorted(df["Budget"].dropna().unique())
)

search_btn = st.sidebar.button("🔎 Find Destinations")

# -----------------------------
# FILTER FUNCTION
# -----------------------------
def get_recommendations():
    filtered = df[
        (df["Type"] == place_type) &
        (df["Best_Season"] == season) &
        (df["Budget"] == budget)
    ]

    if "Rating" in filtered.columns:
        filtered = filtered.sort_values(by="Rating", ascending=False)

    return filtered.head(5)

# -----------------------------
# DISPLAY FUNCTION
# -----------------------------
def show_place(row, rank):
    col1, col2 = st.columns([1, 2])

    with col1:
        if "Image_URL" in row and pd.notna(row["Image_URL"]):
            st.image(row["Image_URL"], use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300")

    with col2:
        place = row.get("Place", "Unknown")
        location = row.get("Location", "")

        st.markdown(f"## #{rank} {place}")

        st.write(f"📍 Location: {location}")
        st.write(f"🏷️ Type: {row.get('Type', 'N/A')}")
        st.write(f"🌤️ Best Season: {row.get('Best_Season', 'N/A')}")
        st.write(f"💰 Budget: {row.get('Budget', 'N/A')}")
        st.write(f"💵 Cost per Day: ₹{row.get('Cost_per_Day', 'N/A')}")
        st.write(f"🏨 Stay Type: {row.get('Stay_Type', 'N/A')}")
        st.write(f"🏨 Hotel / Resort: {row.get('Hotel_Name', 'N/A')}")
        st.write(f"⭐ Rating: {row.get('Rating', 'N/A')}")
        st.write(f"📝 {row.get('Description', '')}")

        # -----------------------------
        # GOOGLE MAPS LINK
        # -----------------------------
        maps_query = f"{place} {location}".replace(" ", "+")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

        # -----------------------------
        # HOTEL BOOKING LINK
        # -----------------------------
        booking_url = f"https://www.booking.com/searchresults.html?ss={maps_query}"

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.markdown(
                f'<a href="{maps_url}" target="_blank">'
                f'<button style="width:100%">📍 View Location</button></a>',
                unsafe_allow_html=True
            )

        with col_btn2:
            st.markdown(
                f'<a href="{booking_url}" target="_blank">'
                f'<button style="width:100%">🏨 Book Hotel</button></a>',
                unsafe_allow_html=True
            )

    st.markdown("---")

# -----------------------------
# MAIN UI
# -----------------------------
st.title("🌍 Tourist Recommendation System")

if search_btn:
    results = get_recommendations()

    if not results.empty:
        for i, (_, row) in enumerate(results.iterrows(), start=1):
            show_place(row, i)
    else:
        st.warning("No matching destinations found 😔")