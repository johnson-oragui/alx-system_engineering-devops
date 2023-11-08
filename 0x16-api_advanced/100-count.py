#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""

import requests
import sys


def count_words(subreddit, word_list, instances={}, after=None, count=0):
    base_url = "https://www.reddit.com"

    end_point = f"/r/{subreddit}/hot/.json"

    headers = {"User-Agent": "hp:0x16.api.advanced:v1.0.0"}

    params = {"limit": 100}
    if after:
        params['after'] = after
        params['count'] = count

    response = requests.get(base_url + end_point,
                            headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        after = data.get('after')
        count = data.get('dist')
        posts = data['data']['children']

        title = [post['data']['title'] for post in posts]

        word_count = count_words_in_title(title, word_list)

        for word in word_count:
            instances[word] = instances.get(word, 0) + word_count[word]

        if after:
            count_words(subreddit, word_list, instances, after, count)
    else:
        print("Request failed with status code: {}".format(response.status_code))  # noqa

    sorted_instances = sorted(instances.items(),
                              key=lambda item: (-item[1], item[0]))

    for word, count in sorted_instances:
        print("{}: {}".format(word, count))
    return instances


def count_words_in_title(titles, word_list):
    word_count = {}
    for title in titles:
        title = title.lower()
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
