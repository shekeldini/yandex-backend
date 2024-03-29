import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from utils import request, sort_items, print_diff


class TestStatistic:
    _ROOT_ID = "b7112a5a-f065-11ec-8ea0-0242ac120002"
    _ITEM_NOT_FOUND_ID = "3944d48a-f170-11ec-8ea0-0242ac120002"
    _STATS_TEST_ALL_TIME = {
        "items": [
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-06-10T12:00:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-06-10T12:01:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": 10978,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": 9658,
                "date": "2022-06-11T14:00:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": "5747cd46-f131-11ec-8ea0-0242ac120002",
                "type": "CATEGORY",
                "price": 9658,
                "date": "2022-06-11T14:00:00.000Z"
            }

        ]
    }
    _STATS_TEST_DATE_START = {
        "items": [
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": 10978,
                "date": "2022-06-11T11:00:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": 9658,
                "date": "2022-06-11T14:00:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": "5747cd46-f131-11ec-8ea0-0242ac120002",
                "type": "CATEGORY",
                "price": 9658,
                "date": "2022-06-11T14:00:00.000Z"
            }
        ]
    }
    _STATS_TEST_DATE_START_DATE_END = {
        "items": [
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-06-10T12:01:00.000Z"
            },
            {
                "id": "b7112a5a-f065-11ec-8ea0-0242ac120002",
                "name": "Товары",
                "parentId": None,
                "type": "CATEGORY",
                "price": 10978,
                "date": "2022-06-11T11:00:00.000Z"
            }
        ]
    }

    @staticmethod
    def all_time():
        start = time.time()
        status, response = request(
            f"/node/{TestStatistic._ROOT_ID}/statistic", json_response=True)
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        sort_items(response)
        sort_items(TestStatistic._STATS_TEST_ALL_TIME)
        if response != TestStatistic._STATS_TEST_ALL_TIME:
            print_diff(TestStatistic._STATS_TEST_ALL_TIME, response)
            print("Test_1 Response tree doesn't match expected tree.")
            sys.exit(1)
        print(f"Test: 'all time' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def start_date():
        params = urllib.parse.urlencode({
            "dateStart": "2022-06-11T10:00:00.000Z"
        })
        start = time.time()
        status, response = request(
            f"/node/{TestStatistic._ROOT_ID}/statistic?{params}", json_response=True)
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        sort_items(response)
        sort_items(TestStatistic._STATS_TEST_DATE_START)
        if response != TestStatistic._STATS_TEST_DATE_START:
            print_diff(TestStatistic._STATS_TEST_ALL_TIME, response)
            print("Test_2 Response tree doesn't match expected tree.")
            sys.exit(1)
        print(f"Test: 'start date' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def start_date_end_date():
        params = urllib.parse.urlencode({
            "dateStart": "2022-06-10T12:01:00.000Z",
            "dateEnd": "2022-06-11T11:00:00.000Z"
        })
        start = time.time()
        status, response = request(
            f"/node/{TestStatistic._ROOT_ID}/statistic?{params}", json_response=True)
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        sort_items(response)
        sort_items(TestStatistic._STATS_TEST_DATE_START_DATE_END)
        if response != TestStatistic._STATS_TEST_DATE_START_DATE_END:
            print_diff(TestStatistic._STATS_TEST_DATE_START_DATE_END, response)
            print("Test_3 Response tree doesn't match expected tree.")
            sys.exit(1)
        print(f"Test: 'start date - end date' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def item_not_found():
        start = time.time()
        status, response = request(
            f"/node/{TestStatistic._ITEM_NOT_FOUND_ID}/statistic", json_response=True)
        end = time.time()
        assert status == 404, f"Expected HTTP status code 404, got {status}"

        print(f"Test: 'item not found' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def test_all():
        TestStatistic.all_time()
        TestStatistic.start_date()
        TestStatistic.start_date_end_date()
        TestStatistic.item_not_found()

