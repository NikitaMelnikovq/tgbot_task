# Telegram Bot Project

## Overview
This Python project utilizes Python 3.11 and various modules listed in the `requirements.txt` file to create a Telegram bot. The bot interacts with users and manages tasks stored in a database.

## Table Structure
There are two tables in the database:

### Tasks Table
- **id**: Unique identifier for each task.
- **user_id**: User ID associated with the task.
- **title**: Title of the task.
- **description**: Description of the task.

### Users Table
- **user_id**: Unique identifier for each user. This field is of type BIGINT to accommodate larger user IDs from Telegram.

## Usage

1. Install the required Python modules:
   ```bash
   pip install -r requirements.txt