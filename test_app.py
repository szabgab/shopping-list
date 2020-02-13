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
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    assert "<li>Apple juice</li>" in rv.data.decode('utf-8')

    rv = web.post('/', data={
        "product": "Loaf of Bread"
    })
    assert rv.status_code == 200
    #print(rv.data)
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    assert "<li>Apple juice</li>" in rv.data.decode('utf-8')
    assert "<li>Loaf of Bread</li>" in rv.data.decode('utf-8')

    rv = web.get('/')
    assert rv.status_code == 200
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    assert "<li>Apple juice</li>" in rv.data.decode('utf-8')
    assert "<li>Loaf of Bread</li>" in rv.data.decode('utf-8')
