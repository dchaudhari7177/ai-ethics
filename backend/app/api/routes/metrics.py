from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime, timedelta

from app.db.base import get_db
from app.models.resume import Resume, Analysis, BiasMetrics
from app.core.logging import logger

router = APIRouter()

@router.get("/summary")
async def get_metrics_summary(
    db: Session = Depends(get_db)
):
    """Get summary of all metrics."""
    try:
        # Get total counts
        total_resumes = db.query(func.count(Resume.id)).scalar()
        total_shortlisted = db.query(func.count(Analysis.id)).filter(
            Analysis.decision == "shortlist"
        ).scalar()
        
        # Get average metrics
        avg_metrics = db.query(
            func.avg(BiasMetrics.demographic_parity).label('avg_demographic_parity'),
            func.avg(BiasMetrics.equal_opportunity).label('avg_equal_opportunity'),
            func.avg(BiasMetrics.disparate_impact).label('avg_disparate_impact')
        ).first()
        
        # Get mitigation statistics
        mitigation_stats = db.query(
            BiasMetrics.mitigation_applied,
            func.count(BiasMetrics.id).label('count')
        ).group_by(BiasMetrics.mitigation_applied).all()
        
        return {
            "total_resumes": total_resumes,
            "total_shortlisted": total_shortlisted,
            "shortlist_rate": total_shortlisted / total_resumes if total_resumes > 0 else 0,
            "average_metrics": {
                "demographic_parity": avg_metrics[0] or 0,
                "equal_opportunity": avg_metrics[1] or 0,
                "disparate_impact": avg_metrics[2] or 0
            },
            "mitigation_statistics": {
                stat[0] or "none": stat[1]
                for stat in mitigation_stats
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting metrics summary"
        )

@router.get("/trends")
async def get_metrics_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get trends of metrics over time."""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily metrics
        daily_metrics = db.query(
            func.date_trunc('day', BiasMetrics.created_at).label('date'),
            func.avg(BiasMetrics.demographic_parity).label('demographic_parity'),
            func.avg(BiasMetrics.equal_opportunity).label('equal_opportunity'),
            func.avg(BiasMetrics.disparate_impact).label('disparate_impact'),
            func.count(BiasMetrics.id).label('total_analyses')
        ).filter(
            BiasMetrics.created_at >= start_date
        ).group_by(
            func.date_trunc('day', BiasMetrics.created_at)
        ).order_by(
            func.date_trunc('day', BiasMetrics.created_at)
        ).all()
        
        return [{
            "date": metric[0].strftime("%Y-%m-%d"),
            "metrics": {
                "demographic_parity": metric[1] or 0,
                "equal_opportunity": metric[2] or 0,
                "disparate_impact": metric[3] or 0
            },
            "total_analyses": metric[4]
        } for metric in daily_metrics]
        
    except Exception as e:
        logger.error(f"Error getting metrics trends: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting metrics trends"
        )

@router.get("/protected-attributes")
async def get_protected_attributes_impact(
    db: Session = Depends(get_db)
):
    """Get impact of protected attributes on decisions."""
    try:
        # Get all bias metrics with protected attributes
        metrics = db.query(BiasMetrics).filter(
            BiasMetrics.protected_attributes.is_not(None)
        ).all()
        
        # Analyze impact by protected attribute
        attribute_impact = {}
        
        for metric in metrics:
            for attr, value in metric.protected_attributes.items():
                if attr not in attribute_impact:
                    attribute_impact[attr] = {
                        "total": 0,
                        "demographic_parity": [],
                        "equal_opportunity": [],
                        "disparate_impact": []
                    }
                
                attribute_impact[attr]["total"] += 1
                attribute_impact[attr]["demographic_parity"].append(
                    metric.demographic_parity
                )
                attribute_impact[attr]["equal_opportunity"].append(
                    metric.equal_opportunity
                )
                attribute_impact[attr]["disparate_impact"].append(
                    metric.disparate_impact
                )
        
        # Calculate averages
        for attr in attribute_impact:
            attribute_impact[attr]["avg_demographic_parity"] = sum(
                attribute_impact[attr]["demographic_parity"]
            ) / len(attribute_impact[attr]["demographic_parity"])
            
            attribute_impact[attr]["avg_equal_opportunity"] = sum(
                attribute_impact[attr]["equal_opportunity"]
            ) / len(attribute_impact[attr]["equal_opportunity"])
            
            attribute_impact[attr]["avg_disparate_impact"] = sum(
                attribute_impact[attr]["disparate_impact"]
            ) / len(attribute_impact[attr]["disparate_impact"])
            
            # Clean up lists to reduce response size
            del attribute_impact[attr]["demographic_parity"]
            del attribute_impact[attr]["equal_opportunity"]
            del attribute_impact[attr]["disparate_impact"]
        
        return attribute_impact
        
    except Exception as e:
        logger.error(f"Error analyzing protected attributes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error analyzing protected attributes"
        ) 