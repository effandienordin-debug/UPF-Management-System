import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def export_to_excel(data, sheet_name="Report"):
    """Exports a list of dicts to an Excel byte stream."""
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

def export_to_pdf(data, title="UPF Management Report"):
    """Exports a list of dicts to a PDF byte stream."""
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, title)
    
    # Body
    c.setFont("Helvetica", 10)
    y_pos = height - 80
    
    if data:
        # Header row
        headers = list(data[0].keys())
        x_pos = 50
        for header in headers:
            c.drawString(x_pos, y_pos, str(header))
            x_pos += 100
        
        y_pos -= 20
        
        # Data rows
        for item in data:
            x_pos = 50
            for key in headers:
                c.drawString(x_pos, y_pos, str(item.get(key, '')))
                x_pos += 100
            y_pos -= 15
            if y_pos < 50:
                c.showPage()
                y_pos = height - 50
    
    c.save()
    return output.getvalue()
