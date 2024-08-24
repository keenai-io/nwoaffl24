import streamlit as st
from models import Team, Pick, session

def display_commissioner():
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Create Team", "Update Team", "Update Picks"])

    # Tab 1: Create a New Team
    with tab1:
        st.subheader("Create a New Team")
        with st.form("create_team_form"):
            team_name = st.text_input("Team Name")
            team_owner = st.text_input("Owner Name")
            profile_pic_path = st.text_input("Profile Picture Path")
            draft_order = st.number_input("Draft Order", min_value=1, step=1)

            submit_button = st.form_submit_button("Create Team")

        if submit_button:
            if team_name and team_owner:
                new_team = Team(name=team_name, owner=team_owner, profile_pic=profile_pic_path, draft_order=draft_order)
                session.add(new_team)
                session.commit()

                # Automatically create 15 picks for 2024 and 2025
                for year in [2024, 2025]:
                    for round_num in range(1, 16):  # Rounds 1 to 15
                        new_pick = Pick(
                            round=round_num,
                            pick_number=draft_order,  # Use draft_order as pick_number
                            year=year,
                            original_owner_id=new_team.id,
                            current_owner_id=new_team.id,
                            team_id=new_team.id
                        )
                        session.add(new_pick)
                
                session.commit()  # Commit the picks to the database
                
                st.success(f"Team '{team_name}' created successfully with draft order {draft_order}! 15 picks for 2024 and 15 picks for 2025 have been automatically generated.")
            else:
                st.error("Please provide both a team name and an owner name.")

    # Tab 2: Update an Existing Team
    with tab2:
        st.subheader("Update an Existing Team")
        
        # Select a team to update
        teams = session.query(Team).all()
        team_names = [team.name for team in teams]
        selected_team_name = st.selectbox("Select a Team", team_names)
        
        if selected_team_name:
            selected_team = session.query(Team).filter_by(name=selected_team_name).first()
            
            # Pre-fill the form with the current team's info
            with st.form("update_team_form"):
                updated_team_name = st.text_input("Update Team Name", value=selected_team.name)
                updated_team_owner = st.text_input("Update Owner Name", value=selected_team.owner)
                updated_profile_pic_path = st.text_input("Update Profile Picture Path", value=selected_team.profile_pic)
                updated_draft_order = st.number_input("Update Draft Order", min_value=1, value=selected_team.draft_order, step=1)

                # Button to submit the updates
                update_button = st.form_submit_button("Update Team")

            if update_button:
                selected_team.name = updated_team_name
                selected_team.owner = updated_team_owner
                selected_team.profile_pic = updated_profile_pic_path
                selected_team.draft_order = updated_draft_order
                session.commit()
                st.success(f"Team '{selected_team_name}' has been updated successfully!")

            # Reset Picks Button with Confirmation
            reset_picks_button = st.button("Reset Picks")
            confirm_reset = st.checkbox("Confirm reset of all 2024 and 2025 picks")

            if reset_picks_button and confirm_reset:
                # Delete existing picks for 2024 and 2025
                session.query(Pick).filter(Pick.team_id == selected_team.id, Pick.year.in_([2024, 2025])).delete()
                session.commit()

                # Recreate the picks for 2024 and 2025
                for year in [2024, 2025]:
                    for round_num in range(1, 16):
                        new_pick = Pick(
                            round=round_num,
                            pick_number=selected_team.draft_order,
                            year=year,
                            original_owner_id=selected_team.id,
                            current_owner_id=selected_team.id,
                            team_id=selected_team.id
                        )
                        session.add(new_pick)

                session.commit()  # Commit the new picks to the database
                
                st.success(f"All 2024 and 2025 picks for '{selected_team_name}' have been reset.")
            elif reset_picks_button and not confirm_reset:
                st.warning("Please confirm the reset by checking the box above.")

    # Tab 3: Update Picks
    with tab3:
        st.subheader("Update Picks Selection")

        # Select the year to filter picks
        available_years = session.query(Pick.year).distinct().order_by(Pick.year).all()
        year_options = [year[0] for year in available_years]
        selected_year = st.selectbox("Select Year", year_options)

        if selected_year:
            # Fetch all picks for the selected year ordered by round and pick number
            picks = session.query(Pick).filter_by(year=selected_year).order_by(Pick.round, Pick.pick_number).all()

            for pick in picks:
                # Check if the pick's current owner is different from the original owner
                is_traded = pick.original_owner_id != pick.current_owner_id
                original_owner = session.query(Team).filter_by(id=pick.original_owner_id).first().name
                current_owner = session.query(Team).filter_by(id=pick.current_owner_id).first().name

                # Annotated pick label with color for traded picks and light blue for numbers
                if is_traded:
                    pick_label = f"<span style='color: #0d6efd;'>{pick.round}.{pick.pick_number}</span> (<span style='color: yellow;'>{original_owner}</span> traded to <span style='color: lightgreen;'>{current_owner}</span>)"
                else:
                    pick_label = f"<span style='color: #0d6efd;'>{pick.round}.{pick.pick_number}</span> (Team: <span style='color: yellow;'>{original_owner}</span>)"

                # Display the pick label using markdown to support HTML
                st.markdown(pick_label, unsafe_allow_html=True)

                # Text input for updating the pick selection
                new_selection = st.text_input(f"Update selection for Round {pick.round}, Pick {pick.pick_number}", value=pick.selection if pick.selection else "", key=f"{pick.id}")

                if new_selection != pick.selection:
                    pick.selection = new_selection
                    session.commit()
                    st.success(f"Selection for Round {pick.round}, Pick {pick.pick_number} updated to '{new_selection}'.", icon="✅")
