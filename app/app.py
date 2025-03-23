import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import itertools  



# Set page config
st.set_page_config(page_title="Fitness Tracker", layout="wide")
# Custom CSS for a cleaner, modern look with emojis
st.markdown("""
    <style>
        /* Background color */
        .main {
            background-color: #f5f7fa;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #2b2d42;
            color: white;
        }

        /* Title Styling */
        h1 {
            color: #1a1a2e;
            text-align: center;
            font-size: 36px;
        }

        /* Metric Box Styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }

        /* Selectbox Dropdown Styling */
        select {
            background-color: #ffffff;
            border-radius: 5px;
            padding: 5px;
        }

        /* Adding emojis to headings */
        h1::before {
            content: "🏋️‍♂️ ";
        }
        h2::before {
            content: "📊 ";
        }
        h3::before {
            content: "📌 ";
        }

        /* Sidebar header emoji */
        [data-testid="stSidebar"] h1::before {
            content: "📂 ";
        }

        /* Style for buttons */
        button {
            background-color: #ff6b6b;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 8px;
        }

        /* Table Styling */
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #4a69bd;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


# Load data function
@st.cache_data
def load_data():
    daily_activity = pd.read_csv('data/dailyActivity_merged.csv')
    daily_steps = pd.read_csv('data/dailySteps_merged.csv')
    heartrate = pd.read_csv('data/heartrate_seconds_merged.csv')
    return daily_activity, daily_steps, heartrate

# Load Data
try:
    daily_activity, daily_steps, heartrate = load_data()
except FileNotFoundError as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# Preprocessing
daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'], format='%m/%d/%Y')
daily_steps['ActivityDay'] = pd.to_datetime(daily_steps['ActivityDay'], format='%m/%d/%Y')
heartrate['Time'] = pd.to_datetime(heartrate['Time'])

# Sidebar for navigation
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Section Divider
    st.markdown("---")

    # Improved Dropdown with Icons
    page = st.selectbox(
        "📌 Select Page:",
        [
            "🏃 Activity Analysis",
            "❤️ Heart Rate Analysis",
            "💤 Deep Sleep Analysis",
            "🏆 Performance"
        ]
    )

    # Another Section Divider for Better Separation
    st.markdown("---")

    # Additional Info / Footer
    st.caption("🔹 Navigate through different sections to analyze your fitness data efficiently.")



# Header
st.markdown("<h1 style='font-size: 2.5rem;'>🏋️ Personal Fitness Tracker</h1>", unsafe_allow_html=True)
st.markdown("**Comprehensive analytics dashboard for Fitbit data**")

# User and date range filter
user_id = st.selectbox("Select User:", daily_activity['Id'].unique())
date_range = st.selectbox("Select Date Range:", ["All Time", "Last 30 Days", "Last 7 Days"])

# Filter data based on user
filtered_activity = daily_activity[daily_activity['Id'] == user_id]
filtered_steps = daily_steps[daily_steps['Id'] == user_id]
filtered_heartrate = heartrate[heartrate['Id'] == user_id]

# Filter based on date range
if date_range == "Last 30 Days":
    start_date = filtered_activity['ActivityDate'].max() - pd.Timedelta(days=30)
    filtered_activity = filtered_activity[filtered_activity['ActivityDate'] >= start_date]
    filtered_steps = filtered_steps[filtered_steps['ActivityDay'] >= start_date]
elif date_range == "Last 7 Days":
    start_date = filtered_activity['ActivityDate'].max() - pd.Timedelta(days=7)
    filtered_activity = filtered_activity[filtered_activity['ActivityDate'] >= start_date]
    filtered_steps = filtered_steps[filtered_steps['ActivityDay'] >= start_date]

# Activity Analysis
if page == "🏃 Activity Analysis":
    st.markdown("## 📊 Activity Analysis")

    # Daily Activity Patterns
    st.markdown("### **Daily Activity Patterns**")

    col1, col2, col3 = st.columns(3)
    with col1:
        avg_steps = filtered_steps['StepTotal'].mean()
        st.metric(label="Average Steps", value=f"{int(avg_steps)}", delta=int(avg_steps))
    
    with col2:
        avg_active_minutes = filtered_activity['VeryActiveMinutes'].mean()
        st.metric(label="Average Active Minutes", value=f"{int(avg_active_minutes)}", delta=int(avg_active_minutes))
    
    with col3:
        avg_calories = filtered_activity['Calories'].mean()
        st.metric(label="Average Calories", value=f"{int(avg_calories)}", delta=int(avg_calories))

    # Activity Distribution Pie Chart (Fixed)
    st.markdown("### **Activity Distribution**")
    activity_distribution = {
        'Sedentary': filtered_activity['SedentaryMinutes'].sum(),
        'Lightly Active': filtered_activity['LightlyActiveMinutes'].sum(),
        'Fairly Active': filtered_activity['FairlyActiveMinutes'].sum(),
        'Very Active': filtered_activity['VeryActiveMinutes'].sum(),
    }

    fig1, ax1 = plt.subplots()
    colors = sns.color_palette('coolwarm')

    # Draw pie chart with better label positioning
    wedges, texts, autotexts = ax1.pie(
        activity_distribution.values(),
        labels=None,  # Remove default labels
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 10},
        labeldistance=1.1,
        pctdistance=0.7
    )

    # Annotate labels outside the pie chart to avoid overlap
    for i, (label, wedge) in enumerate(zip(activity_distribution.keys(), wedges)):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = 1.2 * wedge.r * np.cos(np.deg2rad(angle))
        y = 1.2 * wedge.r * np.sin(np.deg2rad(angle))
        ax1.annotate(label, (x, y), ha='center', va='center', fontsize=10, weight='bold')

    # Add legend
    ax1.legend(wedges, activity_distribution.keys(), title="Activity Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax1.axis('equal')
    plt.tight_layout()
    st.pyplot(fig1)

# Heart Rate Analysis
if page == "❤️ Heart Rate Analysis":
    st.markdown("## ❤️ Heart Rate Analysis")

    # ✅ Print columns to debug the 'Time' key error
    print(filtered_heartrate.columns)  # Add this line

    st.markdown("### **Heart Rate Over Time**")
    fig2, ax2 = plt.subplots()
    sns.lineplot(
        x=filtered_heartrate['Time'],
        y=filtered_heartrate['Value'],
        ax=ax2,
        color='red'
    )

    ax2.set_xlabel("Time")
    ax2.set_ylabel("Heart Rate (BPM)")
    ax2.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    st.pyplot(fig2)

    

# Performance Streaks
if page == "🏆 Performance":
    st.markdown("## 🏆 Best Performance Streak")

    streak_days = (filtered_steps['StepTotal'] >= 10000).sum()
    st.metric(label="🏅 Total Goal Completion Days", value=f"{streak_days} days")

    # Best Streak Calculation
    filtered_steps['GoalMet'] = filtered_steps['StepTotal'] >= 10000
    best_streak = max(
        (sum(1 for _ in group) for key, group in 
         itertools.groupby(filtered_steps['GoalMet']) if key),
        default=0
    )
    st.metric(label="🔥 Best Performance Streak", value=f"{best_streak} days")

# Deep Sleep Analysis (Optional)
if page == "💤 Deep Sleep Analysis":
    st.markdown("## 💤 Deep Sleep Analysis")

    try:
        sleep_data = pd.read_csv('data/minuteSleep_merged.csv')
        sleep_data['date'] = pd.to_datetime(sleep_data['date'])

        filtered_sleep = sleep_data[sleep_data['Id'] == user_id]

        avg_sleep = filtered_sleep['value'].mean()
        st.metric(label="Average Deep Sleep Duration", value=f"{avg_sleep:.1f} hrs")

        fig3, ax3 = plt.subplots()
        sns.lineplot(
            x=filtered_sleep['date'],
            y=filtered_sleep['value'],
            ax=ax3
        )

        ax3.set_xlabel("Date")
        ax3.set_ylabel("Deep Sleep Duration (hrs)")

        # ✅ Clean up x-axis formatting
        ax3.xaxis.set_major_locator(plt.MaxNLocator(6))  # Limit number of x-axis labels to 6
        ax3.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format dates
        plt.xticks(rotation=30, ha='right')  # Rotate and align right for better readability
        
        plt.tight_layout()
        st.pyplot(fig3)
    except Exception as e:
        st.warning("⚠️ Deep sleep data not available")



# Footer
st.markdown("---")
st.markdown("👩‍💻 *Built with Streamlit*")
