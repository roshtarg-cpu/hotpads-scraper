# HotPads Scraper

Extract comprehensive rental listing data from HotPads.com, the Zillow-owned rental marketplace, with ease and reliability. This powerful Apify actor is designed for real estate professionals, market researchers, property managers, and AI agents seeking accurate and up-to-date rental market intelligence.

## Features

*   **Comprehensive Data Extraction:** Scrape critical rental listing details including full **address**, **price**, number of **bedrooms** and **bathrooms**, **square footage (sqft)**, **property type**, high-resolution **images**, and detailed **descriptions**.
*   **PerimeterX Bypass (via Camoufox):** Reliably overcome advanced bot detection and anti-scraping measures like PerimeterX, ensuring consistent access to HotPads data.
*   **Residential Proxy Support:** Leverage residential proxies for enhanced anonymity and higher success rates in data extraction.
*   **`__NEXT_DATA__` Extraction:** Efficiently extract structured data directly from the page's `__NEXT_DATA__` object for speed and accuracy.
*   **AI Integration Ready:** Seamlessly integrate with **Claude**, **ChatGPT**, and other **AI agents** through the Apify platform, making it a perfect data source for large language models and intelligent applications.
*   **Scalable & Reliable:** Built on the Apify platform, ensuring high availability and robust performance for your data needs.

## Use Cases

1.  **Real Estate Market Analysis:** Gain competitive insights by tracking rental prices, property types, and availability across specific neighborhoods or cities. Identify emerging trends, evaluate market saturation, and inform investment strategies for real estate professionals.
2.  **Price Optimization for Property Managers:** Monitor competitor listings and pricing strategies in real-time. Use extracted data to optimize your own rental prices, minimize vacancies, and maximize rental income for properties under management.
3.  **Property Portfolio Research & Expansion:** Researchers and investors can analyze potential acquisition targets, identify high-growth rental areas, and assess the viability of new developments by understanding current market offerings and demand.
4.  **AI Agent & LLM Training Data:** Feed rich, structured rental listing data directly into **AI agents**, **ChatGPT**, or **Claude** for training property valuation models, developing intelligent recommendation systems, or creating advanced conversational AI applications for the rental market.

## Input

The HotPads Scraper actor requires the following input parameters:

| Parameter    | Type    | Required | Description                                                                                                                                                             |
| :----------- | :------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `city`       | `string` | Yes      | The city and state (or full address) to search for rental listings. Examples: `"New York, NY"`, `"Los Angeles, CA"`, `"Miami, FL"`.                                     |
| `maxResults` | `number` | No       | The maximum number of rental listings to retrieve. The actor will stop scraping once this limit is reached. If not specified, a reasonable default limit will be applied. |

**Example Input:**

```json
{
  "city": "Austin, TX",
  "maxResults": 100
}
```

## Output

The actor outputs a list of JSON objects, each representing a single rental listing with detailed information.

**Example JSON Output:**

```json
[
  {
    "address": "123 Main St, Austin, TX 78701",
    "price": "$2,100/mo",
    "bedrooms": "1 Bed",
    "bathrooms": "1 Bath",
    "sqft": "750 sqft",
    "propertyType": "Apartment",
    "description": "Modern 1-bedroom apartment in the heart of downtown Austin. Features stainless steel appliances, in-unit laundry, and access to a rooftop pool. Pets welcome.",
    "images": [
      "https://photos.hotpads.com/p/image1.webp",
      "https://photos.hotpads.com/p/image2.webp",
      "https://photos.hotpads.com/p/image3.webp"
    ],
    "url": "https://www.hotpads.com/austin-tx/123-main-st/pad"
  },
  {
    "address": "456 Oak Ave, Austin, TX 78704",
    "price": "$3,500/mo",
    "bedrooms": "3 Beds",
    "bathrooms": "2.5 Baths",
    "sqft": "1,800 sqft",
    "propertyType": "House",
    "description": "Charming 3-bedroom house in South Austin with a large backyard. Recently renovated kitchen and bathrooms. Close to Zilker Park and vibrant South Congress Ave.",
    "images": [
      "https://photos.hotpads.com/p/house_image1.webp",
      "https://photos.hotpads.com/p/house_image2.webp"
    ],
    "url": "https://www.hotpads.com/austin-tx/456-oak-ave/pad"
  }
]
```

## Pricing

The HotPads Scraper operates on a transparent pay-per-result model:

*   **$0.05 per run**
*   **$0.005 per listing**

This ensures you only pay for the data you successfully extract, making it a cost-effective solution for both small and large-scale data needs.

## FAQ

**Q: Can I use the data from this scraper to train my AI models or integrate with LLMs?**
A: Absolutely! The structured JSON output is perfectly suited for training machine learning models, populating knowledge bases for **AI agents**, or feeding into large language models like **ChatGPT** and **Claude** to enhance their understanding of the rental market. Apify's platform makes it easy to connect this data directly to your AI workflows.

**Q: How does this scraper handle dynamic content and anti-bot measures?**
A: The HotPads Scraper is engineered with advanced capabilities, including a robust **PerimeterX bypass via Camoufox** and the ability to extract data efficiently from the `__NEXT_DATA__` object. This ensures reliable data extraction even from sites with sophisticated anti-bot protections, providing consistent results for your market analysis or **AI agent** data needs.
