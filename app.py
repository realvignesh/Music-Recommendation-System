import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


# ======================================================================================================================

def get_audio_preview_url(song, artist):
    # Search for the song
    query = f"track:{song} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)

    # Check if results were found
    if results['tracks']['items']:
        # Retrieve audio preview URL
        track = results['tracks']['items'][0]
        audio_preview_url = track['preview_url']
        return audio_preview_url
    else:
        return None


# ======================================================================================================================

def recommend(song, recommendation_count):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_audio_prev = []
    for i in distances[1:recommendation_count + 1]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_audio_prev.append(get_audio_preview_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters, recommended_music_audio_prev


# ======================================================================================================================

def display_recommendations(recommended_songs):
    got_recommendations = len(recommended_songs)
    num_columns = 5
    num_rows = (got_recommendations + num_columns - 1) // num_columns  # Calculate number of rows needed

    # Loop through recommendations and display in columns
    for i in range(num_rows):
        with st.container():  # Create a container for each row
            col1, col2, col3, col4, col5 = st.columns(5)
            for j in range(num_columns):
                index = i * num_columns + j
                if index < got_recommendations:
                    if index in [0, 5, 10, 15]:
                        with col1:
                            st.subheader(recommended_music_names[index])
                            st.image(recommended_music_posters[index])
                            if recommended_music_ap[index]:
                                st.audio(recommended_music_ap[index], format='audio/mp3')
                            else:
                                st.write("Audio preview not available.")
                    if index in [1, 6, 11, 16]:
                        with col2:
                            st.subheader(recommended_music_names[index])
                            st.image(recommended_music_posters[index])
                            if recommended_music_ap[index]:
                                st.audio(recommended_music_ap[index], format='audio/mp3')
                            else:
                                st.write("Audio preview not available.")
                    if index in [2, 7, 12, 17]:
                        with col3:
                            st.subheader(recommended_music_names[index])
                            st.image(recommended_music_posters[index])
                            if recommended_music_ap[index]:
                                st.audio(recommended_music_ap[index], format='audio/mp3')
                            else:
                                st.write("Audio preview not available.")
                    if index in [3, 8, 13, 18]:
                        with col4:
                            st.subheader(recommended_music_names[index])
                            st.image(recommended_music_posters[index])
                            if recommended_music_ap[index]:
                                st.audio(recommended_music_ap[index], format='audio/mp3')
                            else:
                                st.write("Audio preview not available.")
                    if index in [4, 9, 14, 19]:
                        with col5:
                            st.subheader(recommended_music_names[index])
                            st.image(recommended_music_posters[index])
                            if recommended_music_ap[index]:
                                st.audio(recommended_music_ap[index], format='audio/mp3')
                            else:
                                st.write("Audio preview not available.")


# ======================================================================================================================

# 1. SPOTIFY CLIENT INITIALIZATION.
CLIENT_ID = "5efb835d0ab8478ab272950784e13bd9"
CLIENT_SECRET = "0597ed049e9445bf91992866ee01dfcf"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ======================================================================================================================

# 2. PAGE CONFIGURATION.
st.set_page_config(
    page_title="Music Recommendation System",
    page_icon=":musical_note:",  # You can customize the favicon
    layout="wide",  # Adjust layout as needed
    initial_sidebar_state="collapsed"  # Adjust sidebar state as needed
)

st.header('Music in the soul can be heard by the universe.')

# ======================================================================================================================

# 3. CUSTOMIZING BACKGROUND IMAGE.
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.pexels.com/photos/6405691/pexels-photo-6405691.jpeg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# ======================================================================================================================

# 4. SIDEBAR FOR SELECTING NUMBER OF RECOMMENDATIONS.
st.sidebar.title("Options\n")
st.sidebar.subheader("Number of Recommendations")
num_recommendations = st.sidebar.slider("", min_value=5, max_value=20, value=10)
st.sidebar.divider()

# ======================================================================================================================

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# ======================================================================================================================

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_music_ap = recommend(selected_music,
                                                                                         num_recommendations)

    # Display recommendations
    display_recommendations(recommended_music_names)

    add_music = None

    with open('saved_recommendations.txt', 'r') as file:
        saved = [line.strip() for line in file]
        print(saved)
        print(recommended_music_names)
        add_music = recommended_music_names + saved
    file.close()

    with open('saved_recommendations.txt', 'w') as f:
        for item in add_music:
            f.write(str(item) + '\n')
    f.close()
    st.success("Recommended songs saved successfully!")

# ======================================================================================================================

st.sidebar.write("\n\n")
if st.sidebar.button("Show Recommendation History"):
    st.subheader('Recommendation History')
    with open('saved_recommendations.txt', 'r') as f:
        # saved = json.load(f)
        saved = [line.strip() for line in f]
    f.close()
    if saved:
        for i in range(len(saved)):
            st.write(
                f"<span style='font-size:24px; font-weight:bold; color:white'>{saved[i]}</span>.",
                unsafe_allow_html=True)
    else:
        st.sidebar.subheader("No history yet.")
    print(saved)
