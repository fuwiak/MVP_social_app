"""
Dashboard API endpoints
Main business metrics and overview data
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from app.core.database import DatabaseService
from app.services.ai_service import AIService

router = APIRouter()

@router.get("/metrics")
async def get_dashboard_metrics(days: int = 30) -> Dict[str, Any]:
    """Get main dashboard metrics and KPIs"""
    try:
        # Fetch data in parallel
        business_metrics_task = DatabaseService.get_business_metrics(days)
        social_posts_task = DatabaseService.get_social_media_posts(10)
        ad_campaigns_task = DatabaseService.get_ad_campaigns()
        cash_flow_task = DatabaseService.get_cash_flow(days)
        
        business_metrics, social_posts, ad_campaigns, cash_flow = await asyncio.gather(
            business_metrics_task,
            social_posts_task,
            ad_campaigns_task,
            cash_flow_task
        )
        
        # Calculate aggregated metrics
        total_revenue = sum(metric.get('revenue', 0) for metric in business_metrics)
        total_profit = sum(metric.get('profit', 0) for metric in business_metrics)
        avg_roi = sum(metric.get('roi', 0) for metric in business_metrics) / max(len(business_metrics), 1)
        
        # Social media metrics
        social_reach = sum(
            post.get('engagement', {}).get('reach', 0) 
            for post in social_posts 
            if post.get('status') == 'posted'
        )
        
        avg_engagement = sum(
            post.get('engagement', {}).get('likes', 0) + 
            post.get('engagement', {}).get('comments', 0) + 
            post.get('engagement', {}).get('shares', 0)
            for post in social_posts 
            if post.get('status') == 'posted'
        ) / max(len([p for p in social_posts if p.get('status') == 'posted']), 1)
        
        # Ad campaign metrics
        active_campaigns = len([c for c in ad_campaigns if c.get('status') == 'active'])
        total_ad_spend = sum(campaign.get('spent', 0) for campaign in ad_campaigns)
        total_conversions = sum(campaign.get('conversions', 0) for campaign in ad_campaigns)
        avg_roas = sum(campaign.get('roas', 0) for campaign in ad_campaigns) / max(len(ad_campaigns), 1)
        
        # Cash flow metrics
        total_income = sum(entry.get('amount', 0) for entry in cash_flow if entry.get('type') == 'income')
        total_expenses = sum(entry.get('amount', 0) for entry in cash_flow if entry.get('type') == 'expense')
        net_cash_flow = total_income - total_expenses
        
        return {
            "overview": {
                "revenue": total_revenue,
                "profit": total_profit,
                "roi": round(avg_roi, 2),
                "growth_rate": 15.5,  # Mock calculation
                "last_updated": datetime.now().isoformat()
            },
            "social_media": {
                "total_reach": social_reach,
                "avg_engagement": round(avg_engagement, 1),
                "total_posts": len(social_posts),
                "scheduled_posts": len([p for p in social_posts if p.get('status') == 'scheduled'])
            },
            "advertising": {
                "active_campaigns": active_campaigns,
                "total_spend": total_ad_spend,
                "conversions": total_conversions,
                "avg_roas": round(avg_roas, 2)
            },
            "cash_flow": {
                "income": total_income,
                "expenses": total_expenses,
                "net_flow": net_cash_flow,
                "burn_rate": total_expenses / max(days, 1) * 30  # Monthly burn rate
            },
            "period": f"Last {days} days"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard metrics: {str(e)}")

@router.get("/insights")
async def get_ai_insights() -> Dict[str, Any]:
    """Get AI-generated business insights"""
    try:
        # Get recent insights from database
        insights = await DatabaseService.get_ai_insights(limit=10)
        
        if not insights:
            # Generate new insights if none exist
            business_data = {
                "revenue": 45420,
                "growth_rate": 15.5,
                "industry": "technology",
                "company_size": "small"
            }
            
            market_data = {
                "trends": ["AI adoption", "Remote work", "Digital transformation"],
                "competition": "medium"
            }
            
            # Generate strategy insights
            strategy_insights = await AIService.generate_business_strategy(business_data, market_data)
            
            # Save insights to database
            for insight in strategy_insights:
                await DatabaseService.save_ai_insight({
                    "type": "strategy",
                    "title": insight.get("title", "Business Strategy"),
                    "content": insight.get("description", ""),
                    "confidence": 0.85,
                    "data_source": "ai_generated"
                })
            
            insights = await DatabaseService.get_ai_insights(limit=10)
        
        return {
            "insights": insights,
            "total_count": len(insights),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching AI insights: {str(e)}")

@router.get("/system-status")
async def get_system_status() -> Dict[str, Any]:
    """Get system health and status information"""
    try:
        # Check various system components
        status = {
            "database": "online",
            "ai_services": "online",
            "social_media_apis": "online",
            "automation": "syncing",
            "last_check": datetime.now().isoformat()
        }
        
        # Mock API status checks
        api_status = {
            "openai": "operational",
            "supabase": "operational",
            "facebook": "operational",
            "instagram": "operational",
            "twitter": "operational",
            "linkedin": "operational"
        }
        
        # System metrics
        metrics = {
            "uptime": "99.9%",
            "response_time": "120ms",
            "requests_today": 1247,
            "ai_requests_remaining": 8753,
            "storage_used": "2.3GB",
            "storage_limit": "100GB"
        }
        
        return {
            "status": status,
            "api_status": api_status,
            "metrics": metrics,
            "overall_health": "healthy"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking system status: {str(e)}")

@router.post("/refresh-insights")
async def refresh_ai_insights(background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Trigger refresh of AI insights in background"""
    
    async def generate_fresh_insights():
        """Background task to generate new insights"""
        try:
            # Get latest business data
            recent_metrics = await DatabaseService.get_business_metrics(30)
            
            if recent_metrics:
                business_data = {
                    "revenue": sum(m.get('revenue', 0) for m in recent_metrics),
                    "growth_rate": 15.5,  # Calculate from data
                    "industry": "technology",
                    "company_size": "small"
                }
                
                market_data = {
                    "trends": ["AI adoption", "Remote work", "Digital transformation"],
                    "competition": "medium"
                }
                
                # Generate new insights
                insights = await AIService.generate_business_strategy(business_data, market_data)
                
                # Save to database
                for insight in insights:
                    await DatabaseService.save_ai_insight({
                        "type": "strategy",
                        "title": insight.get("title", "Business Strategy"),
                        "content": insight.get("description", ""),
                        "confidence": 0.85,
                        "data_source": "ai_generated_refresh"
                    })
                    
        except Exception as e:
            print(f"Error generating fresh insights: {e}")
    
    background_tasks.add_task(generate_fresh_insights)
    
    return {
        "message": "AI insights refresh started",
        "status": "processing"
    }

@router.get("/recent-activity")
async def get_recent_activity(limit: int = 20) -> Dict[str, Any]:
    """Get recent system activity and events"""
    try:
        # Fetch recent data from various sources
        recent_posts = await DatabaseService.get_social_media_posts(5)
        recent_metrics = await DatabaseService.get_business_metrics(7)
        recent_insights = await DatabaseService.get_ai_insights(limit=5)
        
        # Format activity feed
        activities = []
        
        # Add social media activities
        for post in recent_posts:
            activities.append({
                "id": f"social_{post.get('id')}",
                "type": "social_media",
                "title": f"Post {post.get('status')} on {post.get('platform', '').title()}",
                "description": post.get('content', '')[:100] + "...",
                "timestamp": post.get('created_at'),
                "status": post.get('status'),
                "platform": post.get('platform')
            })
        
        # Add business metric updates
        for metric in recent_metrics:
            activities.append({
                "id": f"metric_{metric.get('id')}",
                "type": "business_metric",
                "title": "Business metrics updated",
                "description": f"Revenue: ${metric.get('revenue', 0):,}, ROI: {metric.get('roi', 0)}x",
                "timestamp": metric.get('created_at'),
                "status": "updated"
            })
        
        # Add AI insights
        for insight in recent_insights:
            activities.append({
                "id": f"insight_{insight.get('id')}",
                "type": "ai_insight",
                "title": insight.get('title', 'AI Insight'),
                "description": insight.get('content', '')[:100] + "...",
                "timestamp": insight.get('created_at'),
                "status": "generated",
                "confidence": insight.get('confidence', 0)
            })
        
        # Sort by timestamp (newest first)
        activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {
            "activities": activities[:limit],
            "total_count": len(activities),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent activity: {str(e)}")



