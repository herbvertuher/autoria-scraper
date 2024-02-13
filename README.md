<div align="center" style="margin-top: 0;">
  <h1>🚗 AutoRia Scraper ✨</h1>
</div>

---

This application is designed to scrape data periodically from the AutoRia platform, specifically focusing on used cars. The starting page URL can be hardcoded into the application.

## 👀 Features
- The application is scheduled to run daily at a specified time (e.g., 12:00 PM) and traverse through all pages starting from the initial page, scraping data from each car listing.
- All scraped data is stored in a PostgreSQL database.
- Duplicate entries are filtered out to ensure data integrity.
- The application performs a daily database dump at a specified time (e.g., 11:00 PM) and saves dump files in the "dumps" folder located in the root directory of the application.
- Pip is used as the package manager.
- Application settings are stored in a `.env` file.

## 👉 Structure

    autoria-scraper/
    ├── utils
    │   ├── __init__.py
    │   ├── async_scraper.py
    │   ├── config.py
    │   ├── db_helper.py
    │   └── log.txt
    │
    ├── dumps/
    │
    ├── .env
    ├── main.py
    ├── README.py
    └── requirements.txt

---

## 🚀 Setup

1️⃣ **Clone the repository from GitHub:**
```shell
git clone https://github.com/herbvertuher/autoria-scraper
cd autoria-scraper
```

2️⃣ **Install dependencies using pip:**
```shell
pip install -r requirements.txt
```

3️⃣ **Set up PostgreSQL and create a database.**

4️⃣ **Create a .env file** and specify the required settings (e.g., database connection details, starting page URL, scheduled times).

5️⃣ **Run the application:**
 ```shell
python main.py
 ```

## ✌️ Contributions
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## ☝️ Disclaimer
This application is created for educational and demonstration purposes. Use responsibly and adhere to the terms of service of the AutoRia platform.
