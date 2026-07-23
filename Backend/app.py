from flask import Flask

from config import Config

from controllers.frontend_controller import frontend_bp
from controllers.registration_controller import registration_bp
from controllers.admin_controller import admin_bp



app = Flask(__name__)


# ======================================
# KONFIGURACJA
# ======================================

app.secret_key = Config.SECRET_KEY



# ======================================
# BLUEPRINTS
# ======================================

app.register_blueprint(
    frontend_bp
)


app.register_blueprint(
    registration_bp
)


app.register_blueprint(
    admin_bp
)



# ======================================
# START
# ======================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
