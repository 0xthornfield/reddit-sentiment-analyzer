import logging
import sys
from pathlib import Path


def setup_logging(verbose=False):
    """Setup logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('reddit_analyzer.log')
        ]
    )
    
    return logging.getLogger(__name__)


def validate_output_path(output_path, file_format):
    """Validate and adjust output file path based on format."""
    if not output_path:
        return None
    
    path = Path(output_path)
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add appropriate extension if not present
    extensions = {
        'json': '.json',
        'csv': '.csv', 
        'report': '.txt'
    }
    
    expected_ext = extensions.get(file_format, '.txt')
    if not path.suffix:
        path = path.with_suffix(expected_ext)
    
    return str(path)


def safe_divide(numerator, denominator):
    """Safely divide two numbers, return 0 if denominator is 0."""
    if denominator == 0:
        return 0
    return numerator / denominator


def truncate_text(text, max_length=100):
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'