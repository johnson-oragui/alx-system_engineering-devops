#!/usr/bin/python3
"""
Exports to-do list information for a given employee ID to CSV format.

This script takes an employee ID as a command-line argument and exports
the corresponding user information and to-do list to a CSV file.
"""

import csv
import requests
import sys


if __name__ == "__main__":
    # Get the employee ID from the command-line argument
    user_id = sys.argv[1]

    # Base URL for the JSONPlaceholder API
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch user information using the provided employee ID
    user = requests.get(url + "users/{}".format(user_id)).json()
    username = user.get("username")

    # Fetch the to-do list for the employee using the provided employee ID
    params = {"userId": user_id}
    todos = requests.get(url + "todos", params).json()

    # Create a CSV file with the employee ID as the filename
    with open("{}.csv".format(user_id), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # Write header row to the CSV file
        writer.writerow(["User ID", "Username", "Completed", "Title"])

        # Write each to-do list item as a row in the CSV file
        for t in todos:
            writer.writerow([user_id, username, t.get("completed"),
                            t.get("title")])
