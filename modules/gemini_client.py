import os
import logging
import time
from typing import Optional, Dict, Any

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold

class GeminiClient:
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key."""
        try:
            # Configure the Gemini API with retry logic
            genai.configure(api_key=api_key)
            
            # List available models
            print("Listing available models...")
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    print(f"Model: {model.name}, Supports generateContent: {model.supported_generation_methods}")
            
            # Try to use the most capable available model
            model_name = 'gemini-1.5-flash'  # Try the latest model first
            
            # Initialize the model
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            self.chat = self.model.start_chat(history=[])
            logging.info(f"Gemini client initialized with model: {model_name}")
        except Exception as e:
            logging.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
        
    def answer_question(self, question: str, context: str, subject: str, class_level: str, max_retries: int = 3) -> str:
        """Generate answer for student question with NCERT context."""
        if not question.strip():
            return "Please enter a valid question."
        for attempt in range(max_retries):
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
                
                Answer in markdown format with proper formatting:
                """
                
                response = self.model.generate_content(prompt)
                
                # Handle different response formats
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'parts'):
                    return ' '.join(part.text for part in response.parts if hasattr(part, 'text'))
                elif hasattr(response, 'candidates') and response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    return "I'm sorry, I couldn't generate an answer. Please try rephrasing your question."
                    
            except Exception as e:
                if "quota" in str(e).lower() and attempt < max_retries - 1:
                    # Wait before retrying
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.warning(f"Rate limit hit, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                error_msg = f"Error generating answer: {str(e)}"
                logging.error(error_msg)
                return f"I encountered an error: {error_msg}"
            
            except Exception as e:
                error_msg = f"Error in answer_question: {str(e)}"
                logging.error(error_msg)
                return f"Error: {error_msg}"
    
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
            
            response = self.model.generate_content(prompt)
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
            
            response = self.model.generate_content(prompt)
            return response.text or "I'm sorry, I couldn't generate help. Please try rephrasing your problem."
            
        except Exception as e:
            logging.error(f"Error in provide_homework_help: {e}")
            return f"Error generating help: {str(e)}"
