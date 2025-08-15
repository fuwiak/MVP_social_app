"""
Ad Campaigns API endpoints
Campaign management and performance tracking
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

from app.core.database import DatabaseService
from app.services.ai_service import AIService

router = APIRouter()

class CampaignStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    draft = "draft"

class AdCampaign(BaseModel):
    name: str
    platform: str
    budget: float
    target_audience: str
    campaign_type: str
    start_date: str
    end_date: Optional[str] = None

class CampaignUpdate(BaseModel):
    budget: Optional[float] = None
    status: Optional[CampaignStatus] = None
    target_audience: Optional[str] = None

@router.get("/campaigns")
async def get_ad_campaigns(
    platform: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """Get ad campaigns with optional filtering"""
    try:
        campaigns = await DatabaseService.get_ad_campaigns()
        
        # Apply filters
        if platform:
            campaigns = [c for c in campaigns if c.get('platform', '').lower() == platform.lower()]
        
        if status:
            campaigns = [c for c in campaigns if c.get('status') == status]
        
        # Apply limit
        campaigns = campaigns[:limit]
        
        # Calculate summary stats
        total_spend = sum(c.get('spent', 0) for c in campaigns)
        total_conversions = sum(c.get('conversions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_impressions = sum(c.get('impressions', 0) for c in campaigns)
        
        avg_cpc = total_spend / max(total_clicks, 1)
        avg_ctr = (total_clicks / max(total_impressions, 1)) * 100
        avg_roas = sum(c.get('roas', 0) for c in campaigns) / max(len(campaigns), 1)
        
        # Platform breakdown
        platforms = {}
        for campaign in campaigns:
            platform_name = campaign.get('platform', 'unknown')
            if platform_name not in platforms:
                platforms[platform_name] = {
                    'count': 0,
                    'spend': 0,
                    'conversions': 0,
                    'avg_roas': 0
                }
            
            platforms[platform_name]['count'] += 1
            platforms[platform_name]['spend'] += campaign.get('spent', 0)
            platforms[platform_name]['conversions'] += campaign.get('conversions', 0)
        
        # Calculate average ROAS per platform
        for platform_name, data in platforms.items():
            platform_campaigns = [c for c in campaigns if c.get('platform') == platform_name]
            data['avg_roas'] = round(
                sum(c.get('roas', 0) for c in platform_campaigns) / max(len(platform_campaigns), 1), 2
            )
        
        return {
            "campaigns": campaigns,
            "summary": {
                "total_campaigns": len(campaigns),
                "total_spend": round(total_spend, 2),
                "total_conversions": total_conversions,
                "avg_cpc": round(avg_cpc, 2),
                "avg_ctr": round(avg_ctr, 2),
                "avg_roas": round(avg_roas, 2)
            },
            "platform_breakdown": platforms,
            "filters_applied": {
                "platform": platform,
                "status": status,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching campaigns: {str(e)}")

@router.post("/campaigns")
async def create_ad_campaign(campaign: AdCampaign) -> Dict[str, Any]:
    """Create new ad campaign"""
    try:
        # Validate platform
        valid_platforms = ['facebook', 'instagram', 'google', 'linkedin', 'twitter', 'tiktok']
        if campaign.platform.lower() not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {valid_platforms}"
            )
        
        # Validate budget
        if campaign.budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be positive")
        
        # Validate dates
        try:
            start_date = datetime.fromisoformat(campaign.start_date.replace('Z', '+00:00'))
            if campaign.end_date:
                end_date = datetime.fromisoformat(campaign.end_date.replace('Z', '+00:00'))
                if end_date <= start_date:
                    raise HTTPException(status_code=400, detail="End date must be after start date")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")
        
        # Create campaign data
        campaign_data = {
            "name": campaign.name,
            "platform": campaign.platform.lower(),
            "budget": campaign.budget,
            "spent": 0,
            "clicks": 0,
            "impressions": 0,
            "conversions": 0,
            "ctr": 0,
            "cpc": 0,
            "roas": 0,
            "status": "draft",
            "target_audience": campaign.target_audience,
            "campaign_type": campaign.campaign_type,
            "start_date": campaign.start_date,
            "end_date": campaign.end_date
        }
        
        # Save to database
        created_campaign = await DatabaseService.create_ad_campaign(campaign_data)
        
        return {
            "message": "Campaign created successfully",
            "campaign": created_campaign
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating campaign: {str(e)}")

@router.get("/campaigns/{campaign_id}")
async def get_campaign_details(campaign_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific campaign"""
    try:
        # Mock detailed campaign data (in production, fetch from database)
        campaign = {
            "id": campaign_id,
            "name": "AI Business Tool Launch",
            "platform": "facebook",
            "budget": 2000,
            "spent": 1245.67,
            "remaining_budget": 754.33,
            "clicks": 1847,
            "impressions": 67543,
            "conversions": 89,
            "ctr": 2.73,
            "cpc": 0.67,
            "roas": 3.8,
            "status": "active",
            "target_audience": "Business owners, 25-45, interested in AI and automation",
            "campaign_type": "conversion",
            "start_date": "2024-01-10T09:00:00Z",
            "end_date": "2024-01-25T23:59:59Z",
            "created_at": "2024-01-09T14:30:00Z",
            "daily_performance": [
                {"date": "2024-01-15", "spend": 85.40, "clicks": 127, "conversions": 6, "roas": 4.2},
                {"date": "2024-01-14", "spend": 92.15, "clicks": 134, "conversions": 8, "roas": 4.8},
                {"date": "2024-01-13", "spend": 78.90, "clicks": 118, "conversions": 5, "roas": 3.9},
                {"date": "2024-01-12", "spend": 88.25, "clicks": 129, "conversions": 7, "roas": 4.5}
            ],
            "targeting": {
                "age_range": "25-45",
                "gender": "all",
                "interests": ["artificial intelligence", "business automation", "productivity"],
                "locations": ["United States", "Canada", "United Kingdom"],
                "device_types": ["desktop", "mobile"]
            },
            "creative_assets": [
                {"type": "image", "url": "/assets/ad-creative-1.jpg", "performance": "high"},
                {"type": "video", "url": "/assets/ad-video-1.mp4", "performance": "medium"},
                {"type": "carousel", "url": "/assets/ad-carousel-1.jpg", "performance": "high"}
            ]
        }
        
        # Calculate additional metrics
        campaign["budget_utilization"] = round((campaign["spent"] / campaign["budget"]) * 100, 1)
        campaign["days_running"] = (datetime.now() - datetime.fromisoformat(campaign["start_date"].replace('Z', '+00:00'))).days
        campaign["avg_daily_spend"] = round(campaign["spent"] / max(campaign["days_running"], 1), 2)
        
        return campaign
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching campaign details: {str(e)}")

@router.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: str, updates: CampaignUpdate) -> Dict[str, Any]:
    """Update campaign settings"""
    try:
        update_data = {}
        
        if updates.budget is not None:
            if updates.budget <= 0:
                raise HTTPException(status_code=400, detail="Budget must be positive")
            update_data["budget"] = updates.budget
        
        if updates.status is not None:
            update_data["status"] = updates.status.value
        
        if updates.target_audience is not None:
            update_data["target_audience"] = updates.target_audience
        
        # In production, update in database
        # updated_campaign = await DatabaseService.update_ad_campaign(campaign_id, update_data)
        
        return {
            "message": "Campaign updated successfully",
            "campaign_id": campaign_id,
            "updates_applied": update_data,
            "updated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating campaign: {str(e)}")

@router.post("/campaigns/{campaign_id}/optimize")
async def optimize_campaign(campaign_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Use AI to optimize campaign performance"""
    
    async def run_optimization():
        """Background task for AI optimization"""
        try:
            # Mock campaign data for AI analysis
            campaign_data = {
                "current_performance": {
                    "ctr": 2.73,
                    "cpc": 0.67,
                    "roas": 3.8,
                    "conversions": 89
                },
                "target_audience": "Business owners, 25-45, interested in AI",
                "platform": "facebook",
                "budget": 2000,
                "spent": 1245.67
            }
            
            # Generate optimization recommendations
            # In production, this would call the actual AI service
            recommendations = {
                "bid_adjustments": [
                    {"action": "increase_bid", "audience_segment": "25-35 business owners", "adjustment": "+15%"},
                    {"action": "decrease_bid", "audience_segment": "mobile users", "adjustment": "-10%"}
                ],
                "targeting_suggestions": [
                    "Add 'startup founders' to interests",
                    "Exclude users who visited pricing page but didn't convert",
                    "Expand to include 'small business' keyword"
                ],
                "creative_recommendations": [
                    "Test video creative with customer testimonials",
                    "A/B test headline: 'Transform Your Business with AI'",
                    "Add urgency element: 'Limited time offer'"
                ],
                "budget_allocation": {
                    "suggested_daily_budget": 95,
                    "reasoning": "Increase budget during peak performance hours (2-4 PM)"
                },
                "expected_improvements": {
                    "ctr_improvement": "+12%",
                    "cpc_reduction": "-8%",
                    "roas_improvement": "+18%"
                }
            }
            
            # Save optimization results
            # await DatabaseService.save_ai_insight({
            #     "type": "campaign_optimization",
            #     "title": f"Campaign Optimization - {campaign_id}",
            #     "content": json.dumps(recommendations),
            #     "confidence": 0.82
            # })
            
            print(f"Optimization completed for campaign {campaign_id}")
            
        except Exception as e:
            print(f"Optimization failed for campaign {campaign_id}: {e}")
    
    background_tasks.add_task(run_optimization)
    
    return {
        "message": "Campaign optimization started",
        "campaign_id": campaign_id,
        "status": "processing",
        "estimated_completion": "2-3 minutes"
    }

@router.get("/performance-analytics")
async def get_performance_analytics(days: int = 30) -> Dict[str, Any]:
    """Get comprehensive campaign performance analytics"""
    try:
        campaigns = await DatabaseService.get_ad_campaigns()
        
        # Filter campaigns with activity in the specified period
        cutoff_date = datetime.now() - timedelta(days=days)
        active_campaigns = [
            c for c in campaigns 
            if datetime.fromisoformat(c.get('created_at', '').replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Overall performance metrics
        total_spend = sum(c.get('spent', 0) for c in active_campaigns)
        total_conversions = sum(c.get('conversions', 0) for c in active_campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in active_campaigns)
        total_impressions = sum(c.get('impressions', 0) for c in active_campaigns)
        
        # Platform performance comparison
        platform_performance = {}
        platforms = set(c.get('platform', 'unknown') for c in active_campaigns)
        
        for platform in platforms:
            platform_campaigns = [c for c in active_campaigns if c.get('platform') == platform]
            
            if platform_campaigns:
                platform_spend = sum(c.get('spent', 0) for c in platform_campaigns)
                platform_conversions = sum(c.get('conversions', 0) for c in platform_campaigns)
                platform_clicks = sum(c.get('clicks', 0) for c in platform_campaigns)
                platform_impressions = sum(c.get('impressions', 0) for c in platform_campaigns)
                
                platform_performance[platform] = {
                    "campaigns": len(platform_campaigns),
                    "spend": platform_spend,
                    "conversions": platform_conversions,
                    "clicks": platform_clicks,
                    "impressions": platform_impressions,
                    "avg_cpc": round(platform_spend / max(platform_clicks, 1), 2),
                    "avg_ctr": round((platform_clicks / max(platform_impressions, 1)) * 100, 2),
                    "conversion_rate": round((platform_conversions / max(platform_clicks, 1)) * 100, 2),
                    "avg_roas": round(
                        sum(c.get('roas', 0) for c in platform_campaigns) / len(platform_campaigns), 2
                    )
                }
        
        # Top and bottom performers
        top_campaigns = sorted(
            active_campaigns,
            key=lambda x: x.get('roas', 0),
            reverse=True
        )[:5]
        
        bottom_campaigns = sorted(
            active_campaigns,
            key=lambda x: x.get('roas', 0)
        )[:3]
        
        # Budget utilization analysis
        budget_analysis = []
        for campaign in active_campaigns:
            budget = campaign.get('budget', 0)
            spent = campaign.get('spent', 0)
            utilization = (spent / budget * 100) if budget > 0 else 0
            
            budget_analysis.append({
                "campaign_name": campaign.get('name'),
                "budget": budget,
                "spent": spent,
                "remaining": budget - spent,
                "utilization_percent": round(utilization, 1),
                "performance_score": campaign.get('roas', 0)
            })
        
        return {
            "period": f"Last {days} days",
            "overview": {
                "total_campaigns": len(active_campaigns),
                "total_spend": round(total_spend, 2),
                "total_conversions": total_conversions,
                "total_clicks": total_clicks,
                "total_impressions": total_impressions,
                "overall_cpc": round(total_spend / max(total_clicks, 1), 2),
                "overall_ctr": round((total_clicks / max(total_impressions, 1)) * 100, 2),
                "overall_conversion_rate": round((total_conversions / max(total_clicks, 1)) * 100, 2)
            },
            "platform_performance": platform_performance,
            "top_performers": top_campaigns,
            "underperformers": bottom_campaigns,
            "budget_analysis": sorted(budget_analysis, key=lambda x: x['performance_score'], reverse=True),
            "insights": {
                "best_performing_platform": max(
                    platform_performance.items(),
                    key=lambda x: x[1]['avg_roas']
                )[0] if platform_performance else None,
                "most_cost_effective": max(
                    platform_performance.items(),
                    key=lambda x: x[1]['conversion_rate']
                )[0] if platform_performance else None,
                "optimization_opportunities": len([
                    c for c in active_campaigns if c.get('roas', 0) < 2.0
                ])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing performance: {str(e)}")

@router.post("/generate-ad-creative")
async def generate_ad_creative(
    product_description: str,
    target_audience: str,
    platform: str,
    campaign_objective: str = "conversion"
) -> Dict[str, Any]:
    """Generate AI-powered ad creative content"""
    try:
        # Validate platform
        valid_platforms = ['facebook', 'instagram', 'google', 'linkedin', 'twitter']
        if platform.lower() not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Must be one of: {valid_platforms}"
            )
        
        # Generate ad content using AI service
        ad_content = await AIService.generate_ad_content(
            productService=product_description,
            targetAudience=target_audience,
            platform=platform,
            budget=1000  # Default budget for creative generation
        )
        
        # Generate multiple creative variations
        creative_variations = [
            {
                "type": "headline_primary",
                "content": "Transform Your Business with AI-Powered Automation",
                "character_count": 45
            },
            {
                "type": "headline_secondary", 
                "content": "Save 20+ Hours Weekly with Smart Business Tools",
                "character_count": 42
            },
            {
                "type": "description",
                "content": ad_content.get('content', 'Boost productivity and grow your business with our intelligent automation platform. Join thousands of entrepreneurs who are scaling faster with AI.'),
                "character_count": 150
            },
            {
                "type": "call_to_action",
                "content": "Start Free Trial",
                "character_count": 16
            }
        ]
        
        # Platform-specific recommendations
        platform_specs = {
            "facebook": {
                "image_ratio": "1.91:1",
                "video_length": "15-60 seconds",
                "text_limit": 125,
                "headline_limit": 40
            },
            "instagram": {
                "image_ratio": "1:1 or 4:5",
                "video_length": "15-30 seconds", 
                "text_limit": 125,
                "hashtag_limit": 30
            },
            "google": {
                "headline_limit": 30,
                "description_limit": 90,
                "extensions": "sitelinks, callouts"
            },
            "linkedin": {
                "image_ratio": "1.91:1",
                "text_limit": 150,
                "professional_tone": True
            }
        }
        
        return {
            "creative_variations": creative_variations,
            "platform_specifications": platform_specs.get(platform.lower(), {}),
            "targeting_suggestions": [
                f"Age: 25-54",
                f"Interests: {target_audience.lower()}",
                "Behaviors: Business decision makers",
                "Custom audiences: Website visitors, email subscribers"
            ],
            "optimization_tips": [
                "Test multiple headline variations",
                "Use high-contrast, eye-catching visuals",
                "Include social proof or testimonials",
                "Create urgency with limited-time offers",
                f"Optimize for {campaign_objective} objective"
            ],
            "generated_at": datetime.now().isoformat(),
            "input_parameters": {
                "product_description": product_description,
                "target_audience": target_audience,
                "platform": platform,
                "campaign_objective": campaign_objective
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ad creative: {str(e)}")

@router.get("/budget-recommendations")
async def get_budget_recommendations(
    campaign_objective: str = "conversion",
    target_audience_size: int = 100000,
    competition_level: str = "medium"
) -> Dict[str, Any]:
    """Get AI-powered budget recommendations"""
    try:
        # Base calculations for budget recommendations
        base_daily_budget = {
            "awareness": 50,
            "traffic": 30,
            "engagement": 25,
            "conversion": 75,
            "retention": 40
        }
        
        # Adjust for competition level
        competition_multipliers = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.3,
            "very_high": 1.6
        }
        
        # Adjust for audience size
        audience_multiplier = min(max(target_audience_size / 100000, 0.5), 2.0)
        
        recommended_daily = base_daily_budget.get(campaign_objective, 50) * \
                           competition_multipliers.get(competition_level, 1.0) * \
                           audience_multiplier
        
        # Platform-specific recommendations
        platform_budgets = {
            "facebook": {
                "minimum_daily": max(recommended_daily * 0.8, 20),
                "recommended_daily": recommended_daily,
                "optimal_daily": recommended_daily * 1.5
            },
            "instagram": {
                "minimum_daily": max(recommended_daily * 0.7, 15),
                "recommended_daily": recommended_daily * 0.9,
                "optimal_daily": recommended_daily * 1.3
            },
            "google": {
                "minimum_daily": max(recommended_daily * 1.2, 30),
                "recommended_daily": recommended_daily * 1.5,
                "optimal_daily": recommended_daily * 2.0
            },
            "linkedin": {
                "minimum_daily": max(recommended_daily * 1.5, 40),
                "recommended_daily": recommended_daily * 2.0,
                "optimal_daily": recommended_daily * 2.5
            }
        }
        
        # Calculate monthly budgets
        for platform, budgets in platform_budgets.items():
            for budget_type in ["minimum_daily", "recommended_daily", "optimal_daily"]:
                monthly_key = budget_type.replace("daily", "monthly")
                budgets[monthly_key] = round(budgets[budget_type] * 30, 2)
                budgets[budget_type] = round(budgets[budget_type], 2)
        
        return {
            "recommendations": platform_budgets,
            "factors_considered": {
                "campaign_objective": campaign_objective,
                "target_audience_size": target_audience_size,
                "competition_level": competition_level,
                "audience_multiplier": round(audience_multiplier, 2),
                "competition_multiplier": competition_multipliers.get(competition_level, 1.0)
            },
            "general_tips": [
                "Start with minimum budget and scale based on performance",
                "Monitor CPC and adjust bids accordingly",
                "Allocate 70% budget to top-performing ads",
                "Reserve 30% for testing new creatives",
                f"For {campaign_objective} campaigns, focus on conversion tracking"
            ],
            "budget_allocation_strategy": {
                "testing_phase": "20% of budget for 7-14 days",
                "optimization_phase": "60% of budget for winning variations",
                "scaling_phase": "Increase budget by 20-50% every 3 days"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating budget recommendations: {str(e)}")



