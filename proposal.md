## Proposal

### Motivation and Purpose

We would like to explore how the movie industry has developed over time, particularly regarding revenue streams, both domestic and worldwide, with respect to different genres. The film industry creates and provides entertainment for millions of people worldwide, and is worth a staggering amount of money. The global box office of all films in 2018 was over 41 billion USD, with almost 12 billion USD in just the US alone. This could be of particular interest to someone in the industry in Vancouver, as many movies -- blockbusters and indie films alike -- are shot in Vancouver; with production companies spending around 3.5 billion in 2018 in BC. This app would help illustrate the trends in consumer tastes in film, through box office figures, perceived quality by the audience through IMDB ratings, and how they are correlated with each other. Different filters and options provide ease of access to subset the data as the user likes.

### Describe the dataset

The movies dataset that we'll be working with to make this dashboard is from the [Vega dataset library](https://github.com/vega/vega-datasets). Unfortunately the Vega library does not have additional information about who specifically (which people or organizations) gathered the data or how it was gathered.

In the `movies` dataset, there is a wealth of information on thousands of movies. The information includes foreign and domestic box office returns, DVD sales, budgets (how much a movie cost to make),running times, ratings from the websites [Rotten Tomatoes](https://www.rottentomatoes.com) and [IMDB](https://www.imdb.com), the release date, and more. One notable variable that the data does not have is opening weekend box office returns. This is one metric that studios and industry investors value highly and it is unfortunate that the dataset does not contain this information. 

The `movies` dataset includes movies from 1915 to 2010 and some information on a handful of movies from 2011. There are some movies in the dataset which are listed as having release dates from 2015 to 2046, but these were seemingly entered incorrectly and actually came out between 1915 and 1946. *Birth of a Nation* and *Gone with the Wind* are among the more notable of these incorrectly listed films. 

### Research Questions:

Some research questions that could be answered by this dashboard are: 

- What genre has been most profitable in the last five years?

- How much does critical reception affect profit? What about audience reception?

- What genre of movie is the cheapest to produce? How profitable is it?

#### Example User

Stanley Spielberg is a young executive at a film studio. Every day he is tasked with making decisions over which movies should be made. The film studio is fairly new and doesn’t have as many resources as some of the other bigger companies in the industry so he needs to make smart decisions quickly about how profitable a film might be. When he looks at his “Movie Profitability Dashboard”,  he can see information on box office returns (how much money a movie made in the US) and he can filter by domestic (US) or international box office to get a better understanding of where he might want to focus marketing efforts. He can also look at information on budgets, profits, and profit ratios filtered by genre, year, and month to see how likely a certain movie might perform at a certain time. He can also see how important critical and fan reception is, so he’ll be able to gauge whether or not he should spend more money on better actors and directors.

For example, Stanley might notice that superhero films appear to be incredibly popular, but he wants to know how profitable they are. When he filters the data to show only the most recent ten years, he would see that they do get the highest box office returns, but the budgets are also huge compared to other genres. Therefore, the movies tend to be either very profitable or very unprofitable. This kind of variation in profit indicates a high risk that might not want to take as a new executive at a small studio. 