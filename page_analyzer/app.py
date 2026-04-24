import os
from urllib.parse import urlparse

import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer import checks_repo, urls_repo
from page_analyzer.db import get_connection

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_create():
    raw_url = request.form.get('url', '').strip()
    error = _validate_url(raw_url)
    if error:
        flash(error, 'danger')
        return render_template('index.html', url=raw_url), 422

    name = _normalize_url(raw_url)

    with get_connection() as conn:
        existing = urls_repo.find_by_name(conn, name)
        if existing:
            flash('Страница уже существует', 'info')
            return redirect(url_for('url_show', id=existing['id']))

        new_id = urls_repo.insert(conn, name)

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_show', id=new_id))


@app.get('/urls')
def urls_index():
    with get_connection() as conn:
        urls = urls_repo.get_all_with_last_check(conn)
    return render_template('urls/index.html', urls=urls)


@app.get('/urls/<int:id>')
def url_show(id):
    with get_connection() as conn:
        url = urls_repo.find_by_id(conn, id)
        if url is None:
            return 'Not Found', 404
        checks = checks_repo.get_by_url_id(conn, id)
    return render_template('urls/show.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def url_checks_create(id):
    with get_connection() as conn:
        url = urls_repo.find_by_id(conn, id)
        if url is None:
            return 'Not Found', 404
        checks_repo.insert(conn, id)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_show', id=id))


def _validate_url(value):
    if not value:
        return 'URL обязателен'
    if len(value) > 255:
        return 'URL превышает 255 символов'
    if not validators.url(value):
        return 'Некорректный URL'
    return None


def _normalize_url(value):
    parsed = urlparse(value)
    return f'{parsed.scheme}://{parsed.hostname}'
