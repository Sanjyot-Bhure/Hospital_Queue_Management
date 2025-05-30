import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("Clinic_Appointment_Data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Filter attended patients
df_attended = df[df["No Show"] == 0].copy()

# Existing KPIs
avg_wait = df_attended['Wait Time (min)'].mean()
no_show_rate = 100 * df['No Show'].mean()
patients_today = df['Date'].value_counts().max()
utilization = (len(df_attended) / len(df)) * 100

# New KPIs
avg_consult_duration = df_attended["Consult Duration (min)"].mean()
longest_wait_doc = df_attended.groupby("Doctor")["Wait Time (min)"].mean().idxmax()
df_attended["Hour"] = df_attended["Appointment Time"].str.split(':').str[0].astype(int)
peak_hour = df_attended["Hour"].value_counts().idxmax()
no_show_by_day = df.groupby("Date")["No Show"].mean()
worst_day = no_show_by_day.idxmax()
worst_day_rate = 100 * no_show_by_day.max()
max_patients_served = df.groupby("Date").size().max()

# Display all KPIs
st.title("Clinic Operations Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Patient Wait Time", f"{avg_wait:.1f} min")
col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
col3.metric("Patients Served (Max Day)", patients_today)
col4.metric("Appointment Utilization", f"{utilization:.1f}%")

col5, col6, col7 = st.columns(3)
col5.metric("Avg Consult Duration", f"{avg_consult_duration:.1f} min")
col6.metric("Doctor with Longest Wait", longest_wait_doc)
col7.metric("Peak Appointment Hour", f"{peak_hour}:00")

st.write(f"Worst No-Show Day: **{worst_day.date()}** with a no-show rate of **{worst_day_rate:.1f}%**")
st.write(f"Max Patients Served in One Day: **{max_patients_served}**")

# Chart: Avg Wait vs Consult Time per Doctor
avg_wait_time = df_attended.groupby('Doctor')['Wait Time (min)'].mean()
avg_consult_time = df_attended.groupby('Doctor')['Consult Duration (min)'].mean()

comparison_df = pd.DataFrame({
    'Avg Wait Time (min)': avg_wait_time,
    'Avg Consult Time (min)': avg_consult_time
}).sort_values(by='Avg Wait Time (min)', ascending=False)

st.subheader("Avg Wait Time vs Consult Time per Doctor")
st.bar_chart(comparison_df)


# IN your command prompt run the code: python -m streamlit run clinic_dashboard.py