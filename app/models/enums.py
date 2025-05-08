import enum

class PurchaseOrderStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    SHIPPED = "shipped"
    RECEIVED = "received"
    CANCELLED = "cancelled"