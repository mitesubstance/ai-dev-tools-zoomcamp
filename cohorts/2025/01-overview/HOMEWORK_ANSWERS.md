# Django TODO App - Homework Answers

## Introduction
This document contains detailed answers to all homework questions for the Django TODO application, with explanations for complete beginners.

---

## Question 1: Install Django

**Question:** What's the command you used to install Django?

**Answer:** Using a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install django
```

Or simply: `pip install django` (if already in an activated virtual environment)

### Explanation for Beginners

**What is Django?**
Django is a high-level Python web framework that helps you build websites and web applications quickly. It follows the "batteries included" philosophy, meaning it comes with many built-in features.

**What is a Virtual Environment (venv)?**
A virtual environment is an isolated Python environment that keeps your project dependencies separate from other projects and your system Python. Think of it as a dedicated workspace for your project.

**Why Use Virtual Environments?**
- ✅ **Isolation** - Each project has its own dependencies
- ✅ **No Conflicts** - Different projects can use different versions of packages
- ✅ **Clean System** - Doesn't pollute your global Python installation
- ✅ **Reproducibility** - Easy to recreate the exact environment elsewhere
- ✅ **Best Practice** - Industry standard for Python development

**Complete Installation Steps:**

1. **Create Virtual Environment:**
   ```bash
   python -m venv .venv
   ```
   This creates a `.venv` directory containing an isolated Python environment

2. **Activate Virtual Environment:**
   
   On Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   You'll see `(.venv)` prefix in your terminal when activated

3. **Install Django:**
   ```bash
   pip install django
   ```
   This installs Django only in your virtual environment

4. **Verify Installation:**
   ```bash
   python -m django --version
   ```
   Should display: `5.2.8` (or your Django version)

**Deactivate Virtual Environment:**
When you're done working:
```bash
deactivate
```

**Alternative Methods:**
- `pip3 install django` (if you have both Python 2 and 3)
- `python -m pip install django` (alternative syntax)
- `uv pip install django` (if using uv package manager)
- Direct install without venv: `pip install django` (not recommended)

**What Gets Installed:**
When you install Django, pip also installs these dependencies:
- `asgiref` - ASGI server support
- `sqlparse` - SQL query parsing
- `tzdata` - Timezone data

**Official Documentation:**
- Django Installation Guide: https://docs.djangoproject.com/en/stable/intro/install/
- Getting Started Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Python venv documentation: https://docs.python.org/3/library/venv.html

---

## Question 2: Project and App

**Question:** What's the file you need to edit to include the app in the project?

**Answer:** `settings.py`

### Explanation for Beginners

**Understanding Django Structure**

Django has two main concepts:
1. **Project** - The entire web application (container for settings, configuration)
2. **App** - A specific component/module (like todos, users, blog posts)

**Creating a Project:**
```bash
django-admin startproject todoproject
```
This creates a project with this structure:
```
todoproject/
    manage.py          # Command-line utility
    todoproject/       # Project package
        __init__.py
        settings.py    # Project settings ← WE EDIT THIS FILE
        urls.py        # URL routing
        wsgi.py        # Web server gateway
        asgi.py        # Async server gateway
```

**Creating an App:**
```bash
python manage.py startapp todos
```
This creates:
```
todos/
    __init__.py
    admin.py       # Admin panel configuration
    apps.py        # App configuration
    models.py      # Database models
    tests.py       # Tests
    views.py       # View functions/classes
    migrations/    # Database migrations
```

**Why Edit settings.py?**
Django needs to know which apps are part of your project. In `settings.py`, find `INSTALLED_APPS` and add your app:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todos',  # ← Add your app here
]
```

**Other Options (Incorrect):**
- ❌ `manage.py` - Command-line utility, not for configuration
- ❌ `urls.py` - For URL routing, not app registration
- ❌ `wsgi.py` - For web server deployment, not app registration

**Official Documentation:**
- Projects and Apps: https://docs.djangoproject.com/en/stable/intro/tutorial01/#creating-a-project
- Settings Reference: https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps

---

## Question 3: Django Models

**Question:** What's the next step you need to take after creating models?

**Answer:** Run migrations

### Explanation for Beginners

**What are Models?**
Models are Python classes that represent database tables. Each model maps to a single database table.

**Our Todo Model:**
```python
class Todo(models.Model):
    title = models.CharField(max_length=200)  # Short text field
    description = models.TextField(blank=True)  # Long text field
    due_date = models.DateField(null=True, blank=True)  # Date field
    is_completed = models.BooleanField(default=False)  # True/False field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto update timestamp
```

**Understanding Migrations**

Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

**The Two-Step Process:**

1. **Create Migration Files:**
   ```bash
   python manage.py makemigrations
   ```
   This examines your models and creates migration files in `todos/migrations/`
   These files contain Python code describing database changes

2. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```
   This executes the migration files and updates your actual database

**Why This is Necessary:**
- Databases don't understand Python classes
- Django needs to translate Python models into database tables
- Migrations track changes over time (like version control for your database)

**What Happens Behind the Scenes:**
```
Python Model → makemigrations → Migration File → migrate → Database Table
```

**Other Options (Incorrect):**
- ❌ Run the application - Won't work without database tables
- ❌ Add models to admin panel - This comes after migrations
- ❌ Create a makefile - Not a Django requirement

**Official Documentation:**
- Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Migrations: https://docs.djangoproject.com/en/stable/topics/migrations/

---

## Question 4: TODO Logic

**Question:** Where do we put the TODO logic?

**Answer:** `views.py`

### Explanation for Beginners

**What are Views?**
Views are Python functions or classes that:
1. Receive web requests
2. Process data (query database, perform calculations)
3. Return web responses (HTML pages, JSON data, redirects)

Think of views as the "brain" of your web application.

**Django MVT Pattern:**

Django follows the MVT (Model-View-Template) pattern:
- **Model** - Database structure (models.py)
- **View** - Business logic (views.py) ← THIS IS WHERE LOGIC GOES
- **Template** - HTML presentation (templates/)

**Our View Logic:**

We implemented 5 views for CRUD operations:

```python
# List all TODOs
class TodoListView(ListView):
    model = Todo
    template_name = 'home.html'

# Create new TODO
class TodoCreateView(CreateView):
    model = Todo
    fields = ['title', 'description', 'due_date']

# Update existing TODO
class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['title', 'description', 'due_date', 'is_completed']

# Delete TODO
class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo_list')

# Toggle completion status
def toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')
```

**Why views.py?**
- Standard Django convention
- Separates business logic from presentation (templates) and data (models)
- Makes code organized and maintainable

**Other Options (Incorrect):**
- ❌ `urls.py` - For URL routing, not business logic
- ❌ `admin.py` - For admin panel configuration
- ❌ `tests.py` - For writing tests

**Request/Response Flow:**
```
User clicks button → URL pattern → View function → Database query → Template → HTML Response
```

**Official Documentation:**
- Views: https://docs.djangoproject.com/en/stable/topics/http/views/
- Class-Based Views: https://docs.djangoproject.com/en/stable/topics/class-based-views/

---

## Question 5: Templates

**Question:** Where do you need to register the directory with the templates?

**Answer:** `TEMPLATES['DIRS']` in project's `settings.py`

### Explanation for Beginners

**What are Templates?**
Templates are HTML files with special Django template syntax that lets you:
- Display dynamic data from your views
- Use loops and conditions
- Inherit from base templates
- Include reusable components

**Our Template Structure:**
```
todos/templates/
    base.html                  # Base template (layout)
    home.html                  # TODO list page
    todo_form.html            # Create/Edit form
    todo_confirm_delete.html  # Delete confirmation
```

**Registering Templates Directory**

In `settings.py`, find the `TEMPLATES` configuration:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'todos' / 'templates'],  # ← Add this path
        'APP_DIRS': True,  # Also searches in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Understanding TEMPLATES Settings:**

- **BACKEND** - Which template engine to use (Django's built-in)
- **DIRS** - List of directories where Django looks for templates
- **APP_DIRS** - If True, also looks in each app's `templates/` folder
- **OPTIONS** - Additional template configuration

**Why This is Important:**
- Django needs to know where to find your HTML files
- Without proper configuration, you'll get "TemplateDoesNotExist" errors
- Allows organizing templates in a logical structure

**Template Inheritance Example:**

base.html:
```html
<!DOCTYPE html>
<html>
<head><title>{% block title %}{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

home.html:
```html
{% extends 'base.html' %}
{% block title %}TODO List{% endblock %}
{% block content %}
    <h1>My TODOs</h1>
    {% for todo in todos %}
        <p>{{ todo.title }}</p>
    {% endfor %}
{% endblock %}
```

**Other Options (Incorrect):**
- ❌ `INSTALLED_APPS` - For registering apps, not template directories
- ❌ `TEMPLATES['APP_DIRS']` - Boolean flag, not for directory paths
- ❌ App's `urls.py` - For URL routing, not template configuration

**Official Documentation:**
- Templates: https://docs.djangoproject.com/en/stable/topics/templates/
- Template Language: https://docs.djangoproject.com/en/stable/ref/templates/language/

---

## Question 6: Tests

**Question:** What's the command you use for running tests in the terminal?

**Answer:** `python manage.py test`

### Explanation for Beginners

**What are Tests?**
Tests are automated code that verifies your application works correctly. They:
- Check if functions produce expected results
- Catch bugs before users find them
- Ensure changes don't break existing features
- Document how code should behave

**Our Test Suite**

We wrote 30 tests covering:

1. **Model Tests** (6 tests)
   - Creating TODOs
   - Default values
   - String representation
   - Optional fields
   - Ordering

2. **View Tests** (18 tests)
   - List view functionality
   - Create view with valid/invalid data
   - Update view operations
   - Delete view operations
   - Toggle completion

3. **URL Tests** (6 tests)
   - URL pattern resolution

**Running Tests:**

```bash
python manage.py test
```

This command:
1. Creates a temporary test database
2. Runs all tests in your project
3. Reports results (passed/failed)
4. Destroys the test database

**Example Test:**
```python
from django.test import TestCase
from .models import Todo

class TodoModelTest(TestCase):
    def test_todo_creation(self):
        # Create a TODO
        todo = Todo.objects.create(title="Test TODO")
        
        # Check it was created correctly
        self.assertEqual(todo.title, "Test TODO")
        self.assertFalse(todo.is_completed)
```

**Test Output:**
```
Found 30 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.042s

OK
Destroying test database for alias 'default'...
```

**Why Testing Matters:**
- **Confidence** - Know your code works
- **Safety** - Catch bugs early
- **Documentation** - Tests show how to use your code
- **Refactoring** - Change code without fear

**Other Options (Incorrect):**
- ❌ `pytest` - Different testing framework (can work with Django but not built-in)
- ❌ `python -m django run_tests` - Not a real Django command
- ❌ `django-admin test` - Works but `manage.py` is preferred

**Running Specific Tests:**
```bash
# Test specific app
python manage.py test todos

# Test specific class
python manage.py test todos.tests.TodoModelTest

# Test specific method
python manage.py test todos.tests.TodoModelTest.test_todo_creation
```

**Official Documentation:**
- Testing in Django: https://docs.djangoproject.com/en/stable/topics/testing/
- Writing Tests: https://docs.djangoproject.com/en/stable/topics/testing/overview/

---

## Summary: Complete Django Development Workflow

Here's the typical workflow for building a Django application:

### 1. Setup
```bash
# Install Django
pip install django

# Create project
django-admin startproject myproject
cd myproject

# Create app
python manage.py startapp myapp
```

### 2. Configure (settings.py)
```python
# Add app to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'myapp',
]

# Configure templates
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'myapp' / 'templates'],
        # ...
    }
]
```

### 3. Define Models (models.py)
```python
class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.TextField()
```

### 4. Create and Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Views (views.py)
```python
from django.views.generic import ListView

class MyListView(ListView):
    model = MyModel
    template_name = 'list.html'
```

### 6. Configure URLs (urls.py)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyListView.as_view(), name='list'),
]
```

### 7. Create Templates (templates/)
```html
{% extends 'base.html' %}
{% block content %}
    <h1>My List</h1>
    {% for item in object_list %}
        <p>{{ item.field1 }}</p>
    {% endfor %}
{% endblock %}
```

### 8. Write Tests (tests.py)
```python
from django.test import TestCase

class MyModelTest(TestCase):
    def test_creation(self):
        obj = MyModel.objects.create(field1="Test")
        self.assertEqual(obj.field1, "Test")
```

### 9. Run Tests
```bash
python manage.py test
```

### 10. Run Development Server
```bash
python manage.py runserver
```

---

## Additional Resources for Beginners

### Official Django Documentation
- **Tutorial (Start Here!):** https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **Models Reference:** https://docs.djangoproject.com/en/stable/topics/db/models/
- **Views Reference:** https://docs.djangoproject.com/en/stable/topics/http/views/
- **Templates Reference:** https://docs.djangoproject.com/en/stable/topics/templates/
- **Testing Reference:** https://docs.djangoproject.com/en/stable/topics/testing/

### Learning Paths
1. Complete the official Django tutorial (7 parts)
2. Build a simple blog or todo app
3. Learn about authentication and permissions
4. Explore Django REST Framework for APIs
5. Learn deployment (Heroku, AWS, DigitalOcean)

### Common Django Commands
```bash
# Project management
django-admin startproject name
python manage.py startapp name
python manage.py runserver

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell

# User management
python manage.py createsuperuser

# Testing
python manage.py test
python manage.py test --verbosity=2

# Static files
python manage.py collectstatic

# Shell
python manage.py shell
```

### Tips for Success
1. **Read the Documentation** - Django has excellent docs
2. **Use Class-Based Views** - Less code, more functionality
3. **Write Tests** - Catch bugs early
4. **Use Django Admin** - Free admin interface
5. **Follow Django Conventions** - Makes code predictable
6. **Learn the ORM** - Powerful database queries without SQL
7. **Use Version Control** - Git is essential
8. **Deploy Early** - Test in production-like environment

---

## Homework Submission Checklist

✅ All questions answered
✅ Code pushed to GitHub
✅ Tests passing (30/30)
✅ Application running locally
✅ README.md with setup instructions
✅ .gitignore configured (exclude db.sqlite3, __pycache__, etc.)

**Example GitHub Structure:**
```
ai-dev-tools-zoomcamp/
└── cohorts/
    └── 2025/
        └── 01-overview/
            └── 01-todo/        ← Your submission folder
                ├── manage.py
                ├── db.sqlite3
                ├── todoproject/
                ├── todos/
                └── README.md
```

Good luck with your homework! 🚀
