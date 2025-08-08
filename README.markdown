# Final Project Booking

## Project Overview

**Final Project Booking** is a web application built with Django REST Framework for renting accommodations. Users can browse available listings, book them, and leave reviews. Landlords can create and manage their property listings. The project supports authentication, filtering, search, and automatic updating of booking statuses based on dates.

### Key Features
- **Authentication**: Supports user roles (`L` for landlord, `T` for tenant) with JWT tokens.
- **Accommodation Listings**: Create, view, filter, and search listings by price, city, number of rooms, and housing type.
- **Bookings**: Create, update, and delete bookings with automatic status updates.
- **Reviews**: Users can leave reviews for bookings.
- **Filtering and Search**: Filter by fields (`price`, `address__city`, `number_of_rooms`, `type_housing`) and search by `title` and `description`.
- **Validation**: Validates user data (email, password, phone number, username, date of birth).

## Technologies
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (recommended) or SQLite (for development)
- **Filtering**: django-filter
- **Authentication**: Custom user model, JWT
- **Python**: 3.13

## Project Structure
```
Final_project_booking/
├── apps/
│   ├── booking/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices/
│   │   │   ├── booking_choices.py   # Options for bookings
│   │   │   ├── habitation_choices.py # Options for accommodations
│   │   ├── models/
│   │   │   ├── models_address.py    # AddressModel
│   │   │   ├── models_booking.py    # BookingModel
│   │   │   ├── models_habitation.py # HabitationModel
│   │   │   ├── models_reviews.py    # ReviewModel
│   │   ├── serializers/
│   │   │   ├── serializer_address.py    # Serializers for addresses
│   │   │   ├── serializer_booking.py    # Serializers for bookings
│   │   │   ├── serializer_habitation.py # Serializers for accommodations
│   │   │   ├── serializer_reviews.py    # Serializers for reviews
│   │   ├── signals/
│   │   │   ├── signals_confirmation.py     # Signals for booking confirmation
│   │   │   ├── signals_prohibit_editing.py # Signals to prevent editing
│   │   ├── urls/
│   │   │   ├── booking_urls.py     # URLs for bookings
│   │   │   ├── habitation_urls.py  # URLs for accommodations
│   │   │   ├── reviews_urls.py     # URLs for reviews
│   │   ├── utils/
│   │   │   ├── start_date.py       # Logic for start_date
│   │   ├── views/
│   │   │   ├── views_booking.py    # Views for bookings
│   │   │   ├── views_habitation.py # Views for accommodations
│   │   │   ├── views_reviews.py    # Views for reviews
│   ├── user/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices/
│   │   │   ├── user_choices.py    # Options for users
│   │   ├── models/
│   │   │   ├── models.py          # UserProfileModel
│   │   ├── permissions/
│   │   │   ├── user_permissions.py # User permissions
│   │   ├── serializers/
│   │   │   ├── user_serializers.py # Serializers for users
│   │   ├── urls.py
│   │   ├── utils/
│   │   │   ├── authentication.py   # Authentication logic
│   │   │   ├── middleware.py       # Middleware
│   │   │   ├── set_jwt_cookies.py  # Setting JWT tokens in cookies
│   │   ├── validations/
│   │   │   ├── validation_date_of_birth.py # Date of birth validation
│   │   │   ├── validation_email.py        # Email validation
│   │   │   ├── validation_password.py     # Password validation
│   │   │   ├── validation_phone_number.py # Phone number validation
│   │   │   ├── validation_username.py     # Username validation
│   │   ├── views/
│   │   │   ├── views_auth_user.py  # Authentication views
│   │   │   ├── views_user.py       # User views
├── config/
│   ├── asgi.py
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # API routes
│   ├── wsgi.py
├── manage.py                       # Django management
├── requirements.txt                # Dependencies
```

## Installation

### Requirements
- Python 3.13
- PostgreSQL (or SQLite for development)

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone git@github.com:maksym-poliakov/Final_project_booking.git
   cd Final_project_booking
   ```

2. **Create a virtual environment**:
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
   - In `config/settings.py`, specify the database settings:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'booking_db',
             'USER': 'your_user',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints
- **GET /habitation/list/**: Retrieve a list of accommodations with filtering and search.
  - Filters: `price`, `address__city`, `number_of_rooms`, `type_housing`.
  - Search: `title`, `description`.
  - Sorting: `price`, `created_at`.
  - Note: Landlords (`role='L'`) see only their listings, while tenants cannot see their own landlord listings.
- **GET/PUT/DELETE /booking/<pk>/**: Retrieve, update, or delete a booking.
- **POST /booking/**: Create a booking.
- **GET/POST /reviews/**: Retrieve a list of reviews or create a review.

### Example Request
Retrieve a list of accommodations:
```bash
curl -X GET http://localhost:8000/habitation/list/?price__lte=1000&address__city=Berlin
```

Example Response:
```json
[
  {
    "id": 1,
    "title": "Cozy Apartment",
    "description": "A nice apartment in Berlin",
    "price": 800.00,
    "address": {
      "city": "Berlin",
      "street": "Main St",
      "postcode": "10115"
    },
    "number_of_rooms": 2,
    "type_housing": "A",
    "status": "A"
  }
]
```

### Automatic Booking Status Update
- Booking statuses (`BookingModel.status_order`) are automatically updated to `completed` if `end_date` is earlier than the current date and `start_date` from `apps.booking.utils.start_date` is outdated.
- The logic is implemented in `HabitationListView.update_booking_status`.
- The `start_date` variable is stored as a class attribute in `HabitationListView` and updated to the current date when conditions are met.

## Database Schema
The database schema is described in DBML format for [dbdiagram.io](https://dbdiagram.io):

```dbml
Table user_profile {
  id integer [primary key]
  user_id integer
  role varchar
  phone_number varchar
  created_at datetime
}

Table address {
  id integer [primary key]
  user_id integer [ref: > user_profile.id]
  city varchar(100)
  street varchar(100)
  postcode varchar(12)
  haus_number integer
  house_letter varchar(1) [null]
  created_at datetime
}

Table habitations {
  id integer [primary key]
  title varchar(100)
  description text
  type_housing varchar
  status varchar
  number_of_rooms integer
  price decimal(10,2)
  address_id integer [ref: > address.id]
  created_at datetime
}

Table booking {
  id integer [primary key]
  user_id integer [ref: > user_profile.id]
  housing_details_id integer [ref: > habitations.id]
  is_active varchar
  start_date date
  end_date date
  confirmation varchar
  status_order varchar [null]
  total_price decimal(10,2)
  created_at datetime
}

Table review {
  id integer [primary key]
  user_id integer [ref: > user_profile.id]
  booking_id integer [ref: > booking.id]
  comment text(300)
  rating integer
  created_at datetime
}
```

Paste this code into dbdiagram.io for visualization.

## Development

### Adding New Features
1. Create models in `apps/*/models/`.
2. Create serializers in `apps/*/serializers/`.
3. Add views in `apps/*/views/`.
4. Configure routes in `apps/*/urls/` or `config/urls.py`.

## Known Issues and Limitations
- **Multithreading**: `start_date` is stored as a class attribute in `HabitationListView`. In a multithreaded environment (e.g., Gunicorn), this may cause conflicts. For production, consider storing `start_date` in the database:
  ```python
  from django.db import models

  class AppSettings(models.Model):
      start_date = models.DateField(default=timezone.now)
      class Meta:
          db_table = 'app_settings'
  ```
- **Reset of `start_date`**: On server restart, `start_date` resets to the initial value from `apps.booking.utils.start_date`.

## Contributing
1. Fork the repository: `git@github.com:maksym-poliakov/Final_project_booking.git`.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the repository: `git push origin feature/your-feature`.
5. Create a Pull Request.

## License
MIT License. See the `LICENSE` file.