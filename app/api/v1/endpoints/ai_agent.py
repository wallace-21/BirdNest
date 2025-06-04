from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer
import time
import logging
from typing import Optional

from app.core.ai_agent import BirdNestAIAgent
from app.schemas.ai_agent import ChatRequest, ChatResponse, HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer(auto_error=False)

# Global AI agent instance (initialize once)
ai_agent: Optional[BirdNestAIAgent] = None


def get_ai_agent() -> BirdNestAIAgent:
    """
        Dependency to get AI agent instance
    """
    global ai_agent
    if ai_agent is None:
        try:
            ai_agent = BirdNestAIAgent()
        except Exception as e:
            logger.error(f"Failed to initialize AI agent: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="AI Agent service is currently unavailable"
            )
    return ai_agent


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    agent: BirdNestAIAgent = Depends(get_ai_agent),

):
    """
        Send a message to the AI agent and get a response.

        - **message**: The message to send to the AI agent
        - **include_retrieval**: Whether to include
          retrieval information in the response
        - **session_id**: Optional session ID for conversation tracking
    """
    start_time = time.time()

    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")

        # Query the AI agent
        result = agent.query_agent(
            user_input=request.message,
            include_retrieval=request.include_retrieval
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to get response from AI agent"
            )

        processing_time = time.time() - start_time

        # Log conversation for analytics (background task)
        background_tasks.add_task(
            log_conversation,
            request.message,
            result,
            request.session_id,
            processing_time
        )

        # Return response
        return ChatResponse(
            success=result.get("success", False),
            responses=result.get("responses"),
            message_count=result.get("message_count"),
            original_query=result.get("original_query"),
            error=result.get("error"),
            processing_time=processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
        Check the health status of the AI agent service.
    """
    try:
        # Try to get AI agent instance
        agent = get_ai_agent()
        ai_agent_available = agent is not None and agent.client is not None

        return HealthResponse(
            status="healthy" if ai_agent_available else "unhealthy",
            ai_agent_available=ai_agent_available
        )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            ai_agent_available=False
        )


async def log_conversation(
    message: str,
    result: dict,
    session_id: Optional[str],
    processing_time: float
):
    """
        Background task to log conversation for analytics.
    """
    try:
        # Log conversation details
        log_data = {
            "message": message[:100],  # Truncate for privacy
            "success": result.get("success", False),
            "response_count": result.get("message_count", 0),
            "session_id": session_id,
            "processing_time": processing_time,
            "timestamp": time.time()
        }

        logger.info(f"Conversation logged: {log_data}")

        # Here you could save to database, send to analytics service or somen',
        # but I dont have enough time rn.

    except Exception as e:
        logger.error(f"Failed to log conversation: {str(e)}")
