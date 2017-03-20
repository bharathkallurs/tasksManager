# import logging as log

# from datetime import datetime
from db.task_db import TaskTable as tt
from flask import Flask, request
from logger.loggen import set_log_params
from utils.utils import validate_date, get_response_json

app = Flask(__name__)


@app.route('/')
def hello_world():
    # Change it to a relevant home page
    return 'Hello World!'

@app.route('/task/add', methods=['POST'])
def task_add():
    """
    Adding tasks to
    :return: Success message after addition of task
    """
    task_details = request.get_json()
    print task_details
    task_name = str(task_details['task_name'])
    print task_name
    end_date = str(task_details['end_date'])
    task_end_date, msg = validate_date(end_date)
    print task_end_date
    if not task_end_date:
        return get_response_json(403, msg)

    task_end_date = task_end_date.replace(hour=11, minute=59, second=59)
    print task_end_date
    # task_create_date = datetime.now()
    task_description = str(task_details['task_description'])
    print task_description
    task_owner = str(task_details['task_owner'])
    print task_owner

    status, msg = tt.add_task(task_name=task_name,
                              task_end_date=task_end_date,
                              task_owner=task_owner,
                              task_description=task_description)
    return get_response_json(status, msg)

@app.route('/task/get/<name>', methods=['GET'])
def task_get(name=None):
    """
    Get a particular task matching the name
    :param name: Name of the task
    :return: JSON for task
    """
    if not name:
        return get_response_json(404, "Name is necessary. /task/get/<name>")
    status, result = tt.get_task(name=name)
    return get_response_json(status, result)

@app.route('/task/list', methods=['GET'])
def task_list():
    """
    Get a list of all tasks
    :return: JSON of all tasks
    """
    print "started task listing"
    status, result = tt.list_all_tasks()
    return get_response_json(status, result)

@app.route('/task/list_before/<date>', methods=['GET'])
def task_list_before_date(date):
    """
    Get a list of all tasks before a given date
    :return: List of all tasks before date
    """
    print "task list before"
    filter_date, msg = validate_date(date)
    print "filter date and msg ", filter_date, msg
    if not filter_date:
        return get_response_json(403, "date not in YYYY-MM-DD format")
    filter_date = filter_date.replace(hour=11, minute=59, second=59)
    status, result = tt.list_based_on_date(qdate=filter_date)
    return get_response_json(status, result)

@app.route('/task/list_after/<date>', methods=['GET'])
def task_list_after_date(date):
    """
    Get a list of all tasks after a given date
    :return: List of all tasks after date
    """
    filter_date, msg = validate_date(date)
    print "filter date and msg ", filter_date, msg
    if not filter_date:
        return get_response_json(403, "date not in YYYY-MM-DD format")
    filter_date = filter_date.replace(hour=11, minute=59, second=59)
    status, result = tt.list_based_on_date(qdate=filter_date, after=True)
    return get_response_json(status, result)

@app.route('/task/delete/<name>', methods=['GET'])
def task_delete(name=None):
    """
    Delete a particular task
    :param name: Name of the task to be deleted
    :return: Deletion status of the task
    """
    if not name:
        return (403, "Need a task name to delete. /task/delete/<name>")
    status, result = tt.delete_task(name=name)
    return get_response_json(status, result)

@app.route('/task/update/<task_id>', methods=['PUT'])
def task_update(task_id=None):
    """
    Update a particular task
    :param task_id: Id of the task
    :return: Message of completion on task update
    """
    task_details = request.get_json()
    task_name = str(task_details['task_name'])
    print task_name
    end_date = str(task_details['end_date'])
    task_end_date, msg = validate_date(end_date)
    # print task_end_date
    if not task_end_date:
        return get_response_json(403, msg)

    task_end_date = task_end_date.replace(hour=11, minute=59, second=59)
    print task_end_date
    # task_create_date = datetime.now()
    task_description = str(task_details['task_description'])
    print task_description
    task_owner = str(task_details['task_owner'])
    print task_owner

    status, msg = tt.update_task(task_id=int(task_id),
                                 task_name=task_name,
                                 task_end_date=task_end_date,
                                 task_description=task_description,
                                 task_owner=task_owner)
    return get_response_json(status, msg)


if __name__ == '__main__':
    # Setting logger. log level is DEBUG
    # To change enter level = # log.info or log.WARNING etc.
    # set_log_params(level=# log.info)
    # # log.info("Starting tasks app")
    print "starting here"
    app.run()
