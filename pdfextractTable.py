import requests
import pdfplumber

url = "https://www.globe.com.ph/sites/default/files/reports/secpse/2026/B.%20Quarterly%20Reports/III.%20Quarterly%20Report%20(17Q)/GLO-2Q26-17Q.pdf"

def find_page_with_heading(pdf_path, heading):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if heading.lower() in text.lower():
                print(f"Found '{heading}' on page {i}")
                return i
    return None

def extract_table_from_page(pdf_path, page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        tables = page.extract_tables()  # returns a list of tables found on that page
        return tables

def fetch_pdf(url):
    response = requests.get(url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    text = ""
    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

extracted = fetch_pdf(url)

# Step 1: find it
page_num = find_page_with_heading("temp.pdf", "Results of Operations (Php Mn)")

# Step 2: extract whatever table(s) are on that page
if page_num is not None:
    tables = extract_table_from_page("temp.pdf", page_num)
    for t in tables:
        for row in t:
            print(row)

# url = 'file:///C:/Users/steph/Downloads/oh_so_you_decided_to_ask_about_the_projects_huh.pdf'