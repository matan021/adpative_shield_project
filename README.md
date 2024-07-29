# Web Scraper Project

This project is designed to scrape images and tables from websites and store the data locally or in an S3 bucket.

## Features

- Scrape HTML content from a website
- Download the images concurrently and save them to a local directory.
- Extract image links and download images
- Extract table data and process it
- Save files to an S3 bucket

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/matan021/adaptive_shield_project
    ```

2. Navigate to the project directory:
    ```sh
    cd adaptive_shield_project
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. dev running 
```shell
docker-compose -f docker-compose-dev.yml up
python src/main.py
```

### Running test
To run the tests:
```sh
python -m unittest discover -s tests
```

