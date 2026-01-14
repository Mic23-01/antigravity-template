#!/usr/bin/env python3
"""
Deep Search Aggregator for Antigravity Agents.
Fetch multiple URLs in parallel, convert to Markdown, and bundle into a single research file.

Usage:
  uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE.md
"""

import sys
import argparse
import asyncio
import aiohttp
import html2text
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import random

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_url(session, url, semaphore, timeout=15, retries=3):
    """Fetch a single URL with semantic concurrency limit and retry logic."""
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 429:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Rate limited (429) at {url}. Retrying in {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                        
                    response.raise_for_status()
                    text = await response.text()
                    return url, text, None
            except Exception as e:
                # Only retry on connection errors or specific issues, otherwise fail fast
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {url} after {retries} attempts: {e}")
                    return url, None, str(e)
                await asyncio.sleep(1)
        return url, None, "Max retries exceeded"

def convert_to_markdown(html_content, url):
    """Convert HTML content to readable Markdown."""
    if not html_content:
        return ""
    
    try:
        # 1. Clean with BS4 first (remove scripts, styles)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove noise
        for script in soup(["script", "style", "nav", "footer", "iframe", "svg"]):
            script.decompose()
            
        # 2. Convert with html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0 # No wrapping
        
        markdown = h.handle(str(soup))
        return markdown
    except Exception as e:
        logger.error(f"Failed to convert {url} to markdown: {e}")
        return f"Error converting content: {e}"

async def main():
    parser = argparse.ArgumentParser(description="Deep Search Aggregator")
    parser.add_argument('--urls', nargs='+', required=True, help="List of URLs to fetch")
    parser.add_argument('--output', default="RESEARCH_BUNDLE.md", help="Output file path")
    
    args = parser.parse_args()
    
    logger.info(f"Starting Deep Search for {len(args.urls)} URLs...")
    
    # Brave API / General Web Ethics: 1 concurrent request per domain is polite, 
    # but for different domains we can go higher. conservatively set to 3.
    sem = asyncio.Semaphore(3)
    
    async with aiohttp.ClientSession(headers={'User-Agent': 'Antigravity-Research-Bot/1.0'}) as session:
        tasks = [fetch_url(session, url, sem) for url in args.urls]
        results = await asyncio.gather(*tasks)
        
    # Process results
    final_output = []
    final_output.append(f"# Deep Search Bundle\n")
    final_output.append(f"**Date**: {sys.argv[0]}\n")
    final_output.append(f"**Sources**: {len(args.urls)}\n\n")
    
    success_count = 0
    
    for url, html, error in results:
        final_output.append(f"---\n")
        final_output.append(f"## Source: [{url}]({url})\n\n")
        
        if error:
            final_output.append(f"> [!WARNING]\n> Failed to fetch: {error}\n\n")
        else:
            markdown = convert_to_markdown(html, url)
            final_output.append(markdown)
            final_output.append(f"\n\n")
            success_count += 1
            
    # Write to file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("".join(final_output))
        logger.info(f"Successfully bundled {success_count}/{len(args.urls)} pages into {args.output}")
    except Exception as e:
        logger.error(f"Failed to write output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
