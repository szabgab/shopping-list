import app

def test_app():
    web = app.app.test_client()

    rv = web.get('/')
    assert rv.status_code == 200
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "Apple juice" not in rv.data.decode('utf-8')
    assert "Products" not in rv.data.decode('utf-8')

    rv = web.post('/', data={
        "product": "Apple juice"
    })
    assert rv.status_code == 200
    assert "Shopping List" in rv.data.decode('utf-8')
    assert "<h2>Products</h2>" in rv.data.decode('utf-8')
    assert "<li>Apple juice</li>" in rv.data.decode('utf-8')

