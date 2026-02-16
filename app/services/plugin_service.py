import os
import json
from typing import List, Optional
from pathlib import Path
from ..models.plugin_models import PluginManifest, PluginSchema
from ..core.logging_config import logger

PLUGINS_ROOT = Path("/home/manuel/Documents/LamiNode/laminode_plugins")

class PluginService:
    def get_all_plugins(self) -> List[PluginManifest]:
        logger.info("Scanning for all plugins")
        plugins = []
        
        # Scan Applications
        app_dir = PLUGINS_ROOT / "applications"
        if app_dir.exists():
            for app_name in os.listdir(app_dir):
                app_path = app_dir / app_name
                if app_path.is_dir():
                    for version in os.listdir(app_path):
                        v_path = app_path / version
                        manifest_path = v_path / "manifest.json"
                        if manifest_path.exists():
                            with open(manifest_path, 'r') as f:
                                plugins.append(PluginManifest(**json.load(f)))

        # Scan Sectors
        sector_dir = PLUGINS_ROOT / "sectors"
        if sector_dir.exists():
            for sector_name in os.listdir(sector_dir):
                sector_path = sector_dir / sector_name
                if sector_path.is_dir():
                    for version in os.listdir(sector_path):
                        v_path = sector_path / version
                        manifest_path = v_path / "manifest.json"
                        if manifest_path.exists():
                            with open(manifest_path, 'r') as f:
                                plugins.append(PluginManifest(**json.load(f)))
        
        return plugins

    def get_plugin_manifest(self, plugin_id: str) -> Optional[PluginManifest]:
        logger.info(f"Fetching manifest for plugin: {plugin_id}")
        all_plugins = self.get_all_plugins()
        for p in all_plugins:
            if p.plugin.pluginID == plugin_id:
                return p
        logger.warning(f"Plugin manifest not found: {plugin_id}")
        return None

    def get_plugin_path(self, plugin_id: str) -> Optional[Path]:
        # Search Applications
        app_dir = PLUGINS_ROOT / "applications"
        for app_name in os.listdir(app_dir):
            app_path = app_dir / app_name
            for version in os.listdir(app_path):
                v_path = app_path / version
                manifest_path = v_path / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                        if data['plugin']['pluginID'] == plugin_id:
                            return v_path

        # Search Sectors
        sector_dir = PLUGINS_ROOT / "sectors"
        for sector_name in os.listdir(sector_dir):
            sector_path = sector_dir / sector_name
            for version in os.listdir(sector_path):
                v_path = sector_path / version
                manifest_path = v_path / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                        if data['plugin']['pluginID'] == plugin_id:
                            return v_path
        
        logger.warning(f"Plugin path not found for ID: {plugin_id}")
        return None

    def get_schema(self, plugin_id: str, schema_id: str) -> Optional[PluginSchema]:
        logger.info(f"Fetching schema {schema_id} for plugin {plugin_id}")
        plugin_path = self.get_plugin_path(plugin_id)
        if not plugin_path:
            return None
        
        schema_path = plugin_path / "schemas" / schema_id / "schema.json"
        if not schema_path.exists():
            logger.warning(f"Schema file not found: {schema_path}")
            return None
            
        with open(schema_path, 'r') as f:
            return PluginSchema(**json.load(f))

    def get_adapter_path(self, plugin_id: str, schema_id: Optional[str] = None) -> Optional[Path]:
        logger.info(f"Fetching adapter for plugin: {plugin_id} (schema: {schema_id})")
        plugin_path = self.get_plugin_path(plugin_id)
        if not plugin_path:
            return None
        
        # If schema_id is provided, try to find the adapter in that schema's folder first
        if schema_id:
            adapter_path = plugin_path / "schemas" / schema_id / "adapter.js"
            if adapter_path.exists():
                return adapter_path
        
        # Fallback to root adapter.js
        adapter_path = plugin_path / "adapter.js"
        if adapter_path.exists():
            return adapter_path
        
        # Last resort: search in all schemas if schema_id was not provided
        if not schema_id:
            schemas_dir = plugin_path / "schemas"
            if schemas_dir.exists():
                for sid in os.listdir(schemas_dir):
                    s_path = schemas_dir / sid / "adapter.js"
                    if s_path.exists():
                        return s_path
        
        logger.info(f"No adapter.js found for plugin: {plugin_id}")
        return None

plugin_service = PluginService()
