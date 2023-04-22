import json
import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('b1.jpg')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_khzniaya.json")
# lottie_width = 150
# lottie_height = 150




def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

movies = pickle.load(open('mov.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values

st.markdown("""
    <style>
    .title {
        font-family: 'Olarwe', sans-serif;
        color: #e60000;
        font-size: 3em;
        text-shadow: 2px 2px 4px #000000;
    }
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        color: #ffffff;
        font-size: 1.0em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Your Movie Matchmaker!</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Film recommendations made simple!</h2>", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "",
    movie_list
)





if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# st_lottie(lottie_hello, speed=1, width=90 ,  height=90,  key="hello")



st.write("Created by Yash Talati")