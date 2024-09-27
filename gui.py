import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox, Listbox, Scrollbar, MULTIPLE

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tag_data = {}
            # Collect various elements
            for tag in soup.find_all(True):  # Find all tags
                tag_name = tag.name
                text_content = tag.get_text(strip=True)
                if text_content:
                    if tag_name not in tag_data:
                        tag_data[tag_name] = []
                    tag_data[tag_name].append(text_content)
            return tag_data
        else:
            messagebox.showerror("Error", f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def update_data_options():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    global fetched_data
    fetched_data = fetch_data(url)

    if fetched_data:
        data_listbox.delete(0, END)  # Clear existing items
        for tag in fetched_data.keys():
            # Show the tag names
            data_listbox.insert(END, tag)

def start_scraping():
    output_filename = filename_entry.get()
    if not output_filename:
        messagebox.showwarning("Input Error", "Please enter a name for the output CSV file.")
        return

    selected_indices = data_listbox.curselection()
    selected_data = []

    for index in selected_indices:
        tag = data_listbox.get(index)
        content_list = fetched_data[tag]
        for content in content_list:
            selected_data.append((tag, content))

    if selected_data:
        # Create a DataFrame and save to CSV
        df = pd.DataFrame(selected_data, columns=['Tag', 'Content'])
        output_filename += '.csv' if not output_filename.endswith('.csv') else ''
        df.to_csv(output_filename, index=False)
        messagebox.showinfo("Success", f"Data scraped and saved to {output_filename}.")
    else:
        messagebox.showinfo("No Selection", "No data selected for scraping.")

# Set up the GUI layout
root = Tk()
root.title("Generic Web Scraper")
root.geometry("600x400")

Label(root, text="Enter URL (e.g., www.example.com):").pack(pady=10)
url_entry = Entry(root, width=60)
url_entry.pack(pady=10)

fetch_button = Button(root, text="Fetch Data", command=update_data_options)
fetch_button.pack(pady=10)

Label(root, text="Select Tags to Scrape:").pack(pady=10)

data_listbox = Listbox(root, selectmode=MULTIPLE, width=80, height=15)
data_listbox.pack(pady=10)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
data_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=data_listbox.yview)

Label(root, text="Enter output CSV filename:").pack(pady=10)
filename_entry = Entry(root, width=60)
filename_entry.pack(pady=10)

scrape_button = Button(root, text="Scrape Selected Data", command=start_scraping)
scrape_button.pack(pady=20)

root.mainloop()
