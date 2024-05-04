""" """

from yoyo import step

__depends__ = {}

steps = [
    step("""
        ALTER TABLE devices ADD access_token_hash varchar(64);
    """)
]
