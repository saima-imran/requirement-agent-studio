import streamlit as st

from requirement_agent_studio.ai.ollama_model import OllamaLanguageModel
from requirement_agent_studio.analysis_pipeline import AnalysisPipeline
from requirement_agent_studio.compliance_agent import ComplianceAgent
from requirement_agent_studio.extractor_agent import RequirementExtractionAgent
from requirement_agent_studio.quality_agent import QualityAgent
from requirement_agent_studio.security_agent import SecurityAgent


st.set_page_config(
    page_title="Requirement Agent Studio",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Requirement Agent Studio")

st.markdown(
    """
    Analyze software requirements using:

    - Quality analysis
    - Security analysis
    - Compliance analysis
    - AI-powered ambiguity analysis with Ollama
    """
)

st.divider()

st.subheader("Requirement Input")

requirement_text = st.text_area(
    "Enter one requirement per line:",
    height=250,
    placeholder=(
        "The system shall respond fast.\n"
        "Users shall log in using a password.\n"
        "A human operator must be able to override automated decisions."
    ),
)

analyze_button = st.button(
    "Analyze Requirements",
    type="primary",
)

if analyze_button:
    if not requirement_text.strip():
        st.warning("Please enter at least one requirement.")

    else:
        try:
            with st.spinner(
                "Analyzing requirements with Quality, Security, Compliance, and AI agents..."
            ):
                extractor = RequirementExtractionAgent()
                requirements = extractor.extract(requirement_text)

                language_model = OllamaLanguageModel()

                pipeline = AnalysisPipeline(
                    [
                        QualityAgent(language_model),
                        SecurityAgent(),
                        ComplianceAgent(),
                    ]
                )

                findings = pipeline.run(requirements)

            st.success(
                f"Analysis completed for {len(requirements)} requirement(s)."
            )

            st.subheader("Analysis Summary")

            summary_column_1, summary_column_2 = st.columns(2)

            with summary_column_1:
                st.metric(
                    "Requirements analyzed",
                    len(requirements),
                )

            with summary_column_2:
                st.metric(
                    "Findings detected",
                    len(findings),
                )

            st.divider()
            st.subheader("Findings")

            if not findings:
                st.success(
                    "No quality, security, compliance, or AI findings were detected."
                )

            else:
                for finding in findings:
                    title = (
                        f"{finding.requirement_id} · "
                        f"{finding.agent_name} · "
                        f"{finding.severity.upper()}"
                    )

                    with st.expander(title, expanded=True):
                        st.markdown("**Issue**")
                        st.write(finding.message)

                        st.markdown("**Suggestion**")
                        st.write(finding.suggestion)

        except Exception as error:
            st.error("The requirement analysis could not be completed.")
            st.exception(error)


            

