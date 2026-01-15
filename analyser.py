"""Uses VADER sentiment analysis to analyse Reddit comments."""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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
