import streamlit as st
import plotly.graph_objects as go

from requirement_agent_studio.ai.ollama_model import OllamaLanguageModel
from requirement_agent_studio.analysis_pipeline import AnalysisPipeline
from requirement_agent_studio.compliance_agent import ComplianceAgent
from requirement_agent_studio.extractor_agent import RequirementExtractionAgent
from requirement_agent_studio.quality_agent import QualityAgent
from requirement_agent_studio.security_agent import SecurityAgent


def build_markdown_report(requirements, findings) -> str:
    lines: list[str] = [
        "# Requirement Agent Studio Report",
        "",
        f"Requirements analyzed: {len(requirements)}",
        f"Findings detected: {len(findings)}",
        "",
    ]

    if not findings:
        lines.extend(
            [
                "## Analysis Result",
                "",
                "No findings were detected.",
            ]
        )
        return "\n".join(lines)

    lines.extend(["## Findings", ""])

    for finding in findings:
        lines.extend(
            [
                f"### {finding.requirement_id}",
                "",
                f"- **Agent:** {finding.agent_name}",
                f"- **Severity:** {finding.severity}",
                f"- **Issue:** {finding.message}",
                f"- **Suggestion:** {finding.suggestion}",
                "",
            ]
        )

    return "\n".join(lines)


def count_findings(findings) -> tuple[dict[str, int], dict[str, int]]:
    severity_counts: dict[str, int] = {}
    agent_counts: dict[str, int] = {}

    for finding in findings:
        severity = str(finding.severity).upper()
        agent = finding.agent_name

        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        agent_counts[agent] = agent_counts.get(agent, 0) + 1

    return severity_counts, agent_counts


def create_severity_chart(severity_counts: dict[str, int]) -> go.Figure:
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

    ordered_severities = [
        severity
        for severity in severity_order
        if severity in severity_counts
    ]

    remaining_severities = [
        severity
        for severity in severity_counts
        if severity not in severity_order
    ]

    labels = ordered_severities + remaining_severities
    values = [severity_counts[label] for label in labels]

    chart = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                text=values,
                textposition="auto",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Findings: %{y}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    chart.update_layout(
        xaxis_title="Severity",
        yaxis_title="Number of findings",
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )

    chart.update_yaxes(
        tickmode="linear",
        dtick=1,
        rangemode="tozero",
    )

    return chart


def create_agent_chart(agent_counts: dict[str, int]) -> go.Figure:
    sorted_agents = sorted(
        agent_counts.items(),
        key=lambda item: item[1],
    )

    labels = [agent for agent, _ in sorted_agents]
    values = [count for _, count in sorted_agents]

    chart = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                text=values,
                textposition="auto",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Findings: %{x}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    chart.update_layout(
        xaxis_title="Number of findings",
        yaxis_title="Agent",
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )

    chart.update_xaxes(
        tickmode="linear",
        dtick=1,
        rangemode="tozero",
    )

    return chart


st.set_page_config(
    page_title="Requirement Agent Studio",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Requirement Agent Studio")

st.markdown(
    """
    Welcome to **Requirement Agent Studio**.

    This application analyzes software requirements using:

    - ✅ Quality Analysis
    - 🔒 Security Analysis
    - 📋 Compliance Analysis
    - 🤖 AI-powered Requirement Analysis with Ollama
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

if st.button("Analyze Requirements", type="primary"):
    if not requirement_text.strip():
        st.warning("Please enter at least one requirement.")

    else:
        try:
            with st.spinner("Analyzing requirements..."):
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

                report_content = build_markdown_report(
                    requirements=requirements,
                    findings=findings,
                )

                st.session_state["requirements"] = requirements
                st.session_state["findings"] = findings
                st.session_state["report_content"] = report_content

        except Exception as error:
            st.error("The analysis could not be completed.")
            st.exception(error)


if "requirements" in st.session_state:
    requirements = st.session_state["requirements"]
    findings = st.session_state["findings"]
    report_content = st.session_state["report_content"]

    st.success(
        f"Analysis completed for {len(requirements)} requirement(s)."
    )

    metric_column_1, metric_column_2 = st.columns(2)

    with metric_column_1:
        st.metric(
            "Requirements analyzed",
            len(requirements),
        )

    with metric_column_2:
        st.metric(
            "Findings detected",
            len(findings),
        )

    st.divider()
    st.subheader("Analysis Dashboard")

    if findings:
        severity_counts, agent_counts = count_findings(findings)

        chart_column_1, chart_column_2 = st.columns(2)

        with chart_column_1:
            st.markdown("#### Findings by Severity")

            severity_chart = create_severity_chart(
                severity_counts
            )

            st.plotly_chart(
                severity_chart,
                use_container_width=True,
            )

        with chart_column_2:
            st.markdown("#### Findings by Agent")

            agent_chart = create_agent_chart(
                agent_counts
            )

            st.plotly_chart(
                agent_chart,
                use_container_width=True,
            )

    else:
        st.info(
            "No chart data is available because no findings were detected."
        )

    st.divider()
    st.subheader("Analysis Findings")

    if not findings:
        st.success("No findings were detected.")

    else:
        for finding in findings:
            heading = (
                f"{finding.requirement_id} | "
                f"{finding.agent_name} | "
                f"{str(finding.severity).upper()}"
            )

            with st.expander(heading, expanded=True):
                st.markdown("**Issue**")
                st.write(finding.message)

                st.markdown("**Suggestion**")
                st.write(finding.suggestion)

    st.divider()

    st.download_button(
        label="Download Markdown Report",
        data=report_content,
        file_name="requirement_analysis_report.md",
        mime="text/markdown",
    )

    