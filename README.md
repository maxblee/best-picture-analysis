 # Cleaning data for our Oscar Analysis

 ## Scraping the Oscar data

 You can see the code we used to scrape the oscar data in `diversity_analysis/oscar_results.py`. 

 We decided to specifically focus on TBD. In order to collect those results, we typed:

 ```sh
 python diversity_analysis/oscar_results.py "Best Picture" -o data/best_picture.csv
 ```

 ## Formatting the IMDb data

 IMDb posts data on its movies [online](https://datasets.imdbws.com/). We specifically focused on its
 `title.basics.tsv.gz` file, which contains basic information about movies, including the genre of the movies.

 After downloading and uncompressing this data, we typed this to properly format the data as a CSV file:
 ```sh
xsv input data.tsv --no-quoting | xsv search "movie" -s titleType > imdb_movie_data.csv
```