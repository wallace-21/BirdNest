import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
import sys
from .config import settings

# Configure logging
logger = logging.getLogger(__name__)


class BirdNestAIAgent:
    """
        AI agent for BirdNest application.
    """

    def __init__(self):
        """
            Initialize the AI agent with environment variables and validation
        """
        self.client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """
            Initialize OpenAI client with error handling.
        """
        try:
            # Validate environment variables
            agent_endpoint_base = settings.AGENT_ENDPOINT
            agent_access_key = settings.AGENT_ACCESS_KEY

            if not agent_endpoint_base:
                raise ValueError(
                    "AGENT_ENDPOINT environment variable is not set")

            if not agent_access_key:
                raise ValueError(
                    "AGENT_ACCESS_KEY environment variable is not set")

            # Endpoint URL
            agent_endpoint = agent_endpoint_base.rstrip('/') + "/api/v1/"

            # Initialize OpenAI client
            self.client = OpenAI(
                base_url=agent_endpoint,
                api_key=agent_access_key,
            )

            logger.info("AI Agent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize AI agent: {str(e)}")
            raise

    def _validate_input(self, user_input: str) -> bool:
        """
            Validate user input for safety and security.

            Args:
                user_input: The user's input string

            Returns:
                bool: True if input is valid, False otherwise
        """
        if not user_input or not isinstance(user_input, str):
            return False

        # Basic length validation
        if len(user_input.strip()) == 0:
            return False

        if len(user_input) > 4000:  # Reasonable limit
            logger.warning("Input too long, truncating")
            return False

        # Check for potentially harmful content patterns
        dangerous_patterns = [
            'import os',
            'exec(',
            'eval(',
            '__import__',
            'subprocess',
            'system(',
        ]

        user_input_lower = user_input.lower()
        for pattern in dangerous_patterns:
            if pattern in user_input_lower:
                logger.warning(
                    f"Potentially dangerous pattern detected: {pattern}")
                return False

        return True

    def _sanitize_input(self, user_input: str) -> str:
        """
            Sanitize user input by removing potentially harmful content.

            Args:
                user_input: Raw user input

            Returns:
                str: Sanitized input
        """
        # Strip whitespace and limit length
        sanitized = user_input.strip()[:4000]

        # Remove null bytes and control characters
        sanitized = ''.join(
            char for char in sanitized if ord(char) >= 32 or char in '\n\t')

        return sanitized

    def query_agent(self, user_input: str, include_retrieval: bool = True
                    ) -> Optional[Dict[str, Any]]:
        """
            Send a query to the AI agent with proper error handling.

            Args:
                user_input: The user's question or prompt
                include_retrieval: Whether to include retrieval information

            Returns:
                Dict containing response and metadata, or None if error
        """
        try:
            # Validate and sanitize input
            if not self._validate_input(user_input):
                logger.error("Invalid input provided")
                return {
                    "error": "Invalid input. Please provide a valid question.",
                    "success": False
                }

            sanitized_input = self._sanitize_input(user_input)

            # Prepare extra body parameters
            extra_body = {}
            if include_retrieval:
                extra_body["include_retrieval_info"] = True

            # Make API call
            logger.info(
                f"Sending query to AI agent: {sanitized_input[:100]}...")

            response = self.client.chat.completions.create(
                model="n/a",  # Using default model
                messages=[{
                    "role": "user",
                    "content": sanitized_input
                }],
                extra_body=extra_body
            )

            # Process response
            results = []
            for choice in response.choices:
                if choice.message and choice.message.content:
                    results.append(choice.message.content)

            logger.info("Query completed successfully")

            return {
                "success": True,
                "responses": results,
                "message_count": len(results),
                "original_query": sanitized_input[:100] + "..." if len(
                    sanitized_input) > 100 else sanitized_input
            }

        except Exception as e:
            logger.error(f"Error querying AI agent: {str(e)}")
            return {
                "error": f"Failed to process query: {str(e)}",
                "success": False
            }
