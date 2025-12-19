import streamlit as st
import pickle
import requests

# For App's page config

st.set_page_config(
    page_title="Game Recommendation System",
    page_icon="🎮",
    layout="wide"
)

# For App appearances & UI/UX

st.markdown("""
<style>
.game-card {
    background-color: #1f2937;
    border-radius: 16px;
    padding: 10px;
    margin-bottom: 28px;   /* 👈 THIS IS THE KEY */
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    text-align: center;
}

.game-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
}

.game-img {
    width: 100%;
    height: 170px;
    object-fit: cover;
    border-radius: 12px;
}

.game-title {
    font-weight: 600;
    margin-top: 10px;
    font-size: 14px;
    color: #e5e7eb;
}

.game-score {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# For Header and description

st.title("🎮 Game Recommendation System")
st.caption("AI-based recommendations using content-based, collabrative filtering and hybrid engine.")

st.markdown("---")


games = pickle.load(open("games_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
games_list = games['Name'].values 

# For a game selector sidebar

st.subheader("Game Recommendation Engine Using Python - Machine Learning & AI with large Game Dataset")
selecevalue = st.selectbox(
  "Select Games from the dropdown",
  games['Name'].values
  )

# For fetching Game poster and background while connecting with a game name using API from RAWG

def fetch_background(game_name):
    url = f"https://api.rawg.io/api/games?key=ef0df543c45e45189b7abaa3fc48cfd5&search={game_name}"
    data = requests.get(url).json()

    if data["results"]:
        return data["results"][0]["background_image"]
    return None

def recommend(game):
    index = games[games['Name'] == game].index[0]

    distance = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommend_game = []
    recommend_background = []
    recommend_score = []

    for i in distance[1:11]:
        game_name = games.iloc[i[0]]['Name']
        recommend_game.append(game_name)
        recommend_background.append(fetch_background(game_name))
        recommend_score.append(i[1])

    return recommend_game, recommend_background, recommend_score

# For Click Here button to see the result game recommendations

if st.button("Click Here To Show Game Recommendations"):

  game_names, game_backgrounds, similarity_scores = recommend(selecevalue)
  st.markdown("---")

  st.subheader("🎯 Recommended Games")
  st.caption(f"Because you liked {selecevalue}")

  cols = st.columns(5)
  
# For appearing game cards with 5 game cards per row

  for idx in range(len(game_names)):
    with cols[idx % 5]:

        image_url = game_backgrounds[idx] or "https://via.placeholder.com/300x170?text=No+Image"

        st.markdown(f"""
        <div class="game-card">
          <img src="{image_url}" class="game-img"/>
          <div class="game-title">{game_names[idx]}</div>
          <div class="game-score">Similarity: {similarity_scores[idx]}</div>
        </div>
        """, unsafe_allow_html=True)
                    
st.markdown("---")
st.info("Recommendations are based on similarity & genre of game features.")

st.text("Email Me If Interested - @nyeinsaynaing1432@gmail.com")

      
          
    