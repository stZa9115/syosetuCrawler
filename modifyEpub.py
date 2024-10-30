import ebooklib
from ebooklib import epub
import zipfile
from lxml import etree

def convert_ol_to_ul(epub_file):
    book = epub.read_epub(epub_file+'.epub')

    for item in book.toc:
        content = item.content
        content = content.replace("<ol>", "<ul>", 1)  # Replace the first occurrence
        content = content.replace("<li type=", "<li", 1)  # Remove the first type attribute
        item.content = content

    epub.save(epub_file+'v1.epub')
    
bookName = '転生王女と天才令嬢の魔法革命【Web版】'

convert_ol_to_ul(bookName)