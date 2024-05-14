""" """

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE user_tokens (
            user_id integer not null references users,
            refresh_token varchar(64) not null,
            expire_at timestamp not null default current_timestamp + interval '1 month',
            created_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """)
]
