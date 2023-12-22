from enum import Enum

from django.db import models


class EmployeeStatus(Enum):
    ACTIVE = "ACTIVE"
    NOT_STARTED = "NOT_STARTED"
    TERMINATED = "TERMINATED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def bulk_create(cls, objects):
        objs_to_create = []
        for obj in objects:
            objs_to_create.append(cls(**obj))
        cls.objects.bulk_create(objs_to_create)


class Department(BaseModel):
    name = models.CharField(max_length=50)


class Position(BaseModel):
    name = models.CharField(max_length=50)


class Location(BaseModel):
    name = models.CharField(max_length=50)


class Company(BaseModel):
    name = models.CharField(max_length=50)
    columns = models.JSONField()


class Employee(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=EmployeeStatus.choices(), db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
