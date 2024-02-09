# Django Project Management API

This Django API provides functionalities for project management, allowing users to create projects, contribute, manage issues, and more.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Users](#users)
  - [Projects](#projects)
  - [Issues](#issues)
  - [Comments](#comments)
- [Permissions](#permissions)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python (>=3.6)
- Django (>=3.0)
- Django REST framework (>=3.11)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ChangayaMusic/softdesk2
    cd softdesk2
    ```

2. **Install Poetry (if not already installed):**

    ```bash
    pip install poetry -
    ```

3. **Install the dependencies using Poetry:**

    ```bash
    poetry install
    ```

4. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser account:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

   The API will be accessible at `http://localhost:8000/`.

## API Endpoints

### Users

- `GET /api/users/`: List all users.
- `GET /api/users/{user_id}/`: Retrieve a specific user.
- `POST /api/users/`: Create a new user.
- `PUT /api/users/{user_id}/`: Update a user's information.
- `DELETE /api/users/{user_id}/`: Delete a user.

### Projects

- `GET /api/projects/`: List all projects.
- `GET /api/projects/{project_id}/`: Retrieve a specific project.
- `POST /api/projects/`: Create a new project.
- `PUT /api/projects/{project_id}/`: Update a project's information.
- `DELETE /api/projects/{project_id}/`: Delete a project.

### Issues

- `GET /api/issues/`: List all issues.
- `GET /api/issues/{issue_id}/`: Retrieve a specific issue.
- `POST /api/issues/`: Create a new issue.
- `PUT /api/issues/{issue_id}/`: Update an issue's information.
- `DELETE /api/issues/{issue_id}/`: Delete an issue.

### Comments

- `GET /api/comments/`: List all comments.
- `GET /api/comments/{comment_id}/`: Retrieve a specific comment.
- `POST /api/comments/`: Create a new comment.
- `PUT /api/comments/{comment_id}/`: Update a comment's information.
- `DELETE /api/comments/{comment_id}/`: Delete a comment.

## Permissions

The API uses custom permissions to control access to various endpoints:

- `IsUserOwner`: Allows a user to modify or delete their own profile.
- `IsAuthenticated`: Ensures that only authenticated users can access certain endpoints.
- `IsContributor`: Grants permission to contributors of a specific project.
- `IsProjectAuthor`: Allows the author of a project to modify or delete it.
- `IsIssueAuthor`: Permits the author of an issue to modify or delete it.
- `IsCommentAuthor`: Grants permission to the author of a comment to modify or delete it.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django and Django REST framework communities for providing excellent documentation and resources.
