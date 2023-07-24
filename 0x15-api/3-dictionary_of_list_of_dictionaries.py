#!/usr/bin/python3
""" Exports to-do list information of all employees to JSON format.
"""

import requests
import json


def export_all_employees_todos():
    url = "https://jsonplaceholder.typicode.com/"
    all_employees_data = {}

    # Fetch all users
    users_response = requests.get(url + "users")
    if users_response.status_code != 200:
        print("Error: Failed to fetch user data.")
        return

    users_data = users_response.json()

    # Fetch todos for each employee
    for user in users_data:
        employee_id = user['id']
        employee_name = user['name']

        todos_response = requests.get(url + "todos", params={"userId": employee_id})
        if todos_response.status_code != 200:
            print("Error: Failed to fetch TODO list for employee ID:", employee_id)
            continue

        todos_data = todos_response.json()
        employee_todos = [
            {
                "username": employee_name,
                "task": task['title'],
                "completed": task['completed']
            }
            for task in todos_data
        ]

        all_employees_data[str(employee_id)] = employee_todos

    # Export to JSON
    json_filename = "todo_all_employees.json"
    with open(json_filename, mode='w') as jsonfile:
        json.dump(all_employees_data, jsonfile, indent=4)

    print("Data exported to:", json_filename)

if __name__ == "__main__":
    export_all_employees_todos()
