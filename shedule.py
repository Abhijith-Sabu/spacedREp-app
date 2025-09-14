from datetime import datetime, timedelta, time as dtime
from apscheduler.schedulers.background import BackgroundScheduler
from send_email import send_email
import atexit

# Global scheduler instance
scheduler = BackgroundScheduler()
scheduler.start()

# Ensure scheduler shuts down properly
atexit.register(lambda: scheduler.shutdown())

def schedule_reminders(task_name, intervals):
    """Schedule email reminders for a task at specified intervals."""
    start = datetime.now()
    scheduled_times = []
    
    for day_offset in intervals:
        future_date = start + timedelta(days=day_offset)
        run_time = datetime.combine(future_date, dtime(hour=9, minute=0))
        
        # Add job to scheduler
        scheduler.add_job(
            send_email,
            "date",
            run_date=run_time,
            args=[f"Reminder: {task_name}"],
            id=f"task_{task_name}_{day_offset}",  # Unique job ID
            replace_existing=True
        )
        
        scheduled_times.append(run_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    return scheduled_times