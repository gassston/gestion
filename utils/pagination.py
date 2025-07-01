from fastapi_pagination.cursor import CursorParams

class CustomCursorParams(CursorParams):
    size: int = 10  # Default items per page
    cursor: str | None = None  # Cursor value (encoded ID)
    order: str = "id:asc"  # Default sort order (by ID ascending)
