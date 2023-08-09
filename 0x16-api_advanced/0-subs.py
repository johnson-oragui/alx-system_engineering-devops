#!/usr/bin/python3
"""Script that queries subscribers on a given Reddit subreddit."""
import requests


def number_of_subscribers(subreddit):
    """Return the total number of subscribers on a given subreddit."""
    # Construct the URL for the subreddit's about page in JSON format
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    # Define headers for the HTTP request, including User-Agent
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }

    # Send a GET request to the subreddit's about page
    response = requests.get(url, headers=headers, allow_redirects=False)

    # Check if the response status code indicates a not-found error (404)
    if response.status_code == 404:
        return 0

    # Parse the JSON response and extract the 'data' section
    results = response.json().get("data")

    # Return the number of subscribers from the 'data' section
    return results.get("subscribers")
