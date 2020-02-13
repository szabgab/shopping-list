import app

def test_app():
    web = app.app.test_client()
    rv = web.get('/')
    assert rv.status_code == 200
    assert rv.data.decode('utf-8') == "Shopping List"
