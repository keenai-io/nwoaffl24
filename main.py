import streamlit as st
from components.traderoom import display_trade_room

# Set up the page configuration for a wide layout
st.set_page_config(page_title="NWOAFFL 2024", page_icon=":football:", layout="wide")

# Custom CSS to make the app wider
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

tab1, tab2, tab3 = st.tabs(["Draftboard", "Trade Room", "Commissioner"])

with tab1:
    # st.title("Draftboard")
    from components.draftboard import display_draftboard
    display_draftboard()

with tab2:
    st.title("Trade Room")
    display_trade_room()

with tab3:
    st.title("Commissioner")
    from components.commissioner import display_commissioner
    display_commissioner()
