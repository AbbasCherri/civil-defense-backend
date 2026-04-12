from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import io
import os

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors

from app.core.database import get_db
from app.core.security import get_current_user
from app.repositories import IncidentRepository
from app.models import UserRole, IncidentStatus

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/daily")
async def get_daily_reports(
    date: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get daily incident statistics in JSON format."""
    if current_user["role"] not in [UserRole.ADMIN, UserRole.DISPATCHER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Parse date or use today
    if date:
        try:
            target_date = datetime.fromisoformat(date).date()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    else:
        target_date = datetime.utcnow().date()
    
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())
    
    incident_repo = IncidentRepository(db)
    incidents = await incident_repo.get_by_date_range(start_of_day, end_of_day)
    
    # Calculate statistics
    total_incidents = len(incidents)
    active_incidents = len([i for i in incidents if i.status == IncidentStatus.ACTIVE])
    closed_incidents = len([i for i in incidents if i.status == IncidentStatus.CLOSED])
    waiting_incidents = len([i for i in incidents if i.status == IncidentStatus.WAITING])
    
    category_breakdown = {}
    for incident in incidents:
        category = incident.category.value
        category_breakdown[category] = category_breakdown.get(category, 0) + 1
    
    priority_breakdown = {}
    for incident in incidents:
        priority = incident.priority.value
        priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
    
    return {
        "date": str(target_date),
        "total_incidents": total_incidents,
        "status_breakdown": {
            "waiting": waiting_incidents,
            "active": active_incidents,
            "closed": closed_incidents
        },
        "category_breakdown": category_breakdown,
        "priority_breakdown": priority_breakdown,
        "incidents": [
            {
                "id": i.id,
                "category": i.category.value,
                "priority": i.priority.value,
                "status": i.status.value,
                "description": i.description,
                "created_at": i.created_at.isoformat()
            }
            for i in incidents
        ]
    }


@router.get("/export/pdf")
async def export_pdf_report(
    start_date: str = None,
    end_date: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Export incident report as PDF."""
    if current_user["role"] not in [UserRole.ADMIN, UserRole.DISPATCHER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Parse dates
    try:
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start = datetime.utcnow().replace(day=1)  # First day of current month
        
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            end = datetime.utcnow()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    
    # Fetch closed incidents in date range
    incident_repo = IncidentRepository(db)
    all_incidents = await incident_repo.get_by_date_range(start, end)
    incidents = [i for i in all_incidents if i.status == IncidentStatus.CLOSED]
    
    # Generate PDF
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2ca02c'),
        spaceAfter=12
    )
    
    # Build document content
    content = []
    
    # Title
    title = Paragraph("Civil Defense Emergency Management System<br/>Incident Report", title_style)
    content.append(title)
    content.append(Spacer(1, 0.3*inch))
    
    # Report date range
    date_text = Paragraph(
        f"<b>Report Period:</b> {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}<br/>"
        f"<b>Generated on:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    )
    content.append(date_text)
    content.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    content.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ["Metric", "Value"],
        ["Total Closed Incidents", str(len(incidents))],
        ["Report Period", f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"],
    ]
    
    # Category breakdown
    category_breakdown = {}
    priority_breakdown = {}
    for incident in incidents:
        category = incident.category.value
        priority = incident.priority.value
        category_breakdown[category] = category_breakdown.get(category, 0) + 1
        priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
    
    for category, count in category_breakdown.items():
        summary_data.append([f"Incidents - {category}", str(count)])
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    content.append(summary_table)
    content.append(Spacer(1, 0.3*inch))
    
    # Detailed Incidents Table
    content.append(Paragraph("Detailed Incident Records", heading_style))
    
    if incidents:
        incident_data = [
            ["ID", "Category", "Priority", "Location", "Description", "Closed Date"]
        ]
        
        for incident in incidents:
            incident_data.append([
                str(incident.id),
                incident.category.value,
                incident.priority.value,
                f"({incident.latitude:.4f}, {incident.longitude:.4f})",
                incident.description[:50] + "..." if len(incident.description) > 50 else incident.description,
                incident.closed_at.strftime('%Y-%m-%d %H:%M') if incident.closed_at else "N/A"
            ])
        
        incident_table = Table(incident_data, colWidths=[0.6*inch, 1*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1*inch])
        incident_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        content.append(incident_table)
    else:
        content.append(Paragraph("No closed incidents found for the specified date range.", styles['Normal']))
    
    # Build PDF
    doc.build(content)
    pdf_buffer.seek(0)
    
    filename = f"incident_report_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.pdf"
    
    return StreamingResponse(
        iter([pdf_buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
