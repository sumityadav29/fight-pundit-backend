import os
from flask import Flask

from gyms_api import gyms_api_app

app = Flask(__name__)
app.register_blueprint(gyms_api_app, url_prefix="/")

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(debug=True, host="0.0.0.0", port=port)