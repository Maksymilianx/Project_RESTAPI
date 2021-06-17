import pytest
import pytz
from faker import Faker

from moviebase.settings import TIME_ZONE
from movielist.models import Movie
from showtimes.models import Cinema, Screening
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


@pytest.mark.django_db
# checks if adding new screening works
def test_add_screening(client, set_up):
    screening_count = Screening.objects.count()
    new_screening_date = {
        "cinema": Cinema.objects.first().name,
        "movie": Movie.objects.first().title,
        "date": faker.date_time(tzinfo=TZ).isoformat()
    }
    response = client.post("/screenings/", new_screening_date, format='json')
    assert response.status_code == 201
    assert Screening.objects.count() == screening_count + 1

    new_screening_date["date"] = new_screening_date["date"].replace('+00:00', 'Z')
    for key, value in new_screening_date.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
# checks if list of all screenings works
def test_get_screening_list(client, set_up):
    response = client.get("/screenings/", {}, format='json')
    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
# checks if specific screening view works
def test_get_screening_detail(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.id}/", {}, follow='json')
    assert response.status_code == 200
    for field in ('movie', 'cinema', 'date'):
        assert field in response.data