"""HotPads rental listings scraper with Camoufox for PerimeterX bypass."""
import asyncio
import json
import re
from datetime import datetime
from apify import Actor
from camoufox.async_api import AsyncCamoufox

async def _parse_proxy(proxy_url):
    """Parse proxy configuration from Apify proxy URL."""
    if not proxy_url:
        return None
    match = re.match(r'http://([^:]+):([^@]+)@([^:]+):(\d+)', proxy_url)
    if match:
        return {
            'server': f'http://{match.group(3)}:{match.group(4)}',
            'username': match.group(1),
            'password': match.group(2)
        }
    return None

async def _fetch(url, proxy_url=None):
    """Fetch page content using Camoufox with anti-detection."""
    async with AsyncCamoufox(
        headless=True,
        geoip=True,
        proxy=await _parse_proxy(proxy_url) if proxy_url else None
    ) as browser:
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='networkidle', timeout=90000)
            await page.wait_for_timeout(3000)
            
            html = await page.content()
            
            if len(html) < 500:
                Actor.log.warning(f'Low content size: {len(html)} bytes')
                return None
                
            return html
        except Exception as e:
            Actor.log.error(f'Fetch error for {url}: {e}')
            return None
        finally:
            await page.close()

def _extract_next_data(html):
    """Extract __NEXT_DATA__ JSON from HTML."""
    if not html:
        return None
    
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            Actor.log.warning(f'Failed to parse __NEXT_DATA__: {e}')
    return None

async def main():
    """Main scraper logic."""
    async with Actor:
        actor_input = await Actor.get_input() or {}
        
        # Get inputs
        city = actor_input.get('city', 'new-york-ny')
        max_results = actor_input.get('maxResults', 50)
        proxy_config = actor_input.get('proxyConfiguration', {})
        
        # Create proxy URL
        proxy_url = None
        if proxy_config.get('useApifyProxy'):
            groups = proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
            proxy_conf = await Actor.create_proxy_configuration()
            if proxy_conf:
                session_id = f"hotpads_{city}".replace('-', '_')
                proxy_url = await proxy_conf.new_url(session_id=session_id)
        
        Actor.log.info(f'Starting HotPads scraper: city={city}, max_results={max_results}')
        
        item_count = 0
        request_count = 0
        error_count = 0
        
        try:
            # Build search URL
            url = f'https://www.hotpads.com/search/{city}/rentals'
            Actor.log.info(f'Fetching: {url}')
            
            request_count += 1
            html = await _fetch(url, proxy_url)
            
            if not html:
                raise Exception('Failed to fetch page content')
            
            # Extract data from __NEXT_DATA__
            next_data = _extract_next_data(html)
            
            if not next_data:
                Actor.log.warning('No __NEXT_DATA__ found, trying HTML parsing')
                error_count += 1
            else:
                # Extract listings from JSON structure
                page_props = next_data.get('props', {}).get('pageProps', {})
                listings = page_props.get('listings', []) or page_props.get('results', []) or []
                
                Actor.log.info(f'Found {len(listings)} listings')
                
                for idx, listing in enumerate(listings[:max_results]):
                    try:
                        # Extract fields with null for missing data
                        result = {
                            'url': f"https://www.hotpads.com{listing.get('url', '')}" if listing.get('url') else None,
                            'address': listing.get('address', {}).get('full') if isinstance(listing.get('address'), dict) else listing.get('address'),
                            'price': listing.get('price', {}).get('value') if isinstance(listing.get('price'), dict) else listing.get('price'),
                            'bedrooms': listing.get('beds'),
                            'bathrooms': listing.get('baths'),
                            'sqft': listing.get('sqft'),
                            'propertyType': listing.get('propertyType'),
                            'imageUrl': listing.get('photo', {}).get('url') if isinstance(listing.get('photo'), dict) else listing.get('photo'),
                            'propertyDescription': listing.get('description'),
                            'scrapedAt': datetime.utcnow().isoformat() + 'Z'
                        }
                        
                        await Actor.push_data(result)
                        item_count += 1
                        
                        if item_count % 10 == 0:
                            Actor.log.info(f'Scraped {item_count} listings...')
                            
                    except Exception as e:
                        Actor.log.error(f'Error processing listing {idx}: {e}')
                        error_count += 1
                        continue
            
            Actor.log.info(f'Completed: {item_count} items scraped')
            
        except Exception as e:
            Actor.log.error(f'Fatal error: {e}')
            error_count += 1
        
        # Save task context (MANDATORY)
        await Actor.set_value('SAVED-TASK', {
            'actorId': Actor.get_env().get('actor_id'),
            'actorRunId': Actor.get_env().get('actor_run_id'),
            'defaultDatasetId': Actor.get_env().get('default_dataset_id'),
            'startedAt': Actor.get_env().get('started_at'),
            'input': actor_input,
            'stats': {
                'itemsScraped': item_count,
                'requestsMade': request_count,
                'errors': error_count
            }
        })

if __name__ == '__main__':
    asyncio.run(main())
