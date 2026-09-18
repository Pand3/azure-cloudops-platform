"""Shared pytest configuration for the Platform API."""

from collections.abc import Iterator

import pytest
from platform_api.config import get_settings


@pytest.fixture(autouse=True)
def reset_settings_cache() -> Iterator[None]:
    """Clear cached application settings before and after every test."""

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
