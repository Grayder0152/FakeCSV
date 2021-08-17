from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Schema(models.Model):
    COLUMN_SEPARATOR = (
        ('', '-------'),
        (',', 'Comma(,)'),
        ('.', 'Dot(.)'),
        ('|', 'Stick(|)')
    )
    STRING_SEPARATOR = (
        ('', '-------'),
        ('\"', 'Double-quote(")'),
        ("\'", "Quote(')"),
        (';', 'Semicolon(;)'),
    )

    title = models.CharField(max_length=124)
    modified = models.DateField(auto_now_add=True)
    column_separator = models.CharField(max_length=32, choices=COLUMN_SEPARATOR, default=',')
    string_separator = models.CharField(max_length=32, choices=STRING_SEPARATOR, default=';')
    user_id = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Column(models.Model):
    TYPES = (
        ('', '-------'),
        ('FN', 'Full name'),
        ('E', 'Email'),
        ('DN', 'Domain name'),
        ('CN', 'Company name'),
        ('I', 'Integer'),
        ('D', 'Date')
    )

    name = models.CharField(max_length=124)
    column_type = models.CharField(max_length=32, choices=TYPES)
    order = models.PositiveSmallIntegerField()
    range_from = models.PositiveIntegerField(null=True, blank=True)
    range_to = models.PositiveIntegerField(null=True, blank=True)
    schema = models.ForeignKey(Schema, related_name='columns', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}-{self.schema.title}'


class DataSet(models.Model):
    create_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    csv_file = models.FileField(upload_to='csv-files', null=True, blank=True)
    task_id = models.CharField(max_length=124, null=True, blank=True)
    schema = models.ForeignKey(Schema, related_name='csv_files', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.schema.title}-{self.create_at.strftime("%Y-%m-%d_%H:%M:%S")}'
