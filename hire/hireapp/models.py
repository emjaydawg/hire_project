
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

def name_from_attached_user(user):
    name = ""
    if user.first_name or user.last_name:
        name = "%s %s" % (user.first_name, user.last_name)
    else:
        name = user.username
    return name

class Profile(models.Model):
    STAFF = 1
    COMPANY_CONTACT = 2
    EMPLOYEE = 3
    UNDEFINED_PROFILE = 4
    PROFILE_CHOICES = (
        (STAFF, "Staff"),
        (COMPANY_CONTACT, "Company Contact"),
        (EMPLOYEE, "Future Employee"),
        (UNDEFINED_PROFILE, "Non-Classified Profile"),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.RESTRICT)
    phone_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        unique=True
    )
    profile_type = models.PositiveSmallIntegerField(
        choices=PROFILE_CHOICES,
        null=True,
        blank=True)


    def __str__(self):
        roles = dict(self.PROFILE_CHOICES)
        if self.profile_type:
            label = roles[self.profile_type]
        else:
            label = "Orphaned Profile"
        return "%s: %s" % (label, self.user.username)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        Profile(user=instance).save()


class Employee(models.Model):
    # Intentionally leaving this a text field
    # until we better understand hiring needs
    user = models.OneToOneField(
        User,
        on_delete=models.RESTRICT)
    skills = models.TextField(
        blank=True,
        null=True)
    ratings = models.ManyToManyField(
        'Rating',
        blank=True,
        null=True)

    def average_rating(self):
        sum = 0
        ratings = self.ratings.values()
        num_ratings = len(ratings)
        if num_ratings:
            for rating in ratings:
                sum = sum + rating['score']
        else:
            return "Not yet rated"

        return float(sum) / num_ratings / 2

    def __str__(self):
        name = name_from_attached_user(self.user)
        return "%s (%s)" % (name, self.average_rating())

class HiringManager(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.RESTRICT)
    company = models.ForeignKey(
        'Company',
        blank=True,
        null=True,
        on_delete=models.RESTRICT)

    def __str__(self):
        name = name_from_attached_user(self.user)
        return "%s: %s" % (self.company.name, name)

class Rating(models.Model):
    hiring_manager = models.ForeignKey(
        HiringManager,
        on_delete=models.RESTRICT)
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    def __str__(self):
        name = name_from_attached_user(self.hiring_manager.user)
        return "%s: %s" % (name, float(self.score) / 2)


class Company(models.Model):
    """Business Entity that is hiring"""

    MAX_NAME_LENGTH = 85

    slug = models.SlugField(
        unique=True,
        default='',
        editable=False,
        max_length=MAX_NAME_LENGTH)

    name = models.CharField(
        max_length=MAX_NAME_LENGTH
    )
    description = models.TextField(
        blank=True,
        null=True)
    street = models.CharField(
        max_length=60,
        blank=True,
        null=True)
    city = models.CharField(
        max_length=17,
        blank=True,
        null=True)
    state = models.CharField(
        max_length=2,
        blank=True,
        null=True)
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True)
    website = models.URLField(
        max_length=200,
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        value = self.name
        if not self.slug:
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.slug, self.name)


class Job(models.Model):
    MAX_TITLE_LENGTH = 30
    NOT_SPECIFIED = "N"
    FULL_TIME = "F"
    PART_TIME = "P"

    RATE_HOUR = "H"
    RATE_WEEK = "W"
    RATE_MONTH = "M"
    RATE_YEAR = "Y"

    WORK_TYPE_CHOICES = [
      (NOT_SPECIFIED, 'Not Specified'),
      (FULL_TIME, 'Full Time'),
      (PART_TIME, 'Part Time'),
    ]

    RATE_TYPE_CHOICES = [
      (NOT_SPECIFIED, 'Not Specified'),
      (RATE_HOUR, 'Hourly'),
      (RATE_WEEK, 'Weekly'),
      (RATE_MONTH, 'Monthly'),
      (RATE_YEAR, 'Yearly'),
    ]

    slug = models.SlugField(
        unique=True,
        default='',
        editable=False,
        max_length=Company.MAX_NAME_LENGTH + MAX_TITLE_LENGTH + 1)

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH)
    location = models.CharField(
        max_length=30)
    summary = models.TextField()
    requirements = models.TextField()
    work_type = models.CharField(
        max_length=1,
        choices=WORK_TYPE_CHOICES,
        default=NOT_SPECIFIED)
    posted_date = models.DateTimeField(
        auto_now_add=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.RESTRICT)
    rate_amount = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        blank=True,
        null=True)
    rate_unit = models.CharField(
        max_length=1,
        choices=RATE_TYPE_CHOICES,
        default=NOT_SPECIFIED)

    # Applications

    def save(self, *args, **kwargs):
        value = self.title
        if not self.slug:
            self.slug = slugify(
                "%s-%s" % (self.company.slug, value),
                allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.title, self.slug)

class Application(models.Model):
    STATUS_APPLIED = "P"
    STATUS_CONSIDERING = "C"
    STATUS_ACCEPT = "A"
    STATUS_DECLINE = "D"

    STATUS_CHOICES = [
      (STATUS_APPLIED, 'Applied'),
      (STATUS_CONSIDERING, 'Considering'),
      (STATUS_ACCEPT, 'Accepted'),
      (STATUS_DECLINE, 'Decline'),
    ]

    job = models.ForeignKey(
        'Job',
        on_delete=models.RESTRICT)
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.RESTRICT)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_APPLIED)
    start_date = models.DateField(
        blank=True,
        null=True)

    def __str__(self):
        status = dict(self.STATUS_CHOICES)[self.status]
        return "%s(%s): %s" % (self.employee, self.job, status)

class Message(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name="from_user",
        on_delete=models.RESTRICT)
    to_user = models.ForeignKey(
        User,
        related_name="to_user",
        on_delete=models.RESTRICT)
    subject = models.CharField(
        max_length=60,
    )
    time_sent = models.DateTimeField(
        auto_now_add=True)
    time_read = models.DateTimeField(
        blank=True,
        null=True)
    message = models.TextField()

    def __str__(self):
        from_name = name_from_attached_user(self.from_user)
        to_name = name_from_attached_user(self.to_user)
        return "%s -> %s / %s" % (from_name, to_name, self.subject)
