from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import random
from datetime import datetime, timezone, timedelta
import yaml
import os

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Retrieve database credentials from configuration or environment variables
DB_URL = config["database"].get("url", None)
DB_TYPE = config["database"].get("type", "sqlite")
DB_HOST = config["database"].get("host", "localhost")
DB_NAME = config["database"].get("name", "simple_shop")
DB_USER = os.getenv("DB_USER", config["database"].get("user", ""))
DB_PASSWORD = os.getenv("DB_PASSWORD", config["database"].get("password", ""))

# Construct database URL dynamically
if DB_URL:
    DATABASE_URL = f"{DB_URL}"
elif DB_USER and DB_PASSWORD:
    DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
elif DB_TYPE == "sqlite":
    DATABASE_URL = f"{DB_TYPE}://{DB_NAME}"
else:
    DATABASE_URL = f"{DB_TYPE}://{DB_HOST}/{DB_NAME}"

# Initialize Faker
fake = Faker()

# Define the database
Base = declarative_base()

def generate_price():
    return round(random.uniform(5, 500), 2)

def generate_order_time(base_date):
    # Return a time between 1 and 10 minites after base (or NULL in random 1% cases)
    return base_date + timedelta(minutes=random.randint(1, 10)) if random.uniform(0, 1) > 0.01 else None

# Define tables
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=False, nullable=False) # To save tests - Not need to be unique
    phone = Column(String, unique=False, nullable=False) # To save tests - Not need to be unique
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer')
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('shopping_carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False, default=1)
    cart = relationship('ShoppingCart')
    product = relationship('Product')
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

class SupportAgent(Base):
    __tablename__ = 'support_agents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

class SupportRequest(Base):
    __tablename__ = 'support_requests'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    agent_id = Column(Integer, ForeignKey('support_agents.id'))
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    customer = relationship('Customer')
    agent = relationship('SupportAgent')
    #record_created_at = Column(DateTime, default=datetime.now(timezone.utc))

# Setup the database engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Populate database with fake data
NUM_CUSTOMERS = max(5500, int(5500 * 1.2))
NUM_PRODUCTS = 200
NUM_AGENTS = 5
NUM_SUPPORT_REQUESTS = 600

# Generate customers with different ordering habits
customers = []
for i in range(NUM_CUSTOMERS):
    customers.append(Customer(name=fake.name(), email=fake.email(), phone=fake.phone_number()))
session.add_all(customers)
session.commit()

# Generate products
products = [Product(name=fake.word(), description=fake.sentence(), price=generate_price()) for _ in range(NUM_PRODUCTS)]
session.add_all(products)
session.commit()

# Generate orders over 6 months with different order frequencies
prior_day_range = 180
start_date = datetime.now(timezone.utc) - timedelta(days=prior_day_range)
shopping_carts = []
for day in range(prior_day_range):
    current_date = start_date + timedelta(days=day)
    day_of_week = current_date.weekday()
    if day_of_week == 6:    # Sunday
        num_orders = random.randint(10, 20)
    elif day_of_week == 5:  # Saturday:
        num_orders = random.randint(15, 30)
    else:
        num_orders = random.randint(15, 40)
    daily_customers = random.sample(customers, num_orders)
    for customer in daily_customers:
        created_at = fake.date_time_between(start_date = current_date,
                                            end_date   = current_date + timedelta(hours=23, minutes=59)
                                           )
        completed_at = generate_order_time(created_at)
        shopping_carts.append(ShoppingCart(customer_id=customer.id, created_at=created_at, completed_at=completed_at))

session.add_all(shopping_carts)
session.commit()

# Generate shopping cart items
shopping_cart_items = []
for cart in shopping_carts:
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        shopping_cart_items.append(ShoppingCartItem(cart_id=cart.id, product_id=random.choice(products).id, quantity=random.randint(1, 5)))

session.add_all(shopping_cart_items)
session.commit()

# Add support agents
agents = [SupportAgent(name=fake.name(), email=fake.email()) for _ in range(NUM_AGENTS)]
session.add_all(agents)
session.commit()

# Add support requests
support_requests = [
    SupportRequest(
        customer_id=random.choice(customers).id,
        agent_id=random.choice(agents).id,
        message=fake.sentence()
    )
    for _ in range(NUM_SUPPORT_REQUESTS)
]
session.add_all(support_requests)
session.commit()

print("Sample data generated successfully!")
