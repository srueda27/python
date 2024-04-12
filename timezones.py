from datetime import datetime, timedelta
import pytz


def schedule_task_across_timezones(tasks):
    """
    Schedules tasks across different time zones within working hours.

    Args:
        tasks (list of dict): A list where each item is a dict with keys 'task_name', 'preferred_start_time', and 'timezone'.

    Returns:
        list of dict: A list of tasks with updated 'scheduled_start_time' to fit within working hours.
    """
    scheduled_tasks = []
    working_hours_start = 9
    working_hours_end = 17

    for task in tasks:
        preferred_time = datetime.strptime(task['preferred_start_time'], '%Y-%m-%d %H:%M:%S')
        preferred_time_tz = pytz.timezone(task['timezone'])
        preferred_time = preferred_time_tz.localize(preferred_time)

        utc_time = preferred_time.astimezone(pytz.utc)
        now_utc = datetime.now(pytz.utc)

        # Adjust task time to ensure it's within working hours and in the future
        if utc_time.hour < working_hours_start:
            utc_time = utc_time.replace(hour=working_hours_start, minute=0, second=0)
        elif utc_time.hour >= working_hours_end:
            utc_time += timedelta(days=1)
            utc_time = utc_time.replace(hour=working_hours_start, minute=0, second=0)

        if utc_time < now_utc:
            utc_time += timedelta(days=1)

        # Convert back to local timezone
        task_time_local = utc_time.astimezone(preferred_time_tz)

        scheduled_tasks.append({
            'task_name': task['task_name'],
            'scheduled_start_time': task_time_local.strftime('%Y-%m-%d %H:%M:%S'),
            'timezone': task['timezone']
        })

    # Sort tasks by scheduled time
    sorted_tasks = sorted(scheduled_tasks, key=lambda x: x['scheduled_start_time'])

    return sorted_tasks

# Example of usage
tasks = [
    {'task_name': 'Code Review', 'preferred_start_time': '2024-03-20 14:00:00', 'timezone': 'UTC'},
    {'task_name': 'Design Discussion', 'preferred_start_time': '2024-03-20 16:00:00', 'timezone': 'America/Los_Angeles'},
]
print(schedule_task_across_timezones(tasks))