#!/usr/bin/python3
"""
Script to count words in all hot posts of a given Reddit subreddit.
"""

import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """
    Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (dict): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    # Construct the URL for the subreddit's hot posts in JSON format
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)

    # Define headers for the HTTP request, including User-Agent
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }

    # Define parameters for the request, including pagination and limit
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    # Send a GET request to the subreddit's hot posts page
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    try:
        # Parse the JSON response and check for a not-found error
        results = response.json()
        if response.status_code == 404:
            raise Exception
    except Exception:
        # Handle errors or empty results
        print("")
        return

    # Extract data from the JSON response
    results = results.get("data")
    after = results.get("after")
    count += results.get("dist")

    # Iterate through the posts and count occurrences of words
    for c in results.get("children"):
        # Extract the title of the current post,
        #   convert to lowercase, and split into words
        title = c.get("data").get("title").lower().split()

        # Iterate through each word in the word_list
        for word in word_list:
            # If the lowercase version of
            #   the current word is present in the title
            if word.lower() in title:
                # Count the occurrences of the current word in the title
                times = len([t for t in title if t == word.lower()])

                # If an entry for the word exists in the instances dictionary
                if instances.get(word) is None:
                    # If not, initialize an entry with the times value
                    instances[word] = times
                else:
                    # else add the times value to the existing count
                    instances[word] += times

    # If no more pages, print the word count results
    if after is None:
        # Check if the instances dictionary is empty
        if len(instances) == 0:
            # Print an empty line and return if no word counts were found
            print("")
            return
        # Sort the instances dictionary by values in descending order,
        #   then by keys
        instances = sorted(instances.items(), key=lambda kv: (-kv[1], kv[0]))

        # Print the sorted word counts in the format "word: count"
        [print("{}: {}".format(k, v)) for k, v in instances]
    else:
        # If more pages, recursively call the function with updated parameters
        count_words(subreddit, word_list, instances, after, count)
