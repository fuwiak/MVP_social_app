"""
Brand Assets API endpoints
Digital asset management and organization
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter()

class BrandAsset(BaseModel):
    name: str
    type: str  # 'logo', 'image', 'video', 'document'
    url: str
    tags: List[str]
    description: Optional[str] = None

@router.get("/assets")
async def get_brand_assets(
    asset_type: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """Get brand assets with optional filtering"""
    
    # Mock brand assets data
    assets = [
        {
            "id": "1",
            "name": "Company Logo - Primary",
            "type": "logo",
            "url": "/assets/logo-primary.svg",
            "tags": ["logo", "primary", "svg", "brand"],
            "description": "Main company logo for all official communications",
            "file_size": "12KB",
            "dimensions": "500x200",
            "created_at": "2024-01-01T10:00:00Z",
            "last_used": "2024-01-15T14:30:00Z",
            "usage_count": 45
        },
        {
            "id": "2", 
            "name": "Hero Background",
            "type": "image",
            "url": "/assets/hero-bg.jpg",
            "tags": ["background", "hero", "website", "gradient"],
            "description": "Gradient background for website hero sections",
            "file_size": "1.2MB",
            "dimensions": "1920x1080", 
            "created_at": "2024-01-05T11:20:00Z",
            "last_used": "2024-01-14T16:45:00Z",
            "usage_count": 23
        },
        {
            "id": "3",
            "name": "Product Demo Video",
            "type": "video", 
            "url": "/assets/product-demo.mp4",
            "tags": ["demo", "product", "video", "marketing"],
            "description": "2-minute product demonstration video",
            "file_size": "45MB",
            "duration": "2:15",
            "created_at": "2024-01-10T14:00:00Z",
            "last_used": "2024-01-15T09:30:00Z",
            "usage_count": 18
        },
        {
            "id": "4",
            "name": "Brand Guidelines",
            "type": "document",
            "url": "/assets/brand-guidelines.pdf", 
            "tags": ["guidelines", "brand", "documentation", "pdf"],
            "description": "Complete brand identity and usage guidelines",
            "file_size": "2.8MB",
            "pages": 24,
            "created_at": "2024-01-02T09:15:00Z",
            "last_used": "2024-01-12T11:20:00Z",
            "usage_count": 8
        },
        {
            "id": "5",
            "name": "Social Media Icons",
            "type": "image",
            "url": "/assets/social-icons.png",
            "tags": ["social", "icons", "website", "footer"],
            "description": "Social media platform icons for website footer",
            "file_size": "45KB",
            "dimensions": "400x50",
            "created_at": "2024-01-08T16:30:00Z", 
            "last_used": "2024-01-15T12:00:00Z",
            "usage_count": 31
        }
    ]
    
    # Apply filters
    filtered_assets = assets
    
    if asset_type:
        filtered_assets = [a for a in filtered_assets if a["type"] == asset_type]
    
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        filtered_assets = [
            a for a in filtered_assets 
            if any(tag in a["tags"] for tag in tag_list)
        ]
    
    # Apply limit
    filtered_assets = filtered_assets[:limit]
    
    # Calculate stats
    total_size = sum(
        float(a["file_size"].replace("KB", "").replace("MB", "").replace("GB", "")) 
        for a in assets
    )
    
    asset_types = {}
    for asset in assets:
        asset_type = asset["type"]
        asset_types[asset_type] = asset_types.get(asset_type, 0) + 1
    
    return {
        "assets": filtered_assets,
        "total_assets": len(assets),
        "filtered_count": len(filtered_assets),
        "statistics": {
            "total_storage": f"{total_size:.1f}MB",
            "asset_types": asset_types,
            "most_used": max(assets, key=lambda x: x["usage_count"]),
            "recently_added": max(assets, key=lambda x: x["created_at"])
        },
        "filters_applied": {
            "type": asset_type,
            "tags": tags,
            "limit": limit
        }
    }

@router.post("/assets")
async def create_brand_asset(asset: BrandAsset) -> Dict[str, Any]:
    """Add new brand asset"""
    try:
        # Validate asset type
        valid_types = ["logo", "image", "video", "document", "template", "font"]
        if asset.type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid asset type. Must be one of: {valid_types}"
            )
        
        # Create new asset record
        new_asset = {
            "id": f"asset_{datetime.now().timestamp()}",
            "name": asset.name,
            "type": asset.type,
            "url": asset.url,
            "tags": asset.tags,
            "description": asset.description,
            "file_size": "Unknown",  # Would be calculated from actual file
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "status": "active"
        }
        
        # In production, save to database
        # await DatabaseService.add_brand_asset(new_asset)
        
        return {
            "message": "Brand asset created successfully",
            "asset": new_asset
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating asset: {str(e)}")

@router.post("/assets/upload")
async def upload_brand_asset(
    file: UploadFile = File(...),
    name: str = "",
    asset_type: str = "",
    tags: str = "",
    description: str = ""
) -> Dict[str, Any]:
    """Upload new brand asset file"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size (limit to 50MB for demo)
        max_size = 50 * 1024 * 1024  # 50MB
        file_size = 0
        
        # Read file content (in production, upload to cloud storage)
        content = await file.read()
        file_size = len(content)
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {max_size // (1024*1024)}MB"
            )
        
        # Determine file type if not provided
        if not asset_type:
            extension = file.filename.split(".")[-1].lower()
            type_mapping = {
                "jpg": "image", "jpeg": "image", "png": "image", "gif": "image", "svg": "image",
                "mp4": "video", "mov": "video", "avi": "video", "webm": "video",
                "pdf": "document", "doc": "document", "docx": "document", "txt": "document",
                "ttf": "font", "otf": "font", "woff": "font", "woff2": "font"
            }
            asset_type = type_mapping.get(extension, "document")
        
        # Create asset record
        new_asset = {
            "id": f"upload_{datetime.now().timestamp()}",
            "name": name or file.filename,
            "type": asset_type,
            "url": f"/uploads/{file.filename}",  # In production, use cloud storage URL
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "description": description,
            "file_size": f"{file_size / 1024:.1f}KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f}MB",
            "filename": file.filename,
            "content_type": file.content_type,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        return {
            "message": "File uploaded successfully",
            "asset": new_asset,
            "upload_info": {
                "original_filename": file.filename,
                "size": new_asset["file_size"],
                "type": asset_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/assets/{asset_id}")
async def get_brand_asset(asset_id: str) -> Dict[str, Any]:
    """Get specific brand asset details"""
    # Mock asset detail (in production, fetch from database)
    asset = {
        "id": asset_id,
        "name": "Company Logo - Primary",
        "type": "logo",
        "url": "/assets/logo-primary.svg",
        "tags": ["logo", "primary", "svg", "brand"],
        "description": "Main company logo for all official communications",
        "file_size": "12KB",
        "dimensions": "500x200",
        "created_at": "2024-01-01T10:00:00Z",
        "last_used": "2024-01-15T14:30:00Z",
        "usage_count": 45,
        "metadata": {
            "format": "SVG",
            "color_profile": "sRGB",
            "has_transparency": True,
            "vector": True
        },
        "usage_history": [
            {"date": "2024-01-15", "context": "Website header", "platform": "website"},
            {"date": "2024-01-14", "context": "Email signature", "platform": "email"},
            {"date": "2024-01-13", "context": "Social media post", "platform": "instagram"}
        ]
    }
    
    return asset

@router.put("/assets/{asset_id}")
async def update_brand_asset(asset_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update brand asset metadata"""
    try:
        # In production, update in database
        updated_asset = {
            "id": asset_id,
            "updated_at": datetime.now().isoformat(),
            "updates_applied": updates
        }
        
        return {
            "message": "Asset updated successfully",
            "asset": updated_asset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating asset: {str(e)}")

@router.delete("/assets/{asset_id}")
async def delete_brand_asset(asset_id: str) -> Dict[str, Any]:
    """Delete brand asset"""
    try:
        # In production, soft delete from database and remove from storage
        return {
            "message": f"Asset {asset_id} deleted successfully",
            "deleted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting asset: {str(e)}")

@router.get("/collections")
async def get_asset_collections() -> Dict[str, Any]:
    """Get organized asset collections"""
    collections = [
        {
            "id": "logos",
            "name": "Brand Logos",
            "description": "All logo variations and formats",
            "asset_count": 8,
            "cover_image": "/assets/logo-primary.svg",
            "created_at": "2024-01-01T10:00:00Z"
        },
        {
            "id": "social",
            "name": "Social Media Assets",
            "description": "Graphics and templates for social platforms",
            "asset_count": 15,
            "cover_image": "/assets/social-template.jpg",
            "created_at": "2024-01-05T14:30:00Z"
        },
        {
            "id": "presentations", 
            "name": "Presentation Templates",
            "description": "PowerPoint and Keynote templates",
            "asset_count": 6,
            "cover_image": "/assets/presentation-template.jpg",
            "created_at": "2024-01-08T09:20:00Z"
        }
    ]
    
    return {
        "collections": collections,
        "total_collections": len(collections),
        "total_assets_in_collections": sum(c["asset_count"] for c in collections)
    }

@router.get("/usage-analytics")
async def get_usage_analytics(days: int = 30) -> Dict[str, Any]:
    """Get brand asset usage analytics"""
    return {
        "period": f"Last {days} days",
        "overview": {
            "total_downloads": 234,
            "total_views": 1456,
            "active_assets": 18,
            "most_popular_format": "PNG"
        },
        "top_assets": [
            {"name": "Company Logo", "downloads": 45, "views": 234},
            {"name": "Social Media Template", "downloads": 32, "views": 187},
            {"name": "Email Header", "downloads": 28, "views": 156}
        ],
        "format_usage": {
            "PNG": 35,
            "SVG": 28,
            "JPG": 22,
            "PDF": 15
        },
        "daily_usage": [
            {"date": "2024-01-15", "downloads": 12, "views": 67},
            {"date": "2024-01-14", "downloads": 8, "views": 45},
            {"date": "2024-01-13", "downloads": 15, "views": 89}
        ]
    }



