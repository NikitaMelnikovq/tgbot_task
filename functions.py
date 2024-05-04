from pypika import Query, Table
from db import connect
from datetime import datetime
import logging
import sys
import traceback

def create_error_log(error):
    try:
        with open(f"{datetime.now()}.txt", "w") as file:
            traceback.print_exc(file=file)
            file.write(str(error) + "\n")
    except Exception as e:
        logging.error(f"Error occurred while creating error log: {e}")

async def get_tasks(user_id):
    result = {}
    try:
        connection = await connect()
        tasks = Table("tasks")
        query = Query.from_(tasks).select('*').where(tasks.user_id == user_id)
        task_list = await connection.fetch(str(query))
        for task in task_list:
            title = task.get("title")
            description = task.get("description", "")
            result[str(title)] = str(description)
    except Exception as e:
        create_error_log(e)
    finally:
        await connection.close()

    return result

async def check_user(user_id):
    try:
        connection = await connect()
        users = Table("users")
        query = Query.from_(users).select(users.user_id)
        result = await connection.fetch(str(query))

        users_ids = [user_id.get("user_id") for user_id in result]

        return 1 if user_id in users_ids else 0

    except Exception as e:
        create_error_log(e)
    finally:
        await connection.close()

async def create_task(user_id, task_title, task_description):
    error = 0
    try:
        connection = await connect()
        tasks = Table("tasks")
        query = Query.into(tasks).columns('user_id', 'title', 'description').insert(user_id, task_title, task_description)
        await connection.execute(str(query))
    except Exception as e:
        create_error_log(e)
        error = 1
    finally:
        await connection.close()
    return error

async def add_user(user_id):
    try:
        connection = await connect()
        users = Table("users")
        query = Query.into(users).insert(user_id)
        await connection.execute(str(query))
    except Exception as e:
        create_error_log(e)
    finally:
        await connection.close()

async def clear_task_list(user_id):
    try:
        connection = await connect()
        tasks = Table("tasks")
        query = Query.from_(tasks).where(tasks.user_id == user_id).delete()
        await connection.execute(str(query))
    except Exception as e:
        create_error_log(e)
    finally:
        await connection.close()
