"""PDF processor for XLLM Enterprise.

This module provides specialized PDF processing functionality for
technical documents, extracting structured content that can be
used as a corpus for the XLLM Enterprise system.
"""

import logging
import fitz  # PyMuPDF
import json
import re
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_text_blocks(text_data):
    """Extract text blocks from PDF text data.
    
    Args:
        text_data (dict): Text data from PyMuPDF
        
    Returns:
        list: List of text blocks with their properties
    """
    blocks = []
    
    for block in text_data.get('blocks', []):
        if block.get('type') == 0:  # Text block
            text = ""
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    text += span.get('text', '')
                    
            if text.strip():
                blocks.append({
                    'text': text.strip(),
                    'bbox': block.get('bbox', [0, 0, 0, 0]),
                    'font_size': block.get('lines', [{}])[0].get('spans', [{}])[0].get('size', 0) if block.get('lines') else 0,
                    'font_name': block.get('lines', [{}])[0].get('spans', [{}])[0].get('font', '') if block.get('lines') else '',
                    'color': block.get('lines', [{}])[0].get('spans', [{}])[0].get('color', 0) if block.get('lines') else 0
                })
                
    return blocks


def detect_headings(blocks, title_font_size_threshold=12):
    """Detect headings in text blocks.
    
    Args:
        blocks (list): List of text blocks
        title_font_size_threshold (int, optional): Font size threshold for titles. Defaults to 12.
        
    Returns:
        list: List of text blocks with heading flags
    """
    # Find largest font size for reference
    max_font_size = max([block['font_size'] for block in blocks]) if blocks else 0
    
    # If no blocks or max font size is too small, return unchanged
    if max_font_size < title_font_size_threshold:
        return blocks
        
    # Mark headings
    for block in blocks:
        # Larger font size suggests heading
        if block['font_size'] >= title_font_size_threshold:
            block['is_heading'] = True
            
            # Determine heading level based on font size
            if block['font_size'] >= 0.8 * max_font_size:
                block['heading_level'] = 1
            elif block['font_size'] >= 0.6 * max_font_size:
                block['heading_level'] = 2
            else:
                block['heading_level'] = 3
        else:
            block['is_heading'] = False
            block['heading_level'] = 0
            
    return blocks


def extract_bullet_lists(blocks):
    """Extract bullet lists from text blocks.
    
    Args:
        blocks (list): List of text blocks
        
    Returns:
        list: List of text blocks with bullet list information
    """
    bullet_patterns = [
        r'^\s*•\s+',  # Bullet character
        r'^\s*\*\s+',  # Asterisk
        r'^\s*-\s+',   # Hyphen
        r'^\s*\d+\.\s+',  # Numbered list
        r'^\s*[a-zA-Z]\)\s+',  # Letter with parenthesis
    ]
    
    for block in blocks:
        text = block['text']
        is_bullet = False
        
        for pattern in bullet_patterns:
            if re.match(pattern, text):
                is_bullet = True
                # Remove bullet marker and leading space
                block['text'] = re.sub(pattern, '', text)
                break
                
        block['is_bullet'] = is_bullet
        
    return blocks


def group_blocks_by_section(blocks):
    """Group blocks by section based on headings.
    
    Args:
        blocks (list): List of text blocks with heading flags
        
    Returns:
        list: List of sections with their content
    """
    sections = []
    current_section = None
    current_subsection = None
    
    for block in blocks:
        if block['is_heading']:
            if block['heading_level'] == 1:
                # New top-level section
                current_section = {
                    'title': block['text'],
                    'level': 1,
                    'subsections': [],
                    'content': []
                }
                current_subsection = None
                sections.append(current_section)
            elif block['heading_level'] == 2 and current_section:
                # New subsection
                current_subsection = {
                    'title': block['text'],
                    'level': 2,
                    'content': []
                }
                current_section['subsections'].append(current_subsection)
            elif block['heading_level'] == 3 and current_subsection:
                # Add as content with special marker
                current_subsection['content'].append({
                    'text': block['text'],
                    'is_subheading': True
                })
        else:
            # Regular content
            content_block = {
                'text': block['text'],
                'is_bullet': block.get('is_bullet', False),
                'is_subheading': False
            }
            
            if current_subsection:
                current_subsection['content'].append(content_block)
            elif current_section:
                current_section['content'].append(content_block)
                
    return sections


def convert_pdf_to_entities(pdf_path, output_path=None):
    """Convert PDF to XLLM Enterprise entity format.
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str, optional): Path to output file. Defaults to None.
        
    Returns:
        list: List of entities in XLLM Enterprise format
    """
    try:
        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        entities = []
        entity_id = 1
        
        # Process each page
        for page_num in range(len(pdf_document)):
            logger.info(f"Processing page {page_num+1}/{len(pdf_document)}")
            page = pdf_document.load_page(page_num)
            
            # Extract text data
            text_data = page.get_text("dict")
            
            # Extract and process blocks
            blocks = extract_text_blocks(text_data)
            blocks = detect_headings(blocks)
            blocks = extract_bullet_lists(blocks)
            
            # Group blocks by section
            sections = group_blocks_by_section(blocks)
            
            # Convert sections to entities
            for section in sections:
                # Create entity for section
                section_entity = f"{entity_id}~~{{"
                section_entity += f"title::{section['title']}||"
                section_entity += f"category::document||"
                section_entity += f"tag_list::pdf, technical, document||"
                section_entity += f"meta::page {page_num+1}||"
                
                # Add section content
                content = ""
                if section['content']:
                    content = " ".join([block['text'] for block in section['content']])
                    
                section_entity += f"description::{content}"
                section_entity += "}"
                
                entities.append(section_entity)
                entity_id += 1
                
                # Create entities for subsections
                for subsection in section['subsections']:
                    subsection_entity = f"{entity_id}~~{{"
                    subsection_entity += f"title::{subsection['title']}||"
                    subsection_entity += f"category::{section['title']}||"
                    subsection_entity += f"tag_list::pdf, technical, document, {section['title'].lower()}||"
                    subsection_entity += f"meta::page {page_num+1}||"
                    
                    # Add subsection content
                    content = ""
                    if subsection['content']:
                        content = " ".join([block['text'] for block in subsection['content'] if not block['is_subheading']])
                        
                    subsection_entity += f"description::{content}"
                    subsection_entity += "}"
                    
                    entities.append(subsection_entity)
                    entity_id += 1
        
        # Write to output file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                for entity in entities:
                    f.write(entity + "\n")
            logger.info(f"Wrote {len(entities)} entities to {output_path}")
            
        return entities
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return []


def main():
    """Main function for the PDF processor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process PDF files for XLLM Enterprise")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument("--output", "-o", help="Path to the output file")
    
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    output_path = args.output or f"{Path(pdf_path).stem}_entities.txt"
    
    logger.info(f"Processing PDF: {pdf_path}")
    entities = convert_pdf_to_entities(pdf_path, output_path)
    logger.info(f"Generated {len(entities)} entities")

if __name__ == "__main__":
    main() 