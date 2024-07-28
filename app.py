from tireless import app
from tireless import run

# import the routes
from pages.page import bp as page
from pages.contact import bp as contact
from pages.about import bp as about

# register the routes
app.register_blueprint(page)
app.register_blueprint(contact)
app.register_blueprint(about)

if __name__ == '__main__':
    # run() uncomment this line if you want to run the app in production mode
    run(debug=True)  # comment this line if you want to run the app in production mode

