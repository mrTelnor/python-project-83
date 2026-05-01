from psycopg2.extras import RealDictCursor


def insert(
    conn,
    url_id,
    status_code=None,
    h1=None,
    title=None,
    description=None,
):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''
            INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            ''',
            (url_id, status_code, h1, title, description),
        )
        return cur.fetchone()['id']


def get_by_url_id(conn, url_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            'SELECT * FROM url_checks WHERE url_id = %s '
            'ORDER BY created_at DESC, id DESC',
            (url_id,),
        )
        return cur.fetchall()
