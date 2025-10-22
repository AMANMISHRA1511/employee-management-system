from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('details/<int:pk>/', views.employee_details, name='employee_details'),
    path('files/', views.files_page, name='files'),
    path('settings/', views.settings_page, name='settings'),

    # Export / Import / Backup / Clear
    path('export/<str:format>/', views.export_employees, name='export_employees'),
    path('import/', views.import_employees, name='import_employees'),
    path('create-backup/', views.create_backup, name='create_backup'),
    path('clear-all/', views.clear_all_data, name='clear_all_data'),
    path('create-full-backup/', views.create_full_backup, name='create_full_backup'),
]
