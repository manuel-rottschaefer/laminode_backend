from datetime import datetime, timezone
from typing import List, Optional
from ..models.release_models import LamiNodeRelease
from ..core.logging_config import logger

class ReleaseService:
    def __init__(self):
        # Mock data for demonstration, in a real app this might come from a DB or GitHub API
        self._mock_releases = [
            LamiNodeRelease(
                version="0.1.0",
                obtain_url="https://example.com/laminode/download/v0.1.0",
                changelog=[
                    "Initial Alpha Release",
                    "Basic graph editor",
                    "Plugin system support"
                ],
                published_at=datetime(2025, 12, 1, tzinfo=timezone.utc),
                is_mandatory=False
            ),
            LamiNodeRelease(
                version="0.1.1",
                obtain_url="https://example.com/laminode/download/v0.1.1",
                changelog=[
                    "Fixed crash on startup",
                    "Improved plugin discovery"
                ],
                published_at=datetime(2025, 12, 15, tzinfo=timezone.utc),
                is_mandatory=False
            ),
            LamiNodeRelease(
                version="0.2.0",
                obtain_url="https://example.com/laminode/download/v0.2.0",
                changelog=[
                    "New Plugin System Architecture",
                    "Base (Sector) Schema support",
                    "Improved selective fetching API"
                ],
                published_at=datetime(2026, 1, 19, tzinfo=timezone.utc),
                is_mandatory=True
            )
        ]

    def list_releases(self) -> List[LamiNodeRelease]:
        logger.info("Listing all releases")
        return sorted(self._mock_releases, key=lambda x: x.published_at, reverse=True)

    def get_latest_release(self) -> LamiNodeRelease:
        latest = self.list_releases()[0]
        logger.info(f"Latest release: {latest.version}")
        return latest

    def check_for_update(self, current_version: str) -> Optional[LamiNodeRelease]:
        latest = self.get_latest_release()
        if latest.version != current_version:
            logger.info(f"Update available: {current_version} -> {latest.version}")
            return latest
        return None

release_service = ReleaseService()
