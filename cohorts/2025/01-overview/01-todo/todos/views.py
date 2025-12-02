from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

# List all TODOs
class TodoListView(ListView):
    model = Todo
    template_name = 'home.html'
    context_object_name = 'todos'

# Create a new TODO
class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todo_list')

# Update an existing TODO
class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todo_form.html'
    fields = ['title', 'description', 'due_date', 'is_completed']
    success_url = reverse_lazy('todo_list')

# Delete a TODO
class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

# Toggle TODO completion status
def toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')
