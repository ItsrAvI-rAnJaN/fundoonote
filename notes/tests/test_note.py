import pytest
from rest_framework.reverse import reverse

@pytest.mark.django_db
def test_note_create_without_auth_token(client):
    with pytest.raises(Exception) as e:
        url = reverse("note_api")
        note_data = {"title": "bcde", "description": "hey this is desc of bcde ",}
        note_response = client.post(url, note_data)
        print(note_response.status_code)
        assert str(e) == "Token Authentication required"



@pytest.mark.django_db
def test_note_create_success(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    assert login_response.status_code == 202
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf","user":register_response.data.get("data").get("id")}
    note_response = client.post(url,note_data,content_type="application/json",HTTP_TOKEN=login_response.data.get("data").get("token"))
    assert note_response.status_code == 201

@pytest.mark.django_db
def test_note_create_unsuccess(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    assert register_response.data.get("message") == "User registered sucessfully"
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json")
    assert note_response.status_code ==400

@pytest.mark.django_db
def test_note_reterive_success(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    note_user_id={"user":note_response.data.get("data").get("user")}
    retrive_response=client.get(url,note_user_id,content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    assert retrive_response.status_code==200

@pytest.mark.django_db
def test_note_reterive_unsuccess(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                               HTTP_TOKEN=login_response.data.get("data").get("token"))
    retrive_response = client.get(url, content_type="application/json")
    print(retrive_response.data)
    print(retrive_response.status_code)
    assert retrive_response.status_code == 400

@pytest.mark.django_db
def test_note_update_success(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    note_id = note_response.data.get("data").get("id")
    new_node_data={"id":note_id,"title": "ytf", "description": "hey this is desc of"
                                                            " ytf","user":register_response.data.get("data").get("id")}
    update_response=client.put(url,new_node_data,content_type='application/json',HTTP_TOKEN=login_response.data.get
                                                                                                ("data").get("token"))
    assert update_response.status_code == 201
@pytest.mark.django_db
def test_note_update_unsuccess(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    note_id = note_response.data.get("data").get("id")
    new_node_data = {"id": note_id, "title": "ytf", "description": "hey this is desc of"
                                                                   " ytf",
                     "user": register_response.data.get("data").get("id")}
    update_response = client.put(url, new_node_data, content_type='application/json')
    assert update_response.status_code == 400


@pytest.mark.django_db
def test_note_delete_success(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    note_id = note_id = {"id": note_response.data.get("data").get("id")}
    delete_response = client.delete(url,note_id, content_type='application/json', HTTP_TOKEN=login_response.data.get
    ("data").get("token"))
    assert delete_response.status_code == 200
@pytest.mark.django_db
def test_note_delete_unsuccess(client):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    register_response = client.post(url, user, content_type="application/json")
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    login_response = client.post(url, user_login, content_type="application/json")
    url = reverse("note_api")
    note_data = {"title": "yrf", "description": "het thi is decc of yrf",
                 "user": register_response.data.get("data").get("id")}
    note_response = client.post(url, note_data, content_type="application/json",
                                HTTP_TOKEN=login_response.data.get("data").get("token"))
    note_id = {"id": note_response.data.get("data").get("id")}
    delete_response = client.delete(url, note_id, content_type='application/json')
    assert delete_response.status_code == 400

