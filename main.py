import argparse
import json
import sys
from datetime import datetime
from reddit_client import RedditClient
from sentiment_analyzer import SentimentAnalyzer
from export_utils import DataExporter


def main():
    parser = argparse.ArgumentParser(description='Analyze sentiment of Reddit posts and comments')
    parser.add_argument('--subreddit', '-s', required=True, help='Subreddit name to analyze')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Number of posts to analyze')
    parser.add_argument('--sort', choices=['hot', 'new', 'top'], default='hot', help='Sort posts by')
    parser.add_argument('--comments', '-c', action='store_true', help='Also analyze comments')
    parser.add_argument('--output', '-o', help='Output file path (JSON format)')
    parser.add_argument('--format', choices=['json', 'csv', 'report'], default='json', help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        reddit_client = RedditClient()
        analyzer = SentimentAnalyzer()
        exporter = DataExporter()
        
        print(f"Fetching {args.limit} posts from r/{args.subreddit} (sorted by {args.sort})")
        posts = reddit_client.get_subreddit_posts(args.subreddit, args.limit, args.sort)
        
        if not posts:
            print("No posts found.")
            sys.exit(1)
        
        print("Analyzing post sentiment...")
        post_results = analyzer.analyze_posts(posts)
        
        comment_results = []
        if args.comments:
            print("Analyzing comments...")
            for i, post in enumerate(posts):
                if 'url' in post and 'reddit.com' in post['url']:
                    post_id = post['url'].split('/')[-2]
                    comments = reddit_client.get_post_comments(post_id, 10)
                    comment_analysis = analyzer.analyze_comments(comments)
                    comment_results.extend(comment_analysis)
        
        # Generate summary stats
        post_summary = analyzer.get_summary_stats(post_results)
        
        results = {
            'subreddit': args.subreddit,
            'analysis_date': datetime.now().isoformat(),
            'posts_analyzed': len(post_results),
            'comments_analyzed': len(comment_results),
            'post_summary': post_summary,
            'posts': post_results
        }
        
        if comment_results:
            comment_summary = analyzer.get_summary_stats(comment_results)
            results['comment_summary'] = comment_summary
            results['comments'] = comment_results
        
        # Output results
        if args.output:
            if args.format == 'json':
                message = exporter.export_to_json(results, args.output)
            elif args.format == 'csv':
                message = exporter.export_to_csv(results, args.output)
                if comment_results:
                    comment_output = args.output.replace('.csv', '_comments.csv')
                    comment_message = exporter.export_comments_to_csv(results, comment_output)
                    message += f"\n{comment_message}"
            elif args.format == 'report':
                message = exporter.create_summary_report(results, args.output)
            
            print(message)
        
        # Print summary to console
        print(f"\n--- Analysis Summary for r/{args.subreddit} ---")
        print(f"Posts analyzed: {post_summary['total_analyzed']}")
        print(f"Positive: {post_summary['positive_count']}")
        print(f"Negative: {post_summary['negative_count']}")
        print(f"Neutral: {post_summary['neutral_count']}")
        print(f"Average polarity: {post_summary['average_polarity']}")
        print(f"Overall sentiment: {post_summary['overall_sentiment']}")
        
        if comment_results and 'comment_summary' in results:
            comment_summary = results['comment_summary']
            print(f"\nComments analyzed: {comment_summary['total_analyzed']}")
            print(f"Positive: {comment_summary['positive_count']}")
            print(f"Negative: {comment_summary['negative_count']}")
            print(f"Neutral: {comment_summary['neutral_count']}")
            print(f"Average polarity: {comment_summary['average_polarity']}")
        
        if args.verbose:
            print("\n--- Individual Post Results ---")
            for i, post in enumerate(post_results[:5]):  # Show first 5
                print(f"\nPost {i+1}: {post['title'][:50]}...")
                print(f"Score: {post['score']}, Sentiment: {post['overall_sentiment']['sentiment']}")
                print(f"Polarity: {post['overall_sentiment']['polarity']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()