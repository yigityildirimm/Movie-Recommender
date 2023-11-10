import pandas as pd
import streamlit as st

st.title("Movie Recommender")
st.write("Popular Movie Recommender")
n = st.slider("You can select number of most popular movies.",0,100,1)
st.write("You selected", n)



links_df = pd.read_csv('links.csv')
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
tags_df = pd.read_csv('tags.csv')

ratings_mc_df=ratings_df.groupby("movieId")["rating"].agg(["mean","count"]).reset_index()


ratings_mc_df.sort_values(by=['count', 'mean'], ascending=False).head()

ratings_mc_df["overall_rating"] = (ratings_mc_df["mean"]*2) + (ratings_mc_df["count"]*0.01)


ratings_mc_df.sort_values(by=['overall_rating'], ascending=False).head()

ratings_mc_df_merged=ratings_mc_df.merge(
    movies_df,
    on="movieId",
    how="inner"
)
ratings_mc_merged_df = ratings_mc_df_merged[["movieId","title","genres", "mean", "count", "overall_rating"]]


#create function
def get_top_n(ratings_mc_merged_df, n):
  top_n_movies_df=pd.DataFrame(ratings_mc_merged_df).nlargest(n,"overall_rating")
  return top_n_movies_df


get_top_n(ratings_mc_merged_df, n)


