from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class ApplicationInfo(BaseModel):
    appName: str
    appVersion: str
    vendor: str
    website: str
    sector: str

class TargetAppVersionRange(BaseModel):
    minVersion: str
    maxVersion: str

class FileTypes(BaseModel):
    profileImportBucket: str
    gcodeExportBucket: str

class PluginInfo(BaseModel):
    pluginID: str
    pluginVersion: str
    pluginAuthor: str
    publishedDate: str
    targetAppVersionRange: Optional[TargetAppVersionRange] = None
    sector: str
    fileTypes: Optional[FileTypes] = None

class SchemaRef(BaseModel):
    id: str
    version: str
    releaseDate: str

class PluginManifest(BaseModel):
    pluginType: str  # 'application' or 'sector'
    displayName: str
    description: str
    application: Optional[ApplicationInfo] = None
    plugin: PluginInfo
    schemas: List[SchemaRef]

class SchemaManifest(BaseModel):
    schemaType: str
    schemaVersion: str
    schemaAuthors: List[str]
    lastUpdated: str
    targetAppName: Optional[str] = None
    targetAppSector: Optional[str] = None

class ParameterQuantity(BaseModel):
    type: str
    unit: Optional[str] = None
    symbol: Optional[str] = None
    # options is now a mapping of identifier->display title
    options: Optional[Dict[str, str]] = None

class CamExpressionRelation(BaseModel):
    target: str
    expression: str

class CamParameter(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    baseParam: Optional[str] = None
    category: Optional[str] = None
    
    ancestors: List[str] = []
    
    defaultValue: Optional[CamExpressionRelation] = None
    minThreshold: Optional[CamExpressionRelation] = None
    maxThreshold: Optional[CamExpressionRelation] = None
    enabledCondition: Optional[CamExpressionRelation] = None

    quantity: ParameterQuantity

class CamCategory(BaseModel):
    name: str
    title: str
    color: str
    role: str = "buildJob"

class PluginSchema(BaseModel):
    manifest: SchemaManifest
    categories: Optional[List[CamCategory]] = None
    availableParameters: List[CamParameter]
