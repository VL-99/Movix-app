from flask import Flask, render_template, request
import pickle
import pandas
import requests

app=Flask(__name__)

top_50=pickle.load(open('top_50.pkl', 'rb'))
movies=pickle.load(open('movies.pkl', 'rb'))
movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies_dataframe=pandas.DataFrame(movies_dict)
similarity_scores=pickle.load(open('similarity_scores.pkl', 'rb'))



@app.route('/')
def home():
    print(top_50['title'])
    return render_template("home.html",
                           movie=list(top_50['title'].values),
                           rating=list(top_50['vote_average'].values),
                           homepage=list(top_50['homepage'].values))

@app.route('/suggest')
def suggest():
    return render_template("suggest.html")

@app.route("/display_movies", methods=['POST'])
def recommend():
    user_input=request.form.get('entry')
    try:
        position = movies_dataframe[movies_dataframe['title'] == user_input].index[0]
        distance = similarity_scores[position]
        movies_recommended = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:11]
        movies_suggested = []

        for item in movies_recommended:
            movies_suggested.append(movies_dataframe.iloc[item[0]].title)
    except Exception as e:
        return render_template('suggest.html', data=[], msg="Make sure you enter the right name.")

    return render_template('suggest.html', data=movies_suggested)

if __name__=="__main__":
    app.run(debug=True)