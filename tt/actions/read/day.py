from __future__ import print_function

from collections import defaultdict

from tt.actions.read import status
from tt.actions.utils import reportingutils
from tt.colors.colors import Colorizer
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import *
from datetime import datetime, timedelta, date


def action_day(colorizer, date):
    # Display all entries of today...
    # ... first all entries which has been done (with 'end' entry)...


    sep = '|'
    sep2 = ' | '

    data = get_data_store().load()
    work = data['work']
    report = defaultdict(lambda: {'sum': timedelta(), 'notes': '', 'weekday': '', 'start_time': None, 'end_time': None})

    # date parameter for selecting specific date
    if date is None:
        # today for current workday display
        date = get_today_date()
    elif len(date) < 3:
        # assuming that if date is less then 3, then it is a timedelta in days
        today_date = to_datetime_obj(get_today_date())
        calc_date = today_date.__add__(timedelta(int(date)))
        date = reportingutils.extract_day(to_date(calc_date))
    else:
        # assuming YYYY-MM-DD string
        date_from_param = to_date(to_datetime_obj(date))
        date = reportingutils.extract_day(date_from_param)


    if date == get_today_date():
        print('Displaying all entries for TODAY: ', sep='')
    else:
        print('Displaying all entries for day: ', date, sep='')
    print()


    print('day', sep, 'date', sep, 'activity', sep, 'start', sep, ' end ', sep, 'duration', sep, 'description')
    # print('Day |    Date    | Prj | Start |  End  | Time  | Description')
    print('-' * 64)

    for item in work:
        workday = reportingutils.extract_day(item['start'])

        if (workday == date and 'end') in item:
            activity = item['name']
            weekday = reportingutils.extract_day_custom_formatter(item['start'], '%a')
            start_time = parse_isotime(item['start'])
            end_time = parse_isotime(item['end'])
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            report[workday]['sum'] += duration
            # added notes_delimiter
            notes = reportingutils.get_notes_from_workitem(item)
            report[workday]['start_time'] = get_min_date(report[workday]['start_time'], start_time)
            report[workday]['end_time'] = get_max_date(report[workday]['end_time'], end_time)
            report[workday]['weekday'] = reportingutils.extract_day_custom_formatter(item['start'], '%a')
            # local time
            start_time_local = utc_to_local(start_time).strftime("%H:%M")
            end_time_local = utc_to_local(end_time).strftime("%H:%M")
            duration_local = format_time(duration, colorizer)

            print(weekday, sep2, workday, sep2, activity, sep2, start_time_local, sep2, end_time_local, sep2, duration_local,
                  sep2, notes, sep="")    
    print('-' * 64)
    for date, details in sorted(report.items()):
        weekday = reportingutils.extract_day_custom_formatter(item['start'], '%a')
        # start_time = utc_to_local(details['start_time']).strftime("%H:%M")
        # end_time = utc_to_local(details['end_time']).strftime("%H:%M")
        # break_duration = get_break_duration(details['start_time'], details['end_time'], details['sum'])
        print(weekday,'|', date, '| Total working time: \u03A3', format_time(details['sum'], colorizer))
    #  ...Display secondly the current working entry (no 'end' in entry)
    print()
    for item in work:
        day = reportingutils.extract_day(item['start'])
        colorizer = Colorizer(True)
        if day == get_today_date() and not 'end' in item:
            status.action_status(colorizer)


def get_break_duration(start_time, end_time, net_work_duration):
    total_work_duration = end_time - start_time
    return total_work_duration - net_work_duration


def format_time(duration_timedelta, colorizer):
    return format_time_seconds(duration_timedelta.seconds, colorizer)


def format_time_seconds(duration_secs, colorizer):
    hours, rem = divmod(duration_secs, 3600)
    mins, secs = divmod(rem, 60)
    formatted_time_str = str(hours).rjust(2, str('0')) + ':' + str(mins).rjust(2, str('0'))
    if hours >= 8:
        return colorizer.green(formatted_time_str)
    else:
        # return colorizer.red(formatted_time_str)
        return colorizer.green(formatted_time_str)

def get_min_date(date_1, date_2):
    if date_1 is None:
        date_1 = parse_isotime('2099-01-01T00:00:00.000001Z')
    return date_1 if date_1 < date_2 else date_2


def get_max_date(date_1, date_2):
    if date_1 is None:
        date_1 = parse_isotime('2015-01-01T00:00:00.000001Z')
    return date_1 if date_1 > date_2 else date_2

