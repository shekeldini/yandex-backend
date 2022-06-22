import time

from utils import request


class TestDelete:
    @staticmethod
    def delete(root_id, print_info=True):
        start = time.time()
        status, _ = request(f"/delete/{root_id}", method="DELETE")
        end = time.time()
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        if print_info:
            print(f"Test: 'delete' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def item_not_found(root_id):
        start = time.time()
        status, _ = request(f"/delete/{root_id}", method="DELETE")
        end = time.time()
        assert status == 404, f"Expected HTTP status code 404, got {status}"
        print(f"Test: 'item not found' passed. Time: {round(end - start, 3)}")

    @staticmethod
    def test_all(root_id):
        TestDelete.delete(root_id)
        TestDelete.item_not_found(root_id)
