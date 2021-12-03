from bibliophiliac import create_app

def test_app_env(app):
    assert not create_app().testing
    assert create_app(testing=True) 


def test_app_index(client):
    response = client.get('/')
    assert response.status == '302 FOUND'
    assert b'search' in response.data