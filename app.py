from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

def get_db_file():
    if 'TEST_DB' in os.environ:
        return os.environ['TEST_DB']
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sl.json')

@app.route('/', methods=["GET", "POST"])
def main_post():
    db_file = get_db_file()

    if os.path.exists(db_file):
        with open(db_file) as fh:
            data = json.load(fh)
    else:
        data = {
            'counter': 0,
            'products': []
        }

    if request.method == "POST":
        if 'product' in request.form:
            product = request.form['product']
            data['counter'] += 1
            data['products'].append({
                'id': data['counter'],
                'name': product,
            })
        with open(db_file, 'w') as fh:
            json.dump(data, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    return render_template('main.html',
                           title = "Shopping List",
                           products = data['products'],
                    )