import streamlit as st
import pandas as pd
from scraper import scrape_reddit_post
from analyser import analyse_comments_sentiment


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

                sentiment_summary = analyse_comments_sentiment(data["comments"])

                # Display sentiment analysis metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Verdict", sentiment_summary["verdict"])
                col2.metric("Positive Comments", sentiment_summary["positive_count"])
                col3.metric("Negative Comments", sentiment_summary["negative_count"])
                col4.metric(
                    "Average Score", f"{sentiment_summary['average_score']:.4f}"
                )
                # Display detailed dataframe
                df = sentiment_summary["df"]
                st.subheader(
                    f"Detailed Sentiment Scores per Comment ({len(df)} comments)"
                )
                st.write(
                    "Each comment is scored between -1 (most negative) to +1 (most positive)."
                )

                st.dataframe(
                    df[["comment", "score", "label"]],
                    use_container_width=True,
                    row_height=100,
                )
