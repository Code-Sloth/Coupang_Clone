from django import template
from django.utils import timezone
from datetime import timedelta
import datetime

register = template.Library()

def format_time_since(value):
    now = timezone.now()

    diff = now - value
    if diff < timedelta(minutes=1):
        return f'방금 전'
    elif diff < timedelta(hours=1):
        return f'{diff.seconds // 60}분 전'
    elif diff < timedelta(days=1):
        return f'{diff.seconds // 3600}시간 전'
    else:
        return value.strftime('%Y-%m-%d')

def discount_price(price, discount):
    return round((int(price) * (1 - int(discount) / 100)) / 10) * 10

def get_future_date(days):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=days)
    tomorrow = today + datetime.timedelta(days=1)
    day_of_week = ['월', '화', '수', '목', '금', '토', '일']
    tomo = day_of_week[tomorrow.weekday()]
    future = day_of_week[future_date.weekday()]

    if days == 1:
        return f'내일({tomo}) {tomorrow.month}/{tomorrow.day} 도착 보장'
    else:
        return f'{future}요일 {future_date.month}/{future_date.day} 도착 예정'

def discount_tenth(price):
    return str(int(price)//10)

def total_star(star):
    for i in range(5):
        if i <= star < i+0.5:
            star_rating = i
        elif i+0.5 <= star < i+1:
            star_rating = i+0.5
    return str(int(star_rating*20))

register.filter('format_time_since', format_time_since)
register.filter('discount_price', discount_price)
register.filter('get_future_date', get_future_date)
register.filter('discount_tenth', discount_tenth)
register.filter('total_star', total_star)
