import csv
import re

# Read the column data from the CSV file
column_data = []
with open(r'C:\Users\omarm\Desktop\Whop\Data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        column_data.append(row[-1])  # Assuming "About the seller" is column number 5 (index 4)

# Clean the column data
cleaned_data = []
for item in column_data:
    # Remove reviews part
    # item = re.sub(r'\b\d+\s*reviews\b', '', item)

    # Remove emojis
    item = re.sub(r'[^\w\s]', '', item)

    # Remove newline characters
    item = item.replace('\n\n', '')

    cleaned_data.append(item.strip())

# Extract the links from the "Social data" column
extracted_links = []
for item in cleaned_data:
    # Use regular expressions to find links in the text
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item)
    extracted_links.append(links)

# Update the data in the CSV file
with open(r'C:\Users\omarm\Desktop\Whop\Data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Assuming "Social data" column is the last column
for i in range(len(rows)):
    rows[i][-1] = extracted_links[i]

with open(r'C:\Users\omarm\Desktop\Whop\Data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Data updated successfully.")