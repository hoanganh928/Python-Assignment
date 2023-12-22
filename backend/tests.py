from django.test import TestCase
import random
import string

from backend.models import Company, Department, Location, Position, Employee, EmployeeStatus


def get_random_key(objs, allow_null=True):
    if allow_null:
        objs.append(0)
        key = random.choice(objs)
    else:
        key = random.choice(objs)
    if key == 0:
        return None
    return key


def generate_seed_data():
    all_columns = ['first_name', 'last_name', 'department', 'location', 'position', 'company', 'phone', 'email',
                   'status']
    company_data = [
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            'columns': random.sample(all_columns, k=4)
        },
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            'columns': random.sample(all_columns, k=4)
        }
    ]
    Company.bulk_create(company_data)
    department_data = [
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        },
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    ]
    Department.bulk_create(department_data)
    location_data = [
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        },
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    ]
    Location.bulk_create(location_data)
    position_data = [
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        },
        {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    ]
    Position.bulk_create(position_data)
    companies = Company.objects.all()
    departments = Department.objects.all()
    locations = Location.objects.all()
    positions = Position.objects.all()
    employees = []
    for i in range(100):
        employee = {
            "first_name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
            "last_name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
            "department_id": get_random_key([i.id for i in departments]),
            "location_id": get_random_key([i.id for i in locations]),
            "position_id": get_random_key([i.id for i in positions]),
            "company_id": get_random_key([i.id for i in companies], allow_null=False),
            "phone": str(random.randint(0, 999999999)),
            "email": f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@yopmail.com",
            "status": random.choice(EmployeeStatus.choices())[1]
        }
        employees.append(employee)
    Employee.bulk_create(employees)


class EmployeeTestCase(TestCase):
    def setUp(self):
        generate_seed_data()

    def get_employees(self, company_id, **kwargs):
        queryset = Employee.objects.filter(company_id=company_id)
        query_params = kwargs
        status_query = query_params.get('status', None)
        if status_query:
            status = status_query.upper().split(',')
            queryset = queryset.filter(status__in=status)
        location = query_params.get('location', None)
        if location:
            queryset = queryset.filter(location=location)
        department = query_params.get('department', None)
        if department:
            queryset = queryset.filter(department=department)
        company = query_params.get('company', None)
        if company:
            queryset = queryset.filter(company=company)
        position = query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        limit = query_params.get('limit', 10)
        offset = query_params.get('offset', 0)
        if limit and offset:
            queryset = queryset[offset:offset + limit]
        return queryset.all()

    def test_list_employee(self):
        companies = Company.objects.all()
        company_id = random.choice(companies).id
        query_params = {
            'limit': 10,
            'offset': 10
        }
        resource_url = f'/api/v1/company/{company_id}/employees'
        if query_params:
            query_strs = [f'{k}={v}' for k, v in query_params.items()]
            resource_url += f"?{'&'.join(query_strs)}"
        res = self.client.get(resource_url)
        response_data = res.json()["results"]
        response_ids = [i["id"] for i in response_data]
        employees = self.get_employees(company_id, **query_params)
        employee_ids = [i.id for i in employees]

        assert set(response_ids) == set(employee_ids)

        company = Company.objects.get(id=company_id)
        columns = company.columns
        columns.append('id')
        data_sample = response_data[0]
        for col in data_sample.keys():
            assert col in columns
