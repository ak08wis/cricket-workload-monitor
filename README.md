# Cricket Workload Monitor

A Streamlit data science dashboard for exploring cricket player workload, bowling volume, recovery factors, and reported pain patterns.

## Project Overview

The Cricket Workload Monitor was created to explore how training and match workload may relate to reported pain and recovery indicators in cricket.

The dashboard allows users to record and analyze:

- Session duration
- RPE (Rate of Perceived Exertion)
- Session load
- Balls bowled
- Fatigue
- Soreness
- Sleep
- Reported pain

## Analysis

The dashboard explores relationships between:

- Workload and reported pain
- Bowling volume and reported pain
- Fatigue and soreness
- Sleep and recovery
- Workload, fatigue, and soreness

The current analysis is exploratory and looks for patterns within the available dataset.

## Current Findings

In the current dataset:

- Reported pain was more common in higher-volume bowling sessions.
- Higher bowling-volume groups also showed higher average fatigue and soreness.
- The 71+ balls group had the highest average fatigue and soreness and the lowest average sleep.

These findings describe associations within this dataset and do not establish that bowling volume causes pain or injury.

## Limitations

This project is exploratory and is based on a relatively small dataset.

The data does not establish causal relationships, and reported pain does not necessarily indicate an injury. The dataset may also not represent cricket players more broadly.

Additional data across more players and sessions would be needed to determine whether these patterns remain consistent.

## Technologies

- Python
- Pandas
- Streamlit
- Plotly

## Running the Dashboard

Install the required packages:

```bash
pip install -r requirements.txt