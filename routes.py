from flask import Blueprint, jsonify, redirect, render_template, request, url_for


def create_routes(service):
    routes = Blueprint("links", __name__)

    @routes.get("/")
    def index():
        return render_template("index.html")

    @routes.post("/api/shorten")
    def shorten():
        if not request.is_json:
            return jsonify(error="Send the request as JSON."), 415

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify(error="Send a JSON object with a url field."), 400

        try:
            link = service.shorten(data.get("url"))
        except ValueError as error:
            return jsonify(error=str(error)), 400
        except RuntimeError as error:
            return jsonify(error=str(error)), 503

        return jsonify(
            code=link.code,
            original_url=link.original_url,
            short_url=url_for(
                "links.follow_link",
                code=link.code,
                _external=True,
            ),
        ), 201

    @routes.get("/s/<code>")
    def follow_link(code):
        link = service.get_link(code)

        if link is None:
            return render_template(
                "index.html",
                error="This short link does not exist. Create a new one below.",
            ), 404

        return redirect(link.original_url, code=302)

    return routes