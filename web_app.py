from urllib.parse import quote

from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.exceptions import BadRequest

from app.rhyme import get_rhymes as get_rhymes_function
from app.rhyme import get_random_word as get_random_word_function
from app.settings import DEBUG

app = Flask(__name__, static_folder="web_app")

if DEBUG:

    @app.route("/<path:path>")
    def static_proxy(path):
        # send_static_file will guess the correct MIME type
        return app.send_static_file(path)


@app.route("/")
def root():
    text = request.args.get("q", None)
    groups = None

    if text:
        if len(text) > 40:
            raise BadRequest("The text is too long")

        rhymes = get_rhymes_function(text)

        # Group the rhymes by number syllables
        rhymes_by_num_syllables = {}
        for rhyme in rhymes:
            if rhyme["num_syllables"] not in rhymes_by_num_syllables:
                rhymes_by_num_syllables[rhyme["num_syllables"]] = []

            rhymes_by_num_syllables[rhyme["num_syllables"]].append(rhyme)

        groups = []
        for num_syllables in rhymes_by_num_syllables:
            groups.append(
                {
                    "num_syllables": num_syllables,
                    "rhymes": rhymes_by_num_syllables[num_syllables],
                }
            )

        groups.sort(key=lambda group: group["num_syllables"])

    return render_template("index.html", groups=groups, text=text)


@app.route("/random_word/", methods=["GET"])
def get_random_word():
    random_word = get_random_word_function()

    return redirect("/?q={}".format(quote(random_word)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)
