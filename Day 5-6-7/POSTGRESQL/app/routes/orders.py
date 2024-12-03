from __future__ import annotations

from app.auth import admin_only
from app.database import get_session
from app.models import Orders
from app.models import Product
from app.utils import send_order_confirmation
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import Session

# Importing models, database session, utilities, and authentication utilities

router = APIRouter()

# Endpoint to place a new order (POST /)


@router.post("/", response_model=Orders)
async def place_order(
    order: Orders,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    # Fetch the product using the product_id from the order
    product = session.exec(
        select(Product).where(Product.id == order.product_id),
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    # Check if there is enough stock for the order
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock.")

    # Update product stock and commit the order
    product.stock -= order.quantity
    session.add(order)
    session.add(product)
    session.commit()
    session.refresh(order)

    # Add a background task to send an order confirmation email
    background_tasks.add_task(send_order_confirmation, order.email, order.id)

    # Return the order ID after successful placement
    return order.id
    # Alternative: return a message with order ID (commented out)
    # return {"message": "Order placed successfully.", "order_id": order.id}


# Endpoint to read all orders (GET /)


@router.get("/", dependencies=[Depends(admin_only)])
async def read_orders(session: Session = Depends(get_session)):
    # Fetch all orders from the database
    orders = session.exec(select(Orders)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found.")
    return orders


# Endpoint to read a specific order by its ID (GET /{id})


@router.get("/{id}", dependencies=[Depends(admin_only)])
async def read_order(id: int, session: Session = Depends(get_session)):
    # Fetch the order by its ID
    order = session.exec(select(Orders).where(Orders.id == id)).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {id} not found.")
    return order
