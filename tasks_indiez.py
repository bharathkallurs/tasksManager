import logging as log

from db.task_db import TaskTable as tt
from flask import Flask, request, render_template
from logger.loggen import set_log_params, move_latest_log_to_persistent_file
from utils.utils import validate_date, get_response_json

app = Flask(__name__)


@app.route('/')
def home():
    # Change it to a relevant home page
    return render_template("index.html")

@app.route('/doc')
def documentation():
    # FAQ page for the usage of the app
    return render_template("docs.html")

@app.route('/task/add', methods=['POST'])
def task_add():
    """
    Adding tasks to
    :return: Success message after addition of task
    """
    task_details = request.json['task']
    task_name = str(task_details['task_name'])
    end_date = str(task_details['task_end_date'])
    task_end_date, msg = validate_date(end_date)
    if not task_end_date:
        return get_response_json(403, msg)

    task_end_date = task_end_date.replace(hour=23, minute=59, second=59)
    task_description = str(task_details['task_description'])
    task_owner = str(task_details['task_owner'])

    status, msg = tt.add_task(task_name=task_name,
                              task_end_date=task_end_date,
                              task_owner=task_owner,
                              task_description=task_description)
    return get_response_json(status, msg)

@app.route('/task/get/<task_id>', methods=['GET'])
def task_get(task_id=None):
    """
    Get a particular task matching the name
    :param task_id: task id of the task
    :return: JSON for task
    """
    if not task_id:
        return get_response_json(404, "task_id is necessary. "
                                      "/task/get/<task_id>")
    status, result = tt.get_task(task_id=int(task_id))
    return get_response_json(status, result)

@app.route('/task/list', methods=['GET'])
def task_list():
    """
    Get a list of all tasks
    :return: JSON of all tasks
    """
    status, result = tt.list_all_tasks()
    return get_response_json(status, result)

@app.route('/task/list_before/<date>', methods=['GET'])
def task_list_before_date(date):
    """
    Get a list of all tasks ending before a given date
    :return: JSON of all tasks ending before date
    """
    filter_date, msg = validate_date(date)
    if not filter_date:
        return get_response_json(403, "date not in YYYY-MM-DD format")
    filter_date = filter_date.replace(hour=23, minute=59, second=59)
    status, result = tt.list_based_on_date(qdate=filter_date)
    return get_response_json(status, result)

@app.route('/task/list_after/<date>', methods=['GET'])
def task_list_after_date(date):
    """
    Get a list of all tasks created after a given date
    :return: List of all tasks created after date
    """
    filter_date, msg = validate_date(date)
    if not filter_date:
        return get_response_json(403, "date not in YYYY-MM-DD format")
    filter_date = filter_date.replace(hour=23, minute=59, second=59)
    status, result = tt.list_based_on_date(qdate=filter_date, after=True)
    return get_response_json(status, result)

@app.route('/task/list_bw_cr_dt/<st_date>/<en_date>', methods=['GET'])
def task_list_between_create_date(st_date, en_date):
    """
    Get a list of all tasks created between a date range
    :param st_date: start date
    :param en_date: end date
    :return: List of all tasks created between range of the date
    """
    filter_st_date, msg = validate_date(st_date)
    if not filter_st_date:
        return get_response_json(403, "start date not in YYYY-MM-DD format")
    filter_st_date = filter_st_date.replace(hour=00, minute=01, second=01)

    filter_en_date, msg = validate_date(en_date)
    if not filter_en_date:
        return get_response_json(403, "end date not in YYYY-MM-DD format")
    filter_en_date = filter_en_date.replace(hour=23, minute=59, second=59)
    status, result = tt.list_based_on_date(qdate=filter_st_date,
                                           pdate=filter_en_date,
                                           after=True)
    return get_response_json(status, result)

@app.route('/task/delete/<task_id>', methods=['GET'])
def task_delete(task_id=None):
    """
    Delete a particular task
    :param task_id: task_id of the task to be deleted
    :return: Deletion status of the task
    """
    if not task_id:
        return (403, "Need a task name to delete. /task/delete/<name>")
    status, result = tt.delete_task(task_id=int(task_id))
    return get_response_json(status, result)

@app.route('/task/update/<task_id>', methods=['PUT'])
def task_update(task_id=None):
    """
    Update a particular task
    :param task_id: Id of the task
    :return: Message of completion on task update
    """
    if not task_id:
        return get_response_json(403, "task id necessary. "
                                      "/task/update/<task-id>")
    task_details = request.json['task']
    task_name = str(task_details['task_name'])
    end_date = str(task_details['task_end_date'])
    task_end_date, msg = validate_date(end_date)
    if not task_end_date:
        return get_response_json(403, msg)

    task_end_date = task_end_date.replace(hour=23, minute=59, second=59)
    task_description = str(task_details['task_description'])
    task_owner = str(task_details['task_owner'])

    status, msg = tt.update_task(task_id=int(task_id),
                                 task_name=task_name,
                                 task_end_date=task_end_date,
                                 task_description=task_description,
                                 task_owner=task_owner)
    return get_response_json(status, msg)


if __name__ == '__main__':
    # Setting logger. log level is INFO
    # To change enter level = # log.DEBUG or log.WARNING etc.
    set_log_params(level=log.INFO)
    log.info("Starting tasks app")
    app.run()
    # move latest.log to tasker_<timebased>.log
    move_latest_log_to_persistent_file()
