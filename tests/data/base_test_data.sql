insert into users (username, password_hashed)
values  (
         'test_user',
         '$2b$12$yaclKT7A7AccVuZZRGFXweN5W.M26/DYT7PtuOot4CHLnPhInKPsu'  -- password: Xx7536951xX
         ),
        (
         'test_admin',
         '$2b$12$yaclKT7A7AccVuZZRGFXweN5W.M26/DYT7PtuOot4CHLnPhInKPsu'  -- password: Xx7536951xX
        );

-- user role for test_user
insert into roles_to_users (user_id, role_id)
values  ((select id from users where username = 'test_user'), 2);

-- admin role for test_admin
insert into roles_to_users (user_id, role_id)
values  ((select id from users where username = 'test_admin'), 1);

INSERT INTO devices (id, user_id, name)
VALUES ('65799ccd-bbc4-4026-a560-af152880280a', (select id from users where username = 'test_user'), 'test_device');

