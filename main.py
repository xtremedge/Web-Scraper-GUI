import requests
import csv
from bs4 import BeautifulSoup

# Step 1: Make a request to the website
url = 'http://quotes.toscrape.com'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully retrieved the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract data
quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    print(f"{text} — {author}")


# Step 4: Handle Pagination
while True:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract quotes
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            print(f"{text} — {author}")
        
        # Check for the next page
        next_page = soup.find('li', class_='next')
        if next_page:
            url = next_page.find('a')['href']
            url = f"http://quotes.toscrape.com{url}"  # Update to the full URL
        else:
            break  # Exit the loop if there's no next page
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        break


with open('quotes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Quote', 'Author'])  # Write header

    # Inside your quotes loop, write each quote to the CSV
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        writer.writerow([text, author])  # Write the quote and author
