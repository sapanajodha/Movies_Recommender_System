import pandas as pd
import streamlit as st
import pickle
import requests


# Fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ace57a76830f421a6b72e00e9207553f&language=en-US"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    }

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()

            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://placehold.co/500x750?text=No+Poster"

        except requests.exceptions.ConnectionError:
            if attempt == 2:  # Last attempt
                return "https://placehold.co/500x750?text=No+Poster"
            continue  # Retry

        except requests.exceptions.Timeout:
            if attempt == 2:
                return "https://placehold.co/500x750?text=Timeout"
            continue

        except requests.exceptions.RequestException as e:
            return "https://placehold.co/500x750?text=Error"

    return "https://placehold.co/500x750?text=No+Poster"


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # Show spinner while fetching each poster
        with st.spinner(f"Fetching poster..."):
            recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    # ✅ Use use_container_width=True so all posters display properly
    with col1:
        st.text(names[0])
        st.image(posters[0], use_container_width=True)

    with col2:
        st.text(names[1])
        st.image(posters[1], use_container_width=True)

    with col3:
        st.text(names[2])
        st.image(posters[2], use_container_width=True)

    with col4:
        st.text(names[3])
        st.image(posters[3], use_container_width=True)

    with col5:
        st.text(names[4])
        st.image(posters[4], use_container_width=True)