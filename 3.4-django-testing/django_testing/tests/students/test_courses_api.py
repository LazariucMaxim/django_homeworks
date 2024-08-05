import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_receive_course(client, course_factory):
    course = course_factory()

    response = client.get(f'/api/v1/courses/{course.pk}/')
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_list_course(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['id'] == courses[i].id
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_id_filter_course(client, course_factory):
    courses = course_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?id={course.pk}')

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_name_filter_course(client, course_factory):
    courses = course_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?name={course.name}')

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'Fullstack'}, format='json')
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'Fullstack'
    assert data['students'] == []


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    for course in courses:
        response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': 'update_course'})
        data = response.json()
        assert response.status_code == 200
        assert data['name'] == 'update_course'

        response = client.put(f'/api/v1/courses/{course.id}/', data={'name': 'updatex2_course'})
        data = response.json()
        assert response.status_code == 200
        assert data['name'] == 'updatex2_course'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    for i, course in enumerate(courses):
        response = client.delete(f'/api/v1/courses/{course.id}/')
        assert response.status_code == 204
        assert Course.objects.count() == 9-i
