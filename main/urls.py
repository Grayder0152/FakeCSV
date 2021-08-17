from django.urls import path

from . import views

urlpatterns = [
    path('', views.SchemasViews.as_view(), name='data_schemas'),
    path('new-schema/', views.SchemaColumnCreate.as_view(), name='new_schema'),
    path('update-data-schema/<int:pk>/', views.SchemaColumnUpdate.as_view(), name='update_data_schema'),
    path('delete-data-schema/<int:pk>/', views.SchemaDelete.as_view(), name='delete_data_schema'),
    path('data-sets/<int:pk>/', views.DataSetsViews.as_view(), name='data_sets'),
    path('get-task-info/', views.get_task_info, name='get_task_info')
]
