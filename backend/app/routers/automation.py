"""
Automation API endpoints
N8N integration and workflow management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

router = APIRouter()

class AutomationRule(BaseModel):
    name: str
    description: str
    trigger_type: str
    actions: List[Dict[str, Any]]
    conditions: Optional[Dict[str, Any]] = None
    schedule: Optional[str] = None
    enabled: bool = True

@router.get("/rules")
async def get_automation_rules() -> Dict[str, Any]:
    """Get all automation rules"""
    # Mock automation rules
    rules = [
        {
            "id": "1",
            "name": "Auto-post daily tips",
            "description": "Posts AI-generated business tips to LinkedIn every weekday at 9:00 AM",
            "trigger_type": "schedule",
            "schedule": "0 9 * * 1-5",
            "actions": [
                {"type": "generate_content", "platform": "linkedin"},
                {"type": "post_content", "platform": "linkedin"}
            ],
            "status": "active",
            "last_run": "2024-01-15T09:00:00Z",
            "next_run": "2024-01-16T09:00:00Z",
            "success_rate": 95.5
        },
        {
            "id": "2", 
            "name": "Engagement response",
            "description": "Automatically likes and responds to comments on Instagram posts",
            "trigger_type": "webhook",
            "actions": [
                {"type": "like_comment"},
                {"type": "generate_response"},
                {"type": "post_response"}
            ],
            "status": "active",
            "last_run": "2024-01-15T14:30:00Z",
            "success_rate": 87.2
        },
        {
            "id": "3",
            "name": "Cross-platform sharing", 
            "description": "Automatically shares Instagram posts to Facebook and Twitter",
            "trigger_type": "event",
            "actions": [
                {"type": "adapt_content", "platforms": ["facebook", "twitter"]},
                {"type": "schedule_posts"}
            ],
            "status": "paused",
            "last_run": "2024-01-10T16:20:00Z",
            "success_rate": 76.8
        }
    ]
    
    return {
        "rules": rules,
        "total_rules": len(rules),
        "active_rules": len([r for r in rules if r["status"] == "active"]),
        "avg_success_rate": sum(r["success_rate"] for r in rules) / len(rules)
    }

@router.post("/rules")
async def create_automation_rule(rule: AutomationRule) -> Dict[str, Any]:
    """Create new automation rule"""
    try:
        # Validate rule configuration
        valid_triggers = ["schedule", "webhook", "event", "condition"]
        if rule.trigger_type not in valid_triggers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid trigger type. Must be one of: {valid_triggers}"
            )
        
        # Create rule (in production, this would integrate with N8N)
        new_rule = {
            "id": f"rule_{datetime.now().timestamp()}",
            "name": rule.name,
            "description": rule.description,
            "trigger_type": rule.trigger_type,
            "actions": rule.actions,
            "conditions": rule.conditions,
            "schedule": rule.schedule,
            "enabled": rule.enabled,
            "status": "active" if rule.enabled else "inactive",
            "created_at": datetime.now().isoformat(),
            "success_rate": 0.0
        }
        
        return {
            "message": "Automation rule created successfully",
            "rule": new_rule
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating automation rule: {str(e)}")

@router.get("/workflows/n8n")
async def get_n8n_workflows() -> Dict[str, Any]:
    """Get N8N workflow status and information"""
    # Mock N8N integration data
    workflows = [
        {
            "id": "wf_social_automation",
            "name": "Social Media Automation",
            "status": "active",
            "last_execution": "2024-01-15T14:30:00Z",
            "executions_today": 45,
            "success_rate": 94.2,
            "webhook_url": "https://n8n.your-domain.com/webhook/social-automation"
        },
        {
            "id": "wf_lead_processing", 
            "name": "Lead Processing Pipeline",
            "status": "active",
            "last_execution": "2024-01-15T15:15:00Z", 
            "executions_today": 12,
            "success_rate": 98.1,
            "webhook_url": "https://n8n.your-domain.com/webhook/lead-processing"
        },
        {
            "id": "wf_analytics_sync",
            "name": "Analytics Data Sync",
            "status": "active", 
            "last_execution": "2024-01-15T16:00:00Z",
            "executions_today": 8,
            "success_rate": 100.0,
            "webhook_url": "https://n8n.your-domain.com/webhook/analytics-sync"
        }
    ]
    
    return {
        "workflows": workflows,
        "total_workflows": len(workflows),
        "active_workflows": len([w for w in workflows if w["status"] == "active"]),
        "total_executions_today": sum(w["executions_today"] for w in workflows),
        "avg_success_rate": sum(w["success_rate"] for w in workflows) / len(workflows),
        "connection_status": "connected"
    }

@router.post("/trigger/{rule_id}")
async def trigger_automation_rule(rule_id: str) -> Dict[str, Any]:
    """Manually trigger an automation rule"""
    try:
        # In production, this would trigger the actual N8N workflow
        execution_id = f"exec_{datetime.now().timestamp()}"
        
        return {
            "message": f"Automation rule {rule_id} triggered successfully",
            "execution_id": execution_id,
            "status": "running",
            "triggered_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering automation: {str(e)}")

@router.get("/execution-history")
async def get_execution_history(limit: int = 50) -> Dict[str, Any]:
    """Get automation execution history"""
    # Mock execution history
    executions = []
    
    for i in range(limit):
        executions.append({
            "id": f"exec_{i+1}",
            "rule_name": ["Auto-post daily tips", "Engagement response", "Analytics sync"][i % 3],
            "status": ["success", "success", "failed", "success"][i % 4],
            "started_at": (datetime.now() - timedelta(hours=i)).isoformat(),
            "duration": f"{30 + (i % 60)}s",
            "actions_completed": 3 + (i % 2),
            "error_message": "API rate limit exceeded" if i % 4 == 2 else None
        })
    
    success_count = len([e for e in executions if e["status"] == "success"])
    
    return {
        "executions": executions,
        "total_executions": len(executions),
        "success_rate": round((success_count / len(executions)) * 100, 1),
        "recent_failures": [e for e in executions[:10] if e["status"] == "failed"],
        "avg_duration": "45s"
    }

@router.get("/metrics")
async def get_automation_metrics() -> Dict[str, Any]:
    """Get automation performance metrics"""
    return {
        "overview": {
            "total_automations": 12,
            "active_automations": 8,
            "executions_today": 156,
            "success_rate": 93.2,
            "time_saved_hours": 24.5
        },
        "performance": {
            "avg_execution_time": "42s",
            "fastest_automation": "Analytics sync (8s)",
            "slowest_automation": "Content generation (2m 15s)",
            "most_reliable": "Lead processing (99.1% success)"
        },
        "cost_savings": {
            "manual_hours_avoided": 24.5,
            "cost_per_hour": 25,
            "monthly_savings": 612.5,
            "roi_on_automation": "340%"
        },
        "upcoming_tasks": [
            {
                "name": "Daily tip post",
                "scheduled": "Tomorrow 9:00 AM",
                "estimated_duration": "45s"
            },
            {
                "name": "Analytics sync",
                "scheduled": "Every hour",
                "estimated_duration": "8s"
            }
        ]
    }

