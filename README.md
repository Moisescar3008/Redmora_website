# Redmora: Watershed Data Integration and News Scraping System

**Redmora** RedMORA (Water Reserve Monitoring Network) is a Mexican network that focuses on the monitoring, planning and management of water reserves in the country. Its objective is to promote sustainable water management, both in nature reserves and in basins under human pressure, through research, communication and participatory management. 

---

## 🌊 What is a Watershed?

A **watershed** (*cuenca*) is a geographical region where all water from rain or snow drains into a common outlet such as a river, lake, or ocean. Studying watersheds is crucial for environmental monitoring, conservation, and policy-making.

---

## 📍 Watersheds Covered

This project focuses on the following major Mexican watersheds:

- **Usumacinta**
- **Papaloapan**
- **San Pedro**

Each basin has associated environmental data and metadata, which has been processed and visualized.

---

## 📁 Project Structure

| File/Folder              | Description |
|--------------------------|-------------|
| `app.py`                 | Main Flask application script that serves the dashboard or web interface. |
| `google_scraper.py`      | Python script that scrapes Google Search for watershed-related news. |
| `organizing_urls.py`     | Organizes and filters the URLs retrieved by the scraper. |
| `Dockerfile`             | Docker build configuration for containerizing the app. |
| `compose.yml`            | Docker Compose file to run the app with all required services. |
| `requirements.txt`       | Python dependencies list. |
| `README.md`              | This documentation file. |
| `.venv/`                 | (Optional) Local Python virtual environment. Not needed when using Docker. |
| `Cuencas/`               | Contains raw `.mdb` files (Access Databases) for each watershed. |
| `Databases/`             | Contains preprocessed `.xlsx` files derived from `.mdb` sources. |
| `Preprocess/`            | Jupyter notebooks for transforming and cleaning the raw data. |
| `archivos/`              | Output files from scraping: `.json`, `.xlsx`, and `.csv` formats. |
| `static/`                | Static assets such as images, stylesheets, and JavaScript files. |

---

## 📦 Python Dependencies

If you prefer running the project locally (without Docker), install the dependencies with:

```bash
pip install -r requirements.txt
```
## 🐳 Running with Docker
Using Docker is the easiest and most reliable way to run the project.

## 🛠️ Requirements
Docker Desktop installed and running

## 🔧 Build and Run
From the project root directory, execute:

bash
Copy
Edit
```bash
docker compose up --build
```
This will:

Build the container image from Dockerfile

Use compose.yml to launch the app

Once running, open your browser and go to:

arduino
Copy
Edit
http://localhost:5050
You will see the Redmora dashboard or app interface.

## 📊 Outputs and Data
Scraped news articles are stored in archivos/ as .json and .xlsx files

Transformed environmental datasets are in Databases/

Preprocessing logic and experiments are in Preprocess/

Visual and media content is served from the static/ folder

## 🤝 Authors and Credits
Moises Carrillo — Web Developer

Oscar Martinez — Web Scraper

Iris Flores — Supervisor

## 📌 Notes
.venv/ folder is included for completeness but not needed when using Docker.

.mdb files may require MS Access or ODBC-compatible tools to explore them outside of the notebooks

In case of some error at the moment of copying the path of the docker at a browser, just change the local host to 5050.
Example: If the docker gives you a localhost of 5000:5000 at the moment of paste it to a browser just change the 5000 to 5050.

