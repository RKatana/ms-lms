from django.db import models
from moringaschool.models import Cohort

class Student(models.Model):
    cohort = models.OneToOneField(Cohort, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return f"Enrolled in: {self.cohort.title}"