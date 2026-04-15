import streamlit as st
import sqlite3
import math

conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skill TEXT,
    village TEXT,
    lat REAL,
    lon REAL
)
''')
conn.commit()

def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

st.title("🌾 Farmer Service Platform")

menu = st.sidebar.selectbox("Menu", ["Add Worker", "Find Worker"])

if menu == "Add Worker":
    st.header("Add Worker")

    name = st.text_input("Name")
    skill = st.selectbox("Skill", ["ploughing", "harvesting", "spraying", "repair"])
    village = st.text_input("Village")
    lat = st.text_input("Latitude")
    lon = st.text_input("Longitude")

    if st.button("Add Worker"):
        if name and lat and lon:
            cur.execute("INSERT INTO workers (name, skill, village, lat, lon) VALUES (?, ?, ?, ?, ?)",
                        (name, skill, village, float(lat), float(lon)))
            conn.commit()
            st.success("Worker Added Successfully!")
        else:
            st.error("Fill all fields")

elif menu == "Find Worker":
    st.header("Find Worker")

    skill = st.selectbox("Skill", ["ploughing", "harvesting", "spraying", "repair"])
    lat = st.text_input("Your Latitude")
    lon = st.text_input("Your Longitude")

    if st.button("Search"):
        if lat and lon:
            cur.execute("SELECT name, skill, village, lat, lon FROM workers WHERE skill=?", (skill,))
            data = cur.fetchall()

            results = []

            for w in data:
                dist = calculate_distance(float(lat), float(lon), w[3], w[4])
                if dist < 50:
                    results.append(w)

            if results:
                for w in results:
                    st.write(f"Name: {w[0]}")
                    st.write(f"Village: {w[2]}")
                    st.write("---")
            else:
                st.warning("No workers found")
        else:
            st.error("Enter location")
