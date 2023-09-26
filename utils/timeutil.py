import datetime


async def days_by_range(start, end):
    start_date = datetime.datetime.strptime(str(start), "%Y%m%d")
    end_date = datetime.datetime.strptime(str(end), "%Y%m%d")

    delta = end_date - start_date
    return [
        (start_date + datetime.timedelta(days=i)).strftime("%Y%m%d")
        for i in range(delta.days + 1)
    ]


async def dayrange(range: int):
    today = datetime.datetime.now().strftime("%Y%m%d")
    to = (datetime.datetime.now() + datetime.timedelta(days=range - 1)).strftime(
        "%Y%m%d"
    )

    return today, to


async def timetable_range():
    today = datetime.date.today()
    weekday = today.weekday()

    start_date = today - datetime.timedelta(days=weekday)
    if weekday > 4:
        start_date += datetime.timedelta(days=7)

    end_date = start_date + datetime.timedelta(days=4)

    return start_date, end_date


async def month_range(month: int = None):
    today = datetime.date.today()
    if month is None:
        start_date = today
        month = today.month
    else:
        start_date = datetime.date(today.year, month, 1)

    if month == 12:
        end_date = datetime.date(today.year + 1, 1, 1) - datetime.timedelta(days=1)

    else:
        end_date = datetime.date(today.year, month + 1, 1) - datetime.timedelta(days=1)

    return start_date, end_date
