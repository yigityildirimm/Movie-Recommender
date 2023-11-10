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
  top_n_movies_df=top_n_movies_df[["title","genres"]]  
  top_n_movies_df.reset_index(drop=True,  inplace=True)

  return top_n_movies_df


x = get_top_n(ratings_mc_merged_df, n)

st.write(x)



######
import base64


st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")



st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

#####

# Merging movies and ratings on 'movieId'
movie_ratings = pd.merge(movies_df, ratings_df, on='movieId')

# Merging movie_ratings and tags on 'movieId'
movie_ratings_tags = pd.merge(movie_ratings, tags_df, on='movieId')


# Defining functions

def get_sparse_matrix(data: pd.DataFrame):
    return data.pivot_table(values='rating', index='userId_x', columns='title', fill_value=0)

def item_based_recommender(data: pd.DataFrame, title: str, n: int = 5):
    sparse_matrix = get_sparse_matrix(data)
    
    if title not in sparse_matrix.columns:
        return "Movie not found in the database."

    similar_movies = (
        sparse_matrix.corrwith(sparse_matrix[title])
        .sort_values(ascending=False)
        .index
        .to_list()[1:n+1]
    )
    return similar_movies


# Streamlit app

becouse_you_like = st.container()

with becouse_you_like:
    st.header('Similar Movies Recommendation')
    
    input_feature = st.text_input('Enter a movie title', '')  # Get user input
    
    if input_feature:
        st.write("Your selected movie is:", input_feature)
        similar_movies = item_based_recommender(movie_ratings_tags, input_feature)
        
        if isinstance(similar_movies, list):
            st.write("Recommended movies:")
            st.write(similar_movies)
        else:
            st.write(similar_movies)


