from tests.utils import request


class TestDelete:
    @staticmethod
    def test_delete(root_id, print_info=True):
        status, _ = request(f"/delete/{root_id}", method="DELETE")
        assert status == 200, f"Expected HTTP status code 200, got {status}"

        status, _ = request(f"/nodes/{root_id}", json_response=True)
        assert status == 404, f"Expected HTTP status code 404, got {status}"
        if print_info:
            print("Test delete passed.")
