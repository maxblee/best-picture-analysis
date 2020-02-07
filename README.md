 # Cleaning data for our Oscar Analysis

 ## Installation

 This requires the following dependencies:
 - Selenium Geckodriver
 - `pipenv` --> Optional, but required if you want to follow the installation directly
 - Python

 From here, you can install the Python dependencies:

 ```sh
 pipenv install
 ```

 ## Scraping the Oscar data

 The code we used to scrape the oscar data is `diversity_analysis/oscar_results.py`. 

 In order to analyze Best Picture results, you need to type:

 ```sh
 python diversity_analysis/oscar_results.py "Best Picture" -o data/best_picture.csv
 ```

We initially looked at the directing and acting categories as well, before deciding to focus specifically on Best Picture nominations.

 ## Formatting the IMDb data

 IMDb posts data on its movies [online](https://datasets.imdbws.com/). We specifically focused on its
 `title.basics.tsv.gz` file, which contains basic information about movies, including the genre of the movies.

 After downloading and uncompressing this data, we typed this to properly format the data as a CSV file:
 ```sh
xsv input data.tsv --no-quoting | xsv search "movie" -s titleType > imdb_movie_data.csv
```

## Analysis

From here, we joined the Oscar data to the IMDb data in order to get the genres for each of these movies. The script we used to do this is `joining-data.ipynb`. 

(Note that this requires obtaining an API key for the Open Movie Database and storing that key with the environment variable `OMDB_API`.)

This process involved some manual work in handling false positives and false negatives, so the script will look fairly clunky. However, I've tried to make it at least somewhat replicable.

From here, our actual analysis is in `data-analysis.ipynb`.