import os, sys

from flask import Flask, jsonify, request

from gyms_api import gyms_app


app = Flask(__name__)

app.register_blueprint(gyms_app, url_prefix="/")

@app.route("/")
def hello_world():
  """Example Hello World route."""
  name = os.environ.get("NAME", "World")
  return f"Hello {name}!"
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)