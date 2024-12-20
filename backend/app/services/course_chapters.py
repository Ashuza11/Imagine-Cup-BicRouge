from typing import List
import json
from fastapi import HTTPException
from .query_LLM import call_llm


async def extract_chapters_from_syllabus(syllabus_content: str) -> List[dict]:
    """
    Extracts chapters from the syllabus content using the LLM.

    Args:
        syllabus_content (str): The text content of the syllabus.

    Returns:
        List[dict]: A list of chapters with their details.
    """
    # Provide a clear example of the expected output in the prompt
    prompt = f"""
    Extract chapters from the following syllabus text and return them in the exact JSON format shown below:
    
    Example:
    ```json
         [
            {{
                "number": 1,
                "title": "Introduction",
                "content": "This is the first chapter content."
            }},
            {{
                "number": 2,
                "title": "Chapter Title",
                "content": "This is the second chapter content."
            }}
        ]
    ```

    Now, extract the chapters from this syllabus content:
    {syllabus_content}
    """

    response = await call_llm(prompt)

    # Log the response for debugging
    print(f"LLM response: {response}")

    # If the response is already a dictionary, return it directly
    if isinstance(response, dict):
        return response

    # Parse the JSON response safely
    try:
        return response
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing LLM response: {str(e)}"
        )
