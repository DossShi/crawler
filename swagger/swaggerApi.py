#! /usr/bin/python3
# -*- coding:utf-8  -*-

import random
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger_config = {
    "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_2',
                "route": '/apispecification.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/doc/"
}
template_config = {
  "info": {
    "title": "Sample API",
    "description": "Hahaha, this is a API kingdom!",
    "version": "1.0.0"
  }
}
Swagger(app, template=template_config, config=swagger_config)

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from("api_get.yml")
def index(language):
    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


app.run(debug=True)