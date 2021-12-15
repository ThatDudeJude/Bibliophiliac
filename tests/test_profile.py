
def test_other_user_profile(client):
    with client:
        client.post('/login', data={'username':'test two', 'password': '1234'})
        response = client.get('/profile/test client')
        assert b'Profile' in response.data                
        assert b'4' in response.data
        assert b'1' in response.data       
        assert b'Change Profile' not in response.data

def test_logged_in_user_profile(client, authenticate):
    with client:
        authenticate.login()
        response = client.get('/profile/test client') 
        assert b'Change Profile' in response.data
        assert b'4' in response.data
        assert b'1' in response.data
        assert b'Skipping Christmas' in response.data

# def test_edit_user_profile(client, authenticate):
#         with client:
#             authenticate.login()
#             response = client.post('/profile/update/1', data={'new_name': 'just test'}, files=dict(avatar_photo='../../tests/test_image.jpg'))
#             assert response.status == '302 FOUND'            
