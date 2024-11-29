Here are a few approaches you could take for your recommendation system:

Content-Based Filtering:

Utilize features like genres, tags, categories, platforms, and supported languages to recommend games similar to what a user has liked or played before.
You could create similarity scores using cosine similarity or other distance metrics based on these attributes.

Collaborative Filtering:

Use user reviews and ratings to find similarities between users and games.
Implement user-based or item-based collaborative filtering using algorithms like k-Nearest Neighbors (k-NN) or matrix factorization techniques (e.g., SVD).

Hybrid Approach:
Combine both content-based and collaborative filtering to enhance your model's accuracy and diversity.


Steam review system

95 - 100 | 500+ reviews | positive | overwhelming

85 - 100 | 50+ reviews | positive | very

80 - 100 | 1+ reviews | positive

70 - 79 | 1+ reviews | positive | mostly

40 - 69 | 1+ reviews | mixed

20 - 39 | 1+ reviews | negative | mostly

0 - 19 | 1+ reviews | negative

0 - 19 | 50+ reviews | negative | very

0 - 19 | 500+ reviews | negative | overwhelming

## features being taken to do clustering
1. Platform : windows, linux, mac bool true false
2. Price : float64
3. categories : single player, multipliay , pvp, controller support , etc ...
4. generes : indie, casual, action , adventure, etcccc
5. release year : int exampel 2004

good data base
https://www.kaggle.com/datasets/trolukovich/steam-games-complete-dataset


## Making aggregate features
1. We can use metacritic score that is for 3k games
2. postive/negative scores ratio
3. recommendations 15k

estimated owners is alo useful

number of games that have either
1. metacritic score != 0
2. reccomendatios != 0
3. user_score != 0
4. postive != 0 and negative != 0
5. average_playtime_forever != 0

After Midsem Improvements:
1. Use K-means++ for clustering
2. compare K-means++ with K-means
3. compare K-means++ with eucledian distance, manhattan distance, cosine similarity, mahalnobis distance