import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
)


def generate_report_pdf(report, result):
    """
    Builds a PDF for a CareerReport + its parsed Gemini result dict.
    Returns BytesIO buffer ready to send as a file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Title'], textColor=colors.HexColor('#1a1a2e')
    )
    heading_style = ParagraphStyle(
        'HeadingStyle', parent=styles['Heading2'],
        textColor=colors.HexColor('#4361ee'), spaceBefore=14, spaceAfter=6
    )
    normal_style = styles['Normal']

    elements = []

    elements.append(Paragraph("CareerCompass AI — Career Report", title_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"{report.education_level} • {report.preferred_industry} • "
        f"{report.created_at.strftime('%d %b %Y')}",
        normal_style
    ))
    elements.append(Spacer(1, 12))

    def add_list_section(title, items):
        elements.append(Paragraph(title, heading_style))
        elements.append(ListFlowable(
            [ListItem(Paragraph(str(i), normal_style)) for i in items],
            bulletType='bullet'
        ))

    add_list_section("Career Suggestions", result.get('career_suggestions', []))
    add_list_section("Recommended Degree Programs", result.get('recommended_degree_programs', []))
    add_list_section("Recommended Universities", result.get('recommended_universities', []))
    add_list_section("Skills to Learn", result.get('skills_to_learn', []))
    add_list_section("Certifications", result.get('certifications', []))
    add_list_section("Job Opportunities", result.get('job_opportunities', []))

    elements.append(Paragraph("Salary Estimates", heading_style))
    elements.append(Paragraph(result.get('salary_estimates', 'N/A'), normal_style))

    elements.append(Paragraph("Future Scope", heading_style))
    elements.append(Paragraph(result.get('future_scope', 'N/A'), normal_style))

    elements.append(Paragraph("Roadmap", heading_style))
    elements.append(ListFlowable(
        [ListItem(Paragraph(str(i), normal_style)) for i in result.get('roadmap', [])],
        bulletType='1'
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer