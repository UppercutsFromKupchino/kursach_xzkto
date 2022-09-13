import psycopg2
import psycopg2.extras
import psycopg2.errors


conn = psycopg2.connect(dbname="de0bqj7k0h7b11",
                        user="pvklstfzndomrq",
                        password="b0bdfe5e796b4ec43ed138626c5933080b2782ac184e8a784c0c806e99f34387",
                        host="ec2-3-214-2-141.compute-1.amazonaws.com")


def get_user(username, password):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'SELECT * FROM _user_ WHERE username = \'{username}\' AND _password_ = \'{password}\'')
    account = cursor.fetchone()
    cursor.close()
    return account


def get_user_for_registration(username):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'SELECT * FROM _user_ WHERE username = \'{username}\'')
    account = cursor.fetchone()
    cursor.close()
    return account


def add_user(username, password, first_name, last_name):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'''INSERT INTO _user_(username, _password_, first_name, last_name)
                       VALUES(\'{username}\', \'{password}\', \'{first_name}\', \'{last_name}\')''')
    conn.commit()
    cursor.close()



def add_task(name, date, user_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f"INSERT INTO task(user_id, _name_, _date_) VALUES(\'{user_id}\', \'{name}\', \'{date}\')")
    conn.commit()
    cursor.close()


def get_tasks(user_id, date):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f"SELECT * FROM task WHERE user_id=\'{user_id}\' AND _date_=\'{date}\'")
    tasks = cursor.fetchall()
    cursor.close()
    return tasks
