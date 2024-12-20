from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union, List, Optional
from models.operation_models import Course
from .query_LLM import call_llm
import json


# Take Ass


async def compose_evaluation(
    db: Session,
    assignment_id: int,
    course_id: int,
    question_number: int,
    # chapters: Optional[str],
):
    """
    Generate evaluation questions from course content using LLM.

    Args:
        db (Session): Database session.
        assignment_id (int): Assignment ID.
        course_id (int): ID of the course.
        question_number (int): Number of questions to generate.
        chapterss (Union[str, List[str]], optional): Single chapters or list of chaptersss.

    Returns:
        dict: Generated questions in the specified format.
    """
    # Step 1: Fetch the course by ID
    course = db.query(Course).filter(Course.id == course_id).first()

    # Step 2: Fetch the assignment by ID
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    # Step 3: Fetch the course content based on chapterss
    if not course:
        raise HTTPException(
            status_code=404, detail=f"Course with ID {course_id} not found."
        )

    # Step 2: Retrieve course content based on chapterss
    # if chapters:
    #     if isinstance(chapters, str):
    #         chapters_to_consider = [chapters]
    #     elif isinstance(chapters, list):
    #         chapters_to_consider = chapters
    #     else:
    #         raise HTTPException(
    #             status_code=400, detail="Invalid chapters type provided."
    #         )

    #     content = "\n".join(
    #         [
    #             chapters_content
    #             for chapters_content in course.course_chapters
    #             if chapters_content["name"] in chapters_to_consider
    #         ]
    #     )

    #     if not content:
    #         raise HTTPException(
    #             status_code=400,
    #             detail=f"None of the specified chapterss were found: {chapters_to_consider}.",
    #         )
    # else:

    content = course.course_chapters  # Whole course content

    # Step 3: Construct the prompt in French
    prompt = (
        f"Vous êtes un assistant pédagogique générant des questions d'évaluation et des réponses à partir des supports de cours. "
        f"Sur la base du contenu suivant, générez une liste de {question_number} questions et leurs réponses correctes en français.\n"
        f"La somme des points attribués à chaque question doit etre égale à {assignment.points}. \n\n"
        f"{content}\n\n"
        "Utilisez le format suivant :\n"
        "{\n"
        f'  "assignment_id": {assignment_id},\n'
        '  "questions": [\n'
        "    {\n"
        '      "question_text": "string",\n'
        '      "max_points": 0,\n'
        '      "teacher_answers": [\n'
        "        {'answer_text' : 'string'}\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    # Step 4: Call the LLM to generate questions and answers
    try:
        response = await call_llm(prompt)  # <-- Ensure call_llm is awaited properly
        # # Parse the response into a dictionary
        # parsed_response = json.loads(response)
        print(f"LLM response: {response}")  # Debugging log
        # Validate and append the assignment ID
        if "questions" in response:
            print(f"LLM response: {response}")
            return response

        else:
            raise ValueError("Invalid response structure from LLM.")

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing LLM response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
