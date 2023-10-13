import os

from celery import shared_task
import requests

from datetime import datetime, timedelta, timezone

from main.models import Habit

@shared_task
def send_reminder():
    """Рассылает пользователям напоминания о наступлении времени для выполнения привычки """
    now = datetime.now(timezone.utc)
    token = os.getenv('TELEGRAM_TOKEN')

    for habit in Habit.objects.all():
        message = f'Пришло время выполнить привычку: {habit.action} в {habit.time.strftime("%H:%M")} в {habit.place.title}'
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={habit.created_by.chat_id}&text={message}"
        if habit.last_reminder:  # если напоминание не первое
            if habit.last_reminder <= now - timedelta(days=habit.period):
                requests.get(url)
                habit.last_reminder = now
                habit.save()
        else:  # если напоминание первое
            if habit.time <= now.time():
                requests.get(url)
                habit.last_reminder = now
                habit.save()
