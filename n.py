

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


CSV_PATH = Path("/Users/zainabahmadi/Desktop/N/netflix_titles.csv")  
df = pd.read_csv(CSV_PATH)


print("Shape:", df.shape)
print(df.head(3))


df = df.dropna(subset=["type", "rating", "listed_in"])


df["rating"] = df["rating"].str.strip()
df["listed_in"] = df["listed_in"].str.strip()


type_counts = df["type"].value_counts().sort_index()
type_perc = (type_counts / type_counts.sum() * 100).round(1)

print("\nMovies vs TV Shows (counts):")
print(type_counts)
print("\nMovies vs TV Shows (percent):")
print(type_perc)

plt.figure(figsize=(6, 4))
type_counts.plot(kind="bar")
plt.title("Figure 1. Netflix Catalog by Format")
plt.xlabel("Type")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("figure_1_type_distribution.png", dpi=300)


rating_counts = df["rating"].value_counts()
rating_perc = (rating_counts / rating_counts.sum() * 100).round(1)

print("\nRatings (counts):")
print(rating_counts.head(20))
print("\nRatings (percent):")
print(rating_perc.head(20))


topN = 10
plt.figure(figsize=(8, 5))
rating_counts.head(topN).plot(kind="bar")
plt.title("Figure 2. Distribution of Maturity Ratings (Top 10)")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("figure_2_ratings_distribution.png", dpi=300)

genres = (
    df.assign(genres_list=df["listed_in"].str.split(","))
      .explode("genres_list")
)


genres["genres_list"] = genres["genres_list"].str.strip()


genres["genres_list"] = genres["genres_list"].replace({
    "Children & Family Movies": "Children & Family",
    "TV Dramas": "Dramas",
    "TV Comedies": "Comedies",
    "International TV Shows": "International",
    "International Movies": "International"
})

genre_counts = genres["genres_list"].value_counts()
print("\nTop genres (counts):")
print(genre_counts.head(20))


plt.figure(figsize=(10, 6))
genre_counts.head(10).plot(kind="bar")
plt.title("Figure 3. Top Genres in the Netflix Catalog (After Splitting)")
plt.xlabel("Genre")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("figure_3_top_genres.png", dpi=300)

table = pd.crosstab(df["type"], df["rating"])
table_pct = (table.div(table.sum(axis=1), axis=0) * 100).round(1)

print("\nTable 1. Ratings by Type (percent within row):")
print(table_pct.sort_index(axis=1))  
table_pct_sorted = table_pct[sorted(table_pct.columns)]
table_pct_sorted.to_csv("table_1_ratings_by_type_percent.csv")


df.to_csv("netflix_clean_for_eda.csv", index=False)

print("\nSaved outputs:")
print(" - figure_1_type_distribution.png")
print(" - figure_2_ratings_distribution.png")
print(" - figure_3_top_genres.png")
print(" - table_1_ratings_by_type_percent.csv")
