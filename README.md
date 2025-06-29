# 🤖PhiNANAgent📈
Finantial agent for news summarization based on investment profile. Frist driven LLM for an agent was Phi-2 so there goes the naming. The final solution based on `Qwen/Qwen3-0.6B` with reasoning feature. It can use tools to extract info from Yahoo, read related tikers (just set name of a company) articles and summarize them.

# 🚀 Fast run of phiNANAgent
Run dockerfile:
```
docker build -t phi-agent .
```
If you want it with `jupyter notebook`:
```
docker run --gpus all -it \
  --mount type=bind,source="C:/path/to/your/local/project",target=/app \
  -p 8888:8888 \
  my-cuda-app \
  jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```
Go to `notebooks\phiNANAgent.ipynb` and `Agent` section and play!

# 📚Tools
### `get_ticker_information(ticker: str) -> str`
Returns detailed information about a given stock ticker using Yahoo Finance.
| Parameter | Type | Description |
|----------|------|-------------|
| ticker   | str  | The stock symbol (e.g., `"AAPL"` for Apple Inc.) |

Returns
- A JSON-like string containing detailed information about the stock, such as:
  - Company name
  - Market cap
  - Sector
  - Industry
  - Website
  - Price data
  - Dividends
  - Earnings
  - and more

Example
```python
get_ticker_information("AAPL")
```
### `get_stock_price(ticker: str) -> str`
Returns the current price of the stock associated with the given ticker.
| Parameter | Type | Description |
|----------|------|-------------|
| ticker   | str  | The stock symbol (e.g., `"MSFT"`) |

#### Returns:
- A string representing the current price of the stock.

##### Example:
```python
get_stock_price("TSLA")
```

### `get_financial_news_links(ticker: str, limit: int = 5) -> List[Dict[str, str]]`
Parses the RSS feed from Yahoo Finance and returns links to recent news articles related to the specified ticker.
| Parameter | Type | Description |
|----------|------|-------------|
| ticker   | str  | The stock symbol |
| limit    | int  | Maximum number of news links to return (default: 5) |

#### Returns:
- A list of dictionaries containing article metadata (currently only `'link'` field), e.g.:
```python
[
  {'link': 'https://example.com/article1'},
  {'link': 'https://example.com/article2'}
]
```

#### Example
```python
get_financial_news_links("NVDA", limit=3)
```
### `get_article_link(links: str, i: int) -> str`
Extracts a specific article link from a comma-separated string of links.
| Parameter | Type | Description |
|----------|------|-------------|
| links    | str  | Comma-separated string of article URLs |
| i        | int  | Index of the desired article link (0-based indexing) |

### Returns
- A single URL string at position `i`.

### Example
```python
links = "https://news1.com,https://news2.com"
get_article_link(links, 1)
```
### `get_article_text(url: str) -> dict or None`
Fetches and extracts the text content from a given article URL.
| Parameter | Type | Description |
|----------|------|-------------|
| url      | str  | URL of the article to scrape |

### Returns
- A dictionary containing:
  - `"title"`: Article title
  - `"text"`: Full body text of the article
- Returns `None` if an error occurs or the article text cannot be extracted.

### Notes
- Uses random User-Agent headers to avoid bot detection.
- Handles common timeouts and HTTP errors gracefully.
- Supports major finance websites like Yahoo Finance and Reuters.

#### Example
```python
get_article_text("https://finance.example.com/article-url")
```

# ✅ Calling an agent
Setup the system prompt
```
json_format = 'Action: {"name": "<instrument_name>", "arguments": {<Key>: <value>}}'

system_prompt = f'''
You are working as a finantial agent and have to use only from listed instruments:\n{tools_names}.
You have to return only in the following JSON format: {json_format}. Do not add any extra text before and after.'''
```
How to call
```
with torch.no_grad():
    print("ToolCallingAgent:", agent.run(f"{system_prompt}\n\nAnswer: What is the current news of Apple stock? Is it positive or negative?"))
```
Used `Qwen/Qwen3-0.6B` model also includes reasoning that helps with making descicions wich tool to use and what are steps

```
Output message of the LLM:
<think>
Okay, the user is asking for the current news of Apple stock and whether it's positive or negative. Let me check the available tools. The tools provided are get_ticker_information, get_stock_price get_financial_news_links, get_article_link, and get_article_text.

The user wants to know the news about Apple's stock. The financial_news_links tool can parse news from Yahoo Finance. So I should use that. The arguments needed are the ticker for Apple. The ticker is AAPL ... So the steps are:         
                                                                                                                   
1. Call get_financial_news_links with ticker AAPL to get the news links.
2. Then call get_article_text on those links to get the article text.
3. Then use the article text to determine the sentiment.

But since the ... So the answer would be:
                         
Action:
{                                                                                                                  
  "name": "get_financial_news_links",                                                                              
  "arguments": {"ticker": "AAPL"}                                                                                  
}
```