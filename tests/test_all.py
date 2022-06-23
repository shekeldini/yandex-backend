from test_import import TestImport
from test_nodes import TestNodes
from test_sales import TestSales
from test_stats import TestStatistic
from test_delete import TestDelete

ROOT_ID = "5747cd46-f131-11ec-8ea0-0242ac120002"


def test_all():
    TestImport.test_all()
    TestNodes.test_all()
    TestSales.test_all()
    TestStatistic.test_all()
    TestDelete.test_all(ROOT_ID)


test_all()
