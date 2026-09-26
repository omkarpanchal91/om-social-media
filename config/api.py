"""Django Ninja API entry point."""

from ninja import NinjaAPI

api = NinjaAPI(title="Social Media API", version="1.0.0")


@api.get("/health", tags=["health"])
def health(request):
    """Report that the API process is responding."""
    return {"status": "ok"}
