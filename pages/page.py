from flask import Blueprint, render_template
from tireless import app

bp = Blueprint('page', __name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('page.j2')

