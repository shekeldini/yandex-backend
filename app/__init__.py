import pprint

test = {
    "name": "test1",
    "id": 1,
    "parent_id": None,
    "children": [
        {
            "name": "test2",
            "id": 2,
            "parent_id": 1,
            "children": [
                {
                    "name": "test4",
                    "id": 4,
                    "parent_id": 2
                },
                {
                    "name": "test5",
                    "id": 5,
                    "parent_id": 2
                },
            ]
        },
        {
            "name": "test3",
            "parent_id": 1,
            "id": 3
        }

    ]
}


def chilrens(test):
    res = {}
    cur = ""

    def find(test, res):
        res["id"] = test["id"]
        res["name"] = test["id"]
        res["parent_id"] = test["name"]
        res["children"] = []
        if test.get("children"):
            for item in test["children"]:
                res["children"].append({})
                find(item, res["children"][-1])

    find(test, res)
    return res


pprint.pprint(chilrens(test))
