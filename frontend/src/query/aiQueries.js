export const composeWithAiQuery = async ({ assignmentId, courseId, questionNumber = 5 }) => {
    const requestBody = {
      assignment_id: String(assignmentId),
      course_id: courseId ,
      questionNumber
    };
  
    const token = localStorage.getItem("awesomeToken");
    if (!token) {
      throw new Error("Missing authentication token");
    }
  
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      // body: JSON.stringify(requestBody),
    };
  
    const endpoint = `/api/assignments/${assignmentId}/compose_evaluation/?assignment_id=${assignmentId}&course_id=${courseId}&question_number=${questionNumber}`;
    const response = await fetch(endpoint, requestOptions);
    const data = await response.json();
  
    if (!response.ok) {
      console.log(data)
      throw new Error(data.detail || 'Composition with AI failed');
    }
  
    return data;
  };