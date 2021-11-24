import dill
import pandas as pd
import os
import flask

dill._dill._reverse_typemap['ClassType'] = type

app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to auto price prediction process. Please use 'http://<address>/predict' to POST"""


def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = dill.load(f)
        return model


model_path = "./models/model_pipeline.dill"
model = load_model(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    if flask.request.method == "POST":
        json_data = flask.request.get_json()

        try:
            d = pd.DataFrame({"brand": [json_data['brand']],
                              "model": [json_data['model']],
                              "year": [json_data['year']],
                              "transmission": [json_data['transmission']],
                              "mileage": [json_data['mileage']],
                              "fuelType": [json_data['fuelType']],
                              "tax": [json_data['tax']],
                              "mpg": [json_data['mpg']],
                              "engineSize": [json_data['engineSize']],
                              })
            preds = model.predict(d)

        except AttributeError as e:
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[0]
        data["success"] = True
    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
