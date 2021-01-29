from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Employer(models.Model):
    # Should we call this company? Many other sites do
    company_name = models.CharField(max_length=30)
    company_description = models.TextField()
    website = models.URLField(max_length=200)
    company_name = models.CharField(max_length=30)
    company_size = models.CharField(max_length=30)
    founded = models.IntegerField()

    def __str__(self):
        return self.company_name

class Job(models.Model):
    NOT_SPECIFIED = "N"
    FULL_TIME = "F"
    PART_TIME = "P"

    WORK_TYPE_CHOICES = [
      (NOT_SPECIFIED, 'Not Specified'),
      (FULL_TIME, 'Full Time'),
      (PART_TIME, 'Part Time'),
    ]

    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    summary = models.TextField()
    requirements = models.TextField()
    WorkType = models.CharField(
        max_length=1,
        choices=WORK_TYPE_CHOICES,
        default=NOT_SPECIFIED
    )
    # When posted
    # Industries

    def __str__(self):
        return self.name

