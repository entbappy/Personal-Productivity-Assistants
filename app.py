import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.model import get_response

# Load environment variables
load_dotenv()

os.system("python backend/ingest_data.py")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query_assistant():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    response = get_response(user_query)
    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
