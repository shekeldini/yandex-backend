from tests.test_delete import TestDelete
from tests.utils import request


class TestImport:
    _CORRECT_DATA = [
        {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товары",
                    "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                    "parentId": None,
                    "children": []
                }
            ],
            "updateDate": "2022-06-10T12:00:00.000Z"
        },
        {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Электроника",
                    "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Тостеры",
                    "id": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Видеокарты",
                    "id": "d345f26e-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Процессоры",
                    "id": "d345f35e-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Одежда",
                    "id": "d345f44e-f065-11ec-8ea0-0242ac120002",
                    "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Футболки",
                    "id": "d345f53e-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Обувь",
                    "id": "d345f62e-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345f44e-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Кроссовки",
                    "id": "d345f714-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002"
                },
                {
                    "type": "CATEGORY",
                    "name": "Туфли",
                    "id": "d345f8ea-f065-11ec-8ea0-0242ac120002",
                    "parentId": "d345f62e-f065-11ec-8ea0-0242ac120002"
                }
            ],
            "updateDate": "2022-06-10T12:01:00.000Z"
        },
        {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Тостер_1",
                    "id": "cc750ffa-f066-11ec-8ea0-0242ac120002",
                    "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                    "price": 2000
                },
                {
                    "type": "OFFER",
                    "name": "Тостер_2",
                    "id": "cc75137e-f066-11ec-8ea0-0242ac120002",
                    "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                    "price": 2500
                },
                {
                    "type": "OFFER",
                    "name": "Тостер_3",
                    "id": "cc751586-f066-11ec-8ea0-0242ac120002",
                    "parentId": "cc7532f0-f066-11ec-8ea0-0242ac120002",
                    "price": 3000
                },
                {
                    "type": "OFFER",
                    "name": "Видеокарта_1",
                    "id": "cc75175c-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                    "price": 20000
                },
                {
                    "type": "OFFER",
                    "name": "Видеокарта_2",
                    "id": "cc75189c-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                    "price": 30000
                },
                {
                    "type": "OFFER",
                    "name": "Видеокарта_3",
                    "id": "cc7519e6-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f26e-f065-11ec-8ea0-0242ac120002",
                    "price": 40000
                },
                {
                    "type": "OFFER",
                    "name": "Процессор_1",
                    "id": "cc751b1c-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                    "price": 10000
                },
                {
                    "type": "OFFER",
                    "name": "Процессор_2",
                    "id": "cc751c52-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                    "price": 15000
                },
                {
                    "type": "OFFER",
                    "name": "Процессор_3",
                    "id": "cc752030-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f35e-f065-11ec-8ea0-0242ac120002",
                    "price": 20000
                },
                {
                    "type": "OFFER",
                    "name": "Футболка_1",
                    "id": "cc752166-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                    "price": 1000
                },
                {
                    "type": "OFFER",
                    "name": "Футболка_2",
                    "id": "cc75229c-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f53e-f065-11ec-8ea0-0242ac120002",
                    "price": 1200
                },
                {
                    "type": "OFFER",
                    "name": "Кроссовки_1",
                    "id": "cc7525ee-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                    "price": 3000
                },
                {
                    "type": "OFFER",
                    "name": "Кроссовки_2",
                    "id": "cc75272e-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                    "price": 5000
                },
                {
                    "type": "OFFER",
                    "name": "Фен_1",
                    "id": "8f1eb91c-f11a-11ec-8ea0-0242ac120002",
                    "parentId": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "price": 1000
                }
            ],
            "updateDate": "2022-06-11T11:00:00.000Z"
        },
        {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Кроссовки_3",
                    "id": "cc752878-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                    "price": 5500
                },
                {
                    "type": "OFFER",
                    "name": "Кроссовки_4",
                    "id": "cc7529c2-f066-11ec-8ea0-0242ac120002",
                    "parentId": "d345f714-f065-11ec-8ea0-0242ac120002",
                    "price": 4000
                },
                {
                    "id": "daf5216e-f11a-11ec-8ea0-0242ac120002",
                    "name": "Крем от загара",
                    "parentId": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                    "type": "OFFER",
                    "price": 1000
                }
            ],
            "updateDate": "2022-06-11T14:00:00.000Z"
        }

    ]
    _ROOT_ID = "b7112a5a-f065-11ec-8ea0-0242ac120002"

    @staticmethod
    def correct_data_test(print_info=True):
        for index, batch in enumerate(TestImport._CORRECT_DATA):
            if print_info:
                print(f"Importing batch {index}")
            status, _ = request("/imports", method="POST", data=batch)

            assert status == 200, f"Expected HTTP status code 200, got {status}"
        if print_info:
            print("Test: 'import' passed.")

    @staticmethod
    def update_root():
        import_data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Новая категория",
                    "id": "5747cd46-f131-11ec-8ea0-0242ac120002",
                    "parentId": None,
                    "children": []
                }
            ],
            "updateDate": "2022-06-21T12:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=import_data)

        assert status == 200, f"Expected HTTP status code 200, got {status}"
        import_data = {

            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товары",
                    "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                    "parentId": "5747cd46-f131-11ec-8ea0-0242ac120002",
                    "children": []
                }
            ],
            "updateDate": "2022-06-10T12:00:00.000Z"
        }

        status, _ = request("/imports", method="POST", data=import_data)

        assert status == 200, f"Expected HTTP status code 200, got {status}"
        print("Test: 'update root' passed.")
        return "5747cd46-f131-11ec-8ea0-0242ac120002"

    @staticmethod
    def parent_not_found():
        data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_Offer",
                    "parentId": "3fa85f61-5717-4562-b3fc-2c963f66afa6",
                    "type": "OFFER",
                    "price": 2000
                }
            ],
            "updateDate": "2022-06-21T05:39:25.373Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'parent not found' passed")

    @staticmethod
    def duplicate_id():
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Электроника",
                    "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "parentId": None
                },
                {
                    "type": "CATEGORY",
                    "name": "NEW_Электроника",
                    "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "parentId": None
                }
            ],
            "updateDate": "2022-06-10T12:01:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'duplicate id' passed")

    @staticmethod
    def invalid_offer_price():
        data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_Offer",
                    "type": "OFFER",
                    "price": -2000
                }
            ],
            "updateDate": "2022-06-11T11:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'invalid offer price' passed")

    @staticmethod
    def insert_price_in_category():
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Электроника",
                    "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "parentId": None,
                    "price": 0
                }
            ],
            "updateDate": "2022-06-11T14:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'invalid offer price' passed")

    @staticmethod
    def has_no_name():
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": None,
                    "id": "d345edb4-f065-11ec-8ea0-0242ac120002",
                    "parentId": None
                }
            ],
            "updateDate": "2022-06-11T14:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'has no name' passed")

    @staticmethod
    def offer_has_no_price():
        data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_Offer",
                    "type": "OFFER",
                    "price": None
                }
            ],
            "updateDate": "2022-06-11T11:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        print("Test: 'offer has no price' passed")

    @staticmethod
    def change_type():
        first_data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_CATEGORY",
                    "type": "CATEGORY",
                    "price": None
                }
            ],
            "updateDate": "2022-06-11T11:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=first_data)

        assert status == 200, f"Expected HTTP status code 400, got {status}"

        second_data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_OFFER",
                    "type": "OFFER",
                    "price": None
                }
            ],
            "updateDate": "2022-06-11T11:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=second_data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"
        TestDelete.test_delete("3fa85f64-5717-4562-b3fc-2c963f66afa6", print_info=False)
        print("Test: 'change type' passed")

    @staticmethod
    def invalid_date():
        first_data = {
            "items": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Test_CATEGORY",
                    "type": "CATEGORY",
                    "price": 1000
                }
            ],
            "updateDate": "11-06-2022T11:00:00.000Z"
        }
        status, _ = request("/imports", method="POST", data=first_data)
        assert status == 400, f"Expected HTTP status code 400, got {status}"

        print("Test: 'invalid date' passed")

    @staticmethod
    def test_all():
        TestImport.correct_data_test()
        new_root = TestImport.update_root()
        TestDelete.test_delete(new_root, print_info=False)
        TestImport.parent_not_found()
        TestImport.duplicate_id()
        TestImport.invalid_offer_price()
        TestImport.insert_price_in_category()
        TestImport.has_no_name()
        TestImport.offer_has_no_price()
        TestImport.change_type()
        TestImport.invalid_date()

