#!/usr/bin/python3
"""
Script that queries subscribers on a given Reddit subreddit.
"""
import requests
import sys


def number_of_subscribers(subreddit):
    """Return the total number of subscribers on a given subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        res_json = response.json()
        data = res_json.get('data')
        subscribers = data.get('subscribers')
        return subscribers
    else:
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print("{:d}".format(number_of_subscribers(sys.argv[1])))
