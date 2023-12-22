from backend.models import Company


def run():
    Company.objects.all().delete()