from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main_get():
    return render_template('main.html',
                           title = "Shopping List",
                    )

@app.route('/', methods=["POST"])
def main_post():
    products = []

    if 'product' in request.form:
        product = request.form['product']
        products.append(product)

    return render_template('main.html',
                           title = "Shopping List",
                           products = products,
                    )