from .database import create_tables, lifespan, get_session
from .email_utils import send_order_confirmation
from .models import Category, Product,Orders
from .routes import category,product,orders  