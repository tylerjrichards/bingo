import base64
import os
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NormConf Bingo!", page_icon="🎲")

# Default Bingo options
# Any option starting with http:// or https:// will automatically turn into an image
default_center_piece = "https://user-images.githubusercontent.com/16867691/206601724-97fd1fb8-7cda-4348-a5c5-cb3d1f48c910.png"
default_options = [
    "something something duckdb",
    "Mastodon",
    "Machine Learning Flashcards",
    "x in the browser",
    "chatGPT/GPT3",
    "someone pitches their newsletter",
    "ha timezones are so hard",
    "yet another hot take on Jupyter Notebooks",
    "Modern Data Stack",
    "someone says 'data is the new oil'",
    "data as a product",
    "data problems are actually people problems",
    "memes in place of slides",
]
options = "\n".join(default_options)


# Component Dev Mode
# Set this to True when running "npm run start"
# Set this to False after running "npm run build"
COMPONENT_DEV_MODE = False

if COMPONENT_DEV_MODE:
    bingo_component = components.declare_component(
        "bingo_component", url="http://localhost:3001"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")

    bingo_component = components.declare_component("bingo_component", path=build_dir)


def shuffle_card():
    seed = random.randint(0, 1000)
    st.experimental_set_query_params(seed=seed)
    st.session_state["seed"] = seed


params = st.experimental_get_query_params()

# Seed is used to make the bingo pieces shuffle the same way every time
if "s" not in params:
    st.session_state["seed"] = random.randint(0, 1000)
else:
    st.session_state["seed"] = params["s"][0]

# "v" represent the specific bingo piece values
if "v" not in params:
    bingo_options = "\n".join(default_options)
else:
    bingo_options = base64.b64decode(params["v"][0].encode("ascii")).decode("ascii")

# "c" represents the center piece
if "c" not in params:
    center_piece = default_center_piece
else:
    center_piece = base64.b64decode(params["c"][0].encode("ascii")).decode("ascii")

##################################################################################
## Start Output

st.title("NormConf Bingo!")

with st.expander("Settings"):
    with st.form(key="settings"):
        center_piece = st.text_input("Center Piece", value=center_piece)
        bingo_options = st.text_area(
            "Bingo Options", bingo_options, help="One line per bingo piece"
        )

        st.form_submit_button("Apply")

# Store params in url
st.experimental_set_query_params(
    s=st.session_state["seed"],
    v=base64.b64encode(bingo_options.encode("ascii")),
    c=base64.b64encode(center_piece.encode("ascii")),
)

bingo_options = bingo_options.splitlines()

# Use the seed to always shuffle the same way
random.Random(st.session_state["seed"]).shuffle(bingo_options)

# Use custom component to draw Bingo Board
# Use key to prevent component from redrawing
is_bingo = bingo_component(
    center_piece=center_piece, bingo_options=bingo_options, key="bingo_time"
)

# If the custom component returns true, then show Win Animation!
if is_bingo == True:
    st.balloons()

if st.button("Get a new card!"):
    shuffle_card()
st.caption(f"Streamilt v:{st.__version__}")
