import streamlit as st
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd
import requests
import os
from PIL import Image




##bacround style 
# page_bg_img = """
# <style>
# [data-testid="stAppViewBlockContainer"] {
# background-image: linear-gradient(to right bottom, #000000, #4c2720, #82591d, #8a9e23, #12eb7a);
# background-size: cover;
# }
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)




def display_logo(league, team):
    folder_path = f"teams logo/{league}"  # Replace with the actual path to your folders

    # Check if the league folder exists
    if os.path.exists(folder_path):
        team_logo_path = os.path.join(folder_path, f"{team}.png")

    else:
        team_logo_path=None
    return team_logo_path

# Load data
epl = pd.read_csv("all_shots_epl_2022.csv")
laliga = pd.read_csv("all_shots_laliga_2022.csv")
bundesliga = pd.read_csv("all_shots_bundesliga_2022.csv")
ligue1 = pd.read_csv("all_shots_ligue_1_2022.csv")
seriea = pd.read_csv("all_shots_serie_a_2022.csv")

# Team dictionaries
epl_teams = {"h_teams": sorted(set(epl['h_team'])), "a_teams": sorted(set(epl['a_team']))}
laliga_teams = {"h_teams": sorted(set(laliga['h_team'])), "a_teams": sorted(set(laliga['a_team']))}
bundesliga_teams = {"h_teams": sorted(set(bundesliga['h_team'])), "a_teams": sorted(set(bundesliga['a_team']))}
seriea_teams = {"h_teams": sorted(set(seriea['h_team'])), "a_teams": sorted(set(seriea['a_team']))}
ligue1_teams = {"h_teams": sorted(set(ligue1['h_team'])), "a_teams": sorted(set(ligue1['a_team']))}

# Streamlit app
st.set_page_config(layout="wide")
st.title("Football Match Visualization ⚽")

# Sidebar with league selection
selected_league = st.sidebar.selectbox("Select a League", ["epl", "laliga", "bundesliga", "seriea", "ligue1"])

logo_league=None
# Display teams based on the selected league
if selected_league == 'epl':
    teams = epl_teams
    df = epl
    logo_league='epl'
elif selected_league == 'laliga':
    teams = laliga_teams
    df = laliga
    logo_league='laliga'
elif selected_league == 'bundesliga':
    teams = bundesliga_teams
    df = bundesliga
    logo_league='bundesliga'
elif selected_league == 'seriea':
    teams = seriea_teams
    df = seriea
    logo_league='seriea'
elif selected_league == 'ligue1':
    teams = ligue1_teams
    df = ligue1
    logo_league='ligue1'
else:
    st.error("Invalid league selected.")
    st.stop()
    

# Sidebar with team selection
h_team = st.sidebar.selectbox("Select Home Team", teams['h_teams'])
available_away_teams = [team for team in teams['a_teams'] if team != h_team]
a_team = st.sidebar.selectbox("Select Away Team", available_away_teams)

h_team_logo_path = display_logo(logo_league,h_team)
a_team_logo_path = display_logo(logo_league,a_team)

try:
    if not os.path.exists(h_team_logo_path):
        # Team logos
        print(f"Error: Image file not found at {h_team_logo_path}")
except Exception as e:
    print(f"Error: Unable to open image file - {e}")
    
try:
    if not os.path.exists(a_team_logo_path):
        print(f"Error: Image file not found at {a_team_logo_path}")
except Exception as e:
    print(f"Error: Unable to open image file - {e}")
    # Handle the error or log it as needed



# Sidebar with result type selection
shot_result = df['result'].unique()
result_type = st.sidebar.selectbox("Select Result Type", ["All"] + list(shot_result))

# Filter data based on selected teams and result type
theMatch = df[(df['h_team'] == h_team) & (df['a_team'] == a_team)]
if result_type != "All":
    theMatch = theMatch[theMatch['result'] == result_type]

# Display match date
match_date = theMatch['date'].iloc[0] if not theMatch.empty else "No match date available"
st.subheader(f"Match Date:{match_date}")

# Create a single Pitch instance for the combined pitch
pitch_combined = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc',
                      pitch_length=[-120, 120], pitch_width=[-80, 80])

# Create a figure with a single subplot
fig, ax = plt.subplots(figsize=(7, 7))

# Plot the combined pitch
pitch_combined.draw(ax=ax)

# Display team names and goals only if theMatch is not empty
if not theMatch.empty:
    for index, row in theMatch.iterrows():
        if row['h_team'] == h_team and row['a_team'] == a_team:
            if row['h_a'] == 'h':
                if row['result'] == 'Goal':
                    ax.scatter(row['X'], row['Y'], c="white", alpha=0.5, marker="*", s=190)
                else:
                    ax.scatter(row['X'], row['Y'], c="white", alpha=0.5)
            elif row['h_a'] == 'a':
                if row['result'] == 'Goal':
                    ax.scatter(row['X'], row['Y'], c="#F1A53E", alpha=0.5, marker="*", s=190)
                else:
                    ax.scatter(row['X'], row['Y'], c="#F1A53E", alpha=0.5)


    
    # Display team names and goals
    ax.text(102, 82, f"{a_team}", color="#F1A53E", ha="right", va="center", fontsize=10, fontweight='bold')
    ax.text(99, 67, f"{theMatch['a_goals'].iloc[0]}", color="#F1A53E", ha="right", va="center", fontsize=70, fontweight='bold', alpha=0.3)

    ax.text(18, 82, f"{h_team}", color="white", ha="left", va="center", fontsize=10, fontweight='bold')
    ax.text(20, 67, f"{theMatch['h_goals'].iloc[0]}", color="white", ha="left", va="center", fontsize=70, fontweight='bold', alpha=0.3)

# Optionally, invert both the x and y axes if needed for the entire plot
ax.invert_yaxis()
# Tight layout to make the plot smaller
plt.tight_layout()

# ... (any additional information or controls)
col1, col2 = st.columns([2, 2])

# Display "Hello" text in the first column
with col1:
    if not theMatch.empty:

        # Resize images
        h_team_image = Image.open(h_team_logo_path).resize((100, 100))
        a_team_image = Image.open(a_team_logo_path).resize((100, 100))

        # Create two columns
        col1_1, col1_2,col1_3 = st.columns(3)

        # Place each image in a separate column
        col1_1.image(h_team_image, caption=h_team, use_column_width=False)
        col1_2.title(f"{theMatch['h_goals'].iloc[0]} - {theMatch['a_goals'].iloc[0]}")
        col1_3.image(a_team_image, caption=a_team, use_column_width=False)

        
# Display elements in the second column (adjust as needed)
with col2:
    st.pyplot(fig, clear_figure=True)  # Use clear_figure=True to avoid duplicate plots
