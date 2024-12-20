from typing import Any, Optional
from fastapi import HTTPException
from core.config import settings
from openai import OpenAI
import json


async def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the LLM and returns the response.

    Args:
        prompt (str): The input prompt for the LLM.

    Returns:
        str: The LLM's response.

    Raises:
        HTTPException: If there's an issue with the LLM call.
    """
    try:
        client = OpenAI(api_key=settings.openai_api_key)

        # Make the API call with default parameters
        response = client.chat.completions.create(
            model="gpt-4o",  # Replace with your desired model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Default value for creative but focused output
            max_tokens=1000,  # Adjust based on your typical response length
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract the content from the response
        llm_content = response.choices[0].message.content

        # Clean up the response (remove markdown formatting)
        cleaned_content = llm_content.strip("```").strip()
        if cleaned_content.startswith("json"):
            cleaned_content = cleaned_content[len("json") :].strip()

        # Parse the cleaned content as JSON
        parsed_response = json.loads(cleaned_content)

        return parsed_response

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing LLM response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the LLM: {str(e)}")
