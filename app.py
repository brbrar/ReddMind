import streamlit as st

st.set_page_config(page_title="ReddMind", layout="centered")

st.title("ReddMind - Reddit Sentiment Analysis")

# Input URL

url = st.text_input("Enter the Reddit post URL:", "")

if st.button("Analyse"):
    if not url:
        st.warning9("Please enter a valid Reddit post URL.")
    else:
        with st.spinner("Analysing..."):
            st.success("Analysis complete!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Sentiment", "Neutral")
            col2.metric("Sentiment Score", "0")
            col3.metric("Comments Analysed", "0")
