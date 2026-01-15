"""
Uses JSON scraping to extract data from Reddit posts and comments.
Requires the 'requests' library.
For official API usage, PRAW can be used as an alternative.
"""

import requests


def scrape_reddit_post(url, max_comments=30):
    """Scrape Reddit post from given URL and fetches comments."""

    # Clean the URL to ensure it ends with .json
    if "?" in url:
        json_url = url.split("?")[0]
    else:
        json_url = url

    if json_url.endswith("/"):
        json_url = json_url[:-1]

    if json_url.endswith("/"):
        json_url = json_url[:-1]

    json_url += ".json?sort=top"

    # Set user agent (headers) to avoid request blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(json_url, headers=headers)

        if response.status_code != 200:
            return {
                "error": f"Failed to retrieve data: Status code {response.status_code}"
            }

        data = response.json()

        # Parse data to extract post and comments
        post_data = data[0]["data"]["children"][0]["data"]
        post_title = post_data["title"]
        comments_data = data[1]["data"]["children"]

        extracted_comments = []

        # Loop through comments and get text
        for item in comments_data:
            # Check if item is comment (kind == "t1")
            if item["kind"] == "t1":
                comment_body = item["data"].get("body", "")
                # Filter out deleted or removed comments
                if (
                    comment_body
                    and comment_body != "[deleted]"
                    and comment_body != "[removed]"
                ):
                    extracted_comments.append(comment_body)

        return {
            "post_title": post_title,
            "comments": extracted_comments[:max_comments],
            "error": None,
        }

    except Exception as e:
        return {"error": str(e)}
