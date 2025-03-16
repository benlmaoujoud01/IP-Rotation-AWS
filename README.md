# RSS Feed Scraper with IP Rotation

A Python utility for fetching and parsing RSS feeds with automatic IP rotation to avoid rate limiting and IP bans.

## Features

- Automatically rotates IP addresses using AWS API Gateway
- Handles multiple RSS feed URLs
- Configurable request limits per URL
- Built-in retry mechanism for failed requests
- Customizable delay between requests
- Detailed logging of request status and feed content

## Prerequisites

- Python 3.6+
- AWS account (for IP rotation functionality)
- AWS CLI configured with appropriate permissions

## Installation

1. Clone this repository or download the script
2. Install the required dependencies:

```bash
pip install requests requests-ip-rotator feedparser
```

3. Configure your AWS credentials:

```bash
aws configure
```

## Usage

### Basic Usage

```python
from rss_scraper import fetch_rss_feeds

feed_urls = [
    "https://example.com/feed.rss",
    "https://another-site.com/rss"
]

fetch_rss_feeds(feed_urls)
```

### Advanced Usage

```python
from rss_scraper import fetch_rss_feeds

feed_urls = [
    "https://example.com/feed.rss",
    "https://another-site.com/rss"
]

# Customize parameters
fetch_rss_feeds(
    feed_urls=feed_urls,
    requests_per_url=50,     # Number of requests per URL (default: 100)
    max_retries=5,           # Maximum retry attempts per request (default: 3)
    delay_between_requests=2 # Delay between requests in seconds (default: 1)
)
```

## Function Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `feed_urls` | list | Required | List of RSS feed URLs to fetch |
| `requests_per_url` | int | 100 | Number of requests to make for each URL |
| `max_retries` | int | 3 | Maximum number of retry attempts for failed requests |
| `delay_between_requests` | int | 1 | Delay between consecutive requests in seconds |

## How It Works

1. The script creates an AWS API Gateway for each unique domain in your feed URLs
2. For each URL, it makes the specified number of requests using a rotating IP address
3. It parses the RSS feed content using the feedparser library
4. The script prints information about each request, including the current IP, status code, and feed entries

## IP Rotation

This script uses the `requests-ip-rotator` library to create an AWS API Gateway for each domain. The gateway automatically rotates the source IP address for each request, which helps avoid rate limiting and IP bans.

The API Gateway is set up dynamically for each domain and is automatically shut down when the script completes.

## Example Output

```
=== Starting 100 requests for: https://example.com/feed.rss ===

Request 1/100 for URL: https://example.com/feed.rss
Status: 200
Number of entries: 25
Title: First Article Title
Title: Second Article Title
...

Request 2/100 for URL: https://example.com/feed.rss
Status: 200
Number of entries: 25
...

=== Summary for https://example.com/feed.rss ===
Successful requests: 98
Failed requests: 2
==================================================
```

## AWS Costs

Please note that using AWS API Gateway may incur costs in your AWS account. The script creates and destroys gateways for each domain to minimize costs, but be aware of your AWS usage.

## Customizing Headers

You can customize the request headers in the script by modifying the `headers` dictionary:

```python
headers = {
    'User-Agent': 'Your custom user agent',
    'Accept': 'application/rss+xml',
    # Add more headers as needed
}
```

## Error Handling

The script includes robust error handling for various types of failures:
- Connection errors
- Timeout issues
- HTTP error codes
- Parsing errors

Failed requests are logged and the script attempts to retry based on the `max_retries` parameter.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.