import streamlit as st
import pandas as pd
from scraper import scrape_reddit_post


st.set_page_config(page_title="ReddMind", layout="centered")

st.title("ReddMind - Reddit Sentiment Analysis")

# Sidebar for settings
st.sidebar.header("Settings")
comment_limit = st.sidebar.slider(
    "Max Comments to Analyse",
    min_value=10,
    max_value=100,
    value=30,
    step=5,
    help="Higher limits may take longer and cause Reddit to block requests, but provide more accurate results.",
)

# Input URL

url = st.text_input("Enter the Reddit post URL:", "")

if st.button("Analyse"):
    if not url:
        st.warning("Please enter a valid Reddit post URL.")
    else:
        with st.spinner(f"Scraping and analysing {comment_limit} comments..."):
            data = scrape_reddit_post(url, max_comments=comment_limit)

            if data.get("error"):
                st.error(data["error"])
            else:
                # Display results
                st.success(f"Analysis complete for {data['post_title']}")
                st.info(f"Fetched {len(data['comments'])} comments.")

                # Use dataframe to display comments
                df = pd.DataFrame(data["comments"], columns=["Comments Text"])

                st.subheader("Comments Data")
                st.write(f"Displaying up to {len(df)} comments:")

                st.dataframe(df, use_container_width=True, row_height=100)
