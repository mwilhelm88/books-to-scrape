# 📚 Books to Scrape — Web Scraping Project

A Python project that scrapes book details from the [Books to Scrape](https://books.toscrape.com) demo site.  
This is designed as a portfolio project to demonstrate web scraping, data cleaning, and exporting results to CSV and Excel with custom styling.

---

## 🚀 Features
- Scrapes **title, price, availability, rating, and product page link**
- Handles **pagination** automatically
- **Error handling** for missing pages
- Cleans and formats data into:
  - `books_clean.csv`
  - `Books_Styled.xlsx` (with Excel formatting)
- Adds a **timestamp** to the Excel file for clarity

---

## 🛠️ Technologies Used
- **Python 3**
- `requests`
- `BeautifulSoup4`
- `pandas`
- `openpyxl`

---

## 📦 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/books-to-scrape.git
   cd books-to-scrape

📂 Output
After running, you’ll get:
	•	books_clean.csv — raw cleaned data
	•	Books_Styled.xlsx — Excel file with formatting and timestamp
📜 License
This project is licensed for educational and demonstration purposes only. If you plan to scrape other websites, always:
	•	Review their robots.txt file
	•	Follow their Terms of Service
	•	Avoid scraping personal or copyrighted data without permission