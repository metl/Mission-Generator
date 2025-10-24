import streamlit as st
from mission_objective import Mission  # Your Mission class
from tables.payout import get_payout

# --- Page setup ---
st.set_page_config(page_title="Mission Generator", layout="centered", page_icon="🎯")
st.title("🎯 Mission Objective Generator")
st.markdown("Quickly generate randomized missions from your mission tables.")

# --- Initialize session state ---
if "mission" not in st.session_state:
    st.session_state.mission = None
if "indicator_status" not in st.session_state:
    st.session_state.indicator_status = {}

# --- Generate new mission ---
if st.button("🗺️ Generate Mission"):
    mission = Mission()
    mission.generate_base_mission()
    st.session_state.mission = mission

    # Initialize main mission indicators
    st.session_state.indicator_status = {}
    for ind in mission.success_indicators:
        key = f"branch0_indicator_{ind['name'].replace(' ', '_')}"
        st.session_state.indicator_status[key] = "pending"

# --- Display mission ---
if st.session_state.mission is not None:
    mission = st.session_state.mission
    # Ensure all branch indicators are initialized
    for i, branch in enumerate(mission.branches, start=1):
        for ind in branch.success_indicators:
            key = f"branch{i}_indicator_{ind['name'].replace(' ', '_')}"
            if key not in st.session_state.indicator_status:
                st.session_state.indicator_status[key] = "pending"

    st.subheader("Mission Overview")
    
    # --- Button for post-mission outcomes ---
    if st.button("📝 Generate Post-Mission Outcomes"):
        mission.generate_post_mission()
        st.success(f"Post-Mission Outcome:\n{mission.post_mission_outcome}")

        # Initialize branch indicators
        for i, branch in enumerate(mission.branches, start=1):
            for ind in branch.success_indicators:
                key = f"branch{i}_indicator_{ind['name'].replace(' ', '_')}"
                if key not in st.session_state.indicator_status:
                    st.session_state.indicator_status[key] = "pending"
    
    st.subheader("Mission Overview")

    mission_text = mission.generate_text()

    # Split by lines to preserve line breaks and allow wrapping
    for line in mission_text.split("\n"):
        st.write(line)

    # Main mission indicators
    for ind in mission.success_indicators:
        name = ind["name"]
        level = ind["level"]
        key = f"branch0_indicator_{name.replace(' ', '_')}"
        current_status = st.session_state.indicator_status.get(key, "pending")

        status = st.radio(
            f"{name} ({level})",
            options=["pending", "success", "failure"],
            index=["pending", "success", "failure"].index(current_status),
            key=key
        )
        st.session_state.indicator_status[key] = status

    # Branch indicators
    for i, branch in enumerate(mission.branches, start=1):
        st.markdown(f"### Branch {i} Indicators")
        for ind in branch.success_indicators:
            name = ind["name"]
            level = ind["level"]
            key = f"branch{i}_indicator_{name.replace(' ', '_')}"
            current_status = st.session_state.indicator_status.get(key, "pending")

            status = st.radio(
                f"{name} ({level})",
                options=["pending", "success", "failure"],
                index=["pending", "success", "failure"].index(current_status),
                key=key
            )
            st.session_state.indicator_status[key] = status

    # --- Potential payout (all success) ---
    potential_total = sum(ind["success_value"] for ind in mission.success_indicators)
    for branch in mission.branches:
        potential_total += sum(ind["success_value"] for ind in branch.success_indicators)
    potential_payout = get_payout(potential_total)
    st.markdown(f"### Potential Payout if all indicators succeed: {potential_payout:,} credits")

    # --- Calculate final payout based on selections ---
    final_total = 0

    # Main mission
    for ind in mission.success_indicators:
        key = f"branch0_indicator_{ind['name'].replace(' ', '_')}"
        status = st.session_state.indicator_status.get(key, "pending")
        if status == "success":
            final_total += ind["success_value"]
        elif status == "failure":
            final_total += ind["failure_value"]

    # Branches
    for i, branch in enumerate(mission.branches, start=1):
        for ind in branch.success_indicators:
            key = f"branch{i}_indicator_{ind['name'].replace(' ', '_')}"
            status = st.session_state.indicator_status.get(key, "pending")
            if status == "success":
                final_total += ind["success_value"]
            elif status == "failure":
                final_total += ind["failure_value"]

    final_payout = get_payout(final_total)
    st.markdown(f"### Current Total Value: {final_total}")
    st.markdown(f"### Current Final Payout: {final_payout:,} credits")

    # --- Reset indicators button ---
    if st.button("🔄 Reset Indicators"):
        st.session_state.indicator_status = {}
        for ind in mission.success_indicators:
            key = f"branch0_indicator_{ind['name'].replace(' ', '_')}"
            st.session_state.indicator_status[key] = "pending"
        for i, branch in enumerate(mission.branches, start=1):
            for ind in branch.success_indicators:
                key = f"branch{i}_indicator_{ind['name'].replace(' ', '_')}"
                st.session_state.indicator_status[key] = "pending"

# --- Footer ---
st.markdown("---")
st.caption("Built with Python")
