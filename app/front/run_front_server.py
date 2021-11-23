from flask import Flask, render_template, redirect, url_for, request, flash
import json
import pandas as pd

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='fhfgfahhkmhjrtyrsthfgvcnvb',
)

train_data = pd.read_csv('data/X_train.csv')

# def get_prediction(description, company_profile, benefits):
#     body = {'description': description,
#                             'company_profile': company_profile,
#                             'benefits': benefits}
#
#     myurl = "http://0.0.0.0:8180/predict"
#     req = urllib.request.Request(myurl)
#     req.add_header('Content-Type', 'application/json; charset=utf-8')
#     jsondata = json.dumps(body)
#     jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
#     req.add_header('Content-Length', len(jsondataasbytes))
#     #print (jsondataasbytes)
#     response = urllib.request.urlopen(req, jsondataasbytes)
#     return json.loads(response.read())['predictions']

page_data = {'menu': ['Главная страница', 'О сайте']}
@app.route("/", methods=['GET', 'POST'])
def index():
    allowed_data = {
        'brands': train_data['brand'].unique(),
        'car_models': train_data.groupby('brand')['model'].apply(set),
    }
    page_data.update(allowed_data)
    if request.method == 'POST':
        print(1)
        # data['description'] = request.form.get('description')
        # data['company_profile'] = request.form.get('company_profile')
        # data['benefits'] = request.form.get('benefits')
        #
        #
        # try:
        #     response = str(get_prediction(data['description'],
        #                               data['company_profile'],
        #                               data['benefits']))
        #     print(response)
        # except ConnectionError:
        #     response = json.dumps({"error": "ConnectionError"})
        # return redirect(url_for('predicted', response=response))

    return render_template('index.html', **page_data)


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['description'] = request.form.get('description')
        data['company_profile'] = request.form.get('company_profile')
        data['benefits'] = request.form.get('benefits')


        try:
            response = str(get_prediction(data['description'],
                                      data['company_profile'],
                                      data['benefits']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)