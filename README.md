
## 🚀 Deployment Checklist

For deploying to a production environment:

1.  Set `DEBUG=False` in your `.env` file.
2.  Configure `ALLOWED_HOSTS` with your domain name.
3.  Set up a production database (e.g., PostgreSQL on AWS/RDS).
4.  Configure email backend (e.g., using `django-anymail` with SendGrid/Mailgun).
5.  Run `python manage.py collectstatic`.
6.  Use a WSGI server like Gunicorn to serve the application.
7.  Use a reverse proxy like Nginx to serve static/media files and forward requests to Gunicorn.
8.  Ensure all environment variables are correctly set in the production environment.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📧 Contact

Your Name - Aman mishra

Project Link: [https://github.com/AMANMISHRA1511/employee-management-system](https://github.com/AMANMISHRA1511/employee-management-system)
# Authentication App

This Django app is responsible for all user-related authentication and authorization features.

## Purpose

-   Handles user registration, login, and logout.
-   Manages password reset flows.
-   Implements Two-Factor Authentication (2FA) using `django-otp`.

## Key Components

-   **`views.py`**: Contains the logic for `LoginView`, `SignUpView`, `ForgotPasswordView`, and the 2FA setup/verification views.
-   **`models.py`**: (Optional) If a custom user model is used, it will be defined here. Otherwise, it relies on Django's default `User` model.
-   **`forms.py`**: Defines the forms for user registration, login, and password reset.
-   **`urls.py`**: Contains the URL patterns for all authentication endpoints.
-   **`templates/authentication/`**: Holds all HTML templates for the authentication UI.

## Dependencies

-   `django-otp`: For Two-Factor Authentication.
-   `django-anymail`: For sending password reset emails.
-   `django-crispy-forms`: For rendering forms.

-   # Employees App

This is the core business logic app of the Employee Management System.

## Purpose

-   Manages all CRUD (Create, Read, Update, Delete) operations for employee records.
-   Handles the main dashboard view.
-   Manages file uploads associated with employees.

## Key Components

-   **`models.py`**: Defines the `Employee` model, which stores all employee-related data. It likely has a one-to-one link with the Django `User` model.
-   **`views.py`**: Contains the class-based or function-based views for `EmployeeListView`, `EmployeeDetailView`, `EmployeeCreateView`, `EmployeeUpdateView`, and `EmployeeDeleteView`. Also includes the `DashboardView`.
-   **`forms.py`**: Defines the `EmployeeForm` for creating and updating employee data.
-   **`urls.py`**: Contains the URL patterns for all employee-related pages.
-   **`templates/employees/`**: Holds all HTML templates for the employee dashboard, list, detail, and forms.

## Dependencies

-   `Pillow`: For handling `profile_pic` image uploads.
-   `django-crispy-forms`: For rendering the employee creation/editing forms.
