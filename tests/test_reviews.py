import pytest

def test_add_review(client, authenticate):
    with client:
        authenticate.login()
        client.get('/review/0316228532')
        response = client.post('/review/0316228532', data={'rating': '5', 'user_review': 'Really good book'})
        assert response.status == '302 FOUND'
        response = client.get('/review/0316228532')
        assert response.status == '200 OK'
        assert b'Really' in response.data
        assert b'client' in response.data
        assert b'5' in response.data


@pytest.mark.parametrize(('rating', 'review_input', 'message'),  (
    ('0', 'Excellent', b'Your rating is required!'), 
    ('5', '', b'Your review is required!'),     
))


def test_add_review_input_errors(rating, review_input, message, client, authenticate):
    with client:
        authenticate.login()
        client.get('/review/0316228532')
        response = client.post('/review/0316228532', data={'rating': rating, 'user_review': review_input})
        assert response.status == '302 FOUND'
        response = client.get('/review/0316228532')
        assert response.status == '200 OK'
        assert message in response.data
        
def test_add_review_invalid_request(client, authenticate):
    with client:
        authenticate.login()
        client.get('/review/0316228532')
        response = client.post('/review/0', data={'rating': '5', 'user_review': 'Really good'})
        assert response.status == '302 FOUND'
        response = client.get('/review/0316228532')
        assert response.status == '200 OK'
        assert b'Invalid Request!' in response.data

        authenticate.logout()
        client.get('/review/0316228532')
        response = client.post('/review/0316228532', data={'rating': '5', 'user_review': 'Really good'})
        response = client.post('/review/0316228532', data={'rating': '5', 'user_review': 'Really good'})
        assert response.status == '302 FOUND'
        assert b'redirect' in response.data

def test_all_reviews(client, authenticate):
    with client:
        authenticate.login()
        response = client.get('/your_reviews/1')
        assert response.status == '200 OK'
        # assert b'No Reviews' in response.data
        assert b'My Reviews' in response.data
        assert b'0' in response.data

        client.get('/review/0099481685')
        client.post('/review/0099481685', data={'rating': '5', 'user_review': 'Really good'})
        response = client.get('/your_reviews/1')
        assert response.status == '200 OK'
        assert b'Grisham' in response.data
        assert b'My Reviews' in response.data
        assert b'Number of Reviews' in response.data

        response = client.get('/your_reviews/1')
        assert response.status == '200 OK'
        assert b'Grisham' in response.data
        assert b'test client' in response.data

        response = client.get('/all_reviews')
        assert response.status == '200 OK'
        assert b'Grisham' in response.data
        assert b'test client' in response.data
        assert b'All Reviews' in response.data
        assert b'Reviewed Books' in response.data

        