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
    # Base URL for the JSONPlaceholder API
    url = "https://jsonplaceholder.typicode.com/"

    # Get the employee information using the provided employee ID
    employee_id = sys.argv[1]
    user = requests.get(url + "users/{}".format(employee_id)).json()

    # Get the to-do list for the employee using the provided employee ID
    params = {"userId": employee_id}
    todos = requests.get(url + "todos", params=params).json()

    # Create a CSV file with the employee ID as the filename
    with open("{}.csv".format(employee_id), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # Write header row to the CSV file
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS",
                        "TASK_TITLE"])

        # Write each to-do list item as a row in the CSV file
        for todo in todos:
            writer.writerow([user.get("id"), user.get("username"),
                            todo.get("completed"), todo.get("title")])

    # Print a success message after writing the CSV
    print("Data exported to {}.csv".format(employee_id))
