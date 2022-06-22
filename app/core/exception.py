class TooManyRequests(Exception):
    """
        Raise if request limit is exceeded
    """
    pass


class ParentNotFound(Exception):
    """
        Raise if import item have non-existent parentId
    """
    pass


class OfferCanNotBeParent(Exception):
    """
        Raise if import item have parentId who have type 'OFFER'
    """
    pass


class CanNotChangeType(Exception):
    """
       Raise if try change shop unit type
    """
    pass