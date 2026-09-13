import requests
import pdfplumber

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

url = "https://www.globe.com.ph/sites/default/files/reports/secpse/2026/B.%20Quarterly%20Reports/III.%20Quarterly%20Report%20(17Q)/GLO-2Q26-17Q.pdf"
# url = 'file:///C:/Users/steph/Downloads/oh_so_you_decided_to_ask_about_the_projects_huh.pdf'
extracted = fetch_pdf(url)
print(extracted[:1000])
