import streamlit as st
from models import Team, Pick, session

def display_trade_room():
    # Step 1: Select two teams
    st.subheader("Select Teams for the Trade")
    
    # Fetch all teams and order by name (alphabetical order)
    teams = session.query(Team).order_by(Team.name).all()
    team_names = [team.name for team in teams]

    col1, col2 = st.columns(2)
    with col1:
        team1_name = st.selectbox("Select Team 1", team_names)
    with col2:
        team2_name = st.selectbox("Select Team 2", team_names)

    if team1_name and team2_name:
        if team1_name == team2_name:
            st.error("Please select two different teams.")
            return

        team1 = session.query(Team).filter_by(name=team1_name).first()
        team2 = session.query(Team).filter_by(name=team2_name).first()

        # Step 2: Select picks to trade
        st.subheader("Select Picks to Swap")

        team1_picks = session.query(Pick).filter_by(current_owner_id=team1.id).order_by(Pick.year, Pick.round).all()
        team2_picks = session.query(Pick).filter_by(current_owner_id=team2.id).order_by(Pick.year, Pick.round).all()

        pick_options_team1 = {f"{pick.year}.{pick.round}.{pick.pick_number}": pick for pick in team1_picks}
        pick_options_team2 = {f"{pick.year}.{pick.round}.{pick.pick_number}": pick for pick in team2_picks}

        col3, col4 = st.columns(2)
        with col3:
            team1_pick_selection = st.multiselect(f"{team1_name}'s Picks to Trade", list(pick_options_team1.keys()))
        with col4:
            team2_pick_selection = st.multiselect(f"{team2_name}'s Picks to Trade", list(pick_options_team2.keys()))

        # Step 3: Confirm the trade
        if st.button("Confirm Trade"):
            if not team1_pick_selection and not team2_pick_selection:
                st.warning("Please select at least one pick from each team to trade.")
                return

            # Swap the selected picks
            for pick_key in team1_pick_selection:
                pick = pick_options_team1[pick_key]
                pick.current_owner_id = team2.id

            for pick_key in team2_pick_selection:
                pick = pick_options_team2[pick_key]
                pick.current_owner_id = team1.id

            session.commit()
            st.success(f"Trade completed! {team1_name} and {team2_name} have swapped their selected picks.")
