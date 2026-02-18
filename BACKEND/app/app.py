import app.logging_config 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



from app.scheduler import start_scheduler
import uvicorn



from app.routes import admin_retention
from app.routes import admin_audit_routes
from app.routes import admin_security_routes
from app.routes import admin_files
from app.routes import log_sources, teams
from app.routes import file_formats
import app.models  
from app.routes.user_routes import router as user_router
from app.routes.file_upload import router as file_upload_router
from app.routes.log_processing import router as log_processing_router
from app.routes.admin_meta import router as metadata_router
from app.routes.admin_users import router as admin_users_router
from app.routes.admin_reports import router as admin_reports_router
from app.routes.files_user import router as files_user_router
from app.routes import user_stats
from app.routes import auth
from app.routes import admin_reports
from app.routes.file_formats import router as file_formats_router
from app.routes.log_sources import router as log_sources_router
from app.routes.teams import router as teams_router
from app.routes.admin_logs import router as admin_logs_router
from app.routes.lookups import router as lookups_router
app = FastAPI(
    title="Intelligent Log Management System",
    version="1.0.0",
    description="Centralized log upload, processing, search, and retention system"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(file_upload_router)
app.include_router(log_processing_router)
app.include_router(metadata_router)
app.include_router(auth.router)
app.include_router(admin_reports.router)
app.include_router(user_stats.router)
app.include_router(admin_users_router)
app.include_router(files_user_router)
app.include_router(file_formats_router)
app.include_router(log_sources_router)
app.include_router(teams_router)
app.include_router(admin_logs_router)
app.include_router(admin_reports.router)
app.include_router(admin_files.router)
app.include_router(admin_security_routes.router)
app.include_router(admin_audit_routes.router)
app.include_router(admin_retention.router)
app.include_router(lookups_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "service": "Intelligent Log Management System"
    }


@app.on_event("startup")
def startup_event():
    start_scheduler()


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.3.242", port=8000,reload=True)