CREATE_DEVICE = """
insert into devices (user_id, name, last_activity) 
values ($1, $2, CURRENT_TIMESTAMP)
returning id, name, revoked, last_activity
"""

GET_DEVICES = """
select id, name, revoked, last_activity
from devices
where user_id = $1
"""

GET_DEVICE = GET_DEVICES + ' and id = $2'

ACTIVITY_DEVICE = """
update devices 
set last_activity = CURRENT_TIMESTAMP 
where id = $1
"""

SAVE_TOKEN = """
update devices set 
    access_token_hash = $1
where id = $2
"""

GET_DEVICE_TOKEN = """
select access_token_hash 
from devices
where id = $1
"""
