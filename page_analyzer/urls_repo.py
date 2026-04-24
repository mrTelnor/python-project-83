from psycopg2.extras import RealDictCursor


def find_by_name(conn, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (name,))
        return cur.fetchone()


def find_by_id(conn, id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        return cur.fetchone()


def get_all(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls ORDER BY created_at DESC, id DESC')
        return cur.fetchall()


def insert(conn, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (name,),
        )
        return cur.fetchone()['id']
