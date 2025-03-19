from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import random
import datetime
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

# Define tables
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('shopping_carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False, default=1)
    cart = relationship('ShoppingCart')
    product = relationship('Product')

class SupportAgent(Base):
    __tablename__ = 'support_agents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class SupportRequest(Base):
    __tablename__ = 'support_requests'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    agent_id = Column(Integer, ForeignKey('support_agents.id'))
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    customer = relationship('Customer')
    agent = relationship('SupportAgent')

# Setup the database engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Populate database with fake data
NUM_CUSTOMERS = 10
NUM_PRODUCTS = 15
NUM_AGENTS = 5
NUM_SUPPORT_REQUESTS = 20

# Add customers
customers = [Customer(name=fake.name(), email=fake.email(), phone=fake.phone_number()) for _ in range(NUM_CUSTOMERS)]
session.add_all(customers)
session.commit()

# Add products
products = [Product(name=fake.word(), description=fake.sentence(), price=generate_price()) for _ in range(NUM_PRODUCTS)]
session.add_all(products)
session.commit()

# Add shopping carts
shopping_carts = [ShoppingCart(customer_id=random.choice(customers).id, created_at=fake.date_time_this_year()) for _ in range(NUM_CUSTOMERS)]
session.add_all(shopping_carts)
session.commit()

# Add shopping cart items
shopping_cart_items = [
    ShoppingCartItem(cart_id=random.choice(shopping_carts).id, product_id=random.choice(products).id, quantity=random.randint(1, 5))
    for _ in range(NUM_CUSTOMERS * 2)
]
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

