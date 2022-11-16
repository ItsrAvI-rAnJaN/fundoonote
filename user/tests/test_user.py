import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def user_data(django_user_model):
    return django_user_model.objects.create_user(username="bcd", password="1234", first_name="ravi", last_name="ranjan",
                                                 email="bcd@gmail.com", phone=9955540266, location="abc")


@pytest.mark.django_db
def test_user_registration_success(client, django_user_model):
    user = {"username": "bcd", "password": 1234, "first_name": "ravi", "last_name": "ranjan", "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    url = reverse("registration")
    response = client.post(url, user, content_type="application/json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_registration_unsuccess(client, django_user_model, user_data):
    url = reverse("registration")
    user_data.save()
    user = {"username": "bcd", "password": "1234", "first_name": "ravi", "last_name": "ranjan",
            "email": "bcd@gmail.com",
            "phone": 9955540266, "location": "abc"}
    response = client.post(url, user, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_login_success(client, django_user_model, user_data):
    user_data.save()
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": 1234}
    response = client.post(url, user_login, content_type="application/json")
    assert response.status_code == 202


@pytest.mark.django_db
def test_user_login_unsuccess(client, django_user_model):
    url = reverse("loginapi")
    user_login = {"username": "bcd", "password": "1234"}
    response = client.post(url, user_login, content_type="application/json")
    assert response.status_code == 400
