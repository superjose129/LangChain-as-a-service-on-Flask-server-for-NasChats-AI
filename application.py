from flask import Flask, render_template, request, jsonify
from backend.core import run_llm
from flask_cors import CORS

application = Flask(__name__)
CORS(application)


@application.route("/")
def index():
    return "<h1>Amotions Langchain API</h1>"


@application.route("/process", methods=["POST"])
def process():
    print("request process")
    data = request.get_json()
    query = data.get("query")

    if query is None:
        return jsonify({"error": "Name parameter is missing"}), 400
    
    answer = run_llm(query=query)['result']

    return jsonify( 
        {
            "answer": answer,
        }
    )

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=False)
    # app.run()

# langchain.schema.OutputParserException: Failed to parse PersonIntel from completion {
# return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")

# app.run(host="0.0.0.0", debug=True)