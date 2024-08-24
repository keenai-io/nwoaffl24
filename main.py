import streamlit as st
from components.traderoom import display_trade_room
from components.draftboard import display_draftboard
from components.commissioner import display_commissioner
from components.team import display_team

st.set_page_config(page_title="NWOAFFL 2024", page_icon=":football:", layout="wide")

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 99%;  /* Adjust this value to control the maximum width */
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Top navigation bar using st.tabs
st.markdown("<h5 style='text-align: center;'>NWOAFFL 2024</h5>", unsafe_allow_html=True)

# Define passwords for protected tabs
TRADE_ROOM_PASSWORD = "t"
COMMISSIONER_PASSWORD = "c"

# Initialize session state for password checks
if 'trade_room_access' not in st.session_state:
    st.session_state.trade_room_access = False

if 'commissioner_access' not in st.session_state:
    st.session_state.commissioner_access = False

tab1, tab2, tab3 = st.tabs(["Draftboard", "Team", "Admin"])

with tab1:
    display_draftboard()

with tab2:
    display_team()

with tab3:
    if not st.session_state.commissioner_access:
        st.subheader("Enter Password for Commissioner")
        commissioner_password = st.text_input("Password for Commissioner:", type="password", key="commissioner_password")
        if st.button("Submit", key="commish"):
            if commissioner_password == COMMISSIONER_PASSWORD:
                st.session_state.commissioner_access = True
                st.success("Access granted to Commissioner!")
            else:
                st.error("Incorrect password. Please try again.")
    else:
        st.title("Commissioner")
        display_commissioner()