"""
Adobe India Hackathon 2025 - Challenge 1A
PDF Processor - Main PDF processing and coordination module
"""

import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Any
from outline_extractor import OutlineExtractor

def colored_text(text: str, color_code: str) -> str:
    """Return colored text for terminal output."""
    return f"\033[{color_code}m{text}\033[0m"


class PDFProcessor:
    """Main PDF processing class that coordinates outline extraction."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.outline_extractor = OutlineExtractor()
    
    def extract_outline(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract structured outline from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing title and outline structure
        """
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Extract document metadata and content
            metadata = doc.metadata
            page_count = len(doc)
            
            print(f"  Document info: {page_count} pages")
            
            # Extract text content from all pages
            pages_content = []
            for page_num in range(page_count):
                page = doc[page_num]
                
                # Extract text with font information
                text_dict = page.get_text("dict")
                pages_content.append({
                    'page_num': page_num + 1,
                    'text_dict': text_dict,
                    'plain_text': page.get_text()
                })
            
            # Close document
            doc.close()
            
            # Extract title and outline using the specialized extractor
            title = self.outline_extractor.extract_title(metadata, pages_content)
            outline = self.outline_extractor.extract_headings(pages_content)
            
            return {
                "title": title,
                "outline": outline
            }
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            # Return default structure on error
            return {
                "title": pdf_path.stem.replace('_', ' ').title(),
                "outline": []
            }
    
    def save_result(self, result: Dict[str, Any], output_path: Path) -> None:
        """
        Save the extraction result to a JSON file.
        
        Args:
            result: The extraction result dictionary
            output_path: Path where to save the JSON file
        """
        try:
            # Save the JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving result to {output_path}: {str(e)}")
            raise
