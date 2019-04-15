from datetime import datetime


def delivery_date(length):
    now_date = datetime.today()
    day_sum = now_date.day + length
    if day_sum > 30:
        delivery_date = now_date.replace(month=now_date.month+1, day=(day_sum-30))
    else:
        delivery_date = now_date.replace(day=now_date.day + length)
    return delivery_date