"""
Database connection and operations using Supabase
"""

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime, timezone
from app.core.config import settings
import json

# Global Supabase client
supabase: Optional[Client] = None

async def init_db():
    """Initialize Supabase connection"""
    global supabase
    
    # Skip Supabase initialization if no valid URL provided (development mode)
    if not settings.SUPABASE_URL or settings.SUPABASE_URL == "your_supabase_url":
        print("⚠️  Running in development mode without Supabase")
        return
    
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        print("✅ Supabase client initialized")
    except Exception as e:
        print(f"⚠️  Failed to initialize Supabase: {e}")
        print("⚠️  Running without database connection")

def get_supabase() -> Optional[Client]:
    """Get Supabase client instance"""
    return supabase

class DatabaseService:
    """Database service for all business operations"""
    
    @staticmethod
    async def get_business_metrics(days: int = 30) -> List[Dict[str, Any]]:
        """Get business metrics for the last N days"""
        db = get_supabase()
        
        if db is None:
            # Return mock data when no database connection
            return [
                {
                    "id": "1",
                    "date": datetime.now().isoformat(),
                    "revenue": 45420,
                    "expenses": 33080,
                    "profit": 12340,
                    "roi": 2.8,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "2",
                    "date": (datetime.now() - timedelta(days=1)).isoformat(),
                    "revenue": 42350,
                    "expenses": 31200,
                    "profit": 11150,
                    "roi": 2.6,
                    "created_at": (datetime.now() - timedelta(days=1)).isoformat()
                }
            ]
        
        try:
            # Calculate date threshold
            from datetime import datetime, timedelta
            date_threshold = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = db.table('business_metrics').select('*').gte('date', date_threshold).order('date', desc=True).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching business metrics: {e}")
            # Return mock data for demo
            return [
                {
                    "id": "1",
                    "date": datetime.now().isoformat(),
                    "revenue": 45420,
                    "expenses": 33080,
                    "profit": 12340,
                    "roi": 2.8,
                    "created_at": datetime.now().isoformat()
                }
            ]
    
    @staticmethod
    async def add_business_metric(metric: Dict[str, Any]) -> Dict[str, Any]:
        """Add new business metric"""
        try:
            db = get_supabase()
            metric['created_at'] = datetime.now(timezone.utc).isoformat()
            
            response = db.table('business_metrics').insert(metric).execute()
            return response.data[0] if response.data else metric
        except Exception as e:
            print(f"Error adding business metric: {e}")
            return metric
    
    @staticmethod
    async def get_social_media_posts(limit: int = 50) -> List[Dict[str, Any]]:
        """Get social media posts"""
        try:
            db = get_supabase()
            response = db.table('social_media_posts').select('*').order('created_at', desc=True).limit(limit).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching social media posts: {e}")
            # Return mock data
            return [
                {
                    "id": "1",
                    "platform": "instagram",
                    "content": "Just launched our new AI-powered business analytics dashboard! 🚀",
                    "media_url": None,
                    "scheduled_time": datetime.now().isoformat(),
                    "posted_time": datetime.now().isoformat(),
                    "status": "posted",
                    "engagement": {
                        "likes": 245,
                        "shares": 18,
                        "comments": 32,
                        "reach": 3420
                    },
                    "created_at": datetime.now().isoformat()
                }
            ]
    
    @staticmethod
    async def schedule_social_media_post(post: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a new social media post"""
        try:
            db = get_supabase()
            post['created_at'] = datetime.now(timezone.utc).isoformat()
            post['status'] = 'scheduled'
            
            # Ensure engagement is properly formatted
            if 'engagement' not in post:
                post['engagement'] = {"likes": 0, "shares": 0, "comments": 0, "reach": 0}
            
            response = db.table('social_media_posts').insert(post).execute()
            return response.data[0] if response.data else post
        except Exception as e:
            print(f"Error scheduling social media post: {e}")
            return post
    
    @staticmethod
    async def update_post_engagement(post_id: str, engagement: Dict[str, int]) -> Dict[str, Any]:
        """Update post engagement metrics"""
        try:
            db = get_supabase()
            response = db.table('social_media_posts').update({
                'engagement': engagement
            }).eq('id', post_id).execute()
            
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error updating post engagement: {e}")
            return {}
    
    @staticmethod
    async def get_ad_campaigns() -> List[Dict[str, Any]]:
        """Get all ad campaigns"""
        try:
            db = get_supabase()
            response = db.table('ad_campaigns').select('*').order('created_at', desc=True).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching ad campaigns: {e}")
            # Return mock data
            return [
                {
                    "id": "1",
                    "name": "AI Business Tool Launch",
                    "platform": "facebook",
                    "budget": 1000,
                    "spent": 750,
                    "clicks": 1250,
                    "impressions": 45000,
                    "conversions": 78,
                    "ctr": 2.8,
                    "cpc": 0.60,
                    "roas": 3.2,
                    "status": "active",
                    "created_at": datetime.now().isoformat()
                }
            ]
    
    @staticmethod
    async def create_ad_campaign(campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Create new ad campaign"""
        try:
            db = get_supabase()
            campaign['created_at'] = datetime.now(timezone.utc).isoformat()
            
            response = db.table('ad_campaigns').insert(campaign).execute()
            return response.data[0] if response.data else campaign
        except Exception as e:
            print(f"Error creating ad campaign: {e}")
            return campaign
    
    @staticmethod
    async def get_brand_assets() -> List[Dict[str, Any]]:
        """Get all brand assets"""
        try:
            db = get_supabase()
            response = db.table('brand_assets').select('*').order('created_at', desc=True).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching brand assets: {e}")
            return []
    
    @staticmethod
    async def add_brand_asset(asset: Dict[str, Any]) -> Dict[str, Any]:
        """Add new brand asset"""
        try:
            db = get_supabase()
            asset['created_at'] = datetime.now(timezone.utc).isoformat()
            
            response = db.table('brand_assets').insert(asset).execute()
            return response.data[0] if response.data else asset
        except Exception as e:
            print(f"Error adding brand asset: {e}")
            return asset
    
    @staticmethod
    async def get_cash_flow(days: int = 30) -> List[Dict[str, Any]]:
        """Get cash flow entries"""
        try:
            db = get_supabase()
            
            from datetime import datetime, timedelta
            date_threshold = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = db.table('cash_flow').select('*').gte('date', date_threshold).order('date', desc=True).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching cash flow: {e}")
            return []
    
    @staticmethod
    async def add_cash_flow_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
        """Add cash flow entry"""
        try:
            db = get_supabase()
            entry['created_at'] = datetime.now(timezone.utc).isoformat()
            
            response = db.table('cash_flow').insert(entry).execute()
            return response.data[0] if response.data else entry
        except Exception as e:
            print(f"Error adding cash flow entry: {e}")
            return entry
    
    @staticmethod
    async def get_ai_insights(insight_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get AI insights"""
        try:
            db = get_supabase()
            query = db.table('ai_insights').select('*').order('created_at', desc=True).limit(limit)
            
            if insight_type:
                query = query.eq('type', insight_type)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching AI insights: {e}")
            return []
    
    @staticmethod
    async def save_ai_insight(insight: Dict[str, Any]) -> Dict[str, Any]:
        """Save AI insight"""
        try:
            db = get_supabase()
            insight['created_at'] = datetime.now(timezone.utc).isoformat()
            
            response = db.table('ai_insights').insert(insight).execute()
            return response.data[0] if response.data else insight
        except Exception as e:
            print(f"Error saving AI insight: {e}")
            return insight



