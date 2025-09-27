# Advanced API Project

## Endpoints
- `GET /api/books/` → List all books (public)
- `GET /api/books/<id>/` → Get details of one book (public)
- `POST /api/books/create/` → Create a new book (authenticated)
- `PUT /api/books/<id>/update/` → Update a book (authenticated)
- `DELETE /api/books/<id>/delete/` → Delete a book (authenticated)

## Permissions
- List & Detail → open to all
- Create, Update, Delete → restricted to authenticated users
