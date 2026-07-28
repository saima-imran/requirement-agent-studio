from requirement_agent_studio.models import Requirement


class RequirementExtractionAgent:
    """
    Extracts individual requirements from a plain text document.
    """

    def extract(self, document: str) -> list[Requirement]:

        requirements = []

        lines = [
            line.strip()
            for line in document.splitlines()
            if line.strip()
        ]

        for index, line in enumerate(lines, start=1):

            requirement = Requirement(
                requirement_id=f"REQ-{index:03}",
                text=line,
            )

            requirements.append(requirement)

        return requirements
    