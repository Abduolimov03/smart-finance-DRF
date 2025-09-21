# Kirim-Chiqim Tizimi (Income-Expense Management System)

## Loyihaning maqsadi
Bu loyiha foydalanuvchining kirim va chiqimlarini kuzatish, kategoriyalar bo‘yicha saralash, balansni ko‘rish va kartalar orqali pul boshqarishni osonlashtiradi. Loyihada Django va Django REST Framework ishlatilgan.

## Texnologiyalar
- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL
- Simple JWT (token asosida autentifikatsiya)
- Docker (ixtiyoriy)

## Xususiyatlar
- Foydalanuvchi autentifikatsiyasi: signup, login, logout
- Parolni tiklash (email/telefon orqali)
- Income va Expense CRUD operatsiyalari
- Income va Expense kategoriyalari
- Kartalar bilan ishlash (balance avtomatik yangilanadi)
- Balansni ko‘rish va vaqt oralig‘ida filtr
- Kalendarga ko‘ra kirim/chiqimlarni ko‘rish

## API Endpoints

### Auth
**Signup**
```bash
curl -X POST http://localhost:8000/users/signup/ \
-H "Content-Type: application/json" \
-d '{"email_phone_number":"user@example.com"}'


Login
curl -X POST http://localhost:8000/users/login/ \
-H "Content-Type: application/json" \
-d '{"user_input":"user@example.com","password":"yourpassword"}'

LogOut
curl -X POST http://localhost:8000/users/logout/ \
-H "Content-Type: application/json" \
-d '{"refresh":"<refresh_token>"}'

Income Category
List
curl -X GET http://localhost:8000/finance/income-categories/ \
-H "Authorization: Bearer <access_token>"

Create
curl -X POST http://localhost:8000/finance/income-categories/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"name":"Oylik"}'

Delete
curl -X DELETE http://localhost:8000/finance/income-categories/1/ \
-H "Authorization: Bearer <access_token>"

Expense Category
List
curl -X GET http://localhost:8000/finance/expense-categories/ \
-H "Authorization: Bearer <access_token>"

Create
curl -X POST http://localhost:8000/finance/expense-categories/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"name":"Ovqat"}'

Delete
curl -X DELETE http://localhost:8000/finance/expense-categories/1/ \
-H "Authorization: Bearer <access_token>"

Cards
list
curl -X GET http://localhost:8000/finance/cards/ \
-H "Authorization: Bearer <access_token>"

Create
curl -X POST http://localhost:8000/finance/cards/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"name":"Uzcard","balance":100000,"currency":"UZS"}'

Delete
curl -X DELETE http://localhost:8000/finance/cards/1/delete/ \
-H "Authorization: Bearer <access_token>"

Income
List
curl -X GET http://localhost:8000/finance/incomes/?timeframe=daily \
-H "Authorization: Bearer <access_token>"

Create
curl -X POST http://localhost:8000/finance/incomes/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"category":1,"amount":500000,"source_type":"card","card":1}'

Detail
curl -X GET http://localhost:8000/finance/incomes/1/ \
-H "Authorization: Bearer <access_token>"

Update
curl -X PUT http://localhost:8000/finance/incomes/1/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"category":1,"amount":600000,"source_type":"card","card":1}'

Delete
curl -X DELETE http://localhost:8000/finance/incomes/1/ \
-H "Authorization: Bearer <access_token>"

Loyihani ishga tushirish
git clone <repo_url>
cd kirim-chiqim-DRF
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

