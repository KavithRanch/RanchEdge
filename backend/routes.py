from backend import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/stats')
def stats_page():
    return render_template('stats.html')


@app.route('/stats/<sport>')
def sport_stats_page(sport):
    return render_template(f'{sport}_stats.html')

