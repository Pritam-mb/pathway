"""
Real WHO/FDA website scrapers with HTML parsing
Supports multiple medical data sources for production use
"""
from typing import Dict, List, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class MedicalSiteScraper:
    """Base class for medical website scrapers"""
    
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Bio-Watcher Clinical Intelligence System/1.0'
        })
    
    def fetch_content(self) -> Optional[str]:
        """Fetch raw HTML content"""
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {self.name}: {e}")
            return None
    
    def parse(self, html: str) -> List[Dict]:
        """Parse HTML into structured data - override in subclass"""
        raise NotImplementedError


class WHOOutbreakScraper(MedicalSiteScraper):
    """WHO Disease Outbreak News scraper"""
    
    def __init__(self):
        super().__init__(
            url="https://www.who.int/emergencies/disease-outbreak-news",
            name="WHO Outbreak News"
        )
    
    def parse(self, html: str) -> List[Dict]:
        """Parse WHO outbreak news page"""
        soup = BeautifulSoup(html, 'html.parser')
        alerts = []
        
        # WHO uses article cards for outbreak news
        articles = soup.find_all('div', class_=['list-view--item', 'sf-list-item'])
        
        for article in articles[:5]:  # Get latest 5
            try:
                # Extract title
                title_elem = article.find(['h2', 'h3', 'a'])
                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                
                # Extract date
                date_elem = article.find('time') or article.find('span', class_='date')
                date = date_elem.get_text(strip=True) if date_elem else ""
                
                # Extract summary/description
                desc_elem = article.find(['p', 'div'], class_=['description', 'summary'])
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract link
                link_elem = article.find('a', href=True)
                link = link_elem['href'] if link_elem else ""
                if link and not link.startswith('http'):
                    link = f"https://www.who.int{link}"
                
                alerts.append({
                    'source': 'WHO',
                    'title': title,
                    'date': date,
                    'description': description,
                    'url': link,
                    'type': 'outbreak'
                })
            except Exception as e:
                logger.warning(f"Failed to parse WHO article: {e}")
                continue
        
        return alerts


class FDADrugSafetyScraper(MedicalSiteScraper):
    """FDA Drug Safety Communications scraper"""
    
    def __init__(self):
        super().__init__(
            url="https://www.fda.gov/drugs/drug-safety-and-availability/drug-recalls",
            name="FDA Drug Safety"
        )
    
    def parse(self, html: str) -> List[Dict]:
        """Parse FDA drug safety communications"""
        soup = BeautifulSoup(html, 'html.parser')
        alerts = []
        
        # FDA uses list items for safety communications
        items = soup.find_all(['li', 'div'], class_=['featured-content', 'article', 'item'])
        
        for item in items[:5]:  # Get latest 5
            try:
                # Extract title
                title_elem = item.find(['a', 'h2', 'h3'])
                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                
                # Extract date
                date_elem = item.find(['time', 'span'], class_=['date', 'time'])
                date = date_elem.get_text(strip=True) if date_elem else ""
                
                # Extract description
                desc_elem = item.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract link
                link_elem = item.find('a', href=True)
                link = link_elem['href'] if link_elem else ""
                if link and not link.startswith('http'):
                    link = f"https://www.fda.gov{link}"
                
                alerts.append({
                    'source': 'FDA',
                    'title': title,
                    'date': date,
                    'description': description,
                    'url': link,
                    'type': 'drug_safety'
                })
            except Exception as e:
                logger.warning(f"Failed to parse FDA item: {e}")
                continue
        
        return alerts


class CDCHealthAlertScraper(MedicalSiteScraper):
    """CDC Health Alert Network scraper"""
    
    def __init__(self):
        super().__init__(
            url="https://emergency.cdc.gov/han/index.asp",
            name="CDC Health Alerts"
        )
    
    def parse(self, html: str) -> List[Dict]:
        """Parse CDC health alerts"""
        soup = BeautifulSoup(html, 'html.parser')
        alerts = []
        
        # CDC uses table rows for alerts
        rows = soup.find_all('tr')
        
        for row in rows[:5]:  # Get latest 5
            try:
                cells = row.find_all('td')
                if len(cells) < 2:
                    continue
                
                # Extract date from first cell
                date = cells[0].get_text(strip=True)
                
                # Extract title and link from second cell
                link_elem = cells[1].find('a', href=True)
                if link_elem:
                    title = link_elem.get_text(strip=True)
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = f"https://emergency.cdc.gov/han/{link}"
                else:
                    title = cells[1].get_text(strip=True)
                    link = ""
                
                alerts.append({
                    'source': 'CDC',
                    'title': title,
                    'date': date,
                    'description': '',
                    'url': link,
                    'type': 'health_alert'
                })
            except Exception as e:
                logger.warning(f"Failed to parse CDC row: {e}")
                continue
        
        return alerts


class MockSiteScraper(MedicalSiteScraper):
    """Local mock site scraper for demo"""
    
    def __init__(self, url: str = "http://localhost:5000/alerts"):
        super().__init__(url=url, name="Mock Medical Site")
    
    def parse(self, html: str) -> List[Dict]:
        """Parse mock site HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        alerts = []
        
        # Mock site uses div.alert for each alert
        alert_divs = soup.find_all('div', class_='alert')
        
        for alert_div in alert_divs:
            try:
                # Extract severity
                severity_elem = alert_div.find('strong')
                severity = severity_elem.get_text(strip=True) if severity_elem else ""
                
                # Extract full text
                text = alert_div.get_text(strip=True)
                
                # Extract drug name if mentioned
                drug = ""
                if "Drug-X" in text:
                    drug = "Drug-X"
                
                alerts.append({
                    'source': 'MOCK',
                    'title': f"{severity} Alert",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'description': text,
                    'url': self.url,
                    'type': 'mock_alert',
                    'drug': drug,
                    'severity': severity
                })
            except Exception as e:
                logger.warning(f"Failed to parse mock alert: {e}")
                continue
        
        return alerts


def scrape_all_sources(sources: List[str]) -> List[Dict]:
    """
    Scrape multiple medical data sources
    
    Args:
        sources: List of source names ['WHO', 'FDA', 'CDC', 'MOCK:url']
    
    Returns:
        Combined list of alerts from all sources
    """
    all_alerts = []
    scrapers = []
    
    # Initialize scrapers based on source list
    for source in sources:
        if source == 'WHO':
            scrapers.append(WHOOutbreakScraper())
        elif source == 'FDA':
            scrapers.append(FDADrugSafetyScraper())
        elif source == 'CDC':
            scrapers.append(CDCHealthAlertScraper())
        elif source.startswith('MOCK:'):
            url = source.split(':', 1)[1]
            scrapers.append(MockSiteScraper(url))
        elif source.startswith('http'):
            # Generic URL - treat as mock site
            scrapers.append(MockSiteScraper(source))
    
    # Scrape each source
    for scraper in scrapers:
        try:
            logger.info(f"Scraping {scraper.name}...")
            html = scraper.fetch_content()
            if html:
                alerts = scraper.parse(html)
                all_alerts.extend(alerts)
                logger.info(f"Found {len(alerts)} alerts from {scraper.name}")
        except Exception as e:
            logger.error(f"Failed to scrape {scraper.name}: {e}")
    
    return all_alerts


def format_alerts_as_text(alerts: List[Dict]) -> str:
    """Format scraped alerts as readable text for RAG ingestion"""
    if not alerts:
        return "No alerts found"
    
    text_parts = ["=== MEDICAL ALERTS ===\n"]
    
    for i, alert in enumerate(alerts, 1):
        text_parts.append(f"\n--- Alert {i} ---")
        text_parts.append(f"Source: {alert.get('source', 'Unknown')}")
        text_parts.append(f"Type: {alert.get('type', 'Unknown')}")
        text_parts.append(f"Date: {alert.get('date', 'Unknown')}")
        text_parts.append(f"Title: {alert.get('title', 'No title')}")
        
        if alert.get('description'):
            text_parts.append(f"Description: {alert['description']}")
        
        if alert.get('url'):
            text_parts.append(f"URL: {alert['url']}")
        
        # Add any extra fields
        for key, value in alert.items():
            if key not in ['source', 'type', 'date', 'title', 'description', 'url']:
                text_parts.append(f"{key.title()}: {value}")
    
    return "\n".join(text_parts)


if __name__ == "__main__":
    # Test scrapers
    logging.basicConfig(level=logging.INFO)
    
    print("Testing WHO scraper...")
    who = WHOOutbreakScraper()
    html = who.fetch_content()
    if html:
        alerts = who.parse(html)
        print(f"Found {len(alerts)} WHO alerts")
        if alerts:
            print(f"Latest: {alerts[0]['title']}")
    
    print("\nTesting FDA scraper...")
    fda = FDADrugSafetyScraper()
    html = fda.fetch_content()
    if html:
        alerts = fda.parse(html)
        print(f"Found {len(alerts)} FDA alerts")
        if alerts:
            print(f"Latest: {alerts[0]['title']}")
    
    print("\nTesting mock site...")
    mock = MockSiteScraper("http://localhost:5000/alerts")
    html = mock.fetch_content()
    if html:
        alerts = mock.parse(html)
        print(f"Found {len(alerts)} mock alerts")
        if alerts:
            print(f"Latest: {alerts[0]}")
