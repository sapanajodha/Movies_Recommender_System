Developed a Movie Recommender System using Python and Streamlit that recommends similar movies based on user selection. 
The system uses machine learning similarity techniques and integrates the TMDB API to fetch real-time movie posters and details.

Built an end-to-end content-based Movie Recommender System that suggests 5 similar movies based on a user-selected title. The system uses NLP-driven feature engineering on movie metadata (genres, cast, crew, keywords, overview) to compute cosine similarity between films, and delivers a clean interactive UI via Streamlit with real-time poster fetching from the TMDB API.

# Module Breakdown
1) Data Preprocessing

Loaded and merged TMDB movie and credits datasets using Pandas. Extracted relevant fields — genres, keywords, cast, crew (director), and overview — and parsed JSON-encoded columns into flat text lists for downstream NLP.

2) Feature Engineering

Combined all metadata fields into a single "tags" column per movie. Applied stemming (PorterStemmer) and lowercasing to normalize text. Converted tags into a bag-of-words vector matrix using CountVectorizer (top 5000 features).

3) Similarity Engine

Computed pairwise cosine similarity across all movie vectors using sklearn's cosine_similarity. Serialized the resulting similarity matrix and movie metadata DataFrame as pickle files (similarity.pkl, movie_dict.pkl) for fast loading at runtime.

4) Recommendation Logic

The recommend() function accepts a movie title, fetches its similarity scores from the matrix, sorts by descending score, and returns the top 5 matches along with their TMDB movie IDs for poster retrieval.

5) TMDB API Integration

Implemented fetch_poster() to call the TMDB REST API for each recommended movie. Includes a 3-attempt retry loop for ConnectionError and Timeout exceptions, with graceful fallback to placeholder images on failure.

6) Streamlit UI

Designed the frontend with st.selectbox for movie selection and st.columns(5) for displaying results in a grid. Used @st.cache_data for pickle loading to eliminate redundant disk reads on re-renders, improving app responsiveness.

# Key Highlights

1]Processed 5,000+ movies from the TMDB dataset with multi-field metadata fusion.
2]Achieved sub-second recommendation latency using precomputed cosine similarity matrix.
3]Integrated live TMDB API with fault-tolerant retry logic and fallback handling.
4]Deployed as an interactive web app using Streamlit with optimized state caching.
5]Modular, production-ready code structure with constants, typed functions, and clean separation of concerns.

# Tech Stack

Python 3.x
Pandas
NLTK (PorterStemmer)
Streamlit
Requests
TMDB API
Pickle
CountVectorizer
Cosine Similarity
