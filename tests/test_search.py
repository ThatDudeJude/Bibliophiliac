
def test_search_results(client, authenticate):
    with client:
        response = authenticate.login()
        assert response.status == '302 FOUND'
        client.get('/search')
        response = client.get('/search?search_term=rowling')
        assert b'Casual' in response.data

def test_search_results_redirection_to_review(client, authenticate):
    with client:
        authenticate.login()
        response = client.get('/review/0316228532')
        assert response.status == '200 OK'
        assert b'Casual' in response.data
        assert b'Add' in response.data

