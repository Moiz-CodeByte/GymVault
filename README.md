# GymVault - Gym Management System

## Overview

GymVault is a gym management system built with Django. It provides a platform for gym owners and administrators to manage memberships, payments, lockers, and member information efficiently. The system also allows members to register, select gym plans, and track their membership status.

## Features

- **User Management**
  - Multiple user roles: Super Admin, Gym Admin, and Member
  - User registration and authentication
  - Profile management

- **Gym Management**
  - Multiple gym locations support
  - Membership plan management
  - Locker assignment and tracking

- **Membership Management**
  - Membership registration and renewal
  - Membership status tracking
  - Payment tracking and management

- **Request System**
  - Contact form for inquiries
  - Request status tracking

## Technology Stack

- **Backend**: Django 5.2.2
- **Database**: SQLite (default)
- **Authentication**: Django Allauth (with Google OAuth support)
- **Frontend**: HTML, CSS (Tailwind CSS)

## Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Clone the Repository

```bash
git clone https://github.com/Moiz-CodeByte/GymVault.git
cd GymVault
```

### Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Usage

### Admin Access

1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with the superuser credentials created earlier
3. From here, you can manage users, gyms, membership plans, and more

### User Registration

1. Navigate to http://127.0.0.1:8000/register/
2. Fill in the registration form
3. Select a gym and membership plan
4. Complete the registration process

### Member Dashboard

1. Log in with member credentials
2. View membership status, payments, and locker assignment
3. Update profile information

### Gym Admin Dashboard

1. Log in with gym admin credentials
2. Manage members, lockers, and payments for the assigned gym
3. Create and update membership plans

## Project Structure

- `gymvault/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `forms.py` - Form definitions
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)

- `gymvaultproject/` - Project configuration
  - `settings.py` - Django settings
  - `urls.py` - Main URL routing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
For any questions or support, please contact at [hello@abdulmoiz.net](mailto:hello@abdulmoiz.net).
