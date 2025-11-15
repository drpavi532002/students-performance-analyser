import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# Load CSV
df = pd.read_csv("students.csv")

# Container for slideshow
container = st.empty()

# Function to get color based on value (green high, orange mid, red low)
def color_map(val, max_val=100):
    if val >= max_val*0.8:
        return 'green'
    elif val >= max_val*0.5:
        return 'orange'
    else:
        return 'red'

# ----------------- AUTO SLIDESHOW -----------------
for i in range(len(df)):
    student = df.iloc[i]

    with container.container():
        st.subheader(f"👤 Student: {student['Name']} ({i+1}/{len(df)})")

        subjects = ["Maths", "Science", "English"]
        marks = [student["Maths"], student["Science"], student["English"]]

        col1, col2, col3 = st.columns(3)

        # Bar Chart
        with col1:
            fig, ax = plt.subplots()
            colors = [color_map(m) for m in marks]
            ax.bar(subjects, marks, color=colors)
            ax.set_ylim(0, 100)
            ax.set_title("📊 Subject-wise Marks (Bar Chart)")
            st.pyplot(fig)
            plt.close(fig)

        # Pie Chart
        with col2:
            fig2, ax2 = plt.subplots()
            pie_vals = [student["Attendance"], student["Participation"], sum(marks)/3]
            ax2.pie(pie_vals, labels=["Attendance","Participation","Avg Marks"], autopct='%1.1f%%',
                    startangle=90,
                    colors=[color_map(student["Attendance"]),
                            color_map(student["Participation"],10),
                            color_map(sum(marks)/3)])
            ax2.set_title("🥧 Performance Distribution (Pie Chart)")
            st.pyplot(fig2)
            plt.close(fig2)

        # Line Chart
        with col3:
            fig3, ax3 = plt.subplots()
            ax3.plot(subjects, marks, marker='o', linestyle='-', color='blue')
            ax3.set_ylim(0, 100)
            ax3.set_title("📈 Marks Trend (Line Chart)")
            st.pyplot(fig3)
            plt.close(fig3)

        # Display Attendance, Participation, Marks percentages
        st.write("### 📊 Performance Summary")
        st.write(f"**Attendance:** {student['Attendance']}%")
        st.write(f"**Participation:** {student['Participation']}/10")
        st.write(f"**Avg Marks:** {sum(marks)/3:.2f}")

        # Final Score
        final_score = (sum(marks)/3)*0.5 + student["Attendance"]*0.3 + student["Participation"]*0.2
        st.write(f"**Final Score:** {final_score:.2f}")

        time.sleep(2)  # Auto update every 2 sec

# ----------------- FINAL CLASS RANKING -----------------
st.write("### 🏆 Class Ranking (After Last Student)")

df["FinalScore"] = ((df["Maths"] + df["Science"] + df["English"])/3)*0.5 + df["Attendance"]*0.3 + df["Participation"]*0.2
ranked = df.sort_values(by="FinalScore", ascending=False)

# Top performers per category
st.write("### 🎯 Category-wise Top Performer")
col1, col2, col3 = st.columns(3)

with col1:
    top_att = df.loc[df["Attendance"].idxmax()]
    st.metric(label="Highest Attendance", value=f"{top_att['Name']} ({top_att['Attendance']}%)")

with col2:
    top_part = df.loc[df["Participation"].idxmax()]
    st.metric(label="Highest Participation", value=f"{top_part['Name']} ({top_part['Participation']}/10)")

with col3:
    top_marks = df.loc[((df["Maths"]+df["Science"]+df["English"])/3).idxmax()]
    avg_mark = (top_marks["Maths"]+top_marks["Science"]+top_marks["English"])/3
    st.metric(label="Highest Avg Marks", value=f"{top_marks['Name']} ({avg_mark:.2f})")

# Horizontal scroll for final score ranking
cols = st.columns(len(ranked))
for idx, student in enumerate(ranked.itertuples()):
    with cols[idx]:
        st.metric(label=student.Name, value=f"{student.FinalScore:.2f}")

st.success(f"🥇 Topper Overall: {ranked.iloc[0].Name} ({ranked.iloc[0].FinalScore:.2f})")
st.error(f"🥀 Last Rank Overall: {ranked.iloc[-1].Name} ({ranked.iloc[-1].FinalScore:.2f})")
