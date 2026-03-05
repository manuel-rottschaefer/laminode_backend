import os
import json
from typing import List, Optional
from pathlib import Path
from ..models.plugin_models import PluginManifest, PluginSchema, CamExpressionRelation
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
                            try:
                                with open(manifest_path, 'r') as f:
                                    data = json.load(f)

                                # Ensure each schema entry has a 'name' field so clients
                                # (e.g. Flutter) don't receive null for required fields.
                                for s in data.get('schemas', []):
                                    if not s.get('name'):
                                        schema_file = v_path / 'schemas' / s.get('id', '') / 'schema.json'
                                        if schema_file.exists():
                                            try:
                                                with open(schema_file, 'r') as sf:
                                                    sdata = json.load(sf)
                                                    s['name'] = sdata.get('name') or s.get('version') or 'Untitled Schema'
                                            except Exception:
                                                s['name'] = s.get('version') or 'Untitled Schema'
                                        else:
                                            s['name'] = s.get('version') or 'Untitled Schema'

                                plugins.append(PluginManifest(**data))
                            except Exception as e:
                                logger.error(f"Error parsing manifest in {v_path}: {e}")

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
                            try:
                                with open(manifest_path, 'r') as f:
                                    data = json.load(f)

                                # Enrich schema entries with a 'name' field when missing
                                for s in data.get('schemas', []):
                                    if not s.get('name'):
                                        schema_file = v_path / 'schemas' / s.get('id', '') / 'schema.json'
                                        if schema_file.exists():
                                            try:
                                                with open(schema_file, 'r') as sf:
                                                    sdata = json.load(sf)
                                                    s['name'] = sdata.get('name') or s.get('version') or 'Untitled Schema'
                                            except Exception:
                                                s['name'] = s.get('version') or 'Untitled Schema'
                                        else:
                                            s['name'] = s.get('version') or 'Untitled Schema'

                                plugins.append(PluginManifest(**data))
                            except Exception as e:
                                logger.error(f"Error parsing manifest in {v_path}: {e}")
        
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
        
        # Try both 'schema.json' and 'generated_schema.json'
        base_path = plugin_path / "schemas" / schema_id
        schema_path = base_path / "schema.json"
        
        if not schema_path.exists():
            schema_path = base_path / "generated_schema.json"
            
        if not schema_path.exists():
            logger.warning(f"Schema file not found in {base_path}")
            return None
            
        try:
            with open(schema_path, 'r') as f:
                data = json.load(f)
                schema = PluginSchema(**data)

                # Normalize defaults for choice-type parameters: ensure evaluated
                # default is one of the option keys; otherwise fall back to first key.
                def _coerce_choice_defaults(s: PluginSchema) -> None:
                    for p in s.availableParameters:
                        if not p.options:
                            continue
                        if 'choice' not in p.quantityIds:
                            continue

                        # Do NOT modify or sanitize the original expression here —
                        # leave evaluation to the engine. Only provide a fallback
                        # default when no defaultValue is present at all.
                        if not p.defaultValue:
                            try:
                                first_key = next(iter(p.options.keys()))
                                p.defaultValue = CamExpressionRelation(target=p.name, expression=first_key)
                            except Exception:
                                # If options is empty or unexpected, skip
                                pass

                _coerce_choice_defaults(schema)
                return schema
        except Exception as e:
            logger.error(f"Error parsing schema {schema_id} for {plugin_id}: {str(e)}")
            return None

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
