# Advanced Book API Documentation

## Overview
This Django REST Framework API provides CRUD operations for Books and Authors with advanced features including authentication, filtering, and custom permissions.

## API Endpoints

### Books
- `GET /api/books/` - List all books (public)
- `GET /api/books/<id>/` - Get specific book details (public)
- `POST /api/books/create/` - Create new book (authenticated only)
- `PUT/PATCH /api/books/<id>/update/` - Update book (authenticated only)
- `DELETE /api/books/<id>/delete/` - Delete book (authenticated only)

### Authors
- `GET /api/authors/` - List all authors (public)
- `GET /api/authors/<id>/` - Get specific author details (public)

## Features

### Authentication & Permissions
- Read operations: Public access
- Write operations: Require authentication
- Uses Django's session and basic authentication

### Filtering & Search
- Filter books by: `publication_year`, `author`
- Search books by: `title`
- Order books by: `title`, `publication_year`, `author__name`

### Custom Validations
- Publication year cannot be in the future
- Custom response formats for create/update/delete operations

## Testing
Use the provided test scripts or manual curl commands to verify all endpoints work as expected with proper permission enforcement.
# Install required packages
pip install django djangorestframework django-filter

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for testing
python manage.py createsuperuser

# Run tests
python manage.py test api

# Start development server
python manage.py runserver