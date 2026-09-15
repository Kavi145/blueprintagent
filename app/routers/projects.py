from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.services.llm_agent import generate_execution_plan
from app.services.doc_generator import create_blueprint_docx

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
async def create_project(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    user_request = body.get("user_request")
    
    if not user_request:
        raise HTTPException(status_code=400, detail="user_request is required")

    # 1. Generate plan via Gemini REST API
    plan_data = generate_execution_plan(user_request)
    
    # 2. Save to SQLite database
    project = Project(
        title=plan_data.get("title", "Generated Project"),
        user_request=user_request,
        plan_data=plan_data
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "title": project.title,
        "user_request": project.user_request,
        "plan_data": project.plan_data
    }

@router.get("/{project_id}/download")
def download_project_docx(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    docx_stream = create_blueprint_docx(project.plan_data)
    
    return StreamingResponse(
        docx_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=project_{project.id}_blueprint.docx"}
    )