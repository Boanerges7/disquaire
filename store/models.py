from django.db import models


# Create your models here.
class Artist(models.Model):
	name = models.CharField('nom', max_length=200, unique=True)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'artiste'
		verbose_name_plural = 'artistes'


class Contact(models.Model):
	email = models.EmailField('email', max_length=100)
	name = models.CharField('nom', max_length=200)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'prospect'
		verbose_name_plural = 'prospects'


class Album(models.Model):
	reference = models.IntegerField('référence', null=True)
	created_at = models.DateTimeField('date création', auto_now_add=True)
	available = models.BooleanField('disponible?', default=True)
	title = models.CharField('titre', max_length=200)
	picture = models.URLField('maquette')
	artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

	def __str__(self):
		return self.title


	class Meta:
		verbose_name = 'disque'
		verbose_name_plural = 'disques'


class Booking(models.Model):
	created_at = models.DateTimeField('date création', auto_now_add=True)
	contacted = models.BooleanField('contacté?', default=False)
	album = models.OneToOneField(Album, on_delete=models.CASCADE)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

	def __str__(self):
		return self.contact.name


	class Meta:
		verbose_name = 'réservation'
		verbose_name_plural = 'réservations'