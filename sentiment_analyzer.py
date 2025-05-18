from textblob import TextBlob
import pandas as pd
import re


class SentimentAnalyzer:
    def __init__(self):
        pass
    
    def clean_text(self, text):
        # Remove URLs, mentions, and special characters
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'/u/\w+|/r/\w+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def analyze_sentiment(self, text):
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment': 'neutral'}
        
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
    
    def analyze_posts(self, posts):
        results = []
        for post in posts:
            # Analyze title
            title_sentiment = self.analyze_sentiment(post['title'])
            
            # Analyze selftext if exists
            selftext_sentiment = {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment': 'neutral'}
            if post.get('selftext'):
                selftext_sentiment = self.analyze_sentiment(post['selftext'])
            
            # Combine title and content sentiment
            combined_polarity = (title_sentiment['polarity'] + selftext_sentiment['polarity']) / 2
            combined_subjectivity = (title_sentiment['subjectivity'] + selftext_sentiment['subjectivity']) / 2
            
            if combined_polarity > 0.1:
                combined_sentiment = 'positive'
            elif combined_polarity < -0.1:
                combined_sentiment = 'negative'
            else:
                combined_sentiment = 'neutral'
            
            results.append({
                'title': post['title'],
                'score': post.get('score', 0),
                'num_comments': post.get('num_comments', 0),
                'title_sentiment': title_sentiment,
                'content_sentiment': selftext_sentiment,
                'overall_sentiment': {
                    'polarity': round(combined_polarity, 3),
                    'subjectivity': round(combined_subjectivity, 3),
                    'sentiment': combined_sentiment
                }
            })
        
        return results
    
    def analyze_comments(self, comments):
        results = []
        for comment in comments:
            sentiment = self.analyze_sentiment(comment['body'])
            results.append({
                'comment': comment['body'][:100] + '...' if len(comment['body']) > 100 else comment['body'],
                'score': comment.get('score', 0),
                'sentiment': sentiment
            })
        
        return results
    
    def get_summary_stats(self, results):
        if not results:
            return {}
        
        sentiments = []
        polarities = []
        
        for result in results:
            if 'overall_sentiment' in result:
                sentiments.append(result['overall_sentiment']['sentiment'])
                polarities.append(result['overall_sentiment']['polarity'])
            else:
                sentiments.append(result['sentiment']['sentiment'])
                polarities.append(result['sentiment']['polarity'])
        
        df = pd.DataFrame({'sentiment': sentiments, 'polarity': polarities})
        
        sentiment_counts = df['sentiment'].value_counts()
        avg_polarity = df['polarity'].mean()
        
        return {
            'total_analyzed': len(results),
            'positive_count': sentiment_counts.get('positive', 0),
            'negative_count': sentiment_counts.get('negative', 0),
            'neutral_count': sentiment_counts.get('neutral', 0),
            'average_polarity': round(avg_polarity, 3),
            'overall_sentiment': 'positive' if avg_polarity > 0.1 else 'negative' if avg_polarity < -0.1 else 'neutral'
        }