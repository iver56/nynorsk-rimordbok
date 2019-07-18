from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from app.rhyme import get_rhymes as get_rhymes_function
from app.rhyme import get_random_word as get_random_word_function
from app.settings import DEBUG

app = Flask(__name__, static_folder="web_app")

if DEBUG:
    @app.route("/")
    def root():
        return app.send_static_file("index.html")


    @app.route("/<path:path>")
    def static_proxy(path):
        # send_static_file will guess the correct MIME type
        return app.send_static_file(path)


@app.route("/api/get_rhymes/", methods=["POST"])
def get_rhymes():
    text = request.json.get("text", "")

    if len(text) == 0:
        raise BadRequest("The text empty")

    if len(text) > 40:
        raise BadRequest("The text is too long")

    rhymes = get_rhymes_function(text)

    return jsonify({"rhymes": rhymes})


@app.route("/api/get_random_word/", methods=["GET"])
def get_random_word():
    random_word = get_random_word_function()

    return jsonify({"random_word": random_word})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)
