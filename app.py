import pickle

import requests
import streamlit as st

movies = pickle.load(open('movies_list.pickle', 'rb'))

data = pickle.load(open('top_neighbors.pkl', 'rb'))
new_df = data['new_df']
neighbors = data['neighbors']
titles = new_df['title'].values


def get_year(title):
    match = movies[movies['title'] == title]
    return match['year'].iloc[0] if len(match) else None


@st.cache_data(show_spinner=False)
def fetch_poster(title, year):
    candidates = [f"{title} ({year} film)", title] if year else [title]
    for name in candidates:
        try:
            r = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(name)}",
                headers={'User-Agent': 'MovieRecommender/1.0'},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                img = data.get('thumbnail', {}).get('source') or data.get('originalimage', {}).get('source')
                if img:
                    return img.split('?')[0]
        except Exception:
            continue
    return None


def recommend(movie):
    idx = new_df[new_df['title'] == movie].index[0]
    return [new_df.iloc[i]['title'] for i in neighbors[idx][1:]]


st.title('Movie Recommender System')
option = st.selectbox('Select a movie', titles)

poster = fetch_poster(option, get_year(option))
if poster:
    st.image(poster, caption=option, width=250)
else:
    st.write('No poster found for this movie.')

if st.button('Recommend Similar Movies'):
    recs = recommend(option)
    st.subheader('You may also like these movies:')
    cols = st.columns(5)
    for col, rec in zip(cols, recs):
        with col:
            rec_poster = fetch_poster(rec, get_year(rec))
            if rec_poster:
                st.image(rec_poster, width=130)
            st.write(rec)