from fileinput import filename
import os
from werkzeug.datastructures import FileStorage

basedir = os.path.abspath(os.path.dirname(__name__))


def test_other_user_profile(client, authenticate):
    with client:
        authenticate.login(username="test two", password="1234")
        response = client.get("/profile/test client")
        assert b"Profile" in response.data
        assert b"4" in response.data
        assert b"1" in response.data
        assert b"Change Profile" not in response.data


def test_logged_in_user_profile(client, authenticate):
    with client:
        authenticate.login()
        response = client.get("/profile/test client")
        assert b"Change Profile" in response.data
        assert b"4" in response.data
        assert b"1" in response.data
        assert b"Skipping Christmas" in response.data


def test_edit_user_profile(client, authenticate, config):
    with client:
        authenticate.login()
        profile_image = FileStorage(
            stream=open(
                basedir + "/" + config["DEFAULT_TEST_PROFILE_IMAGE_CHANGE"], "rb"
            ),
            filename="test_image.jpg",
            content_type="image/jpeg",
        )

        response = client.post(
            "/profile/update/1",
            data={
                "new_name": "test client renamed",
                "avatar_photo": profile_image,
            },
            content_type="multipart/form-data",
        )

        assert response.status == "302 FOUND"

        response = client.get("/profile/test client renamed")
        assert b"Change Profile" in response.data
        assert b"test client renamed" in response.data
        assert b"4" in response.data
        assert b"1" in response.data
