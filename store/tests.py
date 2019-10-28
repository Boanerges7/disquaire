from django.test import TestCase
from django.urls import reverse
from .models import Album, Artist, Contact, Booking


# Index page
class IndexPageTestCase(TestCase):
	# test that index page returns a 200
	def test_index_page(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)

# Detail page
class DetailPageTestCase(TestCase):
	# ran before each test
	def setUp(self):
		impossible = Album.objects.create(title='Jesus est la réponse')
		self.album = Album.objects.get(title='Jesus est la réponse')

	# test that detail page returns a 200 if the item exists
	def test_detail_page_returns_200(self):
		album_id = self.album.id
		response = self.client.get(reverse('store:detail', args=(album_id,)))
		self.assertEqual(response.status_code, 200)

	# test that detail page returns a 404 if the item doesn't exist
	def test_detail_page_returns_404(self):
		album_id = self.album.id + 1
		response = self.client.get(reverse('store:detail', args=(album_id,)))
		self.assertEqual(response.status_code, 404)

# Booking page
class BookingPageTestCase(TestCase):
	# ran before each test
	def setUp(self):
		Contact.objects.create(name='Ulrich', email='ul@gmail.com' )
		album = Album.objects.create(title='I open eyes')
		constance = Artist.objects.create(name='Constatance')
		album.artists.add(constance)
		self.album = Album.objects.get(title='I open eyes')
		self.contact = Contact.objects.get(name='Ulrich')

	# test that a new booking is made
	def test_new_booking_is_registered(self):
		old_bookings = Booking.objects.count() # count bookings before a request
		album_id = self.album.id
		name = self.contact.name
		email = self.contact.email
		response = self.client.post(reverse('store:detail', args=(album_id,)),{
				'name': name,
				'email': email
			})
		new_bookings = Booking.objects.count() # count bookings after
		self.assertEqual(new_bookings, old_bookings + 1)

	# test that a booking belongs to a contact
	def test_a_booking_belongs_to_a_contact(self):
		album_id = self.album.id
		name = self.contact.name
		email = self.contact.email

		response = self.client.post(reverse('store:detail', args=(album_id,)),{
				'name': name,
				'email': email
			})
		last_booking = Booking.objects.last() # search album booked

		self.assertEqual(last_booking.contact.id, self.contact.id)

	# test that a booking belongs to an album
	def test_a_booking_belongs_to_an_album(self):
		album_id = self.album.id
		name = self.contact.name
		email = self.contact.email

		response = self.client.post(reverse('store:detail', args=(album_id,)),{
				'name': name,
				'email': email
			})

		last_booking = Booking.objects.last() # search last booking
		self.assertEqual(last_booking.album.id, album_id)

	# test that an album isn't available after a booking is made
	def test_album_is_not_available_after_booking(self):
		album_id = self.album.id
		name = self.contact.name
		email = self.contact.email

		response = self.client.post(reverse('store:detail', args=(album_id,)),{
				'name': name,
				'email': email
			})

		# VERIFICATION: 1RST METHOD

			# search booked album
		album_booked = Album.objects.filter(id=self.album.id).first()
		album_availability = album_booked.available # check is availabilty
		self.assertEqual(album_availability, False)

		# VERIFICATION: 2ND METHOD

			# Make the query again, otherwise `available` will still be set at `True`
		self.album.refresh_from_db()
		self.assertFalse(self.album.available)