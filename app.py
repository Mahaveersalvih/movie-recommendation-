import streamlit as st
import pickle
import pandas as pd
import requests
import difflib
import random

# ==========================================
# 🔑 API KEY CONFIGURATION
# ==========================================
TMDB_API_KEY = 'a7205ed094d651ba8e26f20110eb0805' 
# ==========================================

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Load the files
        movies_dict = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        
        # Ensure movies data is a DataFrame
        if isinstance(movies_dict, dict):
            movies = pd.DataFrame(movies_dict)
        else:
            movies = movies_dict
            
        return movies, similarity
    except FileNotFoundError:
        return None, None

movies_data, similarity = load_data()

# Check if data loaded correctly
if movies_data is None:
    st.error("Error: 'movies.pkl' or 'similarity.pkl' not found. Please make sure these files are in the same folder.")
    st.stop()

# --- HELPER FUNCTIONS ---

def fetch_poster(movie_id):
    """Fetches the movie poster URL from TMDB API"""
    try:
        # Search for the movie by title
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_id}"
        response = requests.get(url)
        data = response.json()
        
        # Check if results exist
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        pass
    
    # Return a fallback image if no poster found
    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend_by_movie(movie_name):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return [], []

    close_match = find_close_match[0]
    
    try:
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    except IndexError:
        return [], []

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []

    # Get top 5 (excluding the movie itself)
    for i in sorted_similar_movies[1:6]:
        index = i[0]
        title = movies_data.iloc[index].title
        
        recommended_movie_names.append(title)
        recommended_movie_posters.append(fetch_poster(title))
        
    return recommended_movie_names, recommended_movie_posters

def recommend_by_mood(mood):
    mood_to_genres = {
        'Happy': ['Comedy', 'Family', 'Animation', 'Adventure'],
        'Sad': ['Drama', 'Tragedy', 'Romance'],
        'Action-packed': ['Action', 'Adventure', 'Science Fiction', 'Thriller'],
        'Romantic': ['Romance', 'Drama'],
        'Thrilling': ['Thriller', 'Action', 'Crime', 'Mystery'],
        'Dark': ['Thriller', 'Crime', 'Mystery', 'Horror'],
    }
    
    if mood not in mood_to_genres:
        return [], []

    target_genres = mood_to_genres[mood]
    mood_candidates = []

    for index, row in movies_data.iterrows():
        # Handle cases where genres might be NaN or not string
        if isinstance(row['genres'], str):
            movie_genres = row['genres'].split(' ') 
            if any(genre in movie_genres for genre in target_genres):
                mood_candidates.append(index)
    
    # Shuffle and pick top 5
    if mood_candidates:
        random.shuffle(mood_candidates)
        selected_indices = mood_candidates[:5]
        
        names = []
        posters = []
        for idx in selected_indices:
            title = movies_data.loc[idx, 'title']
            names.append(title)
            posters.append(fetch_poster(title))
        return names, posters
    
    return [], []

# --- APP LAYOUT ---

st.title('🎬 Movie Recommender System')

# Create Tabs
tab1, tab2 = st.tabs(["🔍 Search by Movie", "😊 Search by Mood"])

# TAB 1: Content Based
with tab1:
    st.header("Find similar movies")
    selected_movie = st.selectbox(
        "Type or select a movie you like:",
        movies_data['title'].values
    )

    if st.button('Show Recommendations', key='btn_movie'):
        with st.spinner('Fetching recommendations...'):
            names, posters = recommend_by_movie(selected_movie)
        
        if names:
            cols = st.columns(5)
            for i in range(len(names)):
                with cols[i]:
                    st.image(posters[i])
                    st.text(names[i])
        else:
            st.error("No recommendations found.")

# TAB 2: Mood Based
with tab2:
    st.header("What is your mood today?")
    mood_list = ['Happy', 'Sad', 'Action-packed', 'Romantic', 'Thrilling', 'Dark']
    selected_mood = st.selectbox("Select a Mood:", mood_list)

    if st.button('Suggest Movies for Mood', key='btn_mood'):
        with st.spinner('Finding movies matching your mood...'):
            names, posters = recommend_by_mood(selected_mood)
        
        if names:
            cols = st.columns(5)
            for i in range(len(names)): 
                with cols[i]:
                    st.image(posters[i])
                    st.text(names[i])
        else:
            st.warning("No movies found for this mood.")
