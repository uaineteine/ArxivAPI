print("[arxiv_paper] importing libraries")
import re
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime

def _format_arxiv_id(year, month, serial, archive=None):
    """
    Returns the correct arXiv ID format based on the date.
    - For pre-April 2007: requires 'archive' (e.g., 'hep-th'), year, month, serial.
    - For post-April 2007: year, month, serial only.
    """
    # arXiv switched to new format in April 2007
    if (year < 2007) or (year == 2007 and month < 4):
        if not archive:
            raise ValueError("Archive (e.g., 'hep-th') required for old-style arXiv IDs.")
        return f"{archive}/{str(year)[-2:]:0>2}{month:0>2}{serial:0>3}"
    else:
        return f"{str(year)[-2:]:0>2}{month:0>2}.{serial:0>4}"

# Examples:
# Old: format_arxiv_id(2006, 12, 123, archive='hep-th') -> 'hep-th/0612123'
# New: format_arxiv_id(2021, 1, 12345) -> '2101.12345'

def _parse_arxiv_id(arxiv_id):
    """
    Parse an ArXiv ID and extract metadata like year, month, serial, archive.
    Supports both old format (archive/YYMMnnn) and new format (YYMM.nnnnn).
    
    Returns:
        dict: Contains 'year', 'month', 'serial', 'archive', 'format_type'
    """
    # Remove version number if present (e.g., "1234.5678v2" -> "1234.5678")
    base_id = arxiv_id.split('v')[0]
    
    # New format: YYMM.nnnnn (post April 2007)
    new_format_match = re.match(r'^(\d{4})\.(\d{4,5})$', base_id)
    if new_format_match:
        yymm_str, serial_str = new_format_match.groups()
        year = 2000 + int(yymm_str[:2])
        month = int(yymm_str[2:4])
        serial = int(serial_str)
        return {
            'year': year,
            'month': month,
            'serial': serial,
            'archive': None,
            'format_type': 'new'
        }
    
    # Old format: archive/YYMMnnn (pre April 2007)
    old_format_match = re.match(r'^([a-z-]+)/(\d{2})(\d{2})(\d{3,4})$', base_id)
    if old_format_match:
        archive, yy_str, mm_str, serial_str = old_format_match.groups()
        year = 1900 + int(yy_str) if int(yy_str) > 90 else 2000 + int(yy_str)  # Heuristic for year
        month = int(mm_str)
        serial = int(serial_str)
        return {
            'year': year,
            'month': month,
            'serial': serial,
            'archive': archive,
            'format_type': 'old'
        }
    
    # If no match, raise an error
    raise ValueError(f"Invalid ArXiv ID format: {arxiv_id}")

def _get_max_id_for_date(year, month):
    """
    Returns the maximum number of digits for the serial part of the arXiv ID
    based on the date (format change in April 2007).
    """
    if (year < 2007) or (year == 2007 and month < 4):
        return 5  # Old format: up to 5 digits, but usually 3
    else:
        return 5  # New format: up to 5 digits

def _summaryText(title, abs):
    return f"Title: {title}\nAbstract: {abs}"

class ArxivPaper:
    def __init__(self, id):
        # Parse and validate the ArXiv ID
        try:
            self.id_metadata = _parse_arxiv_id(id)
        except ValueError as e:
            raise ValueError(f"ID is not in a valid ArXiv format. {str(e)}")
        
        self.id = id
        self.title = ""
        self.abstract = ""
        self.authors = []
        self.published_date = None
        self.updated_date = None
        self.year = self.id_metadata['year']
        self.month = self.id_metadata['month']
        self.archive = self.id_metadata.get('archive')
        self.serial = self.id_metadata['serial']
        self.publisher = "arXiv"  # All papers are from arXiv
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Log the extracted metadata
        self._log_metadata()
    
    def _log_metadata(self):
        """Log the extracted metadata from the ArXiv ID"""
        self.logger.info(f"ArXiv Paper ID: {self.id}")
        self.logger.info(f"Year: {self.year}, Month: {self.month}")
        self.logger.info(f"Serial: {self.serial}")
        if self.archive:
            self.logger.info(f"Archive: {self.archive}")
        self.logger.info(f"Publisher: {self.publisher}")

    def __str__(self):
        return _summaryText(self.title, self.abstract)
    
    def getURL(self):
        return(f"https://arxiv.org/abs/{self.id}")
    
    def extract_using_soup(self):
        # Fetch the HTML content from the URL
        response = requests.get(self.getURL())
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the title
        title = soup.find("h1", class_="title mathjax")
        if title:
            self.title = title.text.split(":", 1)[1].strip()

        # Extract the abstract
        abstract = soup.find("blockquote", class_="abstract mathjax")
        if abstract:
            self.abstract = abstract.text.split(":", 1)[1].strip()
        
        # Extract authors
        authors_div = soup.find("div", class_="authors")
        if authors_div:
            author_links = authors_div.find_all("a")
            self.authors = [link.text.strip() for link in author_links]
        
        # Extract submission dates
        dateline = soup.find("div", class_="dateline")
        if dateline:
            date_text = dateline.text
            # Try to extract submitted and last revised dates
            # Format is typically like: "[Submitted on 3 Apr 2007 (v1), last revised 1 May 2007 (this version, v2)]"
            if "Submitted on" in date_text:
                import re
                submitted_match = re.search(r'Submitted on ([^(]+)', date_text)
                if submitted_match:
                    self.published_date = submitted_match.group(1).strip()
                
                revised_match = re.search(r'last revised ([^(]+)', date_text)
                if revised_match:
                    self.updated_date = revised_match.group(1).strip()
                else:
                    # If no revision, updated date is same as published
                    self.updated_date = self.published_date
        
        # Log the extracted information
        self._log_extracted_data()
    
    def _log_extracted_data(self):
        """Log the extracted paper data"""
        self.logger.info(f"Title: {self.title[:50]}..." if len(self.title) > 50 else f"Title: {self.title}")
        self.logger.info(f"Authors: {', '.join(self.authors[:3])}..." if len(self.authors) > 3 else f"Authors: {', '.join(self.authors)}")
        if self.published_date:
            self.logger.info(f"Published: {self.published_date}")
        if self.updated_date and self.updated_date != self.published_date:
            self.logger.info(f"Updated: {self.updated_date}")
        self.logger.info(f"Abstract: {self.abstract[:100]}..." if len(self.abstract) > 100 else f"Abstract: {self.abstract}")
