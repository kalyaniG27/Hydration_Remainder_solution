# README for Hydration Project

## Overview
The Hydration Project is a Django web application designed to help users track their daily water intake. The application allows users to set daily water intake goals, log their water consumption, and view their progress over time.

## Features
- User authentication (signup, login, logout)
- Daily water intake tracking
- Progress visualization
- User profile management
- History of water intake records
- Email reminders for water intake

## Project Structure
```
hydration_project
├── tracker
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── utils.py
│   └── templates
│       └── tracker
│           ├── dashboard.html
│           ├── history.html
│           ├── home.html
│           ├── login.html
│           ├── profile.html
│           └── signup.html
├── hydration_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd hydration_project
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   python manage.py migrate
   ```
5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

## Configuration
Make sure to configure the email backend in `settings.py` to enable email sending. You can use the following example configuration for Gmail:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
```

## Usage
- Run the development server:
  ```
  python manage.py runserver
  ```
- Access the application at `http://127.0.0.1:8000/`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.