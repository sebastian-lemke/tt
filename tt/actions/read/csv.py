from __future__ import print_function

from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import *
from tt.actions.utils import reportingutils


def action_csv():
    delim = ','
    data = get_data_store().load()
    work = data['work']

    #add csv header
    print('"project-name"',delim,'"duration"',delim,'"start-date"',delim,'"end-date"',delim,'"comments"',sep='')

    for item in work:
        if 'end' in item:
            notes = reportingutils.get_notes_from_workitem(item)
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            duration_total = reportingutils.remove_seconds(duration)
            date = reportingutils.extract_day(item['start'])
            name = item['name']
            start = format_csv_time(item['start'])
            # customization
            start_date = date + ' ' + start
            end = format_csv_time(item['end'])
            end_date = date + ' ' + end
            tags = ''
            if 'tags' in item:
                tags = item['tags']

            print_elements(name, duration_total, start_date, end_date, notes, tags, delim)


def print_elements(name, total_duration, start_date, end_date, notes, tags, delim):
    print(name,delim,total_duration,delim,start_date,delim,end_date,delim,notes,sep='')


def format_csv_time(somedatetime):
    local_dt = isotime_utc_to_local(somedatetime)
    return local_dt.strftime('%H:%M')
