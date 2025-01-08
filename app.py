import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from utils import simplize_html, calculate_frequency, get_leave_classes
import io

st.title("HTML Class Frequency Analyzer")

# File upload
uploaded_file = st.file_uploader("Choose an HTML file", type=['html'])

# Get number of columns and rows
col1, col2 = st.columns(2)
with col1:
    num_columns = st.number_input("Number of columns", min_value=1, value=1)
with col2:
    num_rows = st.number_input("Number of rows", min_value=1, value=1)

if uploaded_file is not None:
    # Read the file
    content = uploaded_file.read().decode()
    soup = BeautifulSoup(content, "html.parser")
    
    # Process HTML
    simplified_soup = simplize_html(soup)
    frequencies = calculate_frequency(simplified_soup)
    
    # Convert frequencies to DataFrame for better display
    df = pd.DataFrame(list(frequencies.items()), columns=['Class', 'Frequency'])
    df = df.sort_values('Frequency', ascending=False)
    # leave_classes = get_leave_classes(df)
    # df = df[df['Class'].isin(leave_classes)]
    
    # Calculate difference from target row count
    df['Difference from Row Count'] = abs(df['Frequency'] - num_rows)
    df = df.sort_values('Difference from Row Count')
    
    # Display results
    st.subheader("Class Frequencies")
    st.dataframe(df)
    
    # Show top matches
    st.subheader(f"Top {num_columns} Classes Closest to {num_rows} Rows")
    top_matches = df.head(int(num_columns))
    st.dataframe(top_matches)
    
    # Visualization
    st.subheader("Frequency Distribution")
    st.bar_chart(df.set_index('Class')['Frequency'])
    
    # User select multiple classes to see the values
    df = df.sort_values('Difference from Row Count')
    selected_classes = st.multiselect("Select classes to see the values", df['Class'], 
                                      default=df['Class'].tolist())
    if selected_classes:
        st.write("Values for selected classes:")
        for cls in selected_classes:
            values = [x.text.strip() for x in simplified_soup.find_all(
                attrs={
                    "parent_ids": str(cls)
                })]
            values_df = pd.DataFrame(values, columns=[cls])
            st.subheader(f"Values for class: {cls} - {len(values)} rows")
            st.dataframe(values_df)
