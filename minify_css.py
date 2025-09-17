#!/usr/bin/env python3
"""
CSS Minifier Script
Removes comments, whitespace, and unnecessary characters to reduce file size.
"""

import re
import os

def minify_css(css_content):
    """
    Minify CSS content by removing comments, whitespace, and unnecessary characters.
    """
    # Remove CSS comments /* ... */
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove leading and trailing whitespace from each line
    css_content = '\n'.join(line.strip() for line in css_content.split('\n'))
    
    # Remove empty lines
    css_content = re.sub(r'\n\s*\n', '\n', css_content)
    
    # Remove whitespace around specific characters
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)
    
    # Remove unnecessary whitespace around operators
    css_content = re.sub(r'\s*>\s*', '>', css_content)
    css_content = re.sub(r'\s*\+\s*', '+', css_content)
    css_content = re.sub(r'\s*~\s*', '~', css_content)
    
    # Remove line breaks and merge into single line (optional - makes it smaller but less readable)
    css_content = re.sub(r'\s*\n\s*', '', css_content)
    
    # Remove any remaining multiple spaces
    css_content = re.sub(r' +', ' ', css_content)
    
    return css_content.strip()

def main():
    # File paths
    input_file = 'css/styles.css'
    output_file = 'css/styles.min.css'
    backup_file = 'css/styles.original.css'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    # Read the original CSS file
    with open(input_file, 'r', encoding='utf-8') as f:
        original_css = f.read()
    
    # Create backup of original file
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(original_css)
    print(f"✅ Backup created: {backup_file}")
    
    # Minify the CSS
    minified_css = minify_css(original_css)
    
    # Write minified CSS to new file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(minified_css)
    
    # Get file sizes
    original_size = len(original_css.encode('utf-8'))
    minified_size = len(minified_css.encode('utf-8'))
    reduction = original_size - minified_size
    reduction_percent = (reduction / original_size) * 100
    
    print(f"✅ CSS minification completed!")
    print(f"📊 Results:")
    print(f"   Original size: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    print(f"   Minified size: {minified_size:,} bytes ({minified_size/1024:.1f} KB)")
    print(f"   Size reduction: {reduction:,} bytes ({reduction_percent:.1f}%)")
    print(f"   Minified file: {output_file}")
    
    # Option to replace original file
    replace = input("\n🔄 Replace original styles.css with minified version? (y/N): ")
    if replace.lower() == 'y':
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        print(f"✅ Original file replaced with minified version")
        print(f"💾 Original backed up as: {backup_file}")
    else:
        print(f"✅ Minified version saved as: {output_file}")
        print(f"💡 To use minified version, update your HTML to reference: {output_file}")

if __name__ == "__main__":
    main()
