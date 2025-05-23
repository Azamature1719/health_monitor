from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager
from src.database import create_tables, delete_tables, get_db_session
from src.routers import main_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
import json
from fastapi.middleware.cors import CORSMiddleware
from src.repositories import ServiceRepository

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
   await delete_tables()
   print("База очищена")
   await create_tables()
   print("База готова")
   await init_services()
   yield
   
app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        body = await request.body()
        
        if body:
            body_str = body.decode('utf-8')
            try:
                json_body = json.loads(body_str)
                logger.info(f"Request body (JSON): {json.dumps(json_body, indent=2)}")
            except:
                logger.info(f"Request body (raw): {body_str}")
                
        request._body = body
    except Exception as e:
        logger.error(f"Error logging request body: {str(e)}")
    
    response = await call_next(request)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        logging.error(f"Raw request body: {body_str}")
        
        try:
            json_body = await request.json()
            logging.error(f"JSON request body: {json_body}")
        except:
            logging.error("Could not parse request body as JSON")
    except Exception as e:
        logging.error(f"Error accessing request body: {str(e)}")
    
    logging.error(f"Validation errors: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def init_services():
    session = None
    async for session_obj in get_db_session():
        session = session_obj
        break
    
    if session:
        repo = ServiceRepository(session)
        existing_services = await repo.get_all_services()
        service_names = [service.name for service in existing_services]
        if "Первичный приём" not in service_names:
            await repo.add_service("Первичный приём")
        if "Повторный приём" not in service_names:
            await repo.add_service("Повторный приём")

@app.on_event("startup")
async def startup_event():
    await init_services()