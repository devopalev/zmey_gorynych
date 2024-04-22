CREATE_DEVICE = """
insert into devices (user_id, name, last_activity) 
values ($1, $2, CURRENT_TIMESTAMP)
returning id, name, revoked, last_activity
"""

GET_DEVICE = """
select id, name, revoked, last_activity
from devices
where id = $1
"""

ACTIVITY_DEVICE = """
update devices 
set last_activity = CURRENT_TIMESTAMP 
where id = $1
"""