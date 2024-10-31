import miro_api
from config.config import MIRO_ACCESS_TOKEN, Config
from database.connection import db
from flask import Flask


class App:
    """
    Main application class that initializes and configures a Flask app, sets up
    the Miro API client, and integrates database connections.

    Attributes:
        miro_client (miro_api.MiroApi): Instance of the Miro API client initialized
            with an access token to interact with the Miro API.
        app (Flask): Flask application instance with configured settings and database
            connection.
    """

    def __init__(self):
        """
        Initializes the App class by creating a Miro API client instance and setting
        up the Flask application.

        - Initializes the `miro_client` attribute with the Miro API client configured
          using the provided access token.
        - Calls the `_create_app()` method to set up the Flask application instance.
        """
        self.miro_client = miro_api.MiroApi(MIRO_ACCESS_TOKEN)
        self.app = self._create_app()

    def _create_app(self):
        """
        Private method to create and configure the Flask application.

        - Sets up the Flask application with configurations from the `Config` object.
        - Integrates the database by initializing it with the Flask app context,
          creating tables if they don't already exist.
        - Placeholder for additional setup, such as adding blueprints and middleware.

        Returns:
            Flask: A configured Flask application instance.
        """
        app = Flask(__name__)
        app.config.from_object(Config)

        # Initialize database with Flask app context
        db.init_app(app)
        with app.app_context():
            db.create_all()  # Create tables if they don't exist

        # Additional setup (blueprints, middleware, etc.) can be added here

        return app

    def run(self, **kwargs):
        """
        Runs the Flask application with optional configurations.

        - Executes the Flask app’s `run()` method, allowing customization of server
          options such as host, port, debug mode, etc., via `kwargs`.

        Args:
            **kwargs: Arbitrary keyword arguments passed to `Flask.run()`, such as
                `host`, `port`, and `debug` to configure server behavior.
        """
        self.app.run(**kwargs)