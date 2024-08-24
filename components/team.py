import streamlit as st
from models import Team, Pick, session

def display_team():
    st.title("Team Page")
    
    # Fetch all teams
    teams = session.query(Team).order_by(Team.name).all()
    team_names = [team.name for team in teams]
    
    selected_team_name = st.selectbox("Select a Team", team_names, key="team_select")
    
    if selected_team_name:
        selected_team = session.query(Team).filter_by(name=selected_team_name).first()
        
        # Display the team's picks in two columns: 2024 and 2025
        st.subheader(f"Picks for {selected_team_name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 2024 Picks")
            picks_2024 = session.query(Pick).filter_by(team_id=selected_team.id, year=2024).order_by(Pick.round, Pick.pick_number).all()
            
            if picks_2024:
                for pick in picks_2024:
                    pick_info = f"**{pick.round}.{pick.pick_number}:** {pick.selection or 'No selection'}"
                    st.markdown(pick_info)
                    st.markdown("---")  # Adds a horizontal line between picks
            else:
                st.write("No picks for 2024.")

        with col2:
            st.markdown("### 2025 Picks")
            picks_2025 = session.query(Pick).filter_by(team_id=selected_team.id, year=2025).order_by(Pick.round, Pick.pick_number).all()
            
            if picks_2025:
                for pick in picks_2025:
                    pick_info = f"**{pick.round}.{pick.pick_number}:** {pick.selection or 'No selection'}"
                    st.markdown(pick_info)
                    st.markdown("---")  # Adds a horizontal line between picks
            else:
                st.write("No picks for 2025.")
