#!/usr/bin/python3
"""
Function to count words in all hot posts of a given Reddit subreddit.
"""
import requests
import sys


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """
    Recursive function that queries the Reddit API, parses the title of all
        hot articles, and prints a sorted count of given keywords
    """
    base_url = "https://www.reddit.com"
    # print statement for debugging
    # print(f"{after = }")

    end_point = f"/r/{subreddit}/hot/.json"

    headers = {"User-Agent": "hp:0x16.api.advanced:v1.0.0"}

    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    response = requests.get(base_url + end_point,
                            headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code == 200:
        data = response.json()

        after = data['data']['after']
        count = data.get('dist')
        posts = data['data']['children']

        title = [post['data']['title'] for post in posts]

        word_count = count_words_in_title(title, word_list)

        for word in word_count:
            instances[word] = instances.get(word, 0) + word_count[word]

        if after:
            count_words(subreddit, word_list, instances, after, count)
    else:
        print()
        return

    if len(instances) == 0:
        print()
        return
    # print statement for debugging
    # print(f"{after = }")

    sorted_instances = sorted(instances.items(),
                              key=lambda item: (-item[1], item[0]))

    for word, count in sorted_instances:
        print("{}: {}".format(word, count))
    return instances


def count_words_in_title(titles, word_list):
    """
    Count the words in the titles
    """
    # create an empty dictionary to store counted words and its occurrence
    word_count = {}

    for title in titles:
        words = title.split()

        for word in words:
            if word in word_list:
                word_count[word] = word_count.get(word, 0) + 1
    return word_count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))  # noqa
    else:
        result = count_words(sys.argv[1], [x for x in sys.argv[2].split()])
