#!/usr/bin/env python3
import pandas as pd
import regex as re
# All variables can be printed by editing the print function in def main()
def read_userData(data):
    # Drop useless data
    data = data.drop(['User id', 'Zip code'], axis=1)

    # Show users with occupation 'other'
    occupation = data.loc[data['Occupation'] == 'other']
    occupation.set_index('Age', inplace=True)

    # Show males over 40
    maleOver40 = data.loc[(data['Gender'] == 'M') & (data['Age'] > 40)]
    maleOver40.set_index('Age', inplace=True)

    # Show mean age of writers
    writers = data.loc[data['Occupation'] == 'writer']
    # writers now returns the mean
    writers = writers['Age'].mean()

    # Looks nicer without index
    data.set_index('Age', inplace=True)

    # Return variables to main()
    return data, occupation, maleOver40, writers

def read_ratingData(data):
    # Group by movie id
    group = data.groupby('Movie id', as_index= True)

    # Mean rating of movies
    mean = group['Rating'].mean()
    # Only movies with over 40 reviews
    ratingSize = group['Rating'].size()
    ratingSize = ratingSize.loc[group['Rating'].size() > 40]

    # Best mean rating for movies with over 40 ratings -->
    # Merge mean list with the shorter ratingSize list to remove movies with too few ratings
    top = pd.merge(ratingSize, mean, left_index=True, right_on="Movie id")
    top.columns = ['Number of ratings', 'Average rating']
    # Now that only movies with > 40 ratings are present, we show the top 10
    top = top.sort_values(['Average rating'], ascending=False)
    top = top.head(10)

    # Return to main()
    return mean, top
    
def read_movieData(data):

    # Fix placement of releas date data
    data['Video release date'] = data['Release date']
    data['Release date'] = data['Movie title'].str.extract(r'(\d+)')
    # Remove the year from movie title (But only year because some movie names contain parantheses)
    data['Movie title'] = data['Movie title'].str.replace(r'(\d+)','')
    # Remove the now epmty parantheses
    data['Movie title'] = data['Movie title'].str.replace(r'\(\)','')
    # Return this data to main()
    return data

def combine_df(jobData):
    # Divide data by gender
    m = jobData.loc[(jobData['Gender'] == 'M')]
    f = jobData.loc[(jobData['Gender'] == 'F')]

    # Group gender by occupation
    mGroup = m.groupby('Occupation')
    fGroup = f.groupby('Occupation')

    # Check who works where
    mJobs = mGroup['Gender'].size().astype(float)
    fJobs = fGroup['Gender'].size().astype(float)
    mTopJobs = mJobs.sort_values(ascending=False)
    fTopJobs = fJobs.sort_values(ascending=False)

    # Combine info to compare genders
    jobs = pd.concat([fTopJobs, mTopJobs], axis=1)
    jobs.columns = ['Females', 'Males']

    # Remove NaN
    jobs['Females'] = jobs['Females'].fillna(0)

    # Add to se total number of occupation
    jobs['All'] = jobs['Females'] + jobs['Males']

    # Divide to se ratio
    jobs['Ratio Male/Female'] = jobs['Males']/jobs['Females']
    # Return to main()
    return jobs
    
def main():
    # Read csv and make it easier to read
    user = pd.read_csv("ml-100k/u.user", sep="|", header=None, encoding='latin-1')
    user.columns = ['User id', 'Age', 'Gender', 'Occupation', 'Zip code']

    rating = pd.read_csv("ml-100k/u.data", sep="\s+|\t+|\s+\t+|\t+\s+", header=None, encoding='latin-1', engine='python', dtype=int)
    rating.columns = ['User id', 'Movie id', 'Rating', 'Timestamp']

    movie = pd.read_csv("ml-100k/u.item", sep="|", header=None, usecols=range(5), encoding='latin-1')
    movie.columns = ['Movie id', 'Movie title', 'Release date', 'Video release date', 'IMDb url']

    # All the calculated variables
    userData, occupation, maleOver40, writers = read_userData(user)
    mean, top = read_ratingData(rating)
    movieData = read_movieData(movie)

    # Typical occupation
    typicalOccupation = combine_df(userData)

    # u.item + u.user
    combined1 = pd.merge(rating, movieData)
    # Remove extra stuff
    combined1 = combined1.drop(['Movie id', 'Timestamp', 'IMDb url'], axis=1)
    # combine with u.user
    combinedFinal = pd.merge(combined1, user)

    # Who is toughest and who is leanest? 
    group = combinedFinal.groupby('User id', as_index=False)
    # Calculate mean review given
    mean = group['Rating'].mean()
    mean = mean.sort_values(by='Rating', ascending=False)
    # Show leanes (top) and toughest (bottom) critics
    top = mean.head(5)
    bottom = mean.tail(5)

    # Combine with u.user to show info about these critics
    userInfoTop = pd.merge(user,top)
    userInfoBottom = pd.merge(user,bottom)


    # Change variable here to view the different data points
    print(typicalOccupation)

if __name__ == "__main__":
    main()