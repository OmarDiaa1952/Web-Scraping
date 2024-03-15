import csv
import re

# Read the CSV data
with open(r'C:\Users\omarm\Desktop\Whop\Data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Assuming "Social Data" is the last column
for i in range(len(rows)):
    social_data = rows[i][-1].strip()  # Remove leading/trailing whitespace

    # Clean the data (optional)
    # You can uncomment these lines if you need specific cleaning steps
    # social_data = re.sub(r'\b\d+\s*reviews\b', '', social_data)  # Remove reviews
    # social_data = re.sub(r'[^\w\s]', '', social_data)  # Remove emojis
    # social_data = social_data.replace('\n\n', '')  # Remove newline characters

    # Extract links
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', social_data)

    # Handle empty links (optional)
    if not links:
        links = ["No links found"]  # Assign a placeholder value

    rows[i][-1] = links  # Update the column with extracted links or placeholder

# Write the modified rows back to the CSV file
with open(r'C:\Users\omarm\Desktop\Whop\Data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Data updated successfully.")