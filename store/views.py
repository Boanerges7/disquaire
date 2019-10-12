from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from .models import Album, Artist, Booking, Contact
from .forms import ContactForm, ParagraphErrorList


def index(request):
	albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
	context = {
		'albums': albums
	}

	return render(request, 'store/index.html', context)

def listing(request):
	albums_list = Album.objects.filter(available=True)
	paginator = Paginator(albums_list, 2)
	page = request.GET.get('page')

	try:

		albums = paginator.page(page)
	except PageNotAnInteger:

		albums = paginator.page(1)
	except:

		albums = paginator.page(paginator.num_pages)

	context = {
		'albums': albums,
		'paginate': True
	}

	return render(request, 'store/listing.html', context)

def detail(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	artists = [artist.name for artist in album.artists.all()]
	artists_name = " ".join(artists)

	context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }

	if request.method == 'POST':
		form = ContactForm(request.POST, error_class=ParagraphErrorList)
		if form.is_valid():
			# Form is correct
			# we can proceed to booking
			email = form.cleaned_data['email']
			name = form.cleaned_data['name']

			# Use a transaction and add an Exception caption
			try:
				with transaction.atomic():
					contact = Contact.objects.filter(email=email)

					# If contact didn't exists, create new one
					if not contact.exists():
						contact = Contact.objects.create(
							name=name,
							email=email
						)
					else:
						contact = contact.first()

					# If no album matches with id, it means the form must have been tweaked
					# so returning a 404 is the bwst solution.
					album = get_object_or_404(Album, id=album_id)
					booking = Booking.objects.create(
						contact = contact,
						album =album
					)

					# Make sure no one can book the album again.
					album.available = False
					album.save()

					context = {
						'album_title': album.title,
					}

					return render(request, 'store/merci.html', context)
			except IntegrityError:
				forms.errors['internal']= "An internal error has happen. Please try again."

	else:
		form = ContactForm()

	# Form data dosen't match the expected format
	# Add errors to the template
	context['form'] = form
	context['errors'] = form.errors.items()

	return render(request, 'store/detail.html', context)

def search(request):
	query = request.GET.get('query')

	if not query:
		albums = Album.objects.all()

	else:
		# title contains the query and query isn't case sensitive
		# (we use icontains instead of contains to add no case sensitive)
		albums = Album.objects.filter(title__icontains=query)

	if not albums.exists():
		albums = Album.objects.filter(artists__name__icontains=query)

	title = f"{query} results"
	context = {
		'albums': albums,
		'title': title
	}

	return render(request, 'store/search.html', context)
	