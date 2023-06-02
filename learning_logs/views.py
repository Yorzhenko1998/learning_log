from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""Main page "Журнал спостережень"."""
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	"""Displays all topics."""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""Show a single topic all its entries."""
	topic = get_object_or_404(Topic, id=topic_id)
	# Make sure the topic belongs to the current user.
	check_topic_owner(topic, request.user)

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""Add a new topic."""
	if request.method != 'POST':
		# No data sent; create an empty form.
		form = TopicForm()
	else:
		# POST sent; process the data.
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('learning_logs:topics')

	# Show empty or invalid form.
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new entry for a particular topic."""
	topic  = Topic.objects.get(id=topic_id)
	check_topic_owner(topic, request.user)

	if request.method != 'POST':
		# No data sent; create an empty form.
		form = EntryForm()
	else:
		# Received data in the POST-request; process the data.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)

	# Show empty or valid form.
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edit an existing entry."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	check_topic_owner(topic, request.user)

	if request.method != 'POST':
		# Initial request; pre-fill form with the current entry.
		form = EntryForm(instance=entry)
	else:
		# POST data submitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(topic, user):
	"""Make sure the currently logged-in user owns the topic that's
	    being requested.

	    Raise Http404 error if the user does not own the topic.
	"""
	if topic.owner != user:
		raise Http404

@login_required
def delete_topic(request, topic_id):
	"""Get the topic object or return a 404 error if the topic does not exist."""
	topic = Topic.objects.get(id=topic_id)

	# We check whether the current user is the owner of the topic.
	check_topic_owner(topic, request.user)

	if request.method == 'POST':
		# Delete topic.
		topic.delete()
		return redirect('learning_logs:topics')

	context = {'topic': topic}
	return render(request, 'learning_logs/delete_topic.html', context)
