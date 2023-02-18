import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_profile(user: str):
    r = requests.get(f"https://dev.to/api/users/by_username?url={user}")
    res = r.json()

    return res


def get_articles(user: str):
    r = requests.get(f"https://dev.to/api/articles?username={user}&per_page=3")
    res = r.json()

    return res


def get_dev_stats(user: str):
    profile = get_profile(user)
    articles = map(
        lambda x: {
            "title": x["title"],
            "url": x["url"],
            "reading_time": x["reading_time_minutes"],
            "reactions": x["public_reactions_count"],
        },
        get_articles(user),
    )

    return {
        "name": profile["name"],
        "username": profile["username"],
        "twitter": profile["twitter_username"],
        "avatar": profile["profile_image"],
        "github": profile["github_username"],
        "articles": list(articles),
    }


@app.route("/api", methods=["GET"])
def api():
    user = request.args.get("user")
    try:
        if user is None:
            return jsonify({"error": "No user provided"}), 400

        return jsonify(get_dev_stats(user)), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong!"}), 500


if __name__ == "__main__":
    app.run(debug=True)