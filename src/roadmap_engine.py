import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class RoadmapEngine:
    def __init__(self):
        """
        Initializes the Roadmap Engine with Gemini.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key.strip())
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_roadmap(self, current_skills, target_role):
        """
        Generates a learning roadmap from current skills to the target role.
        """
        if not hasattr(self, 'model'):
            return "Error: Gemini model not initialized. Check API Key."

        prompt = f"""
        Create a detailed step-by-step learning roadmap for a user who wants to become a {target_role}.
        
        Current Skills: {', '.join(current_skills)}
        
        The roadmap should include:
        1. Key concepts to learn.
        2. Recommended technologies/tools.
        3. Estimated time for each step.
        4. Project ideas to practice.
        5. **Recommended Courses**: Suggest specific courses (Coursera, Udemy, YouTube, etc.) for each major topic.
        6. **Mini-Quiz**: Generate 3-5 multiple-choice questions to test knowledge for each major section.
        
        Format the output clearly in Markdown. Use bolding and lists for readability.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating roadmap: {e}"

if __name__ == "__main__":
    # Test the engine
    engine = RoadmapEngine()
    skills = ["Python", "Basic SQL"]
    role = "Machine Learning Engineer"
    
    # Requires API key
    roadmap = engine.generate_roadmap(skills, role)
    print(roadmap)
