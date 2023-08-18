import streamlit as st
import pickle
import requests
# import streamlit.components.v1 as components


training_data = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = training_data['title'].values

st.header("Movie Recommender System")


def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZTQxNjcxYmM2ZTc4MGM3MTY5ZmU2NTgzOTc4MGE0YiIsInN1YiI6IjY0ZGY0YWZkZDEwMGI2MTRiMGE1OTIzYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Bf2pVSqnhGw7mLdxEwFzmTy2QXFxiGXoCRtZQNLP7oE"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


def recommend(movie):
    index = training_data[training_data['title'] == movie].index[0]
    distance = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movies = []
    recommended_posters = []
    for i in distance[1:6]:
        movies_id = training_data.iloc[i[0]].id
        recommended_movies.append(training_data.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies_id))
    return recommended_movies, recommended_posters


# imageCarouselComponent = components.declare_component(
#     "image-carousel-component", path="frontend/public")


# imageUrls = [
#     fetch_poster(105),
#     fetch_poster(670),
#     fetch_poster(545611),
#     fetch_poster(496243),
#     fetch_poster(13),
#     fetch_poster(769),
#     fetch_poster(346),
#     fetch_poster(539),
#     fetch_poster(324857),
#     fetch_poster(120),
#     fetch_poster(5156),
#     fetch_poster(361743),
#     fetch_poster(807)

# ]


# imageCarouselComponent(imageUrls=imageUrls, height=200)
selected_movie = st.selectbox('Select movie from dropdown', movies_list)


if st.button('Show recommendation'):
    movie_name, movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])

    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])

    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])

    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])

    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
