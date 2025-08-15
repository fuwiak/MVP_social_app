"""
AI Services API endpoints
Core AI functionality for business intelligence
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.ai_service import AIService
from app.core.database import DatabaseService

router = APIRouter()

class StrategyRequest(BaseModel):
    business_data: Dict[str, Any]
    market_data: Dict[str, Any]

class CompetitorAnalysisRequest(BaseModel):
    competitor_data: List[Dict[str, Any]]
    own_business_data: Dict[str, Any]

class ROIForecastRequest(BaseModel):
    historical_data: List[Dict[str, Any]]
    planned_investments: List[Dict[str, Any]]
    market_conditions: Dict[str, Any]

@router.post("/generate-strategy")
async def generate_business_strategy(request: StrategyRequest) -> Dict[str, Any]:
    """Generate AI-powered business strategy recommendations"""
    try:
        strategy_insights = await AIService.generate_business_strategy(
            business_data=request.business_data,
            market_data=request.market_data
        )
        
        # Save insights to database
        for insight in strategy_insights:
            await DatabaseService.save_ai_insight({
                "type": "strategy",
                "title": insight.get("title", "Business Strategy"),
                "content": insight.get("description", ""),
                "confidence": 0.85,
                "data_source": "ai_strategy_generator"
            })
        
        return {
            "strategy_insights": strategy_insights,
            "generated_at": datetime.now().isoformat(),
            "input_data": {
                "business_data": request.business_data,
                "market_data": request.market_data
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating strategy: {str(e)}")

@router.post("/analyze-competitors")
async def analyze_competitors(request: CompetitorAnalysisRequest) -> Dict[str, Any]:
    """Analyze competitor landscape and provide insights"""
    try:
        analysis = await AIService.analyze_competitors(
            competitor_data=request.competitor_data,
            own_business_data=request.own_business_data
        )
        
        # Save competitive insights
        await DatabaseService.save_ai_insight({
            "type": "competitor",
            "title": "Competitive Analysis",
            "content": f"Market position: {analysis.get('market_position', 'Unknown')}",
            "confidence": 0.80,
            "data_source": "competitor_analysis"
        })
        
        return {
            "analysis": analysis,
            "competitors_analyzed": len(request.competitor_data),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing competitors: {str(e)}")

@router.post("/forecast-roi")
async def forecast_roi(request: ROIForecastRequest) -> Dict[str, Any]:
    """Generate ROI forecast based on historical data and planned investments"""
    try:
        forecast = await AIService.forecast_roi(
            historical_data=request.historical_data,
            planned_investments=request.planned_investments,
            market_conditions=request.market_conditions
        )
        
        # Save forecast insights
        await DatabaseService.save_ai_insight({
            "type": "forecast",
            "title": "ROI Forecast",
            "content": f"6-month forecast with {forecast.get('confidence_level', 0.7):.1%} confidence",
            "confidence": forecast.get('confidence_level', 0.7),
            "data_source": "roi_forecasting"
        })
        
        return {
            "forecast": forecast,
            "data_points_analyzed": len(request.historical_data),
            "investments_considered": len(request.planned_investments),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting ROI: {str(e)}")

@router.get("/insights/{insight_type}")
async def get_insights_by_type(insight_type: str, limit: int = 10) -> Dict[str, Any]:
    """Get AI insights filtered by type"""
    try:
        valid_types = ['strategy', 'competitor', 'forecast', 'timing', 'content']
        if insight_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid insight type. Must be one of: {valid_types}"
            )
        
        insights = await DatabaseService.get_ai_insights(insight_type, limit)
        
        return {
            "insights": insights,
            "type": insight_type,
            "count": len(insights),
            "available_types": valid_types
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insights: {str(e)}")



