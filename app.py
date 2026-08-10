import streamlit as st
import pickle
movies_list = pickle.load(open('movies_list.pickle', 'rb'))
movies_list = movies_list['title'].values


st.title('Movie Recommender System')
option = st.selectbox(
'How would youlike to be contacted?',
movies_list)
