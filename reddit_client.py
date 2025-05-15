import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    def get_subreddit_posts(self, subreddit_name, limit=10, sort_by='hot'):
        subreddit = self.reddit.subreddit(subreddit_name)
        
        if sort_by == 'hot':
            posts = subreddit.hot(limit=limit)
        elif sort_by == 'new':
            posts = subreddit.new(limit=limit)
        elif sort_by == 'top':
            posts = subreddit.top(limit=limit)
        else:
            posts = subreddit.hot(limit=limit)
        
        post_data = []
        for post in posts:
            post_data.append({
                'title': post.title,
                'selftext': post.selftext,
                'score': post.score,
                'num_comments': post.num_comments,
                'created_utc': post.created_utc,
                'url': post.url
            })
        
        return post_data
    
    def get_post_comments(self, submission_id, limit=50):
        submission = self.reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)
        
        comments = []
        for comment in submission.comments.list()[:limit]:
            if hasattr(comment, 'body') and comment.body != '[deleted]':
                comments.append({
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc
                })
        
        return comments