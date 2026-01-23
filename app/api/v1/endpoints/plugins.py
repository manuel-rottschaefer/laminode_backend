from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from ....services.plugin_service import plugin_service
from ....models.plugin_models import PluginManifest, PluginSchema
from ....core.logging_config import logger

router = APIRouter()

@router.get("/discover", response_model=List[PluginManifest])
async def discover_plugins():
    """
    Returns a list of all available plugins (Applications and Sectors).
    """
    logger.info("Client requested plugin discovery")
    return plugin_service.get_all_plugins()

@router.get("/{plugin_id}/manifest", response_model=PluginManifest)
async def get_plugin_manifest(plugin_id: str):
    """
    Returns the manifest for a specific plugin.
    """
    manifest = plugin_service.get_plugin_manifest(plugin_id)
    if not manifest:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return manifest

@router.get("/{plugin_id}/schemas/{schema_id}", response_model=PluginSchema)
async def get_plugin_schema(plugin_id: str, schema_id: str):
    """
    Returns a specific schema for a plugin.
    """
    schema = plugin_service.get_schema(plugin_id, schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema

@router.get("/{plugin_id}/adapter", response_class=FileResponse)
async def get_plugin_adapter(plugin_id: str):
    """
    Returns the adapter.js file for a specific plugin.
    """
    adapter_path = plugin_service.get_adapter_path(plugin_id)
    if not adapter_path:
        raise HTTPException(status_code=404, detail="Adapter file not found")
    
    return FileResponse(
        path=adapter_path,
        filename="adapter.js",
        media_type='application/javascript'
    )
