#!/usr/bin/pyth0n3
"""Returns to-do list information for a given employee ID."""

import requests
import sys

def get_employee_todo_progress(employee_id):
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch employee information
    user_response = requests.get(url + "users/{}".format(employee_id))
    if user_response.status_code != 200:
        print("Error: Employee ID not found.")
        return

    user_data = user_response.json()
    employee_name = user_data['name']

    # Fetch todos for the employee
    todos_response = requests.get(url + "todos", params={"userId": employee_id})
    if todos_response.status_code != 200:
        print("Error: Failed to fetch TODO list.")
        return

    todos_data = todos_response.json()
    total_tasks = len(todos_data)
    done_tasks = [task for task in todos_data if task['completed']]

    # Display employee TODO list progress
    print("Employee {} is done with tasks({}/{}):".format(employee_name, len(done_tasks), total_tasks))
    for task in done_tasks:
        print("\t{} {}".format(task['title'], "(completed)"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py EMPLOYEE_ID")
    else:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)

