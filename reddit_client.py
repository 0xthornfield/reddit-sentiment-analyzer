import praw
import logging
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

logger = logging.getLogger(__name__)


class RedditClient:
    def __init__(self):
        if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
            raise ValueError("Missing Reddit API credentials. Please check your .env file.")
        
        try:
            self.reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT
            )
            logger.info("Reddit client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {e}")
            raise
    
    def get_subreddit_posts(self, subreddit_name, limit=10, sort_by='hot'):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            logger.info(f"Fetching {limit} posts from r/{subreddit_name} sorted by {sort_by}")
            
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
                try:
                    post_data.append({
                        'title': post.title,
                        'selftext': post.selftext,
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'url': post.url
                    })
                except Exception as e:
                    logger.warning(f"Failed to process post {post.id}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(post_data)} posts")
            return post_data
            
        except Exception as e:
            logger.error(f"Failed to fetch posts from r/{subreddit_name}: {e}")
            raise
    
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