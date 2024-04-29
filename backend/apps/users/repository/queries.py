GET_USER = """
select 
    u.id,
    u.username, 
    u.password_hashed,
    u.revoked,
    array_agg(ur.code) as roles
from users u
join roles_to_users rtu on u.id = rtu.user_id
join user_roles ur on ur.id = rtu.role_id
where u.username = $1
group by u.id, u.username, u.password_hashed, u.revoked
"""
