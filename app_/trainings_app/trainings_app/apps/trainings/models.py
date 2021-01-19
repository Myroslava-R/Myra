from django.db import models

class Training(models.Model):
	# training_id    = models.PositiveSmallIntegerField('ід походу') # only 0,1, ... ,32767
	name       = models.CharField('назва тренування',max_length = 100)
	photo_url  = models.URLField('посилання на фото тренування',max_length = 1000) # maxlen 200 (default)
	regione    = models.CharField('територія де відбуватиметься тренування',max_length = 50)
	difficulty = models.PositiveSmallIntegerField('складність')

	def __str__(self):
		return f'{self.id}_{self.name}'

	class Meta:
		verbose_name = 'Похід'
		verbose_name_plural = 'Походи'



class Training_event(models.Model):
	date = models.DateTimeField('дата створення події')
	start_date = models.DateTimeField('запланована дата початку тренування')
	training = models.OneToOneField(Training,on_delete = models.CASCADE)

	def __str__(self):
		return f'{self.id}. {self.start_date}_{self.training.name}'

	class Meta:
		verbose_name = 'Подія тренування'
		verbose_name_plural = 'Події тренування'



class Person(models.Model):
	nickname   = models.CharField('нік',max_length = 30)
	password   = models.CharField('пароль',max_length = 40)
	name       = models.CharField('ім`я',max_length = 30)
	age        = models.PositiveSmallIntegerField('вік')
	phone      = models.CharField('мобільний номер',max_length = 30)
	email      = models.EmailField('email',max_length = 30)
	condition  = models.PositiveSmallIntegerField('фізичний стан')
	training_event = models.ForeignKey(Training_event,on_delete = models.SET_NULL,blank=True,null=True) # одна людина не може бути записана одночасно в 2 походи (тому такий зв`язок є коректним)

	def __str__(self):
		return f'{self.id}. {self.name}({self.nickname})'

	class Meta:
		verbose_name = 'Учасник'
		verbose_name_plural = 'Учасники'