import streamlit as st
import math
import pandas as pd
import numpy as np

def calculate_sample_size(N, Z, p, E):
    numerator = N * (Z**2) * p * (1 - p)
    denominator = (N - 1) * (E**2) + (Z**2) * p * (1 - p)
    n = numerator / denominator
    return math.ceil(n)

# Z-scores for common confidence levels
z_scores = {
    "90%": 1.645,
    "95%": 1.96,
    "97%": 2.17,  # Added 97% confidence level
    "99%": 2.58,
    "99.9%": 3.29
}

st.write("---")
st.header("Sample Size Calculator")

# Input fields for calculated sample size
N = st.number_input("Rows of data (N)", min_value=1, value=1000)
confidence_level = st.selectbox("Confidence Level", options=["90%", "95%", "97%", "99%", "99.9%"], index=1)
E = st.number_input("Margin of Error (E)", min_value=0.009, max_value=1.0, value=0.05, step=0.01)
p = st.number_input("Estimated Population Proportion (p) - leave as 0.5 if unsure", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Get the Z-score based on the selected confidence level
Z = z_scores[confidence_level]

if st.button("Calculate Sample Size"):
    sample_size = calculate_sample_size(N, Z, p, E)
    reduction_percentage = round((1 - sample_size / N) * 100, 0)
    
    st.markdown(
        f"For a {confidence_level} confidence level with a {E*100:.0f}% margin of error,<br>"
        f"the minimum sample size needed is <span style='color: orange;'><strong>{sample_size}</strong></span> rows,<br>"
        f"a **{reduction_percentage:.0f}%** reduction from the total population size.",
        unsafe_allow_html=True
    )
    
    st.write("---")
    st.subheader("Sample code to reduce DataFrame rows")
    st.write("Here are three methods you can use to reduce the number of rows in your DataFrame based on the calculated sample size:")

    with st.expander("Method 1: Random Sampling"):
        st.code(f"""
import pandas as pd

# Assuming you have a DataFrame called 'df'
sample_size = {sample_size}

# Random sampling
df_sampled = df.sample(n=sample_size, random_state=42)
        """, language='python')
        st.write("Random sampling with a specified seed will produce replicable results and is suitable for most cases.")

    with st.expander("Method 2: Systematic Sampling"):
        st.code(f"""
import pandas as pd

# Assuming you have a DataFrame called 'df'
sample_size = {sample_size}

# Systematic sampling
step = len(df) // sample_size
df_sampled = df.iloc[::step].head(sample_size)
        """, language='python')
        st.write("Systematic sampling selects every nth row to achieve the desired sample size.")

    with st.expander("Method 3: Stratified Sampling"):
        st.code(f"""
import pandas as pd

# Assuming you have a DataFrame called 'df'
sample_size = {sample_size}

# Stratified sampling (example with a 'category' column)
def stratified_sample(df, column, n):
    return df.groupby(column, group_keys=False).apply(lambda x: x.sample(min(len(x), int(n*len(x)/len(df)))))

df_sampled = stratified_sample(df, 'category', sample_size)
        """, language='python')
        st.write("Stratified sampling ensures that the proportion of samples from each category remains the same as in the original dataset.")

    st.write("Note: Make sure to replace 'df' with your actual DataFrame name and adjust the 'category' column name in the stratified sampling example to match your data.")