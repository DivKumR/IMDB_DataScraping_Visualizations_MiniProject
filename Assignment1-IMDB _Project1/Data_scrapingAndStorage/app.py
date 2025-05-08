## Refrence documents 
# https://docs.streamlit.io/get-started
# https://docs.streamlit.io/develop/concepts/connections/secrets-management
# https://docs.streamlit.io/develop/concepts/design/custom-classes


import streamlit as st # type: ignore
import pandas as pd # type: ignore
import mysql.connector # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
from class_app import Graph # type: ignore

# App Title
st.title("Top IMDb Movies Collection")

# Database Connection
try:
    # conn = mysql.connector.connect(
    #     # host=st.secrets["connections.mysql"]["host"],
    #     # port=st.secrets["connections.mysql"]["port"],
    #     # database=st.secrets["connections.mysql"]["database"],
    #     # user=st.secrets["connections.mysql"]["username"],
    #     # password=st.secrets["connections.mysql"]["password"]
    # )
    conn = mysql.connector.connect(
        host="localhost",
        user="USERNAME",  # Replace with your MySQL username
        password="PASSWORD", # Replace with your MySQL PAssword
        database="imdb_movies"
    )
    cursor = conn.cursor()
    
    # Query to Select data
    query = "SELECT * FROM clean_data_imdb_movies;"  # Connect to table clean_data_imdb_movies
    cursor.execute(query)

    stmovies_data = cursor.fetchall()  # Fetch all data
    columns = [col[0] for col in cursor.description]  # Get column names
    
    # Convert to DataFrame
    stmovies_df = pd.DataFrame(stmovies_data, columns=columns)

except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Initialize session state for toggling database visibility
if "show_database" not in st.session_state:
    st.session_state.show_database = False  # Initial state is "hidden"

# Define a toggle button
if st.button("Click to view the entire dataset"):
    st.session_state.show_database = not st.session_state.show_database # Toggle the visibility state

# Check the state and display or hide the database accordingly
if st.session_state.show_database:
    st.subheader("Data from Database")
    # Prepare the DataFrame for display
    df_todisplay = stmovies_df[["title", "rating", "genre", "votes", "duration"]].copy()
    df_todisplay.rename(
        columns={"title": "Title", "rating": "IMDb Rating", "genre": "Genre", "votes": "Votes", "duration": "Duration"},
        inplace=True
    )
    st.dataframe(df_todisplay) # Display the DataFrame

# ==============================================================================

# # Tasks: Interactive Filtering Functionality
# # Allow users to filter the dataset based on the following criteria:
## 1.Duration (Hrs): Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs).
## 2.Ratings: Filter movies based on IMDb ratings (e.g., > 8.0).
## 3.Voting Counts: Filter based on the number of votes received (e.g., > 10,000 votes).
## 4.Genre: Filter movies within specific genres (e.g., Action, Drama).
## 5.Display the filtered results in a dynamic DataFrame within the Streamlit app.
## 6.Combine filtering options so users can apply multiple filters simultaneously for customized insights.

# Sidebar Filters
st.sidebar.header("Filters")

## 1.Duration (Hrs): Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs).
st.sidebar.subheader("Duration (Hrs):")
duration_filter = st.sidebar.radio(
    "Select Duration Range:",
    options=("All", "< 2 hrs", "2–3 hrs", "> 3 hrs")
)

## 2.Ratings: Filter movies based on IMDb ratings (e.g., > 8.0).
st.sidebar.subheader("Filter by IMDb Rating:")
rating_filter = st.sidebar.slider(
    "Select IMDb Rating Range:",
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 8.0),  # Default range selection
    key="rating_slider"
)

## 3.Voting Counts: Filter based on the number of votes received (e.g., > 10,000 votes).
st.sidebar.subheader("Voting Counts:")
votes_filter = st.sidebar.slider(
    "Minimum Votes:",
    min_value=0,
    max_value=300000,
    value=(0, 300000),
    key="votes_slider"
)
# formatted_votes = f"{votes_filter // 1000}k"
# st.sidebar.write(f"Selected Votes: {formatted_votes}")

## 4.Genre: Filter movies within specific genres (e.g., Action, Drama).
st.sidebar.subheader("Genre:")
genre_filter = st.sidebar.multiselect(
    "Select Genre(s):",
    options=stmovies_df["genre"].unique(),
    default=stmovies_df["genre"].unique(),
    key="genre_select"
)

## 5.Display the filtered results in a dynamic DataFrame within the Streamlit app.
## 6.Combine filtering options so users can apply multiple filters simultaneously for customized insights.

# Input box for the number of top-rated movies
st.sidebar.subheader("Top Rated Movies")
toprating_filter = st.sidebar.number_input(
    "Enter the number to view top rated movies", 
    min_value=1, 
    max_value=1000,
    value=len(stmovies_df),
    key="top_rating"
)

# Input box for the number of top-voted movies
st.sidebar.subheader("Top Voted Movies")
topvoted_filter = st.sidebar.number_input(
    "Enter the number to view top voted movies", 
    min_value=1, 
    max_value=1000,
    value=len(stmovies_df),
    key="top_voting"
)

# Data Preprocessing
# Convert "Duration_in_HH_MM" column to float
stmovies_df["Duration_in_HH_MM"] = stmovies_df["Duration_in_HH_MM"].apply(
    lambda duration: round(int(duration.split(":")[0]) + int(duration.split(":")[1]) / 60, 2)
    if ":" in duration else 0
)

# Ensuring "rating" and "votes" columns are numeric
columns_to_convert = ["rating", "votes"]
stmovies_df[columns_to_convert] = stmovies_df[columns_to_convert].apply(pd.to_numeric, errors="coerce")
stmovies_df.dropna(subset=["rating", "votes"], inplace=True)  # Drop rows with invalid data

# Apply Filters
filtered_df = stmovies_df.copy()

# Filter by Rating Range
filtered_df = filtered_df[
    (filtered_df["rating"] >= rating_filter[0]) & (filtered_df["rating"] <= rating_filter[1])
]
filtered_df = filtered_df.nlargest(toprating_filter, 'rating')

# Filter by Duration
if duration_filter == "< 2 hrs":
    filtered_df = filtered_df[filtered_df["Duration_in_HH_MM"] < 2]
elif duration_filter == "2–3 hrs":
    filtered_df = filtered_df[(filtered_df["Duration_in_HH_MM"] >= 2) & (filtered_df["Duration_in_HH_MM"] <= 3)]
elif duration_filter == "> 3 hrs":
    filtered_df = filtered_df[filtered_df["Duration_in_HH_MM"] > 3]

# Filter by Votes
filtered_df = filtered_df[
    (filtered_df["votes"] >= votes_filter[0]) & (filtered_df["votes"] <= votes_filter[1])
]
filtered_df = filtered_df.nlargest(topvoted_filter, 'votes')
# filtered_df = filtered_df[filtered_df["votes"] >= votes_filter]

# Filter by Genre
filtered_df = filtered_df[filtered_df["genre"].isin(genre_filter)]

# Customize Columns and Display Filtered Results
filtered_df = filtered_df[["title", "rating", "genre", "votes", "duration"]].copy()
filtered_df.rename(
    columns={"title": "Title", "rating": "IMDb Rating", "genre": "Genre", "votes": "Votes", "duration": "Duration"},
    inplace=True
)

st.subheader(f"Filtered Movie Results (Total Rows: {len(filtered_df)})")
st.dataframe(filtered_df)

# Call the method to show the graph
graph = Graph(filtered_df)
graph.show_graph()

# Close the database connection
conn.close()