import operator
from functools import reduce

from django.db.models import Q
from rest_framework.generics import ListAPIView
from backend.models import Employee, Company
from backend.serializers import EmployeeSerializer

FOREIGN_KEY_FIELDS = ['department', 'company', 'position', 'location']


class ListEmployeeView(ListAPIView):
    serializer_class = EmployeeSerializer
    authentication_classes = []

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        queryset = Employee.objects.filter(company_id=company_id)
        query_params = self.request.query_params
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
        search = query_params.get('search', None)
        if search:
            company = Company.objects.get(id=company_id)
            columns = company.columns
            column_search_queries = {k: search for k in columns}

            search_filters = [
                Q(**{f"{key}__name__icontains": val}) if key in FOREIGN_KEY_FIELDS else Q(**{f"{key}__icontains": val})
                for
                key, val in column_search_queries.items()
            ]
            queryset = queryset.filter(reduce(operator.or_, search_filters))
        return queryset
