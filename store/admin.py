from django.contrib import admin
from .models import Booking, Contact, Artist, Album
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class AdminURLMixin(object):
	def get_admin_url(self, obj):

		content_type = ContentType.objects.get_for_model(obj.__class__)
		return reverse(f"admin:store_{content_type.model}_change", args=(obj.id,))

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
	list_filter = ['created_at', 'contacted']
	fields = ['created_at', 'contact_link', 'album_link', 'contacted']
	readonly_fields = ['created_at', 'contact_link', 'contacted', 'album_link']

	def has_add_permission(self, request):
		return False

	def contact_link(self, booking):
		url = self.get.get_admin_url(booking.contact)
		return mark_safe(f"<a href='{url}'>{booking.contact.name}</a>")

	def album_link(self, booking):
		url = self.get_admin_url(booking.album)
		return mark_safe(f'<a href="{url}">{booking.album.title}</a>')


# Relation: "One to One" OR "Many to One"
class BookingInline(admin.TabularInline, AdminURLMixin):
	model = Booking
	extra = 0 # We don't want display an additional 
	# fieldsets = [
	# 	(None, {'fields': ['album', 'contacted']})
	# ] # list columns
	readonly_fields = ['created_at', 'contacted', 'album_link']
	fields = ['created_at', 'album_link', 'contacted']
	# field to add a booking
	# Edit name in admin panel
	verbose_name = 'Réservations'
	verbose_name_plural = 'Réservations'

	# Disallow superadmin to add booking in admin panel
	def has_add_permission(self, request):
		return False

	def album_link(self, booking):
		url = self.get_admin_url(booking.album)
		return mark_safe(f"<a href='{url}'>{booking.album.title}</a>")

	album_link.short_description = 'Album'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	inlines = [BookingInline,] # list of bookings made by a contact


#-------------------------------------------------#


# Relation: "Many to Many"
class AlbumArtistInline(admin.TabularInline):
	model = Album.artists.through # the query goes through an intermediate table
	extra = 1
	verbose_name = 'Disque'
	verbose_name_plural = 'Disques'


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	inlines = [AlbumArtistInline,]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	search_fields = ['reference', 'title']