# Social Media API

A Django REST Framework-based social media API with user authentication and profile management.

## Setup

```bash
git clone <repo-url>
cd social_media_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## 📝 Posts & Comments API

### Endpoints

#### Posts
| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/api/posts/` | List all posts (paginated) |
| POST | `/api/posts/` | Create a new post |
| GET | `/api/posts/{id}/` | Retrieve a single post |
| PUT/PATCH | `/api/posts/{id}/` | Update a post (author only) |
| DELETE | `/api/posts/{id}/` | Delete a post (author only) |

#### Comments
| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/api/comments/` | List comments |
| POST | `/api/comments/` | Add a new comment |
| PUT/PATCH | `/api/comments/{id}/` | Edit comment (author only) |
| DELETE | `/api/comments/{id}/` | Delete comment (author only) |

### Example Response (GET `/api/posts/`)
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "john",
      "title": "My first post",
      "content": "Hello, Django REST World!",
      "created_at": "2025-10-12T19:04:34Z",
      "updated_at": "2025-10-12T19:04:34Z",
      "comments": []
    }
  ]
}
