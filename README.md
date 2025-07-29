# Stripe Checkout Demo — Django + Stripe API

Simple e-commerce backend on Django with Stripe Checkout integration.

##  Stack
- Python 3.11
- Django
- Stripe Python SDK
- Docker + docker-compose
- HTML + JS (stripe.js)

##  Functionality
- `Item` model with `name`, `description`, `price`, `currency` fields
- API:
- `GET /item/<id>` — HTML product page with a payment button via Stripe
- `GET /buy/<id>` — getting Stripe Session ID for paying for one product
- `Order` model with the ability to pay for multiple products
- Support for discounts (`Discount`) and taxes (`Tax`) via Stripe
- Separate payment for `Order` taking into account discounts and taxes
- Stripe support for multi-currency (USD / EUR, etc.)
- Alternative payment method via `Stripe PaymentIntent` (bonus)

##  Local installation

```bash
git clone https://github.com/averageencoreenjoer/stripe-django-store.git
cd stripe-checkout-store
cp .env.example .env
docker-compose up --build
````

After launch:

* Backend: [http://localhost:8000](http://localhost:8000)
* Django Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

##  Example `.env`

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
DJANGO_SECRET_KEY=your_django_secret
DEBUG=True
```

##  Django Admin

* Admin panel is available at `/admin`
* You can add products, orders, discounts and taxes

##  Covered technical task items

* [x] Model `Item`
* [x] `GET /buy/{id}` — get Stripe Session ID
* [x] `GET /item/{id}` — HTML with buy button
* [x] Docker
* [x] ENV variables
* [x] Django Admin
* [x] `Order` model + payment via Stripe
* [x] Discounts and taxes (Stripe Coupons and Tax Rates)
* [x] Multicurrency
* [x] Stripe PaymentIntent (optional)

##  Request example

```bash
curl http://localhost:8000/item/1
```

---

## Testing

The project uses `pytest` together with the `pytest-django` plugin to easily run Django tests.

### Installing dependencies for testing

```bash
pip install pytest pytest-django pytest-cov
```

### Running tests

Before running tests, you need to specify the environment variable `DJANGO_SETTINGS_MODULE`:

```bash
export DJANGO_SETTINGS_MODULE=stripe_project.settings
pytest -v payments/tests.py
```

Or you can run the command in one line:

```bash
DJANGO_SETTINGS_MODULE=stripe_project.settings pytest -v payments/tests.py
```

### Setting up pytest.ini

For convenience, create a file `pytest.ini` in the root of the project with the following contents, so as not to specify the environment variable every times:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = stripe_project.settings
python_files = tests.py test_*.py *_tests.py
```

After that, tests can be run simply with the command:

```bash
pytest -v payments/tests.py
```