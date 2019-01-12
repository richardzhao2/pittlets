from django.shortcuts import render
from .models import Listing
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import ListingForm, SignUpForm, ImageForm, filterForm
from app.forms import Image
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# renders the home screen, saying hello to the user if logged in, and guest if not
def home(request):
    if request.user.is_authenticated:
        authenticated = True
    else:
        authenticated = False

    all_listings = Listing.objects.order_by('-pub_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_listings, 5)

    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    all_images = Image.objects.all()

    context = {'listings': listings, 'is_authenticated': authenticated,
               'user': request.user, 'list_of_image_querysets': all_images}
    return render(request, 'home.html', context)


def about(request):
    if request.user.is_authenticated:
        authenticated = True
    else:
        authenticated = False

    context = {'is_authenticated': authenticated}
    return render(request, 'about.html', context)


def search(request):
    if request.method == 'GET':
        form = filterForm(request.GET)
        amenities = []
        type = 'None'

        search_query = {}

        # check which filter to use
        if form.is_valid():
            amenities = form.cleaned_data.get('amenities')
            type = form.cleaned_data.get('type') # ['doorman, 'furnished', 'pets']

            if amenities != []:
                search_query['amenities'] = amenities
            search_query['type'] = type


        else:
            query = request.GET.get('search_box', '')
            search_query['description'] = query



        all_listings = Listing.objects.order_by('-pub_date')
        if 'amenities' in search_query:
            for amenity in search_query['amenities']:
                all_listings = all_listings.filter(amenities__icontains=amenity)

        if 'type' in search_query:
            all_listings = all_listings.filter(type__icontains= search_query['type'])

        if 'description' in search_query:
            all_listings = Listing.objects.filter(description__icontains=search_query['description'])

        if request.user.is_authenticated:
            authenticated = True
        else:
            authenticated = False

        all_listings = all_listings.order_by('-pub_date')
        page = request.GET.get('page', 1)
        paginator = Paginator(all_listings, 5)

        try:
            listings = paginator.page(page)
        except PageNotAnInteger:
            listings = paginator.page(1)
        except EmptyPage:
            listings = paginator.page(paginator.num_pages)

        all_images = Image.objects.all()

        context = {'listings': listings, 'is_authenticated': authenticated,
                   'user': request.user, 'list_of_image_querysets': all_images, 'form':form}
    else:
        form = filterForm()

    return render(request, 'search.html', context)


@login_required()
def post(request):
    ImageFormSet = modelformset_factory(Image,
                                        form = ImageForm, extra = 1)
    if request.method == 'POST':
        form = ListingForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset= Image.objects.none())
        if form.is_valid() and formset.is_valid():
            amenities = form.cleaned_data.get('amenities')
            type = form.cleaned_data.get('type') # ['doorman, 'furnished', 'pets']

            str_amenities = ''
            for amenity in amenities:
                str_amenities += amenity + ', '

            str_amenities = str_amenities[:-2]

            listing = form.save(commit = False)
            listing.amenities = str_amenities
            listing.user = request.user
            listing.type = type


            listing.save()

            for img in formset.cleaned_data:
                picture = img['image']
                preview = Image(post = listing, photo = picture)
                preview.save()

            return redirect('home')
    else:
        form = ListingForm()
        formset = ImageFormSet(queryset = Image.objects.none())
    return render(request, 'post.html', {'form': form , 'is_authenticated' : True, 'formset' : formset})

@login_required()
def edit(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)

    form = ListingForm(request.POST or None, instance = listing, initial={'user': request.user})

    if request.user == listing.user:
        if form.is_valid(): #and formset.is_valid():
            amenities = form.cleaned_data.get('amenities')
            type = form.cleaned_data.get('type')  # ['doorman, 'furnished', 'pets']

            str_amenities = ''
            for amenity in amenities:
                str_amenities += amenity + ', '

            str_amenities = str_amenities[:-2]
            listing.amenities = str_amenities
            listing.user = request.user
            listing.type = type

            listing.save()

            messages.add_message(
                request, messages.SUCCESS, 'Listing has been modified',
                fail_silently = True,
            )
            return redirect('home')

        return render(request, 'post.html', {'form':form, 'listing':listing}) # add formset:formset to get image
    else:
        messages.error(request, "This isn't your listing")
        return redirect('home')

@login_required()
def delete(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if request.user == listing.user:
        listing.delete()
        messages.add_message(
            request, messages.SUCCESS, 'Listing has been delete',
            fail_silently=True,
        )
        return redirect('home')

    else:
        messages.error(request, "This isn't your listing")
        return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            messages.add_message(request, messages.INFO, 'You have successfully registered')
            return redirect('home')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def listing_post(request, listing_id):
    if request.user.is_authenticated:
        authenticated = True
    else:
        authenticated = False
    listing = Listing.objects.get(pk=listing_id)
    cur_user = request.user

    images = Image.objects.get(post=listing.id)
    listing_owner = listing.user
    return render(request, 'listing.html', {'listing':listing, 'is_authenticated':authenticated, 'images':images, 'owner':listing_owner, 'cur_user':cur_user})
