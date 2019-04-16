import datetime


def delivery_date(length):
    now_date = datetime.datetime.today()
    return now_date + datetime.timedelta(days=length)