# pip install reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json

with open("resultsSavedSpring23.json") as file_js:
    data = json.load(file_js)

sorted_data = sorted(data.items(), key=lambda x: x[1]["sgpa"], reverse=True)

pdf = SimpleDocTemplate("student_table.pdf", pagesize=letter)
elements = []

# Define table headers and data
headers = ["Place No", "Student ID", "Name", "SGPA", "Subjects"]
table_data = [headers]  # Initialize table with headers

# Populate the table with data
for index, (student_id, student_data) in enumerate(sorted_data):
    row = [
        str(index + 1),
        student_id,
        student_data["name"],
        str(student_data["sgpa"]),
        "\n".join(student_data["cTitleNgLetter"]),
    ]
    table_data.append(row)

# Define table style
table_style = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # Header background color
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment for all cells
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Header font style
        ("FONTSIZE", (0, 0), (-1, 0), 12),  # Header font size
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Bottom padding for header row
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Data row background color
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),  # Data row font style
        ("FONTSIZE", (0, 1), (-1, -1), 10),  # Data row font size
        ("TOPPADDING", (0, 1), (-1, -1), 8),  # Top padding for data rows
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),  # Bottom padding for data rows
    ]
)

# Create table and apply style
table = Table(table_data)
table.setStyle(table_style)

# Add table to the elements list
elements.append(table)

# Build the PDF document
pdf.build(elements)

print("PDF generated successfully.")
