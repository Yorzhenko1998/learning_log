from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
	"""Register a new user."""
	if request.method != 'POST':
		# Show empty register form.
		form = UserCreationForm()
	else:
		# Process the completed form.
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()
			# Authorize the user and direct him to the main page.
			login(request, new_user)
			return redirect('learning_logs:index')

	# Show empty or invalid form.
	context = {'form': form}
	return render(request, 'registration/register.html', context)
