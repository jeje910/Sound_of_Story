# Sound_of_Story


## Todo Lists
- [X] Data Downloading
- [X] Data Processing
- [ ] Retrieval Baselines
- [ ] Audio Generation Baselines


## 1. Download Movie datasets

### Download Condensed Movie Dataset

> https://www.robots.ox.ac.uk/~vgg/data/condensed-movies/

### Download LSMDC Dataset

> https://sites.google.com/site/describingmovies


## 2. Data post-processing

0. Before start, you shoud download the description of CondensedMovies from the link below:

> https://github.com/m-bain/CondensedMovies/tree/master/data/metadata


1. After download all the datsets, run the processing codes as follow

```
sh video_processing.sh
```

※ Note that you **MUST** change the path for each data dataset in shell script code

2. After all movies are generated & processed, Run the post processing code as follow

```
sh data_processing.sh
```

## 3. Run models