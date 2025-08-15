"""
AI Service - OpenAI Integration for Business Intelligence
"""

import openai
from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime
from app.core.config import settings

# Initialize OpenAI client
openai.api_key = settings.OPENAI_API_KEY

class AIService:
    """AI service for generating business insights and content"""
    
    @staticmethod
    async def generate_social_media_content(
        prompt: str,
        platform: str,
        tone: str = "professional",
        include_hashtags: bool = True
    ) -> Dict[str, Any]:
        """Generate social media content using AI"""
        try:
            # Platform-specific instructions
            platform_instructions = {
                "instagram": "Generate visually appealing content with emojis and relevant hashtags. Keep it engaging and authentic.",
                "linkedin": "Create professional, business-focused content that provides value. Include industry insights.",
                "twitter": "Write concise, punchy content under 280 characters. Make it shareable and trending-worthy.",
                "facebook": "Create engaging, community-focused content that encourages interaction and sharing."
            }
            
            system_prompt = f"""You are a social media expert creating content for {platform}. 
            {platform_instructions.get(platform, '')}
            Tone: {tone}
            Include hashtags: {include_hashtags}
            
            Return JSON with: title, content, hashtags (array), platform, tone, estimated_engagement (1-10)"""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                result["generated_at"] = datetime.now().isoformat()
                return result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "title": prompt[:50] + "...",
                    "content": content,
                    "hashtags": ["#business", "#ai", "#growth"],
                    "platform": platform,
                    "tone": tone,
                    "estimated_engagement": 7,
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error generating social media content: {e}")
            # Return fallback content
            return {
                "title": "AI-Powered Business Growth",
                "content": f"Discover how AI is transforming businesses like yours! 🚀 #AI #Business #Innovation",
                "hashtags": ["#AI", "#Business", "#Innovation", "#Growth"],
                "platform": platform,
                "tone": tone,
                "estimated_engagement": 6,
                "generated_at": datetime.now().isoformat(),
                "error": "Fallback content due to API error"
            }
    
    @staticmethod
    async def analyze_optimal_posting_times(
        platform: str,
        audience_data: Dict[str, Any],
        historical_performance: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze and suggest optimal posting times"""
        try:
            data_summary = {
                "platform": platform,
                "audience_size": audience_data.get("size", 0),
                "primary_timezone": audience_data.get("timezone", "UTC"),
                "age_group": audience_data.get("age_group", "25-45"),
                "recent_posts": len(historical_performance),
                "avg_engagement": sum(p.get("engagement", 0) for p in historical_performance) / max(len(historical_performance), 1)
            }
            
            system_prompt = """You are a social media analytics expert. Analyze the data and recommend optimal posting times.
            Consider audience behavior, platform algorithms, and historical performance.
            Return JSON with: recommended_times (array of HH:MM), best_days (array), reasoning, confidence (0-1)"""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this data: {json.dumps(data_summary)}"}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                result["analyzed_at"] = datetime.now().isoformat()
                return result
            except json.JSONDecodeError:
                # Fallback
                default_times = {
                    "instagram": ["10:00", "14:00", "19:00"],
                    "linkedin": ["08:00", "12:00", "17:00"],
                    "twitter": ["09:00", "13:00", "18:00"],
                    "facebook": ["10:00", "15:00", "20:00"]
                }
                
                return {
                    "recommended_times": default_times.get(platform, ["10:00", "14:00", "18:00"]),
                    "best_days": ["Tuesday", "Wednesday", "Thursday"],
                    "reasoning": "Based on general platform best practices and audience behavior patterns",
                    "confidence": 0.7,
                    "analyzed_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error analyzing posting times: {e}")
            # Return default recommendations
            default_times = {
                "instagram": ["10:00", "14:00", "19:00"],
                "linkedin": ["08:00", "12:00", "17:00"],
                "twitter": ["09:00", "13:00", "18:00"],
                "facebook": ["10:00", "15:00", "20:00"]
            }
            
            return {
                "recommended_times": default_times.get(platform, ["10:00", "14:00", "18:00"]),
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "reasoning": "General best practices for social media posting",
                "confidence": 0.6,
                "analyzed_at": datetime.now().isoformat(),
                "error": "Fallback due to API error"
            }
    
    @staticmethod
    async def generate_business_strategy(
        business_data: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate business strategy recommendations"""
        try:
            data_context = {
                "revenue": business_data.get("revenue", 0),
                "growth_rate": business_data.get("growth_rate", 0),
                "industry": business_data.get("industry", "technology"),
                "company_size": business_data.get("company_size", "small"),
                "market_trends": market_data.get("trends", []),
                "competition_level": market_data.get("competition", "medium")
            }
            
            system_prompt = """You are a business strategy consultant. Analyze the business and market data to provide actionable strategic recommendations.
            Return an array of JSON objects with: category, title, description, action_items (array), priority (high/medium/low), expected_impact, timeline"""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Provide strategic recommendations for this business: {json.dumps(data_context)}"}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                for item in result:
                    item["generated_at"] = datetime.now().isoformat()
                return result
            except json.JSONDecodeError:
                # Fallback strategies
                return [
                    {
                        "category": "growth",
                        "title": "Digital Marketing Optimization",
                        "description": "Enhance online presence and customer acquisition through improved digital marketing strategies",
                        "action_items": [
                            "Implement SEO best practices",
                            "Expand social media presence",
                            "Launch targeted ad campaigns",
                            "Create valuable content marketing"
                        ],
                        "priority": "high",
                        "expected_impact": "25-40% increase in leads and brand awareness",
                        "timeline": "3-6 months",
                        "generated_at": datetime.now().isoformat()
                    },
                    {
                        "category": "efficiency",
                        "title": "Process Automation",
                        "description": "Automate repetitive tasks to improve efficiency and reduce costs",
                        "action_items": [
                            "Identify manual processes",
                            "Implement automation tools",
                            "Train team on new systems",
                            "Monitor and optimize workflows"
                        ],
                        "priority": "medium",
                        "expected_impact": "15-25% reduction in operational costs",
                        "timeline": "2-4 months",
                        "generated_at": datetime.now().isoformat()
                    }
                ]
                
        except Exception as e:
            print(f"Error generating business strategy: {e}")
            return []
    
    @staticmethod
    async def analyze_competitors(
        competitor_data: List[Dict[str, Any]],
        own_business_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze competitors and provide insights"""
        try:
            analysis_context = {
                "own_business": {
                    "revenue": own_business_data.get("revenue", 0),
                    "market_share": own_business_data.get("market_share", 0),
                    "strengths": own_business_data.get("strengths", []),
                    "products": own_business_data.get("products", [])
                },
                "competitors": competitor_data[:5]  # Limit to top 5 competitors
            }
            
            system_prompt = """You are a competitive intelligence analyst. Analyze the competitive landscape and provide strategic insights.
            Return JSON with: market_position, key_competitors (array), opportunities (array), threats (array), recommendations (array), competitive_advantage"""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this competitive landscape: {json.dumps(analysis_context)}"}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                result["analyzed_at"] = datetime.now().isoformat()
                return result
            except json.JSONDecodeError:
                # Fallback analysis
                return {
                    "market_position": "Competitive player with growth potential",
                    "key_competitors": [comp.get("name", "Unknown") for comp in competitor_data[:3]],
                    "opportunities": [
                        "Underserved market segments",
                        "Technology innovation gaps",
                        "Customer service differentiation"
                    ],
                    "threats": [
                        "Increased competition",
                        "Price pressure",
                        "Market saturation"
                    ],
                    "recommendations": [
                        "Focus on unique value proposition",
                        "Invest in customer relationships",
                        "Leverage technology for competitive advantage"
                    ],
                    "competitive_advantage": "Agility and customer-focused approach",
                    "analyzed_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error analyzing competitors: {e}")
            return {
                "error": "Analysis unavailable",
                "analyzed_at": datetime.now().isoformat()
            }
    
    @staticmethod
    async def forecast_roi(
        historical_data: List[Dict[str, Any]],
        planned_investments: List[Dict[str, Any]],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Forecast ROI based on data analysis"""
        try:
            forecast_context = {
                "historical_performance": historical_data[-12:],  # Last 12 periods
                "planned_investments": planned_investments,
                "market_conditions": market_conditions,
                "current_revenue": historical_data[-1].get("revenue", 0) if historical_data else 0
            }
            
            system_prompt = """You are a financial analyst. Analyze the data and forecast ROI for the next 6 months.
            Return JSON with: monthly_forecast (array of 6 numbers), confidence_level (0-1), key_factors (array), risk_assessment, recommendations (array)"""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Forecast ROI based on this data: {json.dumps(forecast_context)}"}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                result["forecasted_at"] = datetime.now().isoformat()
                return result
            except json.JSONDecodeError:
                # Fallback forecast
                base_roi = 1.0
                growth_rate = 0.05  # 5% monthly growth
                
                return {
                    "monthly_forecast": [
                        round(base_roi * (1 + growth_rate) ** i, 2) 
                        for i in range(1, 7)
                    ],
                    "confidence_level": 0.7,
                    "key_factors": [
                        "Market conditions",
                        "Investment strategy",
                        "Competitive landscape",
                        "Economic trends"
                    ],
                    "risk_assessment": "Medium - subject to market volatility",
                    "recommendations": [
                        "Monitor key performance indicators",
                        "Adjust strategy based on market feedback",
                        "Diversify investment portfolio"
                    ],
                    "forecasted_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error forecasting ROI: {e}")
            return {
                "error": "Forecast unavailable",
                "forecasted_at": datetime.now().isoformat()
            }



