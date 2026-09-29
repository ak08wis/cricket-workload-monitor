



import plotly.express as px
import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_FILE = "player_sessions.csv"

st.set_page_config(
    page_title="Cricket Workload Monitor",
    page_icon="🏏",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
else:
    data = pd.DataFrame()


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("🏏 Cricket Workload Monitor")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "📝 Log Session",
        "📊 Workload Dashboard",
        "⚠️ Pain Analysis",
        "👤 Player Analysis",
        "🏏 Bowling Volume",
        "💤 Recovery Factors",
        "💡 Key Findings"
    ]
)


# ==================================================
# OVERVIEW
# ==================================================

if page == "🏠 Overview":

    st.title("🏏 Cricket Workload Monitor")

    st.header("About This Project")

    st.markdown("""
    This dashboard explores how cricket workload and recovery factors
    may be associated with reported pain.

    The project tracks:

    - Session workload
    - Bowling volume
    - Fatigue
    - Soreness
    - Sleep
    - Reported pain

    The goal is to investigate patterns in player workload and recovery
    using data analysis and visualization.

    *This project is exploratory and is not intended for medical diagnosis
    or injury prediction.*
    """)

    st.divider()

    if not data.empty:

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Sessions",
                len(data)
            )

        with col2:
            st.metric(
                "Players",
                data["Player"].nunique()
            )

        with col3:
            pain_count = (data["Pain Reported"] == "Yes").sum()

            st.metric(
                "Pain Sessions",
                pain_count
            )

    else:
        st.info("No session data has been recorded yet.")


# ==================================================
# LOG SESSION
# ==================================================

elif page == "📝 Log Session":

    st.title("📝 Log a Training Session")

    session_date = st.date_input(
        "Session Date",
        value=date.today()
    )

    player = st.text_input("Player Name")

    player_role = st.selectbox(
        "Player Role",
        ["Bowler", "Batter", "All-Rounder", "Wicketkeeper"]
    )

    session_type = st.selectbox(
        "Session Type",
        ["Practice", "Match", "Recovery"]
    )

    duration = st.number_input(
        "Session Duration (minutes)",
        min_value=0
    )

    rpe = st.slider(
        "How hard was the session? (1-10)",
        1,
        10
    )

    fatigue = st.slider(
        "Current Fatigue (1-10)",
        1,
        10
    )

    soreness = st.slider(
        "Current Soreness (1-10)",
        1,
        10
    )

    sleep = st.number_input(
        "Hours of Sleep Last Night",
        min_value=0.0,
        max_value=24.0,
        value=8.0,
        step=0.5
    )

    pain_reported = st.selectbox(
        "Did you experience pain during or after this session?",
        ["No", "Yes"]
    )

    balls_bowled = st.number_input(
        "Balls Bowled",
        min_value=0
    )

    if st.button("Log Session"):

        session_load = duration * rpe

        new_session = pd.DataFrame({
            "Date": [session_date],
            "Player": [player],
            "Player Role": [player_role],
            "Session Type": [session_type],
            "Duration": [duration],
            "RPE": [rpe],
            "Fatigue": [fatigue],
            "Sleep": [sleep],
            "Pain Reported": [pain_reported],
            "Soreness": [soreness],
            "Balls Bowled": [balls_bowled],
            "Session Load": [session_load]
        })

        if os.path.exists(DATA_FILE):

            old_data = pd.read_csv(DATA_FILE)

            updated_data = pd.concat(
                [old_data, new_session],
                ignore_index=True
            )

        else:

            updated_data = new_session

        updated_data.to_csv(
            DATA_FILE,
            index=False
        )

        st.success("Session saved successfully!")

        st.metric(
            "Session Load",
            f"{session_load:.0f} units"
        )


# ==================================================
# WORKLOAD DASHBOARD
# ==================================================

elif page == "📊 Workload Dashboard":

    st.title("📊 Workload Dashboard")

    if not data.empty:

        st.subheader("Session Load Over Time")

        fig = px.line(
            data,
            x="Date",
            y="Session Load",
            color="Player",
            markers=True,
            title="Player Workload Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("⚠️ Reported Pain Sessions")

        pain_data = data[
            data["Pain Reported"] == "Yes"
        ]

        if not pain_data.empty:

            fig_pain = px.scatter(
                pain_data,
                x="Date",
                y="Session Load",
                color="Player",
                size_max=15,
                title="Sessions Where Players Reported Pain"
            )

            st.plotly_chart(
                fig_pain,
                use_container_width=True
            )

        else:

            st.info("No pain has been reported yet.")

    else:

        st.info("No session data available.")


# ==================================================
# PAIN ANALYSIS
# ==================================================

elif page == "⚠️ Pain Analysis":

    st.title("⚠️ Pain & Workload Analysis")

    if not data.empty:

        pain_sessions = data[
            data["Pain Reported"] == "Yes"
        ]

        no_pain_sessions = data[
            data["Pain Reported"] == "No"
        ]

        if not pain_sessions.empty and not no_pain_sessions.empty:

            st.subheader("Average Session Characteristics")

            comparison = pd.DataFrame({

                "Pain Reported":
                    pain_sessions[
                        [
                            "Session Load",
                            "Balls Bowled",
                            "RPE",
                            "Duration",
                            "Fatigue",
                            "Soreness",
                            "Sleep"
                        ]
                    ].mean(),

                "No Pain Reported":
                    no_pain_sessions[
                        [
                            "Session Load",
                            "Balls Bowled",
                            "RPE",
                            "Duration",
                            "Fatigue",
                            "Soreness",
                            "Sleep"
                        ]
                    ].mean()
            })

            st.dataframe(
                comparison.round(2),
                use_container_width=True
            )

            st.subheader("🔎 Workload, Fatigue, and Soreness")

            fig_combined = px.scatter(
                data,
                x="Session Load",
                y="Fatigue",
                size="Soreness",
                color="Pain Reported",
                hover_data=[
                    "Player",
                    "Player Role",
                    "Balls Bowled",
                    "Sleep"
                ],
                title="Workload vs. Fatigue, with Soreness"
            )

            st.plotly_chart(
                fig_combined,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough pain/no-pain data for comparison."
            )

    else:

        st.info("No session data available.")


# ==================================================
# PLAYER ANALYSIS
# ==================================================

elif page == "👤 Player Analysis":

    st.title("👤 Player Analysis")

    if not data.empty:

        players = data["Player"].dropna().unique()

        selected_player = st.selectbox(
            "Select a player",
            players
        )

        player_data = data[
            data["Player"] == selected_player
        ].copy()

        st.subheader(
            f"{selected_player}'s Sessions"
        )

        st.dataframe(
            player_data,
            use_container_width=True
        )

        latest_date = player_data["Date"].max()

        seven_days_ago = (
            latest_date - pd.Timedelta(days=6)
        )

        recent_data = player_data[
            player_data["Date"] >= seven_days_ago
        ]

        seven_day_load = (
            recent_data["Session Load"].sum()
        )

        st.metric(
            "7-Day Workload",
            f"{seven_day_load:.0f} units"
        )

        st.subheader("📈 Workload Trend")

        player_data = player_data.sort_values("Date")

        player_data = player_data.dropna(
            subset=["Date"]
        )

        player_data["7-Day Workload"] = (
            player_data
            .set_index("Date")["Session Load"]
            .rolling("7D")
            .sum()
            .to_numpy()
        )

        fig_rolling = px.line(
            player_data,
            x="Date",
            y="7-Day Workload",
            markers=True,
            title=f"{selected_player}'s 7-Day Workload"
        )

        st.plotly_chart(
            fig_rolling,
            use_container_width=True
        )

    else:

        st.info("No player data available.")


# ==================================================
# BOWLING VOLUME
# ==================================================

elif page == "🏏 Bowling Volume":

    st.title("🏏 Bowling Volume Analysis")

    if not data.empty:

        bowling_data = data[
            data["Balls Bowled"] > 0
        ].copy()

        if not bowling_data.empty:

            st.subheader(
                "Bowling Volume by Pain Status"
            )

            bowling_summary = (
                bowling_data
                .groupby("Pain Reported")["Balls Bowled"]
                .agg(
                    ["count", "mean", "min", "max"]
                )
                .round(2)
            )

            st.dataframe(
                bowling_summary,
                use_container_width=True
            )

            fig_bowling = px.box(
                bowling_data,
                x="Pain Reported",
                y="Balls Bowled",
                points="all",
                title="Bowling Volume by Reported Pain"
            )

            st.plotly_chart(
                fig_bowling,
                use_container_width=True
            )

            st.subheader(
                "📈 Pain Rate by Bowling Volume"
            )

            bowling_analysis = bowling_data.copy()

            bowling_analysis[
                "Bowling Volume Group"
            ] = pd.cut(
                bowling_analysis["Balls Bowled"],
                bins=[
                    0,
                    50,
                    70,
                    float("inf")
                ],
                labels=[
                    "1–50 balls",
                    "51–70 balls",
                    "71+ balls"
                ]
            )

            pain_rate = (
                bowling_analysis
                .groupby(
                    "Bowling Volume Group",
                    observed=False
                )["Pain Reported"]
                .apply(
                    lambda x:
                    (x == "Yes").mean() * 100
                )
                .reset_index(
                    name="Pain Rate"
                )
            )

            st.dataframe(
                pain_rate.round(1),
                use_container_width=True
            )

            fig_rate = px.bar(
                pain_rate,
                x="Bowling Volume Group",
                y="Pain Rate",
                title="Reported Pain Rate by Bowling Volume",
                labels={
                    "Pain Rate":
                        "Sessions Reporting Pain (%)",
                    "Bowling Volume Group":
                        "Bowling Volume"
                }
            )

            st.plotly_chart(
                fig_rate,
                use_container_width=True
            )

            st.subheader(
                "📊 Sample Size by Bowling Volume"
            )

            sample_sizes = (
                bowling_analysis
                .groupby(
                    "Bowling Volume Group",
                    observed=False
                )["Pain Reported"]
                .agg(
                    Sessions="count",
                    Pain_Sessions=lambda x:
                        (x == "Yes").sum()
                )
            )

            sample_sizes["Pain Rate"] = (
                sample_sizes["Pain_Sessions"]
                / sample_sizes["Sessions"]
                * 100
            ).round(1)

            st.dataframe(
                sample_sizes,
                use_container_width=True
            )

        else:

            st.info(
                "No bowling sessions available."
            )

    else:

        st.info("No session data available.")


# ==================================================
# RECOVERY FACTORS
# ==================================================

elif page == "💤 Recovery Factors":

    st.title("💤 Recovery Factors")

    if not data.empty:

        recovery_data = data[
            [
                "Pain Reported",
                "Fatigue",
                "Soreness",
                "Sleep"
            ]
        ].copy()

        st.subheader(
            "💪 Recovery Factors and Reported Pain"
        )

        recovery_summary = (
            recovery_data
            .groupby("Pain Reported")[
                ["Fatigue", "Soreness", "Sleep"]
            ]
            .mean()
            .round(2)
        )

        st.dataframe(
            recovery_summary,
            use_container_width=True
        )

        st.subheader("Fatigue by Reported Pain")

        fig_recovery = px.box(
            recovery_data,
            x="Pain Reported",
            y="Fatigue",
            points="all",
            title="Fatigue by Reported Pain"
        )

        st.plotly_chart(
            fig_recovery,
            use_container_width=True
        )

        st.subheader("🩹 Soreness by Reported Pain")

        fig_soreness = px.box(
            recovery_data,
            x="Pain Reported",
            y="Soreness",
            points="all",
            title="Soreness by Reported Pain"
        )

        st.plotly_chart(
            fig_soreness,
            use_container_width=True
        )

        st.subheader("😴 Sleep by Reported Pain")

        fig_sleep = px.box(
            recovery_data,
            x="Pain Reported",
            y="Sleep",
            points="all",
            title="Sleep by Reported Pain"
        )

        st.plotly_chart(
            fig_sleep,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🏏 Bowling Volume vs. Recovery"
        )

        bowling_recovery = data[
            data["Balls Bowled"] > 0
        ].copy()

        if not bowling_recovery.empty:

            bowling_recovery[
                "Bowling Volume Group"
            ] = pd.cut(
                bowling_recovery["Balls Bowled"],
                bins=[
                    0,
                    50,
                    70,
                    float("inf")
                ],
                labels=[
                    "1–50 balls",
                    "51–70 balls",
                    "71+ balls"
                ]
            )

            recovery_by_volume = (
                bowling_recovery
                .groupby(
                    "Bowling Volume Group",
                    observed=False
                )[
                    [
                        "Fatigue",
                        "Soreness",
                        "Sleep"
                    ]
                ]
                .mean()
                .round(2)
            )

            st.dataframe(
                recovery_by_volume,
                use_container_width=True
            )

    else:

        st.info("No session data available.")


# ==================================================
# KEY FINDINGS
# ==================================================

elif page == "💡 Key Findings":

    st.title("💡 Key Findings")

    st.markdown("""
    ### Current Observations

    Based on the current exploratory dataset:

    - Reported pain was more common in higher-volume bowling sessions.
    - Higher bowling-volume groups also showed higher average fatigue and soreness.
    - The highest bowling-volume group had the highest average fatigue and soreness.
    - These patterns describe associations within this dataset and do not establish that bowling volume causes pain.
    """)

    st.divider()

    st.header("⚠️ Limitations")

    st.markdown("""
    This analysis is exploratory and is based on a relatively small dataset.

    The results show associations rather than causal relationships.

    The dataset may not represent cricket players more broadly, and reported
    pain does not necessarily indicate an injury.

    Further data would be needed to determine whether these patterns remain
    consistent across players and sessions.
    """)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "Built with Python, Pandas, Plotly & Streamlit"
)
