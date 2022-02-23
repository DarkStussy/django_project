from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class ProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='images/avatars/')


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to='files/')
    mark_done = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Doc(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.task.title


class DocsImage(models.Model):
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to='tasks/images/')

    def __str__(self):
        return self.doc.task.title


class CustomerDoc(models.Model):
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE)
    file_field = models.FileField(upload_to='tasks/files/customer/')

    def __str__(self):
        return self.doc.task.title


class OtherDoc(models.Model):
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE)
    file_field = models.FileField(upload_to='tasks/files/other/')

    def __str__(self):
        return self.doc.task.title


class ObjectDoc(models.Model):
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE)
    file_field = models.FileField(upload_to='tasks/files/objects-analogues/')

    def __str__(self):
        return self.doc.task.title


class BasicDataModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.task.title


class BasicData(models.Model):
    bd_model = models.ForeignKey(BasicDataModel, on_delete=models.CASCADE)
    name_report = models.CharField(max_length=150)
    report_number = models.CharField(max_length=50)
    date_report = models.DateField()
    basis_for_evaluation = models.CharField(max_length=500)
    object_of = models.CharField(max_length=150)
    composition = models.TextField()
    purpose = models.CharField(max_length=500)
    use_obj = models.CharField(max_length=500)
    price_type = models.CharField(max_length=100)
    date_rent_estimate = models.DateField()
    date_inspection = models.DateField()
    range_limits = models.CharField(max_length=100)
    org_legal_form = models.CharField(max_length=500, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    OGRN = models.CharField(max_length=200, blank=True, null=True)
    date_assignment_OGRN = models.DateField(blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    mid_name = models.CharField(max_length=100, blank=True, null=True)
    identity_document = models.ImageField(upload_to='basicdata/identity/', blank=True, null=True)
    location_leg = models.CharField(max_length=250, blank=True, null=True)
    location_ind = models.CharField(max_length=250, blank=True, null=True)
    documents = models.TextField()


class TitleDocument(models.Model):
    bd_model = models.ForeignKey(BasicData, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=200)


class RentEstimateModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.task.title


class RentEstimate1(models.Model):
    re_model = models.ForeignKey(RentEstimateModel, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    area = models.FloatField(default=0)
    price = models.FloatField(default=0)
    offer_price = models.FloatField(default=0)
    info_resource = models.CharField(max_length=250)
    date = models.DateField()
    ad_number = models.CharField(max_length=100)


class CharacteristicsRE1(models.Model):
    re_model = models.ForeignKey(RentEstimateModel, on_delete=models.CASCADE)
    least_offer_price = models.FloatField(default=0)
    greatest_offer_price = models.FloatField(default=0)
    mid_range = models.FloatField(default=0)
    average = models.FloatField(default=0)
    median = models.FloatField(default=0)
    standard_deviation = models.FloatField(default=0)
    coefficient_variation = models.FloatField(default=0)

