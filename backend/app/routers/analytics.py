"""
Analytics API endpoints
Business analytics and performance metrics
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio

from app.core.database import DatabaseService

router = APIRouter()

@router.get("/revenue")
async def get_revenue_analytics(days: int = 30) -> Dict[str, Any]:
    """Get revenue analytics and trends"""
    try:
        metrics = await DatabaseService.get_business_metrics(days)
        
        # Calculate revenue trends
        revenue_data = [
            {
                "date": metric.get('date'),
                "revenue": metric.get('revenue', 0),
                "profit": metric.get('profit', 0),
                "expenses": metric.get('expenses', 0)
            }
            for metric in metrics
        ]
        
        total_revenue = sum(m['revenue'] for m in revenue_data)
        total_profit = sum(m['profit'] for m in revenue_data)
        total_expenses = sum(m['expenses'] for m in revenue_data)
        
        # Calculate growth rate (simplified)
        if len(revenue_data) >= 2:
            recent_revenue = sum(m['revenue'] for m in revenue_data[:len(revenue_data)//2])
            earlier_revenue = sum(m['revenue'] for m in revenue_data[len(revenue_data)//2:])
            growth_rate = ((recent_revenue - earlier_revenue) / max(earlier_revenue, 1)) * 100
        else:
            growth_rate = 0
        
        return {
            "period": f"Last {days} days",
            "summary": {
                "total_revenue": total_revenue,
                "total_profit": total_profit,
                "total_expenses": total_expenses,
                "profit_margin": round((total_profit / max(total_revenue, 1)) * 100, 2),
                "growth_rate": round(growth_rate, 2)
            },
            "daily_data": revenue_data,
            "trends": {
                "revenue_trend": "increasing" if growth_rate > 0 else "decreasing",
                "avg_daily_revenue": round(total_revenue / max(days, 1), 2),
                "best_day": max(revenue_data, key=lambda x: x['revenue']) if revenue_data else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching revenue analytics: {str(e)}")

@router.get("/social-performance")
async def get_social_media_performance(days: int = 30) -> Dict[str, Any]:
    """Get social media performance analytics"""
    try:
        posts = await DatabaseService.get_social_media_posts(200)
        
        # Filter by date range
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_posts = [
            p for p in posts 
            if p.get('status') == 'posted' and 
            datetime.fromisoformat(p.get('created_at', '').replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Platform performance
        platforms = ['instagram', 'linkedin', 'twitter', 'facebook']
        platform_performance = {}
        
        for platform in platforms:
            platform_posts = [p for p in recent_posts if p.get('platform') == platform]
            
            if platform_posts:
                total_engagement = sum(
                    p.get('engagement', {}).get('likes', 0) + 
                    p.get('engagement', {}).get('comments', 0) + 
                    p.get('engagement', {}).get('shares', 0)
                    for p in platform_posts
                )
                total_reach = sum(p.get('engagement', {}).get('reach', 0) for p in platform_posts)
                
                platform_performance[platform] = {
                    "posts": len(platform_posts),
                    "total_engagement": total_engagement,
                    "total_reach": total_reach,
                    "avg_engagement": round(total_engagement / len(platform_posts), 1),
                    "engagement_rate": round((total_engagement / max(total_reach, 1)) * 100, 2),
                    "top_post": max(platform_posts, key=lambda p: 
                        p.get('engagement', {}).get('likes', 0) + 
                        p.get('engagement', {}).get('comments', 0) + 
                        p.get('engagement', {}).get('shares', 0)
                    )
                }
        
        return {
            "period": f"Last {days} days",
            "overview": {
                "total_posts": len(recent_posts),
                "total_platforms": len([p for p in platform_performance.values() if p['posts'] > 0]),
                "avg_daily_posts": round(len(recent_posts) / max(days, 1), 1)
            },
            "platform_performance": platform_performance,
            "top_performers": sorted(
                recent_posts,
                key=lambda p: (
                    p.get('engagement', {}).get('likes', 0) + 
                    p.get('engagement', {}).get('comments', 0) + 
                    p.get('engagement', {}).get('shares', 0)
                ),
                reverse=True
            )[:10]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching social performance: {str(e)}")

@router.get("/ad-performance")
async def get_ad_campaign_performance() -> Dict[str, Any]:
    """Get advertising campaign performance analytics"""
    try:
        campaigns = await DatabaseService.get_ad_campaigns()
        
        # Calculate performance metrics
        active_campaigns = [c for c in campaigns if c.get('status') == 'active']
        total_spend = sum(c.get('spent', 0) for c in campaigns)
        total_conversions = sum(c.get('conversions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_impressions = sum(c.get('impressions', 0) for c in campaigns)
        
        # Platform breakdown
        platform_data = {}
        for campaign in campaigns:
            platform = campaign.get('platform', 'unknown')
            if platform not in platform_data:
                platform_data[platform] = {
                    "campaigns": 0,
                    "spend": 0,
                    "conversions": 0,
                    "clicks": 0,
                    "impressions": 0
                }
            
            platform_data[platform]["campaigns"] += 1
            platform_data[platform]["spend"] += campaign.get('spent', 0)
            platform_data[platform]["conversions"] += campaign.get('conversions', 0)
            platform_data[platform]["clicks"] += campaign.get('clicks', 0)
            platform_data[platform]["impressions"] += campaign.get('impressions', 0)
        
        # Calculate averages
        avg_cpc = total_spend / max(total_clicks, 1)
        avg_ctr = (total_clicks / max(total_impressions, 1)) * 100
        avg_conversion_rate = (total_conversions / max(total_clicks, 1)) * 100
        
        return {
            "overview": {
                "total_campaigns": len(campaigns),
                "active_campaigns": len(active_campaigns),
                "total_spend": total_spend,
                "total_conversions": total_conversions,
                "avg_cpc": round(avg_cpc, 2),
                "avg_ctr": round(avg_ctr, 2),
                "avg_conversion_rate": round(avg_conversion_rate, 2)
            },
            "platform_breakdown": platform_data,
            "top_campaigns": sorted(
                campaigns,
                key=lambda c: c.get('roas', 0),
                reverse=True
            )[:5],
            "performance_trends": {
                "best_performing_platform": max(
                    platform_data.items(),
                    key=lambda x: x[1]['conversions']
                )[0] if platform_data else None,
                "most_expensive_platform": max(
                    platform_data.items(),
                    key=lambda x: x[1]['spend']
                )[0] if platform_data else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ad performance: {str(e)}")

@router.get("/roi-analysis")
async def get_roi_analysis(days: int = 30) -> Dict[str, Any]:
    """Get comprehensive ROI analysis"""
    try:
        # Get data in parallel
        business_metrics_task = DatabaseService.get_business_metrics(days)
        ad_campaigns_task = DatabaseService.get_ad_campaigns()
        cash_flow_task = DatabaseService.get_cash_flow(days)
        
        business_metrics, ad_campaigns, cash_flow = await asyncio.gather(
            business_metrics_task,
            ad_campaigns_task,
            cash_flow_task
        )
        
        # Calculate overall ROI
        total_revenue = sum(m.get('revenue', 0) for m in business_metrics)
        total_investment = sum(entry.get('amount', 0) for entry in cash_flow if entry.get('type') == 'expense')
        
        overall_roi = (total_revenue - total_investment) / max(total_investment, 1)
        
        # Ad campaign ROI
        ad_spend = sum(c.get('spent', 0) for c in ad_campaigns)
        ad_conversions = sum(c.get('conversions', 0) for c in ad_campaigns)
        avg_order_value = 150  # Mock value - should come from actual data
        ad_revenue = ad_conversions * avg_order_value
        ad_roi = (ad_revenue - ad_spend) / max(ad_spend, 1)
        
        # Monthly trend analysis
        monthly_roi = []
        if business_metrics:
            for metric in business_metrics[-6:]:  # Last 6 data points
                revenue = metric.get('revenue', 0)
                investment = metric.get('expenses', 0)
                roi = (revenue - investment) / max(investment, 1)
                monthly_roi.append({
                    "date": metric.get('date'),
                    "roi": round(roi, 3),
                    "revenue": revenue,
                    "investment": investment
                })
        
        return {
            "period": f"Last {days} days",
            "overall_roi": {
                "roi_ratio": round(overall_roi, 3),
                "roi_percentage": round(overall_roi * 100, 2),
                "total_revenue": total_revenue,
                "total_investment": total_investment,
                "net_profit": total_revenue - total_investment
            },
            "advertising_roi": {
                "ad_roi": round(ad_roi, 3),
                "ad_spend": ad_spend,
                "ad_revenue": ad_revenue,
                "conversion_value": avg_order_value,
                "total_conversions": ad_conversions
            },
            "trends": monthly_roi,
            "insights": {
                "best_month": max(monthly_roi, key=lambda x: x['roi']) if monthly_roi else None,
                "roi_trend": "improving" if len(monthly_roi) >= 2 and monthly_roi[-1]['roi'] > monthly_roi[0]['roi'] else "declining",
                "investment_efficiency": round((total_revenue / max(total_investment, 1)), 2)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating ROI analysis: {str(e)}")

@router.get("/dashboard-summary")
async def get_dashboard_summary() -> Dict[str, Any]:
    """Get summary analytics for dashboard widgets"""
    try:
        # Get all data in parallel
        business_metrics_task = DatabaseService.get_business_metrics(30)
        social_posts_task = DatabaseService.get_social_media_posts(50)
        ad_campaigns_task = DatabaseService.get_ad_campaigns()
        
        business_metrics, social_posts, ad_campaigns = await asyncio.gather(
            business_metrics_task,
            social_posts_task,
            ad_campaigns_task
        )
        
        # Quick calculations for dashboard
        total_revenue = sum(m.get('revenue', 0) for m in business_metrics)
        posted_content = len([p for p in social_posts if p.get('status') == 'posted'])
        active_campaigns = len([c for c in ad_campaigns if c.get('status') == 'active'])
        
        social_reach = sum(
            p.get('engagement', {}).get('reach', 0) 
            for p in social_posts 
            if p.get('status') == 'posted'
        )
        
        return {
            "key_metrics": {
                "revenue": total_revenue,
                "social_reach": social_reach,
                "active_campaigns": active_campaigns,
                "content_pieces": posted_content
            },
            "quick_stats": {
                "revenue_growth": "+15.5%",  # Mock calculation
                "engagement_rate": "8.3%",   # Mock calculation
                "roi_improvement": "+12.1%", # Mock calculation
                "campaign_performance": "Above average"
            },
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard summary: {str(e)}")



