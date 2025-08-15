"""
Social Media API endpoints
Content creation, scheduling, and analytics
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from app.core.database import DatabaseService
from app.services.ai_service import AIService

router = APIRouter()

# Pydantic models for request/response
class SocialMediaPost(BaseModel):
    platform: str
    content: str
    media_url: Optional[str] = None
    scheduled_time: str
    hashtags: Optional[List[str]] = []

class ContentGenerationRequest(BaseModel):
    prompt: str
    platform: str
    tone: str = "professional"
    include_hashtags: bool = True

class PostEngagementUpdate(BaseModel):
    likes: int
    comments: int
    shares: int
    reach: int

@router.get("/posts")
async def get_social_media_posts(
    platform: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """Get social media posts with optional filtering"""
    try:
        posts = await DatabaseService.get_social_media_posts(limit)
        
        # Apply filters
        if platform:
            posts = [p for p in posts if p.get('platform') == platform]
        
        if status:
            posts = [p for p in posts if p.get('status') == status]
        
        # Calculate analytics
        total_reach = sum(
            post.get('engagement', {}).get('reach', 0) 
            for post in posts 
            if post.get('status') == 'posted'
        )
        
        total_engagement = sum(
            post.get('engagement', {}).get('likes', 0) + 
            post.get('engagement', {}).get('comments', 0) + 
            post.get('engagement', {}).get('shares', 0)
            for post in posts 
            if post.get('status') == 'posted'
        )
        
        avg_engagement = total_engagement / max(len([p for p in posts if p.get('status') == 'posted']), 1)
        
        return {
            "posts": posts,
            "analytics": {
                "total_posts": len(posts),
                "total_reach": total_reach,
                "total_engagement": total_engagement,
                "avg_engagement": round(avg_engagement, 1),
                "posted": len([p for p in posts if p.get('status') == 'posted']),
                "scheduled": len([p for p in posts if p.get('status') == 'scheduled']),
                "draft": len([p for p in posts if p.get('status') == 'draft'])
            },
            "filters_applied": {
                "platform": platform,
                "status": status,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching posts: {str(e)}")

@router.post("/posts")
async def create_social_media_post(post: SocialMediaPost) -> Dict[str, Any]:
    """Create and schedule a new social media post"""
    try:
        # Validate platform
        valid_platforms = ['instagram', 'linkedin', 'twitter', 'facebook']
        if post.platform not in valid_platforms:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid platform. Must be one of: {valid_platforms}"
            )
        
        # Validate scheduled time
        try:
            scheduled_datetime = datetime.fromisoformat(post.scheduled_time.replace('Z', '+00:00'))
            if scheduled_datetime <= datetime.now():
                raise HTTPException(
                    status_code=400,
                    detail="Scheduled time must be in the future"
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            )
        
        # Create post data
        post_data = {
            "platform": post.platform,
            "content": post.content,
            "media_url": post.media_url,
            "scheduled_time": post.scheduled_time,
            "status": "scheduled",
            "engagement": {
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "reach": 0
            }
        }
        
        # Save to database
        created_post = await DatabaseService.schedule_social_media_post(post_data)
        
        return {
            "message": "Post scheduled successfully",
            "post": created_post,
            "scheduled_time": post.scheduled_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")

@router.post("/generate-content")
async def generate_ai_content(request: ContentGenerationRequest) -> Dict[str, Any]:
    """Generate AI-powered social media content"""
    try:
        # Validate platform
        valid_platforms = ['instagram', 'linkedin', 'twitter', 'facebook']
        if request.platform not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {valid_platforms}"
            )
        
        # Generate content using AI service
        generated_content = await AIService.generate_social_media_content(
            prompt=request.prompt,
            platform=request.platform,
            tone=request.tone,
            include_hashtags=request.include_hashtags
        )
        
        return {
            "generated_content": generated_content,
            "usage_info": {
                "prompt": request.prompt,
                "platform": request.platform,
                "tone": request.tone,
                "include_hashtags": request.include_hashtags
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@router.get("/optimal-times/{platform}")
async def get_optimal_posting_times(platform: str) -> Dict[str, Any]:
    """Get AI-recommended optimal posting times for a platform"""
    try:
        # Mock audience data (in production, fetch from analytics APIs)
        audience_data = {
            "size": 12500,
            "timezone": "UTC",
            "age_group": "25-45",
            "active_hours": ["08:00-10:00", "12:00-14:00", "18:00-21:00"]
        }
        
        # Get historical performance data
        posts = await DatabaseService.get_social_media_posts(100)
        platform_posts = [p for p in posts if p.get('platform') == platform and p.get('status') == 'posted']
        
        historical_performance = [
            {
                "posted_time": post.get('posted_time', post.get('scheduled_time')),
                "engagement": (
                    post.get('engagement', {}).get('likes', 0) + 
                    post.get('engagement', {}).get('comments', 0) + 
                    post.get('engagement', {}).get('shares', 0)
                )
            }
            for post in platform_posts
        ]
        
        # Get AI analysis
        analysis = await AIService.analyze_optimal_posting_times(
            platform=platform,
            audience_data=audience_data,
            historical_performance=historical_performance
        )
        
        return {
            "platform": platform,
            "optimal_times": analysis,
            "audience_insights": audience_data,
            "analysis_based_on": {
                "historical_posts": len(historical_performance),
                "audience_size": audience_data["size"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing optimal times: {str(e)}")

@router.put("/posts/{post_id}/engagement")
async def update_post_engagement(post_id: str, engagement: PostEngagementUpdate) -> Dict[str, Any]:
    """Update engagement metrics for a post"""
    try:
        engagement_data = {
            "likes": engagement.likes,
            "comments": engagement.comments,
            "shares": engagement.shares,
            "reach": engagement.reach
        }
        
        updated_post = await DatabaseService.update_post_engagement(post_id, engagement_data)
        
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {
            "message": "Engagement updated successfully",
            "post_id": post_id,
            "updated_engagement": engagement_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating engagement: {str(e)}")

@router.get("/analytics/engagement")
async def get_engagement_analytics(days: int = 30) -> Dict[str, Any]:
    """Get comprehensive engagement analytics"""
    try:
        # Get posts from specified period
        posts = await DatabaseService.get_social_media_posts(200)
        
        # Filter by date range
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_posts = [
            p for p in posts 
            if p.get('status') == 'posted' and 
            datetime.fromisoformat(p.get('created_at', '').replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Calculate platform-wise analytics
        platform_analytics = {}
        
        for platform in ['instagram', 'linkedin', 'twitter', 'facebook']:
            platform_posts = [p for p in recent_posts if p.get('platform') == platform]
            
            if platform_posts:
                total_likes = sum(p.get('engagement', {}).get('likes', 0) for p in platform_posts)
                total_comments = sum(p.get('engagement', {}).get('comments', 0) for p in platform_posts)
                total_shares = sum(p.get('engagement', {}).get('shares', 0) for p in platform_posts)
                total_reach = sum(p.get('engagement', {}).get('reach', 0) for p in platform_posts)
                
                platform_analytics[platform] = {
                    "posts_count": len(platform_posts),
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "total_shares": total_shares,
                    "total_reach": total_reach,
                    "avg_engagement": round(
                        (total_likes + total_comments + total_shares) / len(platform_posts), 1
                    ),
                    "engagement_rate": round(
                        (total_likes + total_comments + total_shares) / max(total_reach, 1) * 100, 2
                    )
                }
        
        # Overall analytics
        total_posts = len(recent_posts)
        total_engagement = sum(
            p.get('engagement', {}).get('likes', 0) + 
            p.get('engagement', {}).get('comments', 0) + 
            p.get('engagement', {}).get('shares', 0)
            for p in recent_posts
        )
        total_reach = sum(p.get('engagement', {}).get('reach', 0) for p in recent_posts)
        
        return {
            "period": f"Last {days} days",
            "overall": {
                "total_posts": total_posts,
                "total_engagement": total_engagement,
                "total_reach": total_reach,
                "avg_engagement_per_post": round(total_engagement / max(total_posts, 1), 1),
                "overall_engagement_rate": round(total_engagement / max(total_reach, 1) * 100, 2)
            },
            "by_platform": platform_analytics,
            "top_performing_posts": sorted(
                recent_posts,
                key=lambda p: (
                    p.get('engagement', {}).get('likes', 0) + 
                    p.get('engagement', {}).get('comments', 0) + 
                    p.get('engagement', {}).get('shares', 0)
                ),
                reverse=True
            )[:5]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")

@router.post("/bulk-schedule")
async def bulk_schedule_posts(posts: List[SocialMediaPost]) -> Dict[str, Any]:
    """Schedule multiple posts at once"""
    try:
        if len(posts) > 50:
            raise HTTPException(
                status_code=400,
                detail="Cannot schedule more than 50 posts at once"
            )
        
        scheduled_posts = []
        errors = []
        
        for i, post in enumerate(posts):
            try:
                # Validate each post
                valid_platforms = ['instagram', 'linkedin', 'twitter', 'facebook']
                if post.platform not in valid_platforms:
                    errors.append(f"Post {i+1}: Invalid platform '{post.platform}'")
                    continue
                
                # Create post data
                post_data = {
                    "platform": post.platform,
                    "content": post.content,
                    "media_url": post.media_url,
                    "scheduled_time": post.scheduled_time,
                    "status": "scheduled",
                    "engagement": {
                        "likes": 0,
                        "comments": 0,
                        "shares": 0,
                        "reach": 0
                    }
                }
                
                # Save to database
                created_post = await DatabaseService.schedule_social_media_post(post_data)
                scheduled_posts.append(created_post)
                
            except Exception as e:
                errors.append(f"Post {i+1}: {str(e)}")
        
        return {
            "message": f"Bulk scheduling completed. {len(scheduled_posts)} posts scheduled.",
            "scheduled_posts": len(scheduled_posts),
            "total_posts": len(posts),
            "errors": errors,
            "posts": scheduled_posts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in bulk scheduling: {str(e)}")

@router.get("/content-suggestions")
async def get_content_suggestions(
    platform: str,
    industry: str = "technology",
    tone: str = "professional"
) -> Dict[str, Any]:
    """Get AI-generated content suggestions"""
    try:
        # Generate multiple content suggestions
        suggestions = []
        
        prompts = [
            f"Create engaging {industry} content about business growth and innovation",
            f"Write about the latest trends in {industry} and their business impact",
            f"Share a tip for {industry} professionals to improve their workflow",
            f"Discuss the future of {industry} and emerging opportunities",
            f"Create motivational content for {industry} entrepreneurs"
        ]
        
        # Generate content for each prompt
        for prompt in prompts:
            try:
                content = await AIService.generate_social_media_content(
                    prompt=prompt,
                    platform=platform,
                    tone=tone,
                    include_hashtags=True
                )
                suggestions.append(content)
            except Exception as e:
                print(f"Error generating suggestion: {e}")
                continue
        
        return {
            "platform": platform,
            "industry": industry,
            "tone": tone,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")



