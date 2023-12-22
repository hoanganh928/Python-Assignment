from rest_framework import serializers

from backend.models import Employee, Company, Position, Location, Department


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    location = LocationSerializer()
    department = DepartmentSerializer()
    company = CompanySerializer()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_company_columns(self):
        view = self.context.get('view')
        company_id = view.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        columns = company.columns
        columns.append('id')
        return columns

    def to_representation(self, instance):
        data = super(EmployeeSerializer, self).to_representation(instance)
        columns = self.get_company_columns()
        data = {k: data[k] for k in columns}
        return data
