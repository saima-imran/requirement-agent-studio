from requirement_agent_studio.ai.ollama_model import OllamaLanguageModel
from requirement_agent_studio.ai.quality_analyzer import QualityAIAnalyzer
from requirement_agent_studio.models import Requirement

language_model = OllamaLanguageModel()
analyzer = QualityAIAnalyzer(language_model)

requirement = Requirement(
    requirement_id="REQ-001",
    text="The system should respond quickly.",
)

analysis = analyzer.analyse(requirement.text)

print(f"Ambiguous: {analysis.is_ambiguous}")
print(f"Reason: {analysis.reason}")
print(f"Improved requirement: {analysis.improved_requirement}")
print(f"Confidence: {analysis.confidence}")


