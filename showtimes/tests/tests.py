import pytest
import pytz
from faker import Faker

from moviebase.settings import TIME_ZONE
from showtimes.models import Cinema
from showtimes.tests.utils import fake_cinema_data

faker = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


@pytest.mark.django_db
def test_add_cinema(client, set_up):
    cinemas_count = Cinema.objects.count()
    new_cinema = fake_cinema_data()
    response = client.post("/cinemas/", new_cinema, format='json')
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_count + 1
    for key, value in new_cinema.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    response = client.get("/cinemas/", {}, format='json')
    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f"/cinemas/{cinema.id}/", {}, format='json')
    assert response.status_code == 204
    cinemas_ids = [cinema.id for cinema in Cinema.objects.all()]
    assert cinema.id not in cinemas_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')
    cinema_data = response.data
    new_name = "DCF"
    cinema_data["name"] = new_name
    response = client.patch(f"/cinemas/{cinema.id}/", cinema_data, format='json')
    assert response.status_code == 200
    cinema_obj = Cinema.objects.get(id=cinema.id)
    assert cinema_obj.name == new_name

