from tt.exceptz.exceptz import AlreadyOn
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import formatted_str_for_isotime_str

def action_start(colorizer, name, time):
    data = get_data_store().load()
    work = data['work']

    if work and 'end' not in work[-1]:
        raise AlreadyOn("You are already working on %s. Stop it or use a "
                        "different sheet." % (colorizer.yellow(work[-1]['name']),))

    assure_no_timebox_overlap(colorizer, time, work)

    entry = {
        'name': name,
        'start': time,
    }

    work.append(entry)
    get_data_store().dump(data)

    print('Started working on ' + colorizer.green(name) + ' at ' +
           colorizer.yellow(formatted_str_for_isotime_str(time, '%H:%M')) + '.')


def assure_no_timebox_overlap(colorizer, time, all_timeboxes):
    for timebox in all_timeboxes:
        if timebox['start'] <= time <= timebox['end']:
            print(timebox)
            offending_desc = '; '.join(timebox['notes']) if 'notes' in timebox else 'missing description'
            raise AlreadyOn("The starting point you've entered overlaps with a preexisting timebox: "
                            "[ %s ] This is disallowed..." % colorizer.yellow(str(offending_desc)))
