# Kara Solutions

## Overview

This project builds an end-to-end data platform for generating actionable insights about the Ethiopian medical business ecosystem using data scraped from public Telegram channels. The platform follows a modern ELT architecture to transform unstructured Telegram data into analytics-ready datasets and exposes insights through a FastAPI-based analytical API.

## Business Objectives

* Analyze trends in medical products and drugs mentioned across Telegram channels
* Track price and availability variations across channels
* Identify channels with high visual (image-based) medical content
* Monitor daily and weekly posting trends for health-related topics

## Architecture

* **Extract**: Scrape text and image data from public Telegram channels
* **Load**: Store raw data in a data lake and load into PostgreSQL
* **Transform**: Clean, enrich, and model data using dbt into a star schema
* **Enrich**: Apply YOLO-based object detection on images
* **Serve**: Expose analytical insights via a FastAPI service

## Tech Stack

* Python
* PostgreSQL
* dbt
* FastAPI
* YOLO (Object Detection)
* Telegram Scraping Libraries

## Project Structure

```
├── data/                # Raw and processed data
├── medical_warehouse/   # dbt model and tests 
├── api/                 # FastAPI application
├── src/scraping.py      # Telegram scraping scripts
├── notebooks/           
├── requirements.txt     # Python dependencies
└── README.md

```

## Environment Setup

Follow the steps below to set up the project environment locally.

### 1. Clone the Repository

```bash
git clone <https://github.com/RuetGG/Kara_ELT_Week_8.git>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

* **Windows**:

```bash
venv\Scripts\activate
```

* **macOS / Linux**:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

* Ensure PostgreSQL is installed and running
* Create a database for the project
* Update database connection settings in environment variables or config files as required

## Running the Pipeline

1. Run Telegram scraping scripts to populate the raw data lake
2. Load raw data into PostgreSQL
3. Execute dbt models to transform and model the data
4. Run YOLO enrichment on image data

## Running the API

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Future Improvements

* Add scheduling and orchestration (e.g., Airflow)
* Improve NLP-based entity extraction
* Extend API endpoints for advanced analytics

## Author

Kara Solutions Data Engineering Team
