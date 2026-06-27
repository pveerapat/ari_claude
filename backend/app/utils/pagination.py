import math

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def clamp_page(page: int) -> int:
    return max(DEFAULT_PAGE, page)


def clamp_page_size(page_size: int) -> int:
    return max(1, min(page_size, MAX_PAGE_SIZE))


def calc_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size


def calc_total_pages(total_records: int, page_size: int) -> int:
    if page_size <= 0:
        return 0
    return math.ceil(total_records / page_size)


def pagination_meta(page: int, page_size: int, total_records: int) -> dict:
    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_records,
        "total_pages": calc_total_pages(total_records, page_size),
    }
