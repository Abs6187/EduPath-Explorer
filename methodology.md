import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def markdown_to_pdf(markdown_file, pdf_file):
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # Add CSS for styling
    css = CSS(string='''
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 2em; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 1em; border-radius: 5px; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
    ''')
    
    # Generate PDF
    font_config = FontConfiguration()
    HTML(string=html_content).write_pdf(
        pdf_file,
        stylesheets=[css],
        font_config=font_config
    )

# Generate PDF
markdown_to_pdf('methodology.md', 'Course_Recommendation_System_Methodology.pdf')
