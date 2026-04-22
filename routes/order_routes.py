from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from dependencies import get_session, verify_token
from models import Order, OrderStatus, User, OrderItem
from schemas import OrderSchema, OrderItemSchema, OrderResponseSchema
from typing import List

# Router de pedidos com autenticação obrigatória em todas as rotas
order_router = APIRouter(prefix='/orders', tags=['orders'], dependencies=[Depends(verify_token)])


@order_router.get('/')
async def orders():
    '''
    Rota base de pedidos para teste de autenticação

    '''

@order_router.post('/order')
async def create_order(session=Depends(get_session),
user: User= Depends(verify_token)):

    # Cria um novo pedido associado ao usuário
    new_order = Order(user_id=user.id)
    session.add(new_order)
    session.commit()
    return {
        "message": "ORDER_CREATED",
        "order_id": new_order.id
        }


@order_router.post('/order/cancel/{order_id}')
async def cancel_order(order_id: int, session=Depends(get_session), user: User=Depends(verify_token)):
    # Busca o pedido pelo ID
    order = session.query(Order).filter(Order.id == order_id).first()

    # Validação de existência
    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ORDER_ITEM_NOT_FOUND")
    
    # Verifica permissão (admin ou dono do pedido)
    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='ACCESS_DENIED'
        )

    # Atualiza status para cancelado
    order.status = OrderStatus.CANCELED
    session.commit()
    return {
        "message": "ORDER_CANCELED",
        "order_id": order.id 
        }


@order_router.get('/list')
async def list_orders(session=Depends(get_session), user: User=Depends(verify_token)):
    
    # Apenas administradores podem listar todos os pedidos
    if not user.is_admin:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='ACCESS_DENIED'
        )
    else:
        orders = session.query(Order).all()
        return {
            "message": "ORDERS_LISTED",
            "data": orders
        }


@order_router.post('/order/add_item/{order_id}')
async def add_item_order(order_id: int,
                         order_item_schema: OrderItemSchema, 
                         session=Depends(get_session), 
                         user: User=Depends(verify_token)):
    
    # Busca o pedido
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ORDER_ITEM_NOT_FOUND"
        )
    
    # Verifica permissão
    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='ACCESS_DENIED'
    )

    # Cria item do pedido
    order_item = OrderItem(
        order_item_schema.quantity,
        order_item_schema.flavor,
        order_item_schema.size,
        order_item_schema.unit_price,
        order_id
    )   

    session.add(order_item)

    # Recalcula o preço total do pedido
    order.calculate_price()
    session.commit()

    return {
        "message": "ITEM_CREATED",
        "data": {
            "item_id": order_item.id,
            "order_price": order.price
    }
}


@order_router.post('/order/remove_item/{id_order_item}')
async def remove_item_order(id_order_item: int, 
                         session=Depends(get_session), 
                         user: User=Depends(verify_token)):
    
    # Busca item do pedido
    order_item = session.query(OrderItem).filter(OrderItem.id == id_order_item).first()
    if not order_item:  
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ORDER_ITEM_NOT_FOUND"
        )
    
    order = order_item.order
    
    # Verifica permissão
    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='ACCESS_DENIED'
    ) 

    # Remove item e atualiza valor do pedido
    session.delete(order_item)
    order.calculate_price()
    session.commit()

    return{
        'mensagem': "ITEM_REMOVED",
        'order': order,
        'items': order.items
    }


@order_router.post('/order/complete/{order_id}')
async def complete_order(order_id: int, session=Depends(get_session), user: User=Depends(verify_token)):
    
    # Busca o pedido
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ORDER_NOT_FOUND")
    
    # Verifica permissão
    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='ACCESS_DENIED'
        )

    # Marca pedido como concluído
    order.status = OrderStatus.COMPLETED
    session.commit()

    return {
        "message": "ORDER_COMPLETED",
        "order_id": order.id 
        }


@order_router.get('/order/user-orders', response_model=List[OrderResponseSchema])
async def list_orders(session=Depends(get_session), user: User=Depends(verify_token)):
    # Lista pedidos do usuário autenticado
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    return orders


@order_router.get('/order/{order_id}')
async def get_order(order_id: int, session=Depends(get_session), user: User=Depends(verify_token)):
    
    # Busca pedido por ID
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ORDER_NOT_FOUND")
    
    # Verifica permissão
    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='ACCESS_DENIED'
        )
    
    return{
        "order": order
    }
    


