import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app.main import create_app
from app.extensions import db
from app.models.purchase_orders import PurchaseOrdersModel
from app.models.purchase_orders_items import PurchaseOrdersItemsModel

@pytest.fixture(scope='module')
def test_client():
    client = create_app(config_class="app.config.TestingConfig")
    with client.test_client() as test_client:
        with client.app_context():
            yield test_client

@pytest.fixture(scope='function')
def test_db_session():
    connection = db.engine.connect()

    session_factory = sessionmaker(bind=connection)
    test_session = scoped_session(session_factory)

    global_session = db.session
    db.session = test_session

    yield test_session

    connection.close()
    test_session.remove()
    db.session = global_session

@pytest.fixture(scope='function')
def seed_test_db(test_db_session):
    insert_purchase_order = PurchaseOrdersModel(description="Purchase order for test")
    test_db_session.add(insert_purchase_order)
    test_db_session.commit()
    insert_purchase_order_item = PurchaseOrdersItemsModel(description="Item for test purchase order", price=99.99, quantity=5, purchase_order_id=insert_purchase_order.id)
    test_db_session.add(insert_purchase_order_item)
    test_db_session.commit()
    yield {'po': insert_purchase_order, 'poi': insert_purchase_order_item}

@pytest.fixture(scope='function', autouse=True)
def clear_test_db(test_db_session):
    test_db_session.query(PurchaseOrdersItemsModel).delete()
    test_db_session.query(PurchaseOrdersModel).delete()
    test_db_session.commit()