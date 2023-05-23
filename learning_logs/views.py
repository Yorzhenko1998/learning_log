from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""Main page "Журнал спостережень"."""
	return render(request, 'learning_logs/index.html')

def topics(request):
	"""Displays all topics."""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
	"""Show a single topic all its entries."""
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
	"""Add a new topic."""
	if request.method != 'POST':
		# No data sent; create an empty form.
		form = TopicForm()
	else:
		# POST sent; process the data.
		form = TopicForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topics')

	# Show empty or invalid form.
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
	"""Add a new entry for a particular topic."""
	topic  = Topic.objects.get(id=topic_id)
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

def edit_entry(request, entry_id):
	"""Edit an existing entry."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

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