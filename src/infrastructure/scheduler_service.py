from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import Callable

class SchedulerService:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def schedule_daily_job(self, job: Callable, time: str) -> None:
        """
        Schedule a job to run daily at a specific time
        
        Args:
            job: The function to execute
            time: Time in "HH:MM" format (24-hour)
        """
        hour, minute = time.split(":")
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone="local"
        )
        
        self.scheduler.add_job(
            job,
            trigger=trigger,
            name=f"Daily job at {time}"
        )

    def start(self) -> None:
        """Start the scheduler"""
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown() 