from flask import Flask,render_template,request
import pickle
import numpy as np
import joblib

popular_df = joblib.load('pkl/popular.joblib')
pt = joblib.load('pkl/pt.joblib')
books = joblib.load('pkl/books.joblib')
similarity_score = joblib.load('pkl/similarity_score.joblib')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_ratings'].apply(lambda x: round(x,1)).values)


                           )

@app.route('/recommed')
def recommend_ui():
    return render_template('recommed.html')

@app.route('/about')
def about_me():
    return render_template('about.html')


@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data =[]
    
    for i in similar_item:
        item =[]
        temp_df = books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['num_ratings'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['avg_ratings'].values))
        
        data.append(item)
        
    print(data)
    
    return render_template('recommed.html',data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)