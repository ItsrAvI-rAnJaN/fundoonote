import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_note_create(self, client):
    url = reverse("note_api")
    note_data = {"title": "bcde", "description": "hey this is desc of bcde "}
    note_response = client.post(url, note_data)
    assert note_response.status_code == 201
