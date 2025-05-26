# Reddit Sentiment Analyzer

A Python tool for analyzing sentiment in Reddit posts and comments using TextBlob.

## Features

- Fetch posts from any subreddit using Reddit API
- Analyze sentiment of post titles and content 
- Optional comment sentiment analysis
- Multiple export formats (JSON, CSV, summary report)
- Configurable post limits and sorting options
- Command line interface with detailed output

## Installation

1. Clone the repository:
```bash
git clone https://github.com/0xthornfield/reddit-sentiment-analyzer.git
cd reddit-sentiment-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Reddit API credentials:
- Copy `.env.example` to `.env`
- Fill in your Reddit API credentials (get them from https://reddit.com/prefs/apps)
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Usage

Basic usage:
```bash
python main.py --subreddit python --limit 20
```

With comment analysis:
```bash
python main.py -s cryptocurrency -l 50 -c --sort top
```

Export to CSV:
```bash
python main.py -s technology -l 30 --output results.csv --format csv
```

Generate summary report:
```bash
python main.py -s politics -l 100 --output report.txt --format report
```

### Command line options:
- `-s, --subreddit`: Target subreddit (required)
- `-l, --limit`: Number of posts to analyze (default: 10)  
- `--sort`: Sort by 'hot', 'new', or 'top' (default: hot)
- `-c, --comments`: Also analyze comments
- `-o, --output`: Output file path
- `--format`: Output format - 'json', 'csv', or 'report' (default: json)
- `-v, --verbose`: Show detailed individual post results

## Output Formats

- **JSON**: Complete analysis data with all metadata
- **CSV**: Tabular format suitable for data analysis
- **Report**: Human-readable summary with top posts

## Requirements

- Python 3.7+
- Reddit API credentials
- Dependencies listed in requirements.txt