#!/usr/bin/python3
"""
Exports to-do list information of all employees to JSON format.

This script fetches the user information and to-do lists for all employees
from the JSONPlaceholder API and exports the data to a JSON file.
"""

import json
import requests


if __name__ == "__main__":
    # Base URL for the JSONPlaceholder API
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch the list of all users (employees)
    users = requests.get(url + "users").json()

    # Create a dictionary containing to-do list information of all employees
    params = {"userId": u.get("id")}

    data_to_export = {
        u.get("id"): [
            {
                "task": t.get("title"),
                "completed": t.get("completed"),
                "username": u.get("username")
            }
            for t in requests.get(url + "todos", params).json()
        ]
        for u in users
    }

    # Write the data to a JSON file
    with open("todo_all_employees.json", "w") as jsonfile:
        json.dump(data_to_export, jsonfile, indent=4)
