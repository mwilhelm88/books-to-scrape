import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin


titles = []
prices= []
ratings= []
availability_list= []
book_urls = []
categories = []
descriptions = []
upcs = []
product_types = []
price_excl_tax = []
price_incl_tax = []
taxes = []
num_reviews = []

page_num = 1

while True:
    if page_num == 1:
        url = "https://books.toscrape.com/index.html"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    print(f"Scraping page {page_num}: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape page {page_num}: {e}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print(f"No books found on page {page_num}. Stopping.")
        break

    for book in books:
        # Title
        title=book.h3.a["title"]
        # Price
        price=book.select_one('p.price_color').text.strip()
        price=price.replace("Â","")
        # Availability
        availability = book.select_one('p.instock.availability').text.strip()
        # Rating
        rating_tag = book.select_one('p.star-rating')
        rating_classes = rating_tag.get("class", [])
        star_rating = next((c for c in rating_classes if c != "star-rating"), "No Rating")
        # URL for the book
        partial_link = book.h3.a["href"]
        book_url = urljoin(url, partial_link)

       # Get extra details from the book page
        try:
            book_response = requests.get(book_url, timeout=10)
            book_response.raise_for_status()
            book_soup = BeautifulSoup(book_response.text, "html.parser")
            # Category
            breadcrumb = book_soup.select("ul.breadcrumb li a")
            category = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else "Unknown"
            # Description
            description_tag = book_soup.select_one("#prodcut_description ~ p")
            description = description_tag.text.strip() if description_tag else "No description available"
            # Product info table
            table = book_soup.select_one("table")
            table_data = {row.th.text.strip(): row.td.text.strip() for row in table.find_all("tr")}


            upc_val = table_data.get("UPC", "")
            product_type_val = table_data.get("Product Type", "")
            price_excl_val = table_data.get("Price (excl. tax)", "")
            price_incl_val = table_data.get("Price (incl. tax)", "")
            tax_val = table_data.get("Tax", "")
            reviews_val = table_data.get("Number of reviews", "")

        except Exception as e:
            category = "Unknown"
            description = "No description available"
            upc_val = product_type_val = price_excl_val = price_incl_val = tax_val = reviews_val = ""
            print(f"Error scraping category for {title}: {e}")

        #Append all collected data
        titles.append(title)
        prices.append(price)
        ratings.append(star_rating)
        availability_list.append(availability)
        book_urls.append(book_url)
        categories.append(category)
        upcs.append(upc_val)
        product_types.append(product_type_val)
        price_excl_tax.append(price_excl_val)
        price_incl_tax.append(price_incl_val)
        taxes.append(tax_val)
        num_reviews.append(reviews_val)

    page_num += 1
    time.sleep(1)

df=pd.DataFrame({
    "Title":titles,
    "Prices":prices,
    "Rating": ratings,
    "Availability": availability_list,
    "URL": book_urls,
    "Category": categories,
    "Description": descriptions,
    "UPC": upcs,
    "Product Type": product_types,
    "Price (excl. tax)": price_excl_tax,
    "Price (incl. tax)": price_incl_tax,
    "Tax": taxes,
    "Number of Reviews": num_reviews
})

print(df)

df.to_csv("books.csv", index=False)
print("Saved scraped data to books.csv")