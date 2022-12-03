# foodtracker-app-flask

foodtracker made with flask, for learning purposes.

## Credits

    The starting files for this project were provided by PrettyPrinted.
    It doesn't have user level functionality, so I added it.

## Getting started

Once you have created your new app, take a few minutes to look through the files to familiarise yourself with the project structure.

- `app/__init__.py` : entry point to the Flask app
- `app/models.py` : contains all the database models/schemas
- `app/forms.py` : contains all the forms used in the app (using Flask-WTF)
- `app/extensions.py` : contains the SQLAlchemy instance
- `app/main/templates/` : contains the frontend dynamic HTML files
- `app/main/static/` : contains the static frontend assets (images, stylesheets and scripts)

To start the application locally, you can just run `flask run` and this will launch the app on port 5000 (by default).
You will notice a message in the console saying:

`WARNING: Could not connect to the given database URL!`

To fix this, you should set the environment variable DATABASE_URL accordingly. If you have PostgreSQL running locally, you can use that. Alternatively, you could use SQLite which is much simpler and does not require installation, for example, by running `export DATABASE_URL="sqlite:///dev.db"`
or you have to setup a dotenv file and add the following line to it:

- SQLALCHEMY_DATABASE_URI = `<your database url>`
- SECRET_KEY = `<your secret key>`

If you do not want to use a database yet, you can ignore this warning and delete any routes that interact with the database. But you will not be able to use the login functionality. So I don't know why you would want to do that.

If you navigate to `http://localhost:5000`, you will see the response created by the home route defined in `main/routes.py`.

## Deployment

The website is already deployed on Render.com. You can check it out [here](https://foodtrackerappflask.onrender.com/).
