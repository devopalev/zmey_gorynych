GET_USER = """
select 
    u.id,
    u.username, 
    u.password_hashed,
    u.revoked,
    array_agg(ur.code) as roles
from users u
left join roles_to_users rtu on u.id = rtu.user_id
left join user_roles ur on ur.id = rtu.role_id
where u.id = $1 or u.username = $2
group by u.id, u.username, u.password_hashed, u.revoked
"""

GET_REFRESH_TOKEN = """
select user_id, refresh_token
from user_tokens
where user_id = $1
    and refresh_token = $2
    and expire_at > current_timestamp
"""

UPDATE_TOKEN = """
update user_tokens 
set refresh_token = $3,  -- new token
    expire_at = default,
    updated_at = default
where user_id = $1 
    and refresh_token = $2  -- old token
"""

INSERT_TOKEN = """
insert into user_tokens (user_id, refresh_token)
values ($1, $2)
"""

DELETE_EXPIRED_TOKENS = """
delete from user_tokens
where expire_at < current_timestamp
"""
