from sqlalchemy import create_engine, ForeignKey, text, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship
import enum

# Criação do engine para conexão com banco SQLite
db = create_engine('sqlite:///database/banco.db')

# Classe base para os modelos (utilizando dataclass + ORM)
class Base(MappedAsDataclass, DeclarativeBase):
    pass


# Modelo de usuário
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    flavor: Mapped[str]
    size: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[str]
    stock: Mapped[int] = mapped_column(default=0)

    items = relationship("OrderItem", back_populates="product")


# Enum para status do pedido
class OrderStatus(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


# Modelo de pedido
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Status do pedido utilizando Enum
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )

    # Valor total do pedido
    price: Mapped[float] = mapped_column(default=0, server_default=text("0"))

    # Relacionamentos
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", cascade="all, delete-orphan")

    # Calcula o valor total com base nos itens
    def calculate_price(self):
        self.price = sum(item.unit_price * item.quantity for item in self.items)


# Modelo de item do pedido
class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    quantity: Mapped[int]
    unit_price = Mapped[float]

    # Chave estrangeira para o pedido
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    # Relacionamentos
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
