import csv
import json
import pandas as pd
from datetime import datetime


class DataExporter:
    def __init__(self):
        pass
    
    def export_to_csv(self, results, output_path):
        posts = results.get('posts', [])
        
        # Flatten post data for CSV
        csv_data = []
        for post in posts:
            row = {
                'title': post['title'],
                'score': post['score'],
                'num_comments': post['num_comments'],
                'title_polarity': post['title_sentiment']['polarity'],
                'title_subjectivity': post['title_sentiment']['subjectivity'], 
                'title_sentiment': post['title_sentiment']['sentiment'],
                'content_polarity': post['content_sentiment']['polarity'],
                'content_subjectivity': post['content_sentiment']['subjectivity'],
                'content_sentiment': post['content_sentiment']['sentiment'],
                'overall_polarity': post['overall_sentiment']['polarity'],
                'overall_subjectivity': post['overall_sentiment']['subjectivity'],
                'overall_sentiment': post['overall_sentiment']['sentiment']
            }
            csv_data.append(row)
        
        df = pd.DataFrame(csv_data)
        df.to_csv(output_path, index=False)
        
        return f"Exported {len(csv_data)} posts to {output_path}"
    
    def export_to_json(self, results, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return f"Exported complete analysis to {output_path}"
    
    def export_comments_to_csv(self, results, output_path):
        comments = results.get('comments', [])
        
        csv_data = []
        for comment in comments:
            row = {
                'comment': comment['comment'],
                'score': comment['score'],
                'polarity': comment['sentiment']['polarity'],
                'subjectivity': comment['sentiment']['subjectivity'],
                'sentiment': comment['sentiment']['sentiment']
            }
            csv_data.append(row)
        
        df = pd.DataFrame(csv_data)
        df.to_csv(output_path, index=False)
        
        return f"Exported {len(csv_data)} comments to {output_path}"
    
    def create_summary_report(self, results, output_path):
        report = []
        
        report.append(f"Reddit Sentiment Analysis Report")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Subreddit: r/{results.get('subreddit', 'unknown')}")
        report.append("")
        
        # Post summary
        post_summary = results.get('post_summary', {})
        report.append("POST ANALYSIS:")
        report.append(f"  Total posts analyzed: {post_summary.get('total_analyzed', 0)}")
        report.append(f"  Positive posts: {post_summary.get('positive_count', 0)}")
        report.append(f"  Negative posts: {post_summary.get('negative_count', 0)}")
        report.append(f"  Neutral posts: {post_summary.get('neutral_count', 0)}")
        report.append(f"  Average polarity: {post_summary.get('average_polarity', 0)}")
        report.append(f"  Overall sentiment: {post_summary.get('overall_sentiment', 'unknown')}")
        report.append("")
        
        # Comment summary if available
        if 'comment_summary' in results:
            comment_summary = results['comment_summary']
            report.append("COMMENT ANALYSIS:")
            report.append(f"  Total comments analyzed: {comment_summary.get('total_analyzed', 0)}")
            report.append(f"  Positive comments: {comment_summary.get('positive_count', 0)}")
            report.append(f"  Negative comments: {comment_summary.get('negative_count', 0)}")
            report.append(f"  Neutral comments: {comment_summary.get('neutral_count', 0)}")
            report.append(f"  Average polarity: {comment_summary.get('average_polarity', 0)}")
            report.append("")
        
        # Top posts by sentiment
        posts = results.get('posts', [])
        if posts:
            sorted_posts = sorted(posts, key=lambda x: x['overall_sentiment']['polarity'], reverse=True)
            
            report.append("TOP POSITIVE POSTS:")
            for i, post in enumerate(sorted_posts[:3]):
                if post['overall_sentiment']['polarity'] > 0:
                    report.append(f"  {i+1}. {post['title'][:60]}...")
                    report.append(f"     Score: {post['score']}, Polarity: {post['overall_sentiment']['polarity']}")
            
            report.append("")
            report.append("TOP NEGATIVE POSTS:")
            negative_posts = [p for p in reversed(sorted_posts) if p['overall_sentiment']['polarity'] < 0]
            for i, post in enumerate(negative_posts[:3]):
                report.append(f"  {i+1}. {post['title'][:60]}...")
                report.append(f"     Score: {post['score']}, Polarity: {post['overall_sentiment']['polarity']}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        return f"Generated summary report: {output_path}"