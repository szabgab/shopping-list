import app
import os

def test_app(tmpdir):
    print(tmpdir)
    os.environ['TEST_DB'] = os.path.join(tmpdir, 'temp.db')

    web = app.app.test_client()

    rv = web.get('/')
    assert rv.status_code == 200
    #print(rv.data)
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "Products" not in rv.data.decode('utf-8')
    assert "Apple juice" not in rv.data.decode('utf-8')

    rv = web.post('/', data={
        "product": "Apple juice"
    })
    assert rv.status_code == 200
    assert 'Shopping List' in rv.data.decode('utf-8')
    assert '<h2>Products</h2>' in rv.data.decode('utf-8')
    assert '<li>Apple juice <a href="/remove/1">remove</a></li>' in rv.data.decode('utf-8')

    rv = web.post('/', data={
        "product": "Loaf of Bread"
    })
    assert rv.status_code == 200
    #print(rv.data)
    assert 'Shopping List' in rv.data.decode('utf-8')
    assert '<h2>Products</h2>' in rv.data.decode('utf-8')
    assert '<li>Apple juice <a href="/remove/1">remove</a></li>' in rv.data.decode('utf-8')
    assert '<li>Loaf of Bread <a href="/remove/2">remove</a></li>' in rv.data.decode('utf-8')

    rv = web.get('/')
    assert rv.status_code == 200
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    assert '<li>Apple juice <a href="/remove/1">remove</a></li>' in rv.data.decode('utf-8')
    assert '<li>Loaf of Bread <a href="/remove/2">remove</a></li>' in rv.data.decode('utf-8')


def test_remove(tmpdir):
    print(tmpdir)
    os.environ['TEST_DB'] = os.path.join(tmpdir, 'temp.db')

    web = app.app.test_client()

    products = ["Milk", "Bread", "Apple juice", "Toothpaste"]
    for name in products:
        rv = web.post('/', data={
            "product": name
        })

    rv = web.get('/')
    assert rv.status_code == 200
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    for idx, name in enumerate(products):
        assert f'<li>{name} <a href="/remove/{idx+1}">remove</a></li>' in rv.data.decode('utf-8')


    rv = web.get('/remove/3')
    assert rv.status_code == 302
    print(rv.headers)

    rv = web.get('/')
    assert rv.status_code == 200
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    for idx, name in enumerate(products):
        if idx+1 == 3:
            assert name not in rv.data.decode('utf-8')
        else:
            assert f'<li>{name} <a href="/remove/{idx+1}">remove</a></li>' in rv.data.decode('utf-8')
