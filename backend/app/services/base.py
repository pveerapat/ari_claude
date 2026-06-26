class BaseService:
    """Base class for ARI services.

    Session lifecycle rule:
    - commit only after successful operation
    - rollback on exception
    - never share a session across requests
    """
    pass
