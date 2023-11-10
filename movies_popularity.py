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





movies_df['year'] = movies_df['title'].str[-5:-1]


# In[23]:


movies_df['title'] = movies_df['title'].str[:-7].str.strip()


# In[24]:


user_movie_matrix = pd.pivot_table(data=ratings_df,
                                  values='rating',
                                  index='userId',
                                  columns='movieId',
                                  fill_value=0)


# In[ ]:


item_correlations_matrix = user_movie_matrix.corr(method='pearson')


# In[ ]:


# Function to get similar movies
def get_similar_movies(movie_name, n=5):
    # Check if the movie exists in the movies dataframe
    if movie_name not in movies_df['title'].values:
        return f"Movie '{movie_name}' not found in the dataset."

    # Get the movieId for the input movie name
    movie_id = movies_df.loc[movies_df['title'] == movie_name, 'movieId'].values[0]

    # Get the correlation vector for the input movie
    corr_vector = item_correlations_matrix[movie_id]

    # Get the top n similar movies based on correlation
    similar_movie_ids = corr_vector.sort_values(ascending=False).index[1:n+1]

    # Retrieve the movie information (title, genres, year) for the similar movies
    similar_movies_info = movies_df[movies_df['movieId'].isin(similar_movie_ids)][['title', 'genres', 'year']]

    return similar_movies_info


# In[ ]:


# Streamlit app
def main():
    st.title("Movie Recommendation System")

    # Create input fields for the user to specify the movie and number of recommendations
    movie_title = st.text_input("Enter a Movie Title:", "Monsters, Inc.")  # Default value provided
    n = st.slider("Number of Recommendations", min_value=1, max_value=20, value=10)

    # Add a button to trigger recommendations
    if st.button("Get Recommendations"):
        recommendations = get_similar_movies(movie_title, n)

        if isinstance(recommendations, pd.DataFrame):
            st.header(f"Top {n} Movie Recommendations for '{movie_title}':")
            st.table(recommendations)
        else:
            st.warning(recommendations)

if __name__ == "__main__":
    main()


