import datetime as dt


def get_elk_date_format_from_date(sp_date: dt.datetime, time_zone):
    date_format = '%Y-%m-%dT%H:%M:%S.' + time_zone
    return sp_date.strftime(date_format)


def get_date_from_elk_date_format(elk_date_format: str):
    time_zone = elk_date_format[-4:]
    elk_date_format = elk_date_format[:-5]

    ret_date = dt.datetime.strptime(elk_date_format, '%Y-%m-%dT%H:%M:%S')
    return ret_date, time_zone


def get_date_after(current_date: dt.datetime, no_of_days: int):
    return current_date + dt.timedelta(days=no_of_days)
