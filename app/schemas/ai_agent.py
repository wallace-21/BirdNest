from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
        Request schema for chat endpoint
    """

    message: str = Field(..., min_length=1,
                         max_length=4000,
                         description="User message to send to AI agent")
    include_retrieval: bool = Field(
        default=True, description="Whether to include retrieval information")
    session_id: Optional[str] = Field(
        None, description="Optional session ID for conversation tracking")

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()


class ChatResponse(BaseModel):
    """
        Response schema for chat endpoint
    """

    success: bool = Field(...,
                          description="Whether the request was successful")
    responses: Optional[List[str]] = Field(None,
                                           description="AI agent responses")
    message_count: Optional[int] = Field(
        None, description="Number of responses returned")
    original_query: Optional[str] = Field(
        None, description="Sanitized version of original query")
    error: Optional[str] = Field(
        None, description="Error message if request failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow,
                                description="Response timestamp")
    processing_time: Optional[float] = Field(
        None, description="Processing time in seconds")


class HealthResponse(BaseModel):
    """
        Response schema for health check endpoint
    """

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow,
                                description="Health check timestamp")
    ai_agent_available: bool = Field(
        ..., description="Whether AI agent is available")
    version: str = Field(default="1.0.0", description="API version")
