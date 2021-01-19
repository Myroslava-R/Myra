from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Training,Training_event,Person
# from request import get as GET, put as PUT, delete as DELETE

import json
from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)

# redis -> R
def Rget(key):
	return redis_instance.get(key)

def Rput(key,val):
	redis_instance.set(key, val)

def Rdelete(key):
	redis_instance.delete(key)

# http://127.0.0.1:8000
def start(request):
	return HttpResponseRedirect(reverse('trainings:training_list_view'))

# http://127.0.0.1:8000/training_list
def training_list_view(request):
	training_list = Training.objects.order_by('difficulty')

	PersonID = Rget('PersonID')
	if PersonID:
		login = Person.objects.get(id = int(PersonID))
		return render(request, 'trainings/trainings_list.html', {'training_list': training_list,'login':login})

	return render(request, 'trainings/trainings_list.html', {'training_list': training_list})

# http://127.0.0.1:8000/training_list/<int:training_id>
def training_view(request, training_id):
	try:
		training = Training.objects.get(id = training_id)
	except:
		raise Http404('Виникла помилка, тренування з таким id не має)')

	PersonID = Rget('PersonID')
	if PersonID:
		login = Person.objects.get(id = int(PersonID))
		return render(request, 'trainings/training.html', {'training': training,'login': login})

	return render(request, 'trainings/training.html', {'training': training})

# http://127.0.0.1:8000/training_list/<int:training_id>/add_person
def add_person(request, training_id):
	return HttpResponseRedirect(reverse('trainings:start'))

# http://127.0.0.1:8000/register
def register_view(request):
	return render(request, 'accounts/register.html')

# http://127.0.0.1:8000/register/create_person
def create_person(request):
	user = Person(
		nickname  = request.GET['nickname' ],
		password  = request.GET['password' ], 
		name      = request.GET['name'     ],
		age       = request.GET['age'      ],
		phone     = request.GET['phone'    ],
		email     = request.GET['email'    ],
		condition = request.GET['condition'],
	)

	user.save()
	Rput('PersonID',user.id)

	return HttpResponseRedirect(reverse('trainings:training_list_view'))

# http://127.0.0.1:8000/log_in
def log_in_view(request):
	return render(request, 'accounts/log_in.html')

# http://127.0.0.1:8000/log_in/check
def log_in(request):
	try:
		user = Person.objects.get(nickname=request.GET['nickname'])
		if user.password == request.GET['password']:
			Rput('PersonID',user.id)
			return HttpResponseRedirect(reverse('trainings:training_list_view'))
		else:
			return Http404('Такого Акаунту з таким паролем не існує')
	except:
		raise Http404('Такого Акаунту з таким паролем не існує')
	# return render(request, 'accounts/log_in.html')

# http://127.0.0.1:8000/log_out
def log_out(request):
	Rdelete('PersonID')
	return HttpResponseRedirect(reverse('trainings:training_list_view'))


