from psycopg2.extras import RealDictCursor


def find_by_name(conn, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (name,))
        return cur.fetchone()


def find_by_id(conn, id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        return cur.fetchone()


def get_all_with_last_check(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''
            SELECT
                u.id,
                u.name,
                MAX(uc.created_at) AS last_check_at,
                (
                    SELECT status_code FROM url_checks
                    WHERE url_id = u.id
                    ORDER BY created_at DESC, id DESC
                    LIMIT 1
                ) AS last_status_code
            FROM urls u
            LEFT JOIN url_checks uc ON uc.url_id = u.id
            GROUP BY u.id
            ORDER BY u.created_at DESC, u.id DESC
            '''
        )
        return cur.fetchall()


def insert(conn, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (name,),
        )
        return cur.fetchone()['id']
