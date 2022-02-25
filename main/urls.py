from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('task/<int:task_id>/', views.detail_task, name='detail-task'),
    path('docs/', views.docs_view, name='docs-view'),
    path('docs/<int:docs_id>/', views.detail_docs, name='detail-docs'),
    path('docs/deleteimgs/<int:docs_id>/', views.delete_docs_images, name='delete-imgs-docs'),
    path('docs/deletecstmd/<int:docs_id>/', views.delete_docs_customer, name='delete-cstm-docs'),
    path('docs/deleteotherdcs/<int:docs_id>/', views.delete_docs_other, name='delete-other-docs'),
    path('docs/deleteobjdocs/<int:docs_id>/', views.delete_docs_obj, name='delete-obj-docs'),
    path('help/', views.help_view, name='help'),
    path('basicdata/', views.show_basic_data, name='show-basic-data'),
    path('basicdata/<int:d_id>/', views.detail_basic_data, name='detail-basic-data'),
    path('rentestimates/', views.main_rent_estimates, name='main-rent-estimates'),
    path('rentestimate1/<int:re_id>/', views.show_rent_estimate1, name='show-rent-estimate1'),
    path('rentestimate2/<int:re_id>/', views.show_rent_estimate2, name='show-rent-estimate2'),
    path('rentestimates/delete/<int:re_id>/<int:table_id>/', views.delete_tables, name='delete-tables'),

    # auth
    path('accounts/loginuser/', views.login_user, name='login-user'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
]
