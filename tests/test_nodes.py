import sys
from tests.test_delete import TestDelete
from tests.test_import import TestImport
from tests.utils import request, deep_sort_children, print_diff


class TestNodes:
    _ROOT_ID = "b7112a5a-f065-11ec-8ea0-0242ac120002"
    _NEW_ROOT_ID = "5747cd46-f131-11ec-8ea0-0242ac120002"
    _EXPECTED_TREE = {
        "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
        "name": "Товары",
        "date": "2022-06-11T14:00:00.000Z",
        "parentId": "5747cd46-f131-11ec-8ea0-0242ac120002",
        "type": "CATEGORY",
        "price": 9658,
        "children": [
            {
                "id": "daf5216e-f11a-11ec-8ea0-0242ac120002",
                "name": "Крем от загара",
                "date": "2022-06-11T14:00:00.000Z",
                "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "type": "OFFER",
                "price": 1000,
                "children": None
            },
            {
                "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                "name": "Электроника",
                "date": "2022-06-11T11:00:00.000Z",
                "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "type": "CATEGORY",
                "price": 14350,
                "children": [
                    {
                        "id": "8f1eb91c-f11a-11ec-8ea0-0242ac120002",
                        "name": "Фен_1",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                        "type": "OFFER",
                        "price": 1000,
                        "children": None
                    },
                    {
                        "id": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                        "name": "Тостеры",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 2500,
                        "children": [
                            {
                                "id": "cc750ffa-f066-11ec-8ea0-0242ac120002",
                                "name": "Тостер_1",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 2000,
                                "children": None
                            },
                            {
                                "id": "cc75137e-f066-11ec-8ea0-0242ac120002",
                                "name": "Тостер_2",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 2500,
                                "children": None
                            },
                            {
                                "id": "cc751586-f066-11ec-8ea0-0242ac120002",
                                "name": "Тостер_3",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 3000,
                                "children": None
                            }
                        ]
                    },
                    {
                        "id": "d345f26e-f065-11ec-8ea0-0242ac120002",
                        "name": "Видеокарты",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 30000,
                        "children": [
                            {
                                "id": "cc75189c-f066-11ec-8ea0-0242ac120002",
                                "name": "Видеокарта_2",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 30000,
                                "children": None
                            },
                            {
                                "id": "cc7519e6-f066-11ec-8ea0-0242ac120002",
                                "name": "Видеокарта_3",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 40000,
                                "children": None
                            },
                            {
                                "id": "cc75175c-f066-11ec-8ea0-0242ac120002",
                                "name": "Видеокарта_1",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 20000,
                                "children": None
                            }
                        ]
                    },
                    {
                        "id": "d345f35e-f065-11ec-8ea0-0242ac120002",
                        "name": "Процессоры",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 15000,
                        "children": [
                            {
                                "id": "cc751b1c-f066-11ec-8ea0-0242ac120002",
                                "name": "Процессор_1",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 10000,
                                "children": None
                            },
                            {
                                "id": "cc751c52-f066-11ec-8ea0-0242ac120002",
                                "name": "Процессор_2",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 15000,
                                "children": None
                            },
                            {
                                "id": "cc752030-f066-11ec-8ea0-0242ac120002",
                                "name": "Процессор_3",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 20000,
                                "children": None
                            }
                        ]
                    }
                ]
            },
            {
                "id": "d345f44e-f065-11ec-8ea0-0242ac120002",
                "name": "Одежда",
                "date": "2022-06-11T14:00:00.000Z",
                "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "type": "CATEGORY",
                "price": 3283,
                "children": [
                    {
                        "id": "d345f53e-f065-11ec-8ea0-0242ac120002",
                        "name": "Футболки",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 1100,
                        "children": [
                            {
                                "id": "cc752166-f066-11ec-8ea0-0242ac120002",
                                "name": "Футболка_1",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 1000,
                                "children": None
                            },
                            {
                                "id": "cc75229c-f066-11ec-8ea0-0242ac120002",
                                "name": "Футболка_2",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 1200,
                                "children": None
                            }
                        ]
                    },
                    {
                        "id": "d345f62e-f065-11ec-8ea0-0242ac120002",
                        "name": "Обувь",
                        "date": "2022-06-11T14:00:00.000Z",
                        "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 4375,
                        "children": [
                            {
                                "id": "d345f714-f065-11ec-8ea0-0242ac120002",
                                "name": "Кроссовки",
                                "date": "2022-06-11T14:00:00.000Z",
                                "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 4375,
                                "children": [
                                    {
                                        "id": "cc7525ee-f066-11ec-8ea0-0242ac120002",
                                        "name": "Кроссовки_1",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 3000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc75272e-f066-11ec-8ea0-0242ac120002",
                                        "name": "Кроссовки_2",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 5000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc752878-f066-11ec-8ea0-0242ac120002",
                                        "name": "Кроссовки_3",
                                        "date": "2022-06-11T14:00:00.000Z",
                                        "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 5500,
                                        "children": None
                                    },
                                    {
                                        "id": "cc7529c2-f066-11ec-8ea0-0242ac120002",
                                        "name": "Кроссовки_4",
                                        "date": "2022-06-11T14:00:00.000Z",
                                        "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 4000,
                                        "children": None
                                    }
                                ]
                            },
                            {
                                "id": "d345f8ea-f065-11ec-8ea0-0242ac120002",
                                "name": "Туфли",
                                "date": "2022-06-10T12:01:00.000Z",
                                "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": None,
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
    _UPDATED_EXPECTED_TREE = {
        "id": "5747cd46-f131-11ec-8ea0-0242ac120002",
        "name": "Новая категория",
        "date": "2022-06-11T14:00:00.000Z",
        "parentId": None,
        "type": "CATEGORY",
        "price": 9658,
        "children": [
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "date": "2022-06-11T14:00:00.000Z",
                "parentId": "5747cd46-f131-11ec-8ea0-0242ac120002",
                "type": "CATEGORY",
                "price": 9658,
                "children": [
                    {
                        "id": "d345f44e-f065-11ec-8ea0-0242ac120002",
                        "name": "Одежда",
                        "date": "2022-06-11T14:00:00.000Z",
                        "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 3283,
                        "children": [
                            {
                                "id": "d345f53e-f065-11ec-8ea0-0242ac120002",
                                "name": "Футболки",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 1100,
                                "children": [
                                    {
                                        "id": "cc752166-f066-11ec-8ea0-0242ac120002",
                                        "name": "Футболка_1",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 1000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc75229c-f066-11ec-8ea0-0242ac120002",
                                        "name": "Футболка_2",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 1200,
                                        "children": None
                                    }
                                ]
                            },
                            {
                                "id": "d345f62e-f065-11ec-8ea0-0242ac120002",
                                "name": "Обувь",
                                "date": "2022-06-11T14:00:00.000Z",
                                "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 4375,
                                "children": [
                                    {
                                        "id": "d345f714-f065-11ec-8ea0-0242ac120002",
                                        "name": "Кроссовки",
                                        "date": "2022-06-11T14:00:00.000Z",
                                        "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002",
                                        "type": "CATEGORY",
                                        "price": 4375,
                                        "children": [
                                            {
                                                "id": "cc7525ee-f066-11ec-8ea0-0242ac120002",
                                                "name": "Кроссовки_1",
                                                "date": "2022-06-11T11:00:00.000Z",
                                                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                                "type": "OFFER",
                                                "price": 3000,
                                                "children": None
                                            },
                                            {
                                                "id": "cc75272e-f066-11ec-8ea0-0242ac120002",
                                                "name": "Кроссовки_2",
                                                "date": "2022-06-11T11:00:00.000Z",
                                                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                                "type": "OFFER",
                                                "price": 5000,
                                                "children": None
                                            },
                                            {
                                                "id": "cc752878-f066-11ec-8ea0-0242ac120002",
                                                "name": "Кроссовки_3",
                                                "date": "2022-06-11T14:00:00.000Z",
                                                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                                "type": "OFFER",
                                                "price": 5500,
                                                "children": None
                                            },
                                            {
                                                "id": "cc7529c2-f066-11ec-8ea0-0242ac120002",
                                                "name": "Кроссовки_4",
                                                "date": "2022-06-11T14:00:00.000Z",
                                                "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                                                "type": "OFFER",
                                                "price": 4000,
                                                "children": None
                                            }
                                        ]
                                    },
                                    {
                                        "id": "d345f8ea-f065-11ec-8ea0-0242ac120002",
                                        "name": "Туфли",
                                        "date": "2022-06-10T12:01:00.000Z",
                                        "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002",
                                        "type": "CATEGORY",
                                        "price": None,
                                        "children": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "daf5216e-f11a-11ec-8ea0-0242ac120002",
                        "name": "Крем от загара",
                        "date": "2022-06-11T14:00:00.000Z",
                        "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                        "type": "OFFER",
                        "price": 1000,
                        "children": None
                    },
                    {
                        "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                        "name": "Электроника",
                        "date": "2022-06-11T11:00:00.000Z",
                        "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                        "type": "CATEGORY",
                        "price": 14350,
                        "children": [
                            {
                                "id": "8f1eb91c-f11a-11ec-8ea0-0242ac120002",
                                "name": "Фен_1",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                                "type": "OFFER",
                                "price": 1000,
                                "children": None
                            },
                            {
                                "id": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                "name": "Тостеры",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 2500,
                                "children": [
                                    {
                                        "id": "cc750ffa-f066-11ec-8ea0-0242ac120002",
                                        "name": "Тостер_1",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 2000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc75137e-f066-11ec-8ea0-0242ac120002",
                                        "name": "Тостер_2",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 2500,
                                        "children": None
                                    },
                                    {
                                        "id": "cc751586-f066-11ec-8ea0-0242ac120002",
                                        "name": "Тостер_3",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 3000,
                                        "children": None
                                    }
                                ]
                            },
                            {
                                "id": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                "name": "Видеокарты",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 30000,
                                "children": [
                                    {
                                        "id": "cc75175c-f066-11ec-8ea0-0242ac120002",
                                        "name": "Видеокарта_1",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 20000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc75189c-f066-11ec-8ea0-0242ac120002",
                                        "name": "Видеокарта_2",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 30000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc7519e6-f066-11ec-8ea0-0242ac120002",
                                        "name": "Видеокарта_3",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 40000,
                                        "children": None
                                    }
                                ]
                            },
                            {
                                "id": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                "name": "Процессоры",
                                "date": "2022-06-11T11:00:00.000Z",
                                "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                                "type": "CATEGORY",
                                "price": 15000,
                                "children": [
                                    {
                                        "id": "cc751b1c-f066-11ec-8ea0-0242ac120002",
                                        "name": "Процессор_1",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 10000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc751c52-f066-11ec-8ea0-0242ac120002",
                                        "name": "Процессор_2",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 15000,
                                        "children": None
                                    },
                                    {
                                        "id": "cc752030-f066-11ec-8ea0-0242ac120002",
                                        "name": "Процессор_3",
                                        "date": "2022-06-11T11:00:00.000Z",
                                        "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                                        "type": "OFFER",
                                        "price": 20000,
                                        "children": None
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    @staticmethod
    def basic():

        status, response = request(f"/nodes/{TestNodes._ROOT_ID}", json_response=True)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

        deep_sort_children(response)
        deep_sort_children(TestNodes._EXPECTED_TREE)
        if response != TestNodes._EXPECTED_TREE:
            print_diff(TestNodes._EXPECTED_TREE, response)
            print("Response tree doesn't match expected tree.")
            sys.exit(1)

        print("Test: 'basic' passed.")

    @staticmethod
    def updated():
        status, response = request(f"/nodes/{TestNodes._NEW_ROOT_ID}", json_response=True)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

        deep_sort_children(response)
        deep_sort_children(TestNodes._UPDATED_EXPECTED_TREE)
        if response != TestNodes._UPDATED_EXPECTED_TREE:
            print_diff(TestNodes._UPDATED_EXPECTED_TREE, response)
            print("Response tree doesn't match expected tree.")
            sys.exit(1)

        print("Test: 'updated' passed.")

    @staticmethod
    def test_all():
        TestNodes.basic()
        TestNodes.updated()


