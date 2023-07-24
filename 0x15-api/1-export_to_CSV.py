#!/usr/bin/python3

import requests
import csv
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

    # Export to CSV
    csv_filename = "{}.csv".format(employee_id)
    with open(csv_filename, mode='w', newline='') as csvfile:
        fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for task in todos_data:
            writer.writerow({
                "USER_ID": employee_id,
                "USERNAME": employee_name,
                "TASK_COMPLETED_STATUS": "completed" if task['completed'] else "not completed",
                "TASK_TITLE": task['title']
            })

    print("Data exported to:", csv_filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py EMPLOYEE_ID")
    else:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
