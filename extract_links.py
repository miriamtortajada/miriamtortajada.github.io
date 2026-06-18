import os
import re
import PyPDF2

pdf_dir = "assets/pdf/"
url_regex = re.compile(r'https?://[a-zA-Z0-9./\-_?=]+')

results = {}

for filename in os.listdir(pdf_dir):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(pdf_dir, filename)
    
    links = []
    
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            # Find URLs
            urls = url_regex.findall(text)
            
            # Also try to extract actual link annotations
            for page in reader.pages:
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        annot_obj = annot.get_object()
                        if "/A" in annot_obj and "/URI" in annot_obj["/A"]:
                            links.append(annot_obj["/A"]["/URI"])
                            
            # Combine text URLs and link URLs
            all_urls = set(urls + links)
            
            # Filter for relevant links
            relevant = [url for url in all_urls if any(x in url.lower() for x in ["osf.io", "github.com", "prospero", "clinicaltrials", "zenodo", "aspredicted"])]
            
            if relevant:
                results[filename] = relevant
    except Exception as e:
        results[filename] = [f"Error: {e}"]

for f, urls in results.items():
    print(f"--- {f} ---")
    for u in urls:
        print(u)
