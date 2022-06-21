from tests.test_import import TestImport
from tests.test_nodes import TestNodes
from tests.test_sales import TestSales
from tests.test_stats import TestStatistic
from tests.test_delete import TestDelete

NEW_ROOT_ID = "5747cd46-f131-11ec-8ea0-0242ac120002"


def test_all():
    # TestImport.test_all(delete_after=False)
    # TestNodes.test_all(new_data=False, delete_after=False)
    # TestSales.test_all(new_data=False, delete_after=False)
    # TestStatistic.test_all(new_data=False, delete_after=True)
    TestDelete.test_delete(NEW_ROOT_ID)

test_all()
