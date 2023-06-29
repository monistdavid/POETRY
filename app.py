from flask import Flask, jsonify, request
from banana_dev import Client
from PIL import Image
import csv

app = Flask(__name__)


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        jsonify({"message": "Get From Python!"})
    else:
        # Create a reference to your model on Banana
        my_model = Client(
            api_key="ccc24bc8-1468-4576-8a37-ef18dcdd7b8e",  # Found in dashboard
            model_key="20b2c17e-f401-49db-9f49-d59aeb3cbf28",  # Found in model view in dashboard
            url="https://poetry_banana-ljfrxw9fcc.run.banana.dev"
        )

        # Specify the model's input JSON
        inputs = {
            "prompt": "Software developers start with a Hello, [MASK]! script",
        }
        image = Image.open('guan.jpg')

        # Call your model's inference endpoint on Banana
        result, meta = my_model.call("/", inputs)

        def read_strings_from_csv(filename):
            strings = []
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header if present
                for row in reader:
                    if row:
                        strings.append(row[0])
            return strings

        # Example usage
        all_poetry = read_strings_from_csv('all_poetry.csv')
        similar_poetry = [all_poetry[result[0][i]['corpus_id']] for i in range(len(result[0]))][0]


        return jsonify({"message": similar_poetry})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
