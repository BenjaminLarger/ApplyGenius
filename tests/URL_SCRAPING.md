# Using URL Scraping for Job Analysis

The CV Generator now supports job posting URL scraping. This allows you to directly provide a link to a job posting instead of copying and pasting the job description text.

## How to Use URL Scraping

1. When running the application, you will be prompted to enter a job posting URL:
   ```
   Enter the job posting URL (or press Enter to use the default job offer):
   ```

2. Enter the complete URL of the job posting (including https://):
   ```
   Enter the job posting URL: https://www.linkedin.com/jobs/view/job-title-at-company-123456789/
   ```

3. The system will use the ScrapeWebsiteTool to extract content from the URL and analyze it.

4. If URL scraping fails or the URL is not provided, the system will automatically fall back to using the default job description text from the configuration file.

## Testing URL Scraping

You can test the URL scraping functionality separately using the included test script:

```bash
python test_scrape_tool.py
```

This will prompt you to enter a URL to test, or you can press Enter to use a default test URL.

## Supported Job Posting Sites

The scraper should work with most job posting sites, including:
- LinkedIn
- Indeed
- Glassdoor
- Monster
- Company career pages

If you encounter issues with a specific site, try using a different URL or fall back to the text-based input.

## Troubleshooting

If URL scraping doesn't work as expected:
1. Make sure the URL is complete and valid
2. Check if the job posting is publicly accessible without login
3. Try using the text-based input instead by pressing Enter at the URL prompt
