import models.model as my_model
import data_preprocessing

# Load the model
model = my_model.load_model()


def labels_to_sentiment(polarity):
    if polarity == "LABEL_1":
        return 'Positive'
    elif polarity == 'LABEL_0':
        print(polarity)
        return 'Negative'

def sentiment_predict(df_reviews):
    temp_df = df_reviews.copy()
    temp_df["cleaned_reviews"] = temp_df["Reviews"].apply(data_preprocessing.preprocessing)
    temp_df = temp_df[temp_df['cleaned_reviews'].str.len() > 0]
    temp_df['Sentiment'] = ''
    temp_df['Score'] = ''

    for index, row in temp_df.iterrows():
        text = row["Reviews"]
        sentiment = 'Positive' if model(str(text))[0]["label"] == 'LABEL_1' else 'Negative'
        score = model(str(text))[0]["score"]
        temp_df.at[index, "Sentiment"] = sentiment
        temp_df.at[index, "Score"] = score

    return temp_df.reset_index(drop=True)

def sentiment_predict_user_input(user_review):
    user_review = data_preprocessing.preprocessing(user_review)
    if len(user_review) == 0:
        return "None", 0
    else:
        prediction = model(user_review)
        if prediction[0]['label'] == 'LABEL_1':
            return 'Positive', prediction[0]['score']
        else:
            return 'Negative', prediction[0]['score']

