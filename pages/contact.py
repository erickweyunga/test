# imports
from flask import Blueprint, render_template

# blueprint
bp = Blueprint('contact', __name__, url_prefix="/contact", template_folder='templates', static_folder='static')


# routing
@bp.route("/")
def index():

    # you can pass objects, variables from the server to client
    context = {}
    # rendering the contact jinja/html template on the templates directory
    return render_template('contact.j2', context=context )