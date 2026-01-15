"""Uses VADER sentiment analysis to analyse Reddit comments."""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def analyse_comments_sentiment(comments):
    """Analyse sentiment of Reddit comments using VADER."""

    analyser = SentimentIntensityAnalyzer()
    results = []

    total_compound = 0
    pos_count = 0
    neg_count = 0

    for comment in comments:
        # Get sentiment scores
        scores = analyser.polarity_scores(comment)
        # Extract compound score and accumulate
        compound = scores["compound"]
        total_compound += compound

        # Classify sentiment based on compound score
        sentiment_label = "Neutral"
        if compound >= 0.05:
            sentiment_label = "Positive"
            pos_count += 1
        elif compound <= -0.05:
            sentiment_label = "Negative"
            neg_count += 1

        results.append(
            {"comment": comment, "score": compound, "label": sentiment_label}
        )

    # Calculate average compound score
    avg_score = total_compound / len(comments) if comments else 0

    verdict = (
        "Positive"
        if avg_score >= 0.05
        else "Negative" if avg_score <= -0.05 else "Neutral"
    )

    summary = {
        "verdict": verdict,
        "average_score": avg_score,
        "positive_count": pos_count,
        "negative_count": neg_count,
        "df": pd.DataFrame(results),
    }

    return summary


def cluster_comments(comments, n_clusters=3):
    """Cluster comments into groups using KMeans clustering."""
    if len(comments) < n_clusters:
        n_clusters = len(comments)

    # Convert text to numeric vectors using TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    X = vectorizer.fit_transform(comments)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    # Extract cluster labels
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    # Get top terms for each cluster
    themes = []
    for i in range(n_clusters):
        cluster_terms = [terms[ind] for ind in order_centroids[i, :4]]
        themes.append(cluster_terms)

    return themes
