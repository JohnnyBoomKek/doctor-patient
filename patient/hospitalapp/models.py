from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    full_name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self) -> str:
        return self.full_name

class Treatment(models.Model):
    RESULT_CHOICES = (
        ('S', 'Successful'),
        ('U', 'Unsuccessful')
    )
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    treatment_start = models.DateField()
    treatment_end = models.DateField(null=True)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)

    def __str__(self) -> str:
        return f'{self.patient.full_name}\'s treatment '

class Document(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    treatment = models.ForeignKey('Treatment', null=True, on_delete=models.CASCADE, related_name='document')
    header = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.header

class DocumentBody(models.Model):
    document = models.OneToOneField('Document', on_delete=models.CASCADE, related_name='document_body')
    body = models.JSONField()