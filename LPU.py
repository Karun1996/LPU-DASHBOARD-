import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Title and university name
st.title('Student Result System')
st.header('LOVELY PROFESSIONAL UNIVERSITY')

# Input fields
name = st.text_input('Enter your name', key='name')
registration = st.text_input('Enter your registration number', key='registration')

# Validate registration number (only numeric)
if registration and not registration.isdigit():
    st.error('Please enter numbers only for Registration Number.')

roll_no = st.text_input('Enter your roll number', key='roll_no')

# Dropdown for subjects
subject_options = {
    'Accounts (A-01)': 40,
    'Finance (F-03)': 40,
    'Soft Skills (P-06)': 40,
    'Hadoop (H-09)': 40,
    'Machine Learning (ML-012)': 50,
    'Analytical Skills (AS-011)': 50
}

selected_subjects = st.multiselect('Select subjects', list(subject_options.keys()), key='selected_subjects')

# Data collection
def calculate_results(subjects):
    results = []
    total_marks = 0
    total_passing_marks = 0

    if len(subjects) == 0:
        return results, 0, 'No Subjects Selected'

    for subject in subjects:
        passing_marks = subject_options[subject]
        marks = st.number_input(f'Enter marks for {subject} (out of {passing_marks}):', min_value=0, max_value=passing_marks, key=f'marks_{subject}')

        # Determine pass/fail status and grade
        if marks >= passing_marks * 0.7:
            result = 'Pass'
            if marks >= passing_marks * 0.8:
                grade = 'A'
            elif marks >= passing_marks * 0.7:
                grade = 'B'
            else:
                grade = 'C'
        else:
            result = 'Fail'
            grade = 'D'

        results.append({
            'Name': name,
            'Registration Number': registration,
            'Roll Number': roll_no,
            'Subject': subject,
            'Marks': marks,
            'Result': result,
            'Grade': grade,
            'Passing Marks': passing_marks
        })

        total_marks += marks
        total_passing_marks += passing_marks

    # Calculate overall statistics
    if total_passing_marks > 0:
        overall_marks = total_marks
        overall_passing_marks = total_passing_marks * len(subjects) * 0.7
        overall_percentage = (overall_marks / overall_passing_marks) * 100

        if overall_percentage >= 80:
            overall_grade = 'Distinction'
        elif overall_percentage >= 60:
            overall_grade = 'First Division'
        elif overall_percentage >= 50:
            overall_grade = 'Second Division'
        else:
            overall_grade = 'Pass'
    else:
        overall_percentage = 0
        overall_grade = 'No Subjects Selected'

    return results, overall_percentage, overall_grade

results, overall_percentage, overall_grade = calculate_results(selected_subjects)

# Display results in table format and line chart for overall statistics
if st.button('Show Results') or len(selected_subjects) != len(results):
    df_results = pd.DataFrame(results)
    st.subheader('Results Summary')
    st.table(df_results)

    # Display average and total percentage
    st.subheader('Average and Total Percentage')
    st.write(f'Overall Percentage: {overall_percentage:.2f}%')
    st.write(f'Overall Grade: {overall_grade}')

    # Plot overall statistics as a line chart (trendline)
    if len(selected_subjects) > 0:
        fig, ax = plt.subplots()
        ax.plot(selected_subjects, df_results['Marks'], marker='o', linestyle='-', color='b', label='Marks')
        ax.set_xlabel('Subjects')
        ax.set_ylabel('Marks')
        ax.set_title('Overall Marks Distribution')
        plt.xticks(rotation=45)
        ax.axhline(y=df_results['Marks'].mean(), color='r', linestyle='--', label='Mean Marks')
        ax.legend()
        st.pyplot(fig)

# Footer
st.text('© 2024 Lovely Professional University')
