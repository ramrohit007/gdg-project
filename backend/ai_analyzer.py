import os
from typing import List, Dict
from dotenv import load_dotenv
import json

load_dotenv()

class AIAnalyzer:
    """Handles AI-based analysis using OpenAI API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not set. Using mock responses.")
    
    def _call_openai(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call OpenAI API or return mock response"""
        if not self.api_key:
            # Mock response for development
            return self._mock_ai_response(prompt)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return self._mock_ai_response(prompt)
    
    def _mock_ai_response(self, prompt: str) -> str:
        """Mock AI response for development/testing"""
        if "topics" in prompt.lower() or "syllabus" in prompt.lower():
            return json.dumps([
                "Mathematics Fundamentals",
                "Algebra and Equations",
                "Geometry and Trigonometry",
                "Calculus",
                "Statistics and Probability"
            ])
        elif "analyze" in prompt.lower() or "answer" in prompt.lower():
            return json.dumps({
                "Mathematics Fundamentals": 75.0,
                "Algebra and Equations": 80.0,
                "Geometry and Trigonometry": 65.0,
                "Calculus": 70.0,
                "Statistics and Probability": 85.0
            })
        return "{}"
    
    def extract_topics_from_syllabus(self, syllabus_text: str) -> List[str]:
        """
        Extract individual topics from syllabus text using AI
        """
        prompt = f"""Analyze the following syllabus text and extract all individual topics/subjects.
        Return ONLY a JSON array of topic names, nothing else.
        Each topic should be a clear, distinct subject area.
        
        Syllabus text:
        {syllabus_text[:3000]}  # Limit to first 3000 chars
        
        Return format: ["Topic 1", "Topic 2", "Topic 3", ...]
        """
        
        response = self._call_openai(prompt, max_tokens=500)
        
        try:
            # Try to parse JSON response
            topics = json.loads(response)
            if isinstance(topics, list):
                return topics
            else:
                # If response is not a list, try to extract topics from text
                return self._extract_topics_from_text(response)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract topics from text
            return self._extract_topics_from_text(response)
    
    def _extract_topics_from_text(self, text: str) -> List[str]:
        """Fallback method to extract topics from text"""
        # Simple extraction: look for numbered items or bullet points
        lines = text.split('\n')
        topics = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                # Remove common prefixes
                for prefix in ['-', '*', '•', '1.', '2.', '3.', '4.', '5.']:
                    if line.startswith(prefix):
                        line = line[len(prefix):].strip()
                if line:
                    topics.append(line)
        
        return topics[:20]  # Limit to 20 topics
    
    def analyze_answer_sheet(self, answer_text: str, topics: List[str]) -> Dict[str, float]:
        """
        Analyze answer sheet and determine understanding score for each topic
        Returns a dictionary mapping topic names to scores (0-100)
        """
        prompt = f"""Analyze the following student answer sheet and determine the student's understanding level for each topic.
        Score each topic from 0-100 based on:
        - Correctness of answers related to the topic
        - Depth of understanding demonstrated
        - Completeness of responses
        
        Topics to analyze:
        {json.dumps(topics)}
        
        Answer sheet text:
        {answer_text[:4000]}  # Limit to first 4000 chars
        
        Return ONLY a JSON object with topic names as keys and scores (0-100) as values.
        Format: {{"Topic 1": 75.5, "Topic 2": 80.0, ...}}
        """
        
        response = self._call_openai(prompt, max_tokens=1000)
        
        try:
            scores = json.loads(response)
            if isinstance(scores, dict):
                # Ensure all topics have scores
                result = {}
                for topic in topics:
                    result[topic] = scores.get(topic, 0.0)
                return result
            else:
                return self._mock_scores(topics)
        except json.JSONDecodeError:
            return self._mock_scores(topics)
    
    def _mock_scores(self, topics: List[str]) -> Dict[str, float]:
        """Generate mock scores for development"""
        import random
        return {topic: round(random.uniform(60, 95), 1) for topic in topics}

