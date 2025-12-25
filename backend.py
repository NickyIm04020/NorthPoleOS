import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

# --- 1. DATA MODELS ---
class UserStory(BaseModel):
    id: str
    role: str
    desire: str
    benefit: str
    acceptance_criteria: List[str]

class PRDStructure(BaseModel):
    project_name: str
    priority_level: str
    executive_summary: str
    user_stories: List[UserStory]
    risk_analysis: str

# --- 2. AI ENGINE (WITH SMART MOCK SYSTEM) ---
class NorthPoleEngine:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
            self.structured_llm = self.llm.with_structured_output(PRDStructure)
            self.api_active = True
        except:
            self.api_active = False

    def process_text_request(self, text):
        if self.api_active:
            try:
                prompt = f"Act as a Senior PM at North Pole Inc. Convert this wish into a strict Engineering PRD: {text}"
                return self.structured_llm.invoke(prompt)
            except Exception:
                pass # Fall through to mock if API fails (Error 429)
        
        # --- SMART MOCK SYSTEM (No API needed) ---
        text_lower = text.lower()
        
        # Scenario A: Cars/Vehicles
        if any(x in text_lower for x in ["bmw", "car", "ferrari", "porsche", "drive"]):
            return PRDStructure(
                project_name="Project Autobahn Sleigh (High-Speed Transport)",
                priority_level="CRITICAL (Naughty List Override)",
                executive_summary="Target Subject has requested a high-performance combustion vehicle. Reindeer velocity insufficient. Engineering recommends deploying the 'Ultimate Driving Machine' protocol.",
                risk_analysis="High risk of speeding tickets in residential zones.",
                user_stories=[
                    UserStory(id="TOY-884", role="Speed Enthusiast", desire="A BMW M5 Competition", benefit="To outrun Rudolph", acceptance_criteria=["V8 Engine", "0-60 < 3s", "Red Paint"]),
                    UserStory(id="TOY-885", role="Safety Officer", desire="Autonomous Drifting", benefit="Safe cookie consumption", acceptance_criteria=["Lidar Sensors", "Drift Mode"])
                ]
            )
        
        # Scenario B: Animals/Pets
        elif any(x in text_lower for x in ["pony", "dog", "cat", "unicorn", "pet"]):
            return PRDStructure(
                project_name="Project Bio-Synthetic Companion",
                priority_level="HIGH",
                executive_summary="Request for biological entity detected. Due to zoning laws, R&D suggests a 'Bio-Mimicry' android unit with hypoallergenic fur.",
                risk_analysis="Unit may require charging via carrot-interface.",
                user_stories=[
                    UserStory(id="PET-101", role="Lonely Child", desire="A Unicorn", benefit="Companionship", acceptance_criteria=["Must Sparkle", "Horn durability > 9000", "Low Maintenance"]),
                    UserStory(id="PET-102", role="Parent", desire="Volume Control", benefit="Peace and Quiet", acceptance_criteria=["Mute Button", "Self-Cleaning Mode"])
                ]
            )

        # Scenario C: Default (Robots/Tech)
        else:
            return PRDStructure(
                project_name="Project Cyber-Toy 9000",
                priority_level="STANDARD",
                executive_summary=f"Analysis of input '{text[:20]}...' suggests demand for advanced electronics. Initiating silicon fabrication sequence.",
                risk_analysis="Batteries not included.",
                user_stories=[
                    UserStory(id="TECH-001", role="Gamer", desire="Infinite Robux", benefit="Digital Dominance", acceptance_criteria=["API Integration", "Lag-free latency"]),
                    UserStory(id="TECH-002", role="Developer", desire="A bug-free codebase", benefit="Sanity preservation", acceptance_criteria=["100% Test Coverage", "Auto-Documentation"])
                ]
            )

# --- 3. PDF GENERATOR ---
def generate_pdf(prd: PRDStructure):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"NORTH POLE ENGINEERING: {prd.project_name[:40]}", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"PRIORITY: {prd.priority_level}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. EXECUTIVE SUMMARY", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, prd.executive_summary.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. ENGINEERING TICKETS", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for story in prd.user_stories:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, f"[{story.id}] {story.desire}", ln=True, fill=True)
        pdf.multi_cell(0, 8, f"   Persona: {story.role} | Benefit: {story.benefit}")
        pdf.ln(2)

    filename = "NorthPole_Blueprint.pdf"
    pdf.output(filename)
    return filename