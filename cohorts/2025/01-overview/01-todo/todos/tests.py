from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for the Todo model"""
    
    def setUp(self):
        """Set up test data"""
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="This is a test TODO",
            due_date=date.today() + timedelta(days=7)
        )
    
    def test_todo_creation(self):
        """Test that a TODO can be created"""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "This is a test TODO")
        self.assertIsNotNone(self.todo.due_date)
        self.assertFalse(self.todo.is_completed)
    
    def test_todo_default_is_completed(self):
        """Test that is_completed defaults to False"""
        new_todo = Todo.objects.create(title="Another TODO")
        self.assertFalse(new_todo.is_completed)
    
    def test_todo_string_representation(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.todo), "Test TODO")
    
    def test_todo_optional_fields(self):
        """Test that optional fields can be null/blank"""
        minimal_todo = Todo.objects.create(title="Minimal TODO")
        self.assertEqual(minimal_todo.description, "")
        self.assertIsNone(minimal_todo.due_date)
    
    def test_todo_ordering(self):
        """Test that TODOs are ordered by created_at descending"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0].title, "Second")
        self.assertEqual(todos[1].title, "First")


class TodoListViewTest(TestCase):
    """Test cases for the list view"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.url = reverse('todo_list')
        
    def test_list_view_status_code(self):
        """Test that list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Test that list view uses home.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_list_view_displays_todos(self):
        """Test that list view displays TODOs"""
        Todo.objects.create(title="Test TODO 1")
        Todo.objects.create(title="Test TODO 2")
        response = self.client.get(self.url)
        self.assertContains(response, "Test TODO 1")
        self.assertContains(response, "Test TODO 2")
    
    def test_list_view_empty_state(self):
        """Test list view when no TODOs exist"""
        response = self.client.get(self.url)
        self.assertContains(response, "No TODOs yet!")


class TodoCreateViewTest(TestCase):
    """Test cases for the create view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('todo_create')
    
    def test_create_view_status_code(self):
        """Test that create view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_uses_correct_template(self):
        """Test that create view uses todo_form.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_form.html')
    
    def test_create_todo_with_valid_data(self):
        """Test creating a TODO with valid data"""
        data = {
            'title': 'New TODO',
            'description': 'Description here',
            'due_date': '2025-12-31'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
    
    def test_create_todo_without_required_field(self):
        """Test that title is required"""
        data = {
            'description': 'Description without title',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Stays on form page
        self.assertFalse(Todo.objects.filter(description='Description without title').exists())
    
    def test_create_todo_with_minimal_data(self):
        """Test creating a TODO with only required fields"""
        data = {'title': 'Minimal TODO'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='Minimal TODO').exists())


class TodoUpdateViewTest(TestCase):
    """Test cases for the update view"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original Description"
        )
        self.url = reverse('todo_update', args=[self.todo.pk])
    
    def test_update_view_status_code(self):
        """Test that update view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_update_view_uses_correct_template(self):
        """Test that update view uses todo_form.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_form.html')
    
    def test_update_todo_with_valid_data(self):
        """Test updating a TODO with valid data"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'is_completed': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertTrue(self.todo.is_completed)
    
    def test_update_nonexistent_todo(self):
        """Test updating a TODO that doesn't exist"""
        url = reverse('todo_update', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    """Test cases for the delete view"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.todo = Todo.objects.create(title="To Be Deleted")
        self.url = reverse('todo_delete', args=[self.todo.pk])
    
    def test_delete_view_status_code(self):
        """Test that delete view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_view_uses_correct_template(self):
        """Test that delete view uses todo_confirm_delete.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_confirm_delete.html')
    
    def test_delete_todo(self):
        """Test deleting a TODO"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
    
    def test_delete_nonexistent_todo(self):
        """Test deleting a TODO that doesn't exist"""
        url = reverse('todo_delete', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleCompleteTest(TestCase):
    """Test cases for the toggle complete function"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.todo = Todo.objects.create(title="Toggle TODO")
        self.url = reverse('todo_toggle', args=[self.todo.pk])
    
    def test_toggle_from_incomplete_to_complete(self):
        """Test toggling a TODO from incomplete to complete"""
        self.assertFalse(self.todo.is_completed)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_completed)
    
    def test_toggle_from_complete_to_incomplete(self):
        """Test toggling a TODO from complete to incomplete"""
        self.todo.is_completed = True
        self.todo.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_completed)
    
    def test_toggle_nonexistent_todo(self):
        """Test toggling a TODO that doesn't exist"""
        url = reverse('todo_toggle', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoURLTest(TestCase):
    """Test cases for URL patterns"""
    
    def test_list_url_resolves(self):
        """Test that todo_list URL resolves"""
        url = reverse('todo_list')
        self.assertEqual(url, '/')
    
    def test_create_url_resolves(self):
        """Test that todo_create URL resolves"""
        url = reverse('todo_create')
        self.assertEqual(url, '/create/')
    
    def test_update_url_resolves(self):
        """Test that todo_update URL resolves"""
        url = reverse('todo_update', args=[1])
        self.assertEqual(url, '/update/1/')
    
    def test_delete_url_resolves(self):
        """Test that todo_delete URL resolves"""
        url = reverse('todo_delete', args=[1])
        self.assertEqual(url, '/delete/1/')
    
    def test_toggle_url_resolves(self):
        """Test that todo_toggle URL resolves"""
        url = reverse('todo_toggle', args=[1])
        self.assertEqual(url, '/toggle/1/')
