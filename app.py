from flask import Flask, render_template, request, abort, redirect
import os
import json

app = Flask(__name__)

def get_db_file():
    if 'TEST_DB' in os.environ:
        return os.environ['TEST_DB']
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sl.json')

def save(data):
    db_file = get_db_file()
    with open(db_file, 'w') as fh:
        json.dump(data, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


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
        save(data)

    return render_template('main.html',
                           title = "Shopping List",
                           products = data['products'],
                    )

@app.route('/remove/<int:idx>', methods=["GET"])
def remove(idx):
    db_file = get_db_file()
    if not os.path.exists(db_file):
        abort(500)

    with open(db_file) as fh:
        data = json.load(fh)
    for ix in range(len(data["products"])):
        app.logger.info(data["products"][ix]["id"])
        if data["products"][ix]["id"] == idx:
            break
    else:
        abort(404)

    data["products"].pop(ix)
    save(data)
    return redirect('/')