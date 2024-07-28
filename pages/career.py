# imports
from flask import Blueprint, render_template

# blueprint
bp = Blueprint('career', __name__, url_prefix="/career", template_folder='templates', static_folder='static')


# routing
@bp.route("/")
def index():

    # you can pass objects, variables from the server to client
    context = {}
    # rendering the career jinja/html template on the templates directory
    return render_template('career.j2', context=context )