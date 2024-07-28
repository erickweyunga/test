# imports
from flask import Blueprint, render_template

# blueprint
bp = Blueprint('about', __name__, url_prefix="/about", template_folder='templates', static_folder='static')


# routing
@bp.route("/")
def index():

    # you can pass objects, variables from the server to client
    context = {}
    # rendering the about jinja/html template on the templates directory
    return render_template('about.j2', context=context )