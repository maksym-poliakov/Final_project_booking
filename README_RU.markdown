# Final Project Booking

## Описание проекта

**Final Project Booking** — это веб-приложение на базе Django REST Framework для аренды жилья. Пользователи могут просматривать доступное жильё, бронировать его и оставлять отзывы. Арендодатели могут создавать и управлять объявлениями о жилье. Проект поддерживает аутентификацию, фильтрацию, поиск и автоматическое обновление статуса бронирований на основе дат.

### Основные возможности
- **Аутентификация**: Поддержка ролей пользователей (`L` — арендодатель, `T` — арендатор) с JWT-токенами.
- **Объявления жилья**: Создание, просмотр, фильтрация и поиск жилья по цене, городу, количеству комнат и типу жилья.
- **Бронирования**: Создание, обновление и удаление бронирований с автоматическим изменением статуса.
- **Отзывы**: Пользователи могут оставлять отзывы о бронированиях.
- **Фильтрация и поиск**: Фильтрация по полям (`price`, `address__city`, `number_of_rooms`, `type_housing`) и поиск по `title` и `description`.
- **Валидация**: Проверка данных пользователя (email, пароль, номер телефона, имя, дата рождения).

## Технологии
- **Backend**: Django, Django REST Framework
- **База данных**: PostgreSQL (рекомендуется) или SQLite (для разработки)
- **Фильтрация**: django-filter
- **Аутентификация**: Кастомная модель пользователя, JWT
- **Python**: 3.13

## Структура проекта
```
Final_project_booking/
├── apps/
│   ├── booking/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices/
│   │   │   ├── booking_choices.py   # Опции для бронирований
│   │   │   ├── habitation_choices.py # Опции для жилья
│   │   ├── models/
│   │   │   ├── models_address.py    # Модель AddressModel
│   │   │   ├── models_booking.py    # Модель BookingModel
│   │   │   ├── models_habitation.py # Модель HabitationModel
│   │   │   ├── models_reviews.py    # Модель ReviewModel
│   │   ├── serializers/
│   │   │   ├── serializer_address.py    # Сериализаторы для адресов
│   │   │   ├── serializer_booking.py    # Сериализаторы для бронирований
│   │   │   ├── serializer_habitation.py # Сериализаторы для жилья
│   │   │   ├── serializer_reviews.py    # Сериализаторы для отзывов
│   │   ├── signals/
│   │   │   ├── signals_confirmation.py     # Сигналы для подтверждения бронирований
│   │   │   ├── signals_prohibit_editing.py # Сигналы для запрета редактирования
│   │   ├── urls/
│   │   │   ├── booking_urls.py     # URL для бронирований
│   │   │   ├── habitation_urls.py  # URL для жилья
│   │   │   ├── reviews_urls.py     # URL для отзывов
│   │   ├── utils/
│   │   │   ├── start_date.py       # Логика для start_date
│   │   ├── views/
│   │   │   ├── views_booking.py    # Представления для бронирований
│   │   │   ├── views_habitation.py # Представления для жилья
│   │   │   ├── views_reviews.py    # Представления для отзывов
│   ├── user/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices/
│   │   │   ├── user_choices.py    # Опции для пользователей
│   │   ├── models/
│   │   │   ├── models.py          # Модель UserProfileModel
│   │   ├── permissions/
│   │   │   ├── user_permissions.py # Права доступа для пользователей
│   │   ├── serializers/
│   │   │   ├── user_serializers.py # Сериализаторы для пользователей
│   │   ├── urls.py
│   │   ├── utils/
│   │   │   ├── authentication.py   # Логика аутентификации
│   │   │   ├── middleware.py       # Промежуточный слой
│   │   │   ├── set_jwt_cookies.py  # Установка JWT-токенов в cookies
│   │   ├── validations/
│   │   │   ├── validation_date_of_birth.py # Валидация даты рождения
│   │   │   ├── validation_email.py        # Валидация email
│   │   │   ├── validation_password.py     # Валидация пароля
│   │   │   ├── validation_phone_number.py # Валидация номера телефона
│   │   │   ├── validation_username.py     # Валидация имени пользователя
│   │   ├── views/
│   │   │   ├── views_auth_user.py  # Представления для аутентификации
│   │   │   ├── views_user.py       # Представления для пользователей
├── config/
│   ├── asgi.py
│   ├── settings.py                 # Настройки проекта
│   ├── urls.py                     # Маршруты API
│   ├── wsgi.py
├── manage.py                       # Управление Django
├── requirements.txt                # Зависимости
```

## Установка

### Требования
- Python 3.13
- PostgreSQL (или SQLite для разработки)

### Шаги установки
1. **Клонируйте репозиторий**:
   ```bash
   git clone git@github.com:maksym-poliakov/Final_project_booking.git
   cd Final_project_booking
   ```

2. **Создайте виртуальное окружение**:
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных**:
   - В `config/settings.py` укажите настройки базы данных:
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
   - Выполните миграции:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Создайте суперпользователя**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Запустите сервер**:
   ```bash
   python manage.py runserver
   ```

## Использование

### Эндпоинты API
- **GET /habitation/list/**: Получение списка жилья с фильтрацией и поиском.
  - Фильтры: `price`, `address__city`, `number_of_rooms`, `type_housing`.
  - Поиск: `title`, `description`.
  - Сортировка: `price`, `created_at`.
  - Примечание: Арендодатели (`role='L'`) видят только свои объявления, а арендаторы не видят собственные объявления арендодателя.
- **GET/PUT/DELETE /booking/<pk>/**: Получение, обновление или удаление бронирования.
- **POST /booking/**: Создание бронирования.
- **GET/POST /reviews/**: Получение списка или создание отзывов.

### Пример запроса
Получение списка жилья:
```bash
curl -X GET http://localhost:8000/habitation/list/?price__lte=1000&address__city=Berlin
```

Пример ответа:
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

### Автоматическое обновление статуса бронирований
- Статус бронирований (`BookingModel.status_order`) автоматически обновляется на `completed`, если `end_date` меньше текущей даты и `start_date` из `apps.booking.utils.start_date` устарела.
- Логика реализована в `HabitationListView.update_booking_status`.
- Переменная `start_date` хранится как атрибут класса `HabitationListView` и обновляется на текущую дату при выполнении условий.

## Структура базы данных
Схема базы данных описана в формате DBML для [dbdiagram.io](https://dbdiagram.io):

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

Вставьте этот код в dbdiagram.io для визуализации.

## Разработка

### Добавление новых функций
1. Создайте модели в `apps/*/models/`.
2. Создайте сериализаторы в `apps/*/serializers/`.
3. Добавьте представления в `apps/*/views/`.
4. Настройте маршруты в `apps/*/urls/` или `config/urls.py`.

## Проблемы и ограничения
- **Многопоточность**: `start_date` хранится как атрибут класса в `HabitationListView`. В многопоточном окружении (например, Gunicorn) это может вызвать конфликты. Для продакшена рекомендуется хранить `start_date` в базе данных:
  ```python
  from django.db import models

  class AppSettings(models.Model):
      start_date = models.DateField(default=timezone.now)
      class Meta:
          db_table = 'app_settings'
  ```
- **Сброс `start_date`**: При перезапуске сервера `start_date` сбрасывается на начальное значение из `apps.booking.utils.start_date`.

## Контрибьютинг
1. Форкните репозиторий: `git@github.com:maksym-poliakov/Final_project_booking.git`.
2. Создайте ветку: `git checkout -b feature/your-feature`.
3. Зафиксируйте изменения: `git commit -m "Add your feature"`.
4. Отправьте в репозиторий: `git push origin feature/your-feature`.
5. Создайте Pull Request.

## Лицензия
MIT License. См. файл `LICENSE`.