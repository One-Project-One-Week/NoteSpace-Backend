import pymupdf

def extract_texts_from_files(file) -> str:
    
    filetype = file.name.split('.')[-1]
    
    document = pymupdf.open(stream=file.read(), filetype=filetype)
            
    extracted_content = ""

    for page in range(len(document)):
        print(document.load_page(page).get_text(), "\n")
        extracted_content += document.load_page(page).get_text()
    
    return extracted_content