# Django TODO Application

A fully functional TODO application built with Django, featuring CRUD operations, due dates, and completion status tracking.

## Features

- ✅ Create, Read, Update, Delete TODOs
- 📅 Assign due dates to tasks
- ✓ Mark TODOs as completed/incomplete
- 🎨 Clean, responsive user interface
- ✅ Comprehensive test coverage (30 tests)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Install Django

```bash
pip install django
```

### 2. Navigate to Project Directory

```bash
cd cohorts/2025/01-overview/01-todo
```

### 3. Run Migrations

```bash
python manage.py migrate
```

This creates the necessary database tables.

### 4. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests with verbose output:
```bash
python manage.py test --verbosity=2
```

Run specific test class:
```bash
python manage.py test todos.tests.TodoModelTest
```

## Project Structure

```
01-todo/
├── manage.py                  # Django management script
├── db.sqlite3                 # SQLite database
├── todoproject/               # Project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
└── todos/                     # TODO app
    ├── __init__.py
    ├── admin.py              # Admin configuration
    ├── apps.py               # App configuration
    ├── models.py             # Database models
    ├── views.py              # View logic (CRUD operations)
    ├── urls.py               # App URL patterns
    ├── tests.py              # Test suite (30 tests)
    ├── migrations/           # Database migrations
    │   └── 0001_initial.py
    └── templates/            # HTML templates
        ├── base.html         # Base template
        ├── home.html         # TODO list page
        ├── todo_form.html    # Create/Edit form
        └── todo_confirm_delete.html
```

## Usage

### Creating a TODO

1. Click "➕ Add New TODO" button
2. Fill in the title (required)
3. Optionally add description and due date
4. Click "Save TODO"

### Editing a TODO

1. Click "✏️ Edit" next to any TODO
2. Modify the fields
3. Check "Mark as completed" to mark it done
4. Click "Save TODO"

### Deleting a TODO

1. Click "🗑️ Delete" next to any TODO
2. Confirm deletion on the confirmation page

### Toggling Completion Status

Click "✅ Complete" or "↩️ Reopen" to quickly toggle status

## Models

### Todo Model

```python
class Todo(models.Model):
    title = models.CharField(max_length=200)          # Required
    description = models.TextField(blank=True)         # Optional
    due_date = models.DateField(null=True, blank=True) # Optional
    is_completed = models.BooleanField(default=False)  # Default: False
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Views

- **TodoListView** - Display all TODOs
- **TodoCreateView** - Create new TODO
- **TodoUpdateView** - Edit existing TODO
- **TodoDeleteView** - Delete TODO with confirmation
- **toggle_complete** - Quick toggle completion status

## Test Coverage

30 comprehensive tests covering:
- Model creation and validation (6 tests)
- CRUD operations via views (18 tests)
- URL routing (6 tests)

All tests passing ✅

## Homework Answers

For detailed explanations of each homework question, see: [HOMEWORK_ANSWERS.md](../HOMEWORK_ANSWERS.md)

Quick answers:
1. **Install Django:** `pip install django`
2. **App registration:** `settings.py`
3. **After creating models:** Run migrations
4. **TODO logic location:** `views.py`
5. **Template registration:** `TEMPLATES['DIRS']` in `settings.py`
6. **Run tests:** `python manage.py test`

## Technologies Used

- **Django 5.2.8** - Web framework
- **SQLite** - Database
- **Python 3.12** - Programming language
- **HTML/CSS** - Frontend

## Development

### Creating a Superuser (Optional)

To access Django admin panel:

```bash
python manage.py createsuperuser
```

Then visit: http://127.0.0.1:8000/admin

### Running Django Shell

```bash
python manage.py shell
```

Example:
```python
from todos.models import Todo
Todo.objects.create(title="My first TODO")
Todo.objects.all()
```

## Troubleshooting

### Port Already in Use

If port 8000 is busy, specify a different port:
```bash
python manage.py runserver 8080
```

### Migrations Not Applied

If you see database errors:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Tests Failing

Ensure you're in the project directory and all dependencies are installed:
```bash
cd cohorts/2025/01-overview/01-todo
pip install django
python manage.py test
```

## Contributing

This is a homework project for the AI Dev Tools Zoomcamp. Feel free to fork and extend!

## License

Educational project - free to use and modify.

## Acknowledgments

Built as part of the [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) by DataTalks.Club.
