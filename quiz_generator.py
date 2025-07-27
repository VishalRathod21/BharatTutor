import json
import logging
from typing import Dict, List, Any
from gemini_client import GeminiClient

class QuizGenerator:
    def __init__(self, gemini_client: GeminiClient):
        """Initialize quiz generator with Gemini client."""
        self.gemini_client = gemini_client
    
    def generate_quiz(self, chapter: str, subject: str, class_level: str, 
                     num_questions: int, difficulty: str, question_type: str) -> dict:
        """Generate a quiz based on the specified parameters."""
        try:
            prompt = self._create_quiz_prompt(
                chapter, subject, class_level, num_questions, difficulty, question_type
            )
            
            response = self.gemini_client.client.models.generate_content(
                model=self.gemini_client.model,
                contents=prompt
            )
            
            if response.text:
                # Parse the response to extract quiz data
                quiz_data = self._parse_quiz_response(response.text, question_type)
                return quiz_data
            else:
                return {"error": "Failed to generate quiz"}
                
        except Exception as e:
            logging.error(f"Error generating quiz: {e}")
            return {"error": f"Error generating quiz: {str(e)}"}
    
    def _create_quiz_prompt(self, chapter: str, subject: str, class_level: str,
                           num_questions: int, difficulty: str, question_type: str) -> str:
        """Create prompt for quiz generation."""
        
        question_format = {
            "Multiple Choice": "Provide 4 options (A, B, C, D) with one correct answer",
            "True/False": "Create statements that can be answered with True or False",
            "Short Answer": "Create questions requiring brief written answers"
        }
        
        prompt = f"""
        You are an AI tutor creating a quiz for Indian students following NCERT curriculum.
        
        Quiz Parameters:
        - Subject: {subject}
        - Class: {class_level}
        - Chapter/Topic: {chapter}
        - Number of Questions: {num_questions}
        - Difficulty: {difficulty}
        - Question Type: {question_type}
        
        Instructions:
        1. Create {num_questions} questions based on {chapter} from {subject} {class_level} NCERT curriculum
        2. {question_format.get(question_type, 'Create appropriate questions')}
        3. Ensure questions are age-appropriate for {class_level} students
        4. Make difficulty level {difficulty}
        5. Include clear, unambiguous questions
        6. For multiple choice, ensure only one option is clearly correct
        
        Format your response as follows:
        
        Question 1: [Question text]
        {self._get_answer_format(question_type)}
        Correct Answer: [Answer]
        
        Question 2: [Question text]
        {self._get_answer_format(question_type)}
        Correct Answer: [Answer]
        
        Continue for all {num_questions} questions.
        
        Generate Quiz:
        """
        
        return prompt
    
    def _get_answer_format(self, question_type: str) -> str:
        """Get the answer format based on question type."""
        if question_type == "Multiple Choice":
            return "A) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]"
        elif question_type == "True/False":
            return "Options: True / False"
        else:  # Short Answer
            return "Answer: [Brief answer expected]"
    
    def _parse_quiz_response(self, response_text: str, question_type: str) -> Dict[str, Any]:
        """Parse the AI response to extract quiz questions and answers."""
        try:
            questions: List[Dict[str, Any]] = []
            lines = response_text.split('\n')
            current_question: Dict[str, Any] = {}
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('Question '):
                    # Save previous question if exists
                    if current_question:
                        questions.append(current_question)
                    
                    # Start new question
                    question_text = line.split(':', 1)[1].strip() if ':' in line else line
                    current_question = {"question": question_text}
                    
                    if question_type == "Multiple Choice":
                        current_question["options"] = []
                
                elif question_type == "Multiple Choice" and line.startswith(('A)', 'B)', 'C)', 'D)')):
                    option_text = line[2:].strip()  # Remove "A)" prefix
                    if "options" not in current_question:
                        current_question["options"] = []
                    current_question["options"].append(option_text)
                
                elif line.startswith('Correct Answer:'):
                    answer = line.replace('Correct Answer:', '').strip()
                    current_question["correct_answer"] = answer
            
            # Add the last question
            if current_question:
                questions.append(current_question)
            
            quiz_data = {
                "questions": questions,
                "total_questions": len(questions),
                "question_type": question_type
            }
            
            return quiz_data
            
        except Exception as e:
            logging.error(f"Error parsing quiz response: {e}")
            # Return a fallback quiz structure
            return {
                "questions": [
                    {
                        "question": "Sample question about the topic",
                        "options": ["Option A", "Option B", "Option C", "Option D"] if question_type == "Multiple Choice" else None,
                        "correct_answer": "Option A" if question_type == "Multiple Choice" else "True"
                    }
                ],
                "total_questions": 1,
                "question_type": question_type,
                "error": "Quiz parsing failed, showing sample question"
            }
    
    def evaluate_quiz(self, quiz_data: dict, user_answers: list) -> dict:
        """Evaluate user's quiz answers and provide feedback."""
        try:
            correct_count = 0
            total_questions = len(quiz_data["questions"])
            detailed_results = []
            
            for i, question in enumerate(quiz_data["questions"]):
                user_answer = user_answers[i] if i < len(user_answers) else ""
                correct_answer = question.get("correct_answer", "")
                
                is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
                if is_correct:
                    correct_count += 1
                
                detailed_results.append({
                    "question": question["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct
                })
            
            score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            
            return {
                "score": correct_count,
                "total": total_questions,
                "percentage": score_percentage,
                "detailed_results": detailed_results,
                "feedback": self._generate_feedback(score_percentage)
            }
            
        except Exception as e:
            logging.error(f"Error evaluating quiz: {e}")
            return {"error": f"Error evaluating quiz: {str(e)}"}
    
    def _generate_feedback(self, percentage: float) -> str:
        """Generate encouraging feedback based on quiz performance."""
        if percentage >= 90:
            return "Excellent work! You have a strong understanding of the topic. 🌟"
        elif percentage >= 75:
            return "Great job! You're doing well. Review the incorrect answers to improve further. 👍"
        elif percentage >= 60:
            return "Good effort! Keep practicing to strengthen your understanding. 📚"
        elif percentage >= 40:
            return "You're making progress! Spend more time reviewing the concepts. 💪"
        else:
            return "Don't worry! Learning takes time. Review the material and try again. 🌱"
