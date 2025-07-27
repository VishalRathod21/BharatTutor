import os
import logging
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key."""
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
    def answer_question(self, question: str, context: str, subject: str, class_level: str) -> str:
        """Generate answer for student question with NCERT context."""
        try:
            prompt = f"""
            You are an AI tutor for Indian students following the NCERT curriculum. 
            
            Student Details:
            - Class: {class_level}
            - Subject: {subject}
            
            Question: {question}
            
            Relevant NCERT Context: {context}
            
            Instructions:
            1. Provide a clear, age-appropriate answer based on NCERT curriculum
            2. Use simple language suitable for the student's class level
            3. Include examples where helpful
            4. If the question is beyond the curriculum, gently guide to appropriate level
            5. Always be encouraging and supportive
            
            Answer:
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "I'm sorry, I couldn't generate an answer. Please try rephrasing your question."
            
        except Exception as e:
            logging.error(f"Error in answer_question: {e}")
            return f"Error generating answer: {str(e)}"
    
    def explain_topic(self, topic: str, context: str, subject: str, class_level: str, explanation_type: str) -> str:
        """Generate topic explanation based on NCERT curriculum."""
        try:
            type_instructions = {
                "Summary": "Provide a concise overview of the topic covering main points",
                "Detailed": "Give a comprehensive explanation with examples and applications",
                "Step-by-step": "Break down the topic into easy-to-follow steps"
            }
            
            prompt = f"""
            You are an AI tutor for Indian students following the NCERT curriculum.
            
            Student Details:
            - Class: {class_level}
            - Subject: {subject}
            
            Topic to Explain: {topic}
            
            Relevant NCERT Context: {context}
            
            Explanation Type: {explanation_type}
            Instructions: {type_instructions.get(explanation_type, 'Provide a clear explanation')}
            
            Additional Guidelines:
            1. Use language appropriate for {class_level} students
            2. Include relevant examples and analogies
            3. Structure the explanation clearly
            4. Connect to real-world applications where possible
            5. Ensure accuracy according to NCERT standards
            
            Explanation:
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "I'm sorry, I couldn't generate an explanation. Please try again."
            
        except Exception as e:
            logging.error(f"Error in explain_topic: {e}")
            return f"Error generating explanation: {str(e)}"
    
    def provide_homework_help(self, problem: str, context: str, subject: str, class_level: str, help_type: str) -> str:
        """Provide homework assistance based on the type of help requested."""
        try:
            help_instructions = {
                "Step-by-step solution": "Provide a complete step-by-step solution with explanations",
                "Concept explanation": "Explain the underlying concepts needed to solve this problem",
                "Hint only": "Give helpful hints to guide the student without giving away the answer",
                "Similar examples": "Provide similar examples to help understand the pattern"
            }
            
            prompt = f"""
            You are an AI tutor helping Indian students with their homework based on NCERT curriculum.
            
            Student Details:
            - Class: {class_level}
            - Subject: {subject}
            
            Homework Problem: {problem}
            
            Relevant NCERT Context: {context}
            
            Help Type Requested: {help_type}
            Instructions: {help_instructions.get(help_type, 'Provide appropriate help')}
            
            Guidelines:
            1. Help the student learn, don't just give answers
            2. Use teaching methods appropriate for {class_level}
            3. Encourage independent thinking
            4. Relate to NCERT curriculum standards
            5. Be patient and supportive
            
            Help Response:
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "I'm sorry, I couldn't generate help. Please try rephrasing your problem."
            
        except Exception as e:
            logging.error(f"Error in provide_homework_help: {e}")
            return f"Error generating help: {str(e)}"
