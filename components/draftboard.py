import streamlit as st
import base64
from models import session, Team, Pick

def display_draftboard():
    # Number of rounds and teams
    rounds = 15
    
    # Fetch all teams ordered by draft_order
    teams = session.query(Team).order_by(Team.draft_order).all()
    
    # Start HTML table
    html = """
    <style>
    .table-container {
        overflow-y: auto;
        max-height: 70vh;  /* Adjust based on your desired height */
    }
    table {
        width: calc(100% - 5px);  /* Full width minus 5px padding (2.5px on each side) */
        border-collapse: separate;
        border-spacing: 5px; /* Adds padding between cells */
        table-layout: fixed;
    }
    th, td {
        text-align: center;
        width: 125px;  /* Explicit width */
        height: 125px; /* Explicit height */
        vertical-align: top;
        font-size: 14px;
        border-radius: 10px; /* Rounded corners */
    }
    th {
        border: none;
        background-color: #0E1117;
        color: white;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    td {
        border: 2px solid #444444;
        color: white;
        background-color: transparent;
    }
    .pick-selection {
        color: lightgreen;  /* Changed to light green */
        margin-top: 5px;
        display: block;
    }
    hr {
        border: 0;
        border-top: 1px solid lightgreen;  /* Changed to light green */
        margin: 5px 0;
    }
    img {
        width: 50px;  /* Adjust the size of the image */
        height: 50px;
        border-radius: 50%;  /* Make the image circular */
        display: block;
        margin: 0 auto 5px;  /* Center the image and add some margin below */
    }
    </style>
    <div class="table-container">
    <table>
    <thead>
        <tr>
    """
    
    # Create table headers for each team
    for team in teams:
        html += """<th style='border: none';><img src='data:image/png;base64,{encoded_image}'>{team}</th>""".format(
            team=team.name,
            encoded_image=base64.b64encode(open(team.profile_pic, "rb").read()).decode()
        )

    html += "</tr></thead><tbody>"

    # Add rounds and team picks
    for round_num in range(1, rounds + 1):
        html += "<tr>"
        for team in teams:
            pick = session.query(Pick).filter_by(team_id=team.id, round=round_num, year=2024).first()  # Assuming you want to display 2024 picks
            if pick:
                pick_display = f"{pick.round}.{pick.pick_number}"
                cell_style = ""
                if pick.original_owner_id != pick.current_owner_id:
                    current_owner = session.query(Team).filter_by(id=pick.current_owner_id).first()
                    pick_display += f"<br>{current_owner.name}"
                    cell_style = "color: yellow; border-color: yellow;"

                # Add pick selection with light green color and a horizontal rule
                selection_display = f"<hr><span class='pick-selection'>{pick.selection}</span>" if pick.selection else ""
                html += f"<td style='{cell_style}'>{pick_display}{selection_display}</td>"
            else:
                html += "<td>—</td>"
        html += "</tr>"

    html += "</tbody></table></div>"

    # Render the table in Streamlit
    st.markdown(html, unsafe_allow_html=True)

# Display the draft board
st.title("NWOAFFL 2024 Draftboard")
display_draftboard()
