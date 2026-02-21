from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from enum import Enum

class QuantityType(str, Enum):
    NUMERIC = "numeric"
    CHOICE = "choice"
    BOOLEAN = "boolean"
    STRING = "string"
    PERCENTAGE = "percentage"
    RELATIVE = "relative"
    CUSTOM = "custom"

class QuantityDefinition(BaseModel):
    id: str
    type: QuantityType
    title: Optional[str] = None
    unit: Optional[str] = None
    symbol: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    default: Optional[Any] = None
    fallback: Optional[Any] = None

    @model_validator(mode='after')
    def validate_quantity(self) -> 'QuantityDefinition':
        if self.type in [QuantityType.PERCENTAGE, QuantityType.RELATIVE]:
            if not self.meta or not self.meta.get("requiresReference"):
                 raise ValueError(f"Quantity {self.id} of type '{self.type}' MUST have meta.requiresReference = True")
        
        return self

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

class CamExpressionRelation(BaseModel):
    target: str
    expression: str

class CamParameter(BaseModel):
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    baseParam: Optional[str] = None
    category: Optional[str] = None
    
    ancestors: List[str] = []
    
    defaultValue: Optional[CamExpressionRelation] = None
    minThreshold: Optional[CamExpressionRelation] = None
    maxThreshold: Optional[CamExpressionRelation] = None
    enabledCondition: Optional[CamExpressionRelation] = None

    quantityIds: List[str]
    options: Optional[Dict[str, str]] = None

class CamCategory(BaseModel):
    name: str
    title: str
    color: str
    parent: Optional[str] = None
    role: str = "buildJob"

class PluginSchema(BaseModel):
    manifest: SchemaManifest
    quantities: Dict[str, QuantityDefinition]
    categories: Optional[List[CamCategory]] = None
    availableParameters: List[CamParameter]

    @field_validator("quantities")
    @classmethod
    def quantities_not_empty(cls, v: Dict[str, QuantityDefinition]) -> Dict[str, QuantityDefinition]:
        if not v:
            raise ValueError("quantities mapping MUST be present and non-empty")
        return v
