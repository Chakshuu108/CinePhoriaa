
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=898cf6103011e26636cdbcfa0b4f0469&language=en-US'.format(movie_id))
    data = response.json()
    # poster_path error aa rha h becoz we are considering the index 0 1 ... which may not be available but we need movie_id
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']
    #we dont have complete path : -> tmdb image path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        # poster_path error aa rha h becoz we are considering the index 0 1 ... which may not be available but we need movie_id
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api : login in tmdb:
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Cinephoria')

selected_movie_name = st.selectbox(
    'Search for your favourite movie recommendations',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Use st.columns instead of beta_columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
