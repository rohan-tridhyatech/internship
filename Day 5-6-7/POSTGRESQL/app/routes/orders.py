from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import select, Session
from app import Orders, Product
from app import get_session
from app import send_order_confirmation

router = APIRouter()

@router.post("/", response_model=Orders)
async def place_order(order: Orders, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == order.product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock.")

    product.stock -= order.quantity
    session.add(order)
    session.add(product)
    session.commit()
    session.refresh(order)

    background_tasks.add_task(send_order_confirmation, order.email, order.id)
    return {"message": "Order placed successfully.", "order_id": order.id}

@router.get("/")
async def read_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Orders)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found.")
    return orders

@router.get("/{id}")
async def read_order(id: int, session: Session = Depends(get_session)):
    order = session.exec(select(Orders).where(Orders.id == id)).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {id} not found.")
    return order
