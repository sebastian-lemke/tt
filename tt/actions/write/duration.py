from tt.dateutils import dateutils
from datetime import datetime
from tt.actions.write import start, note, stop

def action_duration(colorizer, name, time_input, content):
    # 1. Calculate the start time based on duration
    start_time_iso = dateutils.get_past_datetime_iso(time_input)
    
    # 2. Trigger the sequence of actions
    # We pass the calculated start time to action_start
    start.action_start(colorizer, name, time=start_time_iso)
    
    
    end_time_iso = dateutils.local_to_utc(datetime.now()).isoformat() + 'Z'
    
    # Add the note
    note.action_note(colorizer, content)
    
    # Stop the activity at the current time (Now)
    stop.action_stop(colorizer, time=end_time_iso)