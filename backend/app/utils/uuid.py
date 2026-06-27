from uuid import UUID, uuid4


def generate_uuid() -> str:
    return str(uuid4())


def is_valid_uuid(value: str) -> bool:
    try:
        UUID(str(value))
        return True
    except ValueError:
        return False
