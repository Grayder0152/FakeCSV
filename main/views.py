from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView
)
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from celery.result import AsyncResult

from .models import Schema, DataSet
from .forms import ColumnSchemaFormSet, SchemaForm
from .tasks import generate_task


def get_task_info(request):
    task_id = request.GET.get('task_id')
    file_id = request.GET.get('file_id')
    task = AsyncResult(task_id)
    data = {'state': task.state}
    if task.state == 'SUCCESS':
        data_set = DataSet.objects.get(id=file_id)
        data_set.status = True
        data_set.csv_file = f'media/csv-files/{str(data_set)}.csv'
        data_set.task_id = None
        data_set.save(update_fields=['status', 'csv_file', 'task_id'])

        data.update({'file_url': data_set.csv_file.name})
    return JsonResponse(data)


class SchemasViews(LoginRequiredMixin, ListView):
    model = Schema
    login_url = '/user/login/'
    context_object_name = 'schema_list'

    def get_queryset(self):
        return Schema.objects.filter(user_id=self.request.user.id)


class SchemaDelete(DeleteView):
    model = Schema
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DataSetsViews(LoginRequiredMixin, DetailView):
    model = Schema
    context_object_name = 'schema'
    template_name = 'main/data_sets.html'

    def post(self, request, *args, **kwargs):
        rows = request.POST.get('rows')
        schema = self.get_object()
        data_set = DataSet.objects.create(schema=schema)
        columns = schema.columns.order_by('order')
        columns_with_range = [column for column in columns if column.column_type == 'I']
        columns_ranges = {column.name: (column.range_from, column.range_to) for column in columns_with_range}
        task = generate_task.delay(
            rows=int(rows),
            filename=str(data_set),
            column_separated=schema.column_separator,
            string_separated=schema.string_separator,
            columns_headers=[header.name for header in columns],
            columns_types=[header.column_type for header in columns],
            columns_ranges=columns_ranges
        )

        data_set.task_id = task.task_id
        data_set.save()
        return super().get(request, *args, **kwargs)


class _SchemaColumnBase(LoginRequiredMixin):
    model = Schema
    form_class = SchemaForm
    login_url = '/user/login/'
    success_url = '/'
    template_name = 'main/new_schema.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnSchemaFormSet(self.request.POST, instance=self.object)
        else:
            data['columns'] = ColumnSchemaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']

        with transaction.atomic():
            self.object = form.save()

            if columns.is_valid():
                columns.instance = self.object
                columns.save()
            else:
                print(columns.errors)
                return super().form_invalid(form)
        return super().form_valid(form)


class SchemaColumnCreate(_SchemaColumnBase, CreateView):
    pass


class SchemaColumnUpdate(_SchemaColumnBase, UpdateView):
    pass
