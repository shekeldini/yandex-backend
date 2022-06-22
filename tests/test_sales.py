import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from utils import request, sort_items, print_diff


class TestSales:
    _SALES_TEST_1 = {
        "items": [
            {
                "id": "cc750ffa-f066-11ec-8ea0-0242ac120002",
                "name": "Тостер_1",
                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 2000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc75137e-f066-11ec-8ea0-0242ac120002",
                "name": "Тостер_2",
                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 2500,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc751586-f066-11ec-8ea0-0242ac120002",
                "name": "Тостер_3",
                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 3000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc75175c-f066-11ec-8ea0-0242ac120002",
                "name": "Видеокарта_1",
                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 20000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc75189c-f066-11ec-8ea0-0242ac120002",
                "name": "Видеокарта_2",
                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 30000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc7519e6-f066-11ec-8ea0-0242ac120002",
                "name": "Видеокарта_3",
                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 40000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc751b1c-f066-11ec-8ea0-0242ac120002",
                "name": "Процессор_1",
                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 10000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc751c52-f066-11ec-8ea0-0242ac120002",
                "name": "Процессор_2",
                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 15000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc752030-f066-11ec-8ea0-0242ac120002",
                "name": "Процессор_3",
                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 20000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc752166-f066-11ec-8ea0-0242ac120002",
                "name": "Футболка_1",
                "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 1000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc75229c-f066-11ec-8ea0-0242ac120002",
                "name": "Футболка_2",
                "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 1200,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc7525ee-f066-11ec-8ea0-0242ac120002",
                "name": "Кроссовки_1",
                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 3000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "cc75272e-f066-11ec-8ea0-0242ac120002",
                "name": "Кроссовки_2",
                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 5000,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "8f1eb91c-f11a-11ec-8ea0-0242ac120002",
                "name": "Фен_1",
                "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 1000,
                "date": "2022-06-11T11:00:00.000Z"
            }
        ]
    }
    _SALES_TEST_2 = {
        "items": [
            {
                "id": "cc752878-f066-11ec-8ea0-0242ac120002",
                "name": "Кроссовки_3",
                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 5500,
                "date": "2022-06-11T14:00:00.000Z"
            },
            {
                "id": "cc7529c2-f066-11ec-8ea0-0242ac120002",
                "name": "Кроссовки_4",
                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 4000,
                "date": "2022-06-11T14:00:00.000Z"
            },
            {
                "id": "daf5216e-f11a-11ec-8ea0-0242ac120002",
                "name": "Крем от загара",
                "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 1000,
                "date": "2022-06-11T14:00:00.000Z"
            }
        ]
    }
    _ROOT_ID = "b7112a5a-f065-11ec-8ea0-0242ac120002"

    @staticmethod
    def test_1():
        params = urllib.parse.urlencode({
            "date": "2022-06-10T12:00:00.000Z"
        })
        start = time.time()
        status, response = request(f"/sales?{params}", json_response=True)
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        sort_items(response)
        sort_items(TestSales._SALES_TEST_1)
        if response != TestSales._SALES_TEST_1:
            print_diff(TestSales._SALES_TEST_1, response)
            print("Test_1 Response tree doesn't match expected tree.")
            sys.exit(1)
        print(f"Test: 'sales_1' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def test_2():
        params = urllib.parse.urlencode({
            "date": "2022-06-11T12:00:00.000Z"
        })
        start = time.time()
        status, response = request(f"/sales?{params}", json_response=True)
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        sort_items(response)
        sort_items(TestSales._SALES_TEST_2)
        if response != TestSales._SALES_TEST_2:
            print_diff(TestSales._SALES_TEST_2, response)
            print("Test_2 Response tree doesn't match expected tree.")
            sys.exit(1)

        print(f"Test: 'sales_2' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def test_all():
        TestSales.test_1()
        TestSales.test_2()
