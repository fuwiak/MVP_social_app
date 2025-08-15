"""
Cash Flow API endpoints
Financial tracking and management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

from app.core.database import DatabaseService

router = APIRouter()

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class CashFlowEntry(BaseModel):
    type: TransactionType
    category: str
    amount: float
    description: str
    date: str
    tags: Optional[List[str]] = []

@router.get("/entries")
async def get_cash_flow_entries(
    days: int = 30,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """Get cash flow entries with filtering options"""
    try:
        entries = await DatabaseService.get_cash_flow(days)
        
        # Apply filters
        if transaction_type:
            entries = [e for e in entries if e.get('type') == transaction_type]
        
        if category:
            entries = [e for e in entries if e.get('category').lower() == category.lower()]
        
        # Apply limit
        entries = entries[:limit]
        
        # Calculate summary statistics
        income_entries = [e for e in entries if e.get('type') == 'income']
        expense_entries = [e for e in entries if e.get('type') == 'expense']
        
        total_income = sum(e.get('amount', 0) for e in income_entries)
        total_expenses = sum(e.get('amount', 0) for e in expense_entries)
        net_flow = total_income - total_expenses
        
        # Category breakdown
        categories = {}
        for entry in entries:
            cat = entry.get('category', 'Other')
            if cat not in categories:
                categories[cat] = {'income': 0, 'expense': 0, 'count': 0}
            
            categories[cat][entry.get('type')] += entry.get('amount', 0)
            categories[cat]['count'] += 1
        
        return {
            "entries": entries,
            "summary": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_cash_flow": net_flow,
                "transaction_count": len(entries),
                "period": f"Last {days} days"
            },
            "breakdown": {
                "income_transactions": len(income_entries),
                "expense_transactions": len(expense_entries),
                "categories": categories,
                "avg_transaction_size": sum(e.get('amount', 0) for e in entries) / max(len(entries), 1)
            },
            "filters_applied": {
                "type": transaction_type,
                "category": category,
                "days": days,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cash flow entries: {str(e)}")

@router.post("/entries")
async def create_cash_flow_entry(entry: CashFlowEntry) -> Dict[str, Any]:
    """Add new cash flow entry"""
    try:
        # Validate amount
        if entry.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        # Validate date format
        try:
            datetime.fromisoformat(entry.date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
            )
        
        # Create entry data
        entry_data = {
            "type": entry.type.value,
            "category": entry.category,
            "amount": entry.amount,
            "description": entry.description,
            "date": entry.date,
            "tags": entry.tags or []
        }
        
        # Save to database
        created_entry = await DatabaseService.add_cash_flow_entry(entry_data)
        
        return {
            "message": "Cash flow entry created successfully",
            "entry": created_entry
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating cash flow entry: {str(e)}")

@router.get("/summary")
async def get_cash_flow_summary(days: int = 30) -> Dict[str, Any]:
    """Get comprehensive cash flow summary"""
    try:
        entries = await DatabaseService.get_cash_flow(days)
        
        # Calculate totals
        income_entries = [e for e in entries if e.get('type') == 'income']
        expense_entries = [e for e in entries if e.get('type') == 'expense']
        
        total_income = sum(e.get('amount', 0) for e in income_entries)
        total_expenses = sum(e.get('amount', 0) for e in expense_entries)
        net_flow = total_income - total_expenses
        
        # Monthly burn rate
        monthly_burn_rate = (total_expenses / max(days, 1)) * 30
        
        # Cash flow by category
        income_categories = {}
        expense_categories = {}
        
        for entry in income_entries:
            cat = entry.get('category', 'Other')
            income_categories[cat] = income_categories.get(cat, 0) + entry.get('amount', 0)
        
        for entry in expense_entries:
            cat = entry.get('category', 'Other')
            expense_categories[cat] = expense_categories.get(cat, 0) + entry.get('amount', 0)
        
        # Weekly trends
        weekly_data = []
        for week in range(min(4, days // 7)):
            week_start = datetime.now() - timedelta(days=(week + 1) * 7)
            week_end = datetime.now() - timedelta(days=week * 7)
            
            week_entries = [
                e for e in entries 
                if week_start <= datetime.fromisoformat(e.get('date', '').replace('Z', '+00:00')) < week_end
            ]
            
            week_income = sum(e.get('amount', 0) for e in week_entries if e.get('type') == 'income')
            week_expenses = sum(e.get('amount', 0) for e in week_entries if e.get('type') == 'expense')
            
            weekly_data.append({
                "week": f"Week {week + 1}",
                "income": week_income,
                "expenses": week_expenses,
                "net": week_income - week_expenses,
                "start_date": week_start.strftime("%Y-%m-%d"),
                "end_date": week_end.strftime("%Y-%m-%d")
            })
        
        return {
            "period": f"Last {days} days",
            "overview": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_cash_flow": net_flow,
                "cash_flow_ratio": round(total_income / max(total_expenses, 1), 2),
                "monthly_burn_rate": round(monthly_burn_rate, 2)
            },
            "income_breakdown": {
                "categories": income_categories,
                "largest_source": max(income_categories.items(), key=lambda x: x[1])[0] if income_categories else None,
                "transaction_count": len(income_entries),
                "average_size": round(total_income / max(len(income_entries), 1), 2)
            },
            "expense_breakdown": {
                "categories": expense_categories,
                "largest_expense": max(expense_categories.items(), key=lambda x: x[1])[0] if expense_categories else None,
                "transaction_count": len(expense_entries),
                "average_size": round(total_expenses / max(len(expense_entries), 1), 2)
            },
            "trends": {
                "weekly_data": weekly_data,
                "trend_direction": "positive" if net_flow > 0 else "negative",
                "sustainability": "healthy" if monthly_burn_rate < total_income else "concerning"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cash flow summary: {str(e)}")

@router.get("/categories")
async def get_cash_flow_categories() -> Dict[str, Any]:
    """Get available cash flow categories with usage stats"""
    # Predefined categories with common business expenses/income
    categories = {
        "income": [
            {"name": "Sales Revenue", "description": "Product/service sales", "usage_count": 45},
            {"name": "Consulting", "description": "Consulting services", "usage_count": 12},
            {"name": "Investment", "description": "Investment returns", "usage_count": 3},
            {"name": "Grants", "description": "Government or private grants", "usage_count": 2},
            {"name": "Other Income", "description": "Other income sources", "usage_count": 8}
        ],
        "expense": [
            {"name": "Marketing", "description": "Advertising and promotion", "usage_count": 34},
            {"name": "Office Supplies", "description": "Office equipment and supplies", "usage_count": 28},
            {"name": "Software", "description": "Software subscriptions and licenses", "usage_count": 22},
            {"name": "Travel", "description": "Business travel expenses", "usage_count": 15},
            {"name": "Utilities", "description": "Internet, phone, electricity", "usage_count": 18},
            {"name": "Professional Services", "description": "Legal, accounting, consulting", "usage_count": 9},
            {"name": "Equipment", "description": "Hardware and equipment purchases", "usage_count": 6},
            {"name": "Other Expenses", "description": "Other business expenses", "usage_count": 12}
        ]
    }
    
    return {
        "categories": categories,
        "total_income_categories": len(categories["income"]),
        "total_expense_categories": len(categories["expense"]),
        "most_used_income": max(categories["income"], key=lambda x: x["usage_count"]),
        "most_used_expense": max(categories["expense"], key=lambda x: x["usage_count"])
    }

@router.get("/forecast")
async def get_cash_flow_forecast(months: int = 6) -> Dict[str, Any]:
    """Generate cash flow forecast"""
    try:
        # Get historical data for trend analysis
        historical_entries = await DatabaseService.get_cash_flow(90)  # 3 months of data
        
        if not historical_entries:
            # Return basic forecast with no historical data
            return {
                "forecast_period": f"{months} months",
                "methodology": "No historical data available",
                "monthly_projections": [
                    {
                        "month": f"Month {i+1}",
                        "projected_income": 5000,
                        "projected_expenses": 3500,
                        "net_flow": 1500,
                        "confidence": 0.3
                    }
                    for i in range(months)
                ],
                "summary": {
                    "total_projected_income": 5000 * months,
                    "total_projected_expenses": 3500 * months,
                    "cumulative_net_flow": 1500 * months,
                    "runway_months": "Unknown - insufficient data"
                }
            }
        
        # Calculate monthly averages from historical data
        monthly_income = sum(e.get('amount', 0) for e in historical_entries if e.get('type') == 'income') / 3
        monthly_expenses = sum(e.get('amount', 0) for e in historical_entries if e.get('type') == 'expense') / 3
        
        # Simple growth assumption (5% monthly growth for income, 3% for expenses)
        income_growth = 1.05
        expense_growth = 1.03
        
        monthly_projections = []
        for i in range(months):
            projected_income = monthly_income * (income_growth ** i)
            projected_expenses = monthly_expenses * (expense_growth ** i)
            net_flow = projected_income - projected_expenses
            
            monthly_projections.append({
                "month": f"Month {i+1}",
                "month_name": (datetime.now() + timedelta(days=30*i)).strftime("%B %Y"),
                "projected_income": round(projected_income, 2),
                "projected_expenses": round(projected_expenses, 2),
                "net_flow": round(net_flow, 2),
                "confidence": max(0.9 - (i * 0.1), 0.4)  # Decreasing confidence over time
            })
        
        total_income = sum(p["projected_income"] for p in monthly_projections)
        total_expenses = sum(p["projected_expenses"] for p in monthly_projections)
        cumulative_net = sum(p["net_flow"] for p in monthly_projections)
        
        # Calculate runway (how long until cash runs out)
        current_cash = 50000  # Mock current cash balance
        avg_monthly_burn = sum(p["projected_expenses"] for p in monthly_projections) / len(monthly_projections)
        runway_months = current_cash / avg_monthly_burn if avg_monthly_burn > 0 else float('inf')
        
        return {
            "forecast_period": f"{months} months",
            "methodology": "Based on 3-month historical average with growth projections",
            "monthly_projections": monthly_projections,
            "summary": {
                "total_projected_income": round(total_income, 2),
                "total_projected_expenses": round(total_expenses, 2),
                "cumulative_net_flow": round(cumulative_net, 2),
                "avg_monthly_income": round(total_income / months, 2),
                "avg_monthly_expenses": round(total_expenses / months, 2),
                "runway_months": round(runway_months, 1) if runway_months != float('inf') else "Indefinite"
            },
            "assumptions": {
                "income_growth_rate": "5% monthly",
                "expense_growth_rate": "3% monthly",
                "current_cash_balance": current_cash,
                "data_source": "3-month historical average"
            },
            "recommendations": [
                "Monitor actual vs projected performance monthly",
                "Consider diversifying income sources",
                "Review and optimize major expense categories",
                "Maintain cash reserves for unexpected expenses"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

@router.get("/budget-analysis")
async def get_budget_analysis(days: int = 30) -> Dict[str, Any]:
    """Analyze spending against budget targets"""
    # Mock budget targets (in production, these would be user-defined)
    budget_targets = {
        "Marketing": {"budget": 2000, "priority": "high"},
        "Software": {"budget": 800, "priority": "medium"},
        "Office Supplies": {"budget": 300, "priority": "low"},
        "Travel": {"budget": 1200, "priority": "medium"},
        "Utilities": {"budget": 400, "priority": "high"},
        "Professional Services": {"budget": 600, "priority": "medium"}
    }
    
    try:
        entries = await DatabaseService.get_cash_flow(days)
        expense_entries = [e for e in entries if e.get('type') == 'expense']
        
        # Calculate actual spending by category
        actual_spending = {}
        for entry in expense_entries:
            category = entry.get('category', 'Other')
            actual_spending[category] = actual_spending.get(category, 0) + entry.get('amount', 0)
        
        # Compare with budget
        budget_analysis = {}
        total_budget = 0
        total_actual = 0
        
        for category, budget_info in budget_targets.items():
            budget = budget_info["budget"]
            actual = actual_spending.get(category, 0)
            variance = actual - budget
            variance_percent = (variance / budget * 100) if budget > 0 else 0
            
            budget_analysis[category] = {
                "budget": budget,
                "actual": actual,
                "variance": variance,
                "variance_percent": round(variance_percent, 1),
                "status": "over" if variance > 0 else "under" if variance < -budget*0.1 else "on_track",
                "priority": budget_info["priority"],
                "utilization": round((actual / budget * 100), 1) if budget > 0 else 0
            }
            
            total_budget += budget
            total_actual += actual
        
        # Categories not in budget
        unbudgeted_spending = {
            cat: amount for cat, amount in actual_spending.items() 
            if cat not in budget_targets
        }
        
        return {
            "period": f"Last {days} days",
            "overview": {
                "total_budget": total_budget,
                "total_actual": total_actual,
                "total_variance": total_actual - total_budget,
                "budget_utilization": round((total_actual / total_budget * 100), 1) if total_budget > 0 else 0,
                "categories_over_budget": len([c for c in budget_analysis.values() if c["status"] == "over"]),
                "categories_under_budget": len([c for c in budget_analysis.values() if c["status"] == "under"])
            },
            "category_analysis": budget_analysis,
            "unbudgeted_spending": {
                "categories": unbudgeted_spending,
                "total": sum(unbudgeted_spending.values()),
                "percentage_of_total": round(sum(unbudgeted_spending.values()) / max(total_actual, 1) * 100, 1)
            },
            "alerts": [
                {
                    "category": cat,
                    "message": f"Over budget by ${abs(data['variance']):.0f} ({abs(data['variance_percent']):.1f}%)",
                    "severity": "high" if data['variance_percent'] > 20 else "medium"
                }
                for cat, data in budget_analysis.items()
                if data['status'] == 'over'
            ],
            "recommendations": [
                "Review over-budget categories and identify cost-saving opportunities",
                "Consider reallocating budget from under-utilized categories",
                "Set up automated alerts for budget thresholds",
                "Track unbudgeted spending and consider adding to formal budget"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing budget: {str(e)}")



