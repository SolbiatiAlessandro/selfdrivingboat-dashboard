import os
import psycopg2
try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    with open('db.secret', 'r') as f:
        DATABASE_URL = f.read()

#https://www.psycopg.org/docs/usage.html

"""
theselfdrivingboat::DATABASE=> \d boat_commands
                                              Table "public.boat_commands"
    Column     |            Type             | Collation | Nullable |                      Default
---------------+-----------------------------+-----------+----------+---------------------------------------------------
 command_id    | integer                     |           | not null | nextval('boat_commands_command_id_seq'::regclass)
 command_name  | character varying(100)      |           |          |
 created_on    | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 has_been_read | boolean                     |           |          | false
 read_by       | character varying(100)      |           |          |
Indexes:
    "boat_commands_pkey" PRIMARY KEY, btree (command_id)
"""

def add_new_command(command):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO boat_commands (command_name) VALUES (%s)", (command, ))
    conn.commit()
    cur.close()
    conn.close()

def read_last_command(boat_name):
    "return None if last command was already read"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("WITH last_command AS (SELECT * FROM boat_commands ORDER BY command_id DESC LIMIT 1) UPDATE boat_commands SET (has_been_read, read_by) = (TRUE, %s) FROM last_command WHERE last_command.has_been_read = FALSE RETURNING last_command.command_name", (boat_name,));
    last_command = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return last_command