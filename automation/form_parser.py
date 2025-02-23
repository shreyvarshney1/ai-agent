from bs4 import BeautifulSoup

from bs4 import BeautifulSoup

def get_form_fields(page):
    """
    Extracts form fields from the page, ignoring hidden inputs and system fields.
    """
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    fields = {}
    
    # Iterate over input elements
    for input_tag in soup.find_all("input"):
        input_type = input_tag.get("type", "text").lower()
        # Skip hidden fields
        if input_type == "hidden":
            continue
        
        name = input_tag.get("name")
        # Skip common system-generated field names (customize as needed)
        if name and not name.startswith(("entry.", "fvv", "partialResponse", "pageHistory", "fbzx")):
            fields[name] = ""
    return fields
