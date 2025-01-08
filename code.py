from bs4 import BeautifulSoup
import csv

def extract_table_data(html_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize list to store rows
    rows = []
    
    # Find all rows (div class="7" contains each row)
    row_divs = soup.find_all('div', class_='7')
    
    for row_div in row_divs:
        # Extract index number (span class="43")
        index_span = row_div.find('span', class_='43')
        index = index_span.text.strip() if index_span else ''
        
        # Extract main content (span class="52" inside anchor)
        content_span = row_div.find('span', class_='52')
        if content_span and content_span.find('a'):
            content = content_span.find('a').text.strip()
        else:
            content = ''
            
        # Only add non-empty rows
        if index and content:
            rows.append([index, content])
    
    return rows

def write_to_csv(data, output_file):
    # Write data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Index', 'Content'])
        # Write data rows
        writer.writerows(data)

def main():
    # Input and output files
    html_file = 'html_snippet_modified.html'
    output_file = 'output.csv'
    
    # Extract data from HTML
    table_data = extract_table_data(html_file)
    
    # Write to CSV
    write_to_csv(table_data, output_file)
    
    print(f"Successfully extracted {len(table_data)} rows to {output_file}")

if __name__ == "__main__":
    main()
