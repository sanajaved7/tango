from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	return render(request, 'rango/index.html', context_dict)

def about(request):
	context_dict = {'boldmessage': "This is my about page!"}
	return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name 

		pages = Page.objects.filter(category=category)

		context_dict['pages'] = pages

		context_dict['category'] = category
	except Category.DoesNotExist:
		pass

	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {'form':form, 'category':cat}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	#Tells the template whether registration was successful. Default is False and changes to True when registration is completed successfully.
	registered = False

	#Only want to process the the form data if it's a POST request
	if request.method == 'POST':
		#Grabbing data from the raw form information
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#Checks if forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			#Hash password and update user object
			user.set_password(user.password)
			user.save()

			#Handling UserProfile instance but delaying saving until we're ready to avoid integrity problems
			profile = profile_form.save(commit=False)
			
			#Establishing link between two model instances. This is where user attribute of the UserProfileForm is populted.
			profile.user = user

			#If user provides pictures, input it from the form and put it in the UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			#Save UserProfile model instance
			profile.save()

			#Update variable to tell template registration complete
			registered = True

		#Prints errors if there were issues or mistakes with forms
		else:
			print user_form.errors, profile_form.errors
	#Handles requests that are not HTTP POST by rendering blank version of both forms ready for input
	else:
		user_form = UserForm()
		profile_form = UserProfileForm

	#Renders the template depending on the context
	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

