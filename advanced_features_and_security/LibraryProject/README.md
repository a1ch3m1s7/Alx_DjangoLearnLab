# Permissions & Groups Setup

We use Django's built-in groups and custom permissions to manage access:

- **Custom Permissions (in Book model)**:
  - `can_view` → Allows viewing books
  - `can_create` → Allows creating books
  - `can_edit` → Allows editing books
  - `can_delete` → Allows deleting books

- **Groups** (configured in Django Admin):
  - **Viewers** → can_view
  - **Editors** → can_create, can_edit
  - **Admins** → can_view, can_create, can_edit, can_delete

- **Views**:
  - `view_books` → requires `can_view`
  - `create_book` → requires `can_create`
  - `edit_book` → requires `can_edit`
  - `delete_book` → requires `can_delete`

Users are assigned to groups, and groups hold permissions.