from django.urls import path
from . import views

app_name = 'trainings'
urlpatterns = [
	path('',views.start, name = 'start'),
	path('training_list',views.training_list_view, name = 'training_list_view'),
	path('training_list/<int:training_id>',views.training_view, name = 'training_view'),
	path('training_list/<int:training_id>/add_person',views.add_person, name = 'add_person'),
	path('register',views.register_view, name = 'register_view'),
	path('register/create_person',views.create_person, name = 'create_person'),
	path('log_in',views.log_in_view, name = 'log_in_view'),
	path('log_in/check',views.log_in, name = 'log_in'),
	path('log_out',views.log_out, name = 'log_out'),
]