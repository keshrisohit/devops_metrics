import os

from flask import Flask

from application.flask_api import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
