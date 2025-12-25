"""
Test script for real WHO/FDA scrapers
Run this to verify web scraping works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.pathway_engine.real_scrapers import (
    WHOOutbreakScraper,
    FDADrugSafetyScraper,
    CDCHealthAlertScraper,
    MockSiteScraper,
    scrape_all_sources,
    format_alerts_as_text
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def test_who():
    """Test WHO outbreak news scraper"""
    print("\n" + "="*70)
    print("🌍 WHO Disease Outbreak News")
    print("="*70)
    
    scraper = WHOOutbreakScraper()
    html = scraper.fetch_content()
    
    if not html:
        print("❌ Failed to fetch WHO content")
        return False
    
    alerts = scraper.parse(html)
    print(f"✅ Found {len(alerts)} outbreak alerts\n")
    
    for i, alert in enumerate(alerts[:3], 1):  # Show first 3
        print(f"Alert {i}:")
        print(f"  Title: {alert['title']}")
        print(f"  Date: {alert['date']}")
        print(f"  URL: {alert['url']}")
        print()
    
    return True


def test_fda():
    """Test FDA drug safety scraper"""
    print("\n" + "="*70)
    print("💊 FDA Drug Safety Communications")
    print("="*70)
    
    scraper = FDADrugSafetyScraper()
    html = scraper.fetch_content()
    
    if not html:
        print("❌ Failed to fetch FDA content")
        return False
    
    alerts = scraper.parse(html)
    print(f"✅ Found {len(alerts)} safety alerts\n")
    
    for i, alert in enumerate(alerts[:3], 1):  # Show first 3
        print(f"Alert {i}:")
        print(f"  Title: {alert['title']}")
        print(f"  Date: {alert['date']}")
        print(f"  URL: {alert['url']}")
        print()
    
    return True


def test_cdc():
    """Test CDC health alerts scraper"""
    print("\n" + "="*70)
    print("🏥 CDC Health Alert Network")
    print("="*70)
    
    scraper = CDCHealthAlertScraper()
    html = scraper.fetch_content()
    
    if not html:
        print("❌ Failed to fetch CDC content")
        return False
    
    alerts = scraper.parse(html)
    print(f"✅ Found {len(alerts)} health alerts\n")
    
    for i, alert in enumerate(alerts[:3], 1):  # Show first 3
        print(f"Alert {i}:")
        print(f"  Title: {alert['title']}")
        print(f"  Date: {alert['date']}")
        print(f"  URL: {alert['url']}")
        print()
    
    return True


def test_mock():
    """Test mock site scraper"""
    print("\n" + "="*70)
    print("🎭 Mock Medical Site (Demo)")
    print("="*70)
    
    scraper = MockSiteScraper("http://localhost:5000/alerts")
    html = scraper.fetch_content()
    
    if not html:
        print("⚠️  Mock site not running (this is OK for real source testing)")
        return False
    
    alerts = scraper.parse(html)
    print(f"✅ Found {len(alerts)} mock alerts\n")
    
    for i, alert in enumerate(alerts, 1):
        print(f"Alert {i}:")
        print(f"  Title: {alert['title']}")
        print(f"  Description: {alert['description'][:100]}...")
        print()
    
    return True


def test_multi_source():
    """Test scraping all sources together"""
    print("\n" + "="*70)
    print("🌐 Multi-Source Scraping")
    print("="*70)
    
    sources = ["WHO", "FDA", "CDC"]
    print(f"Scraping: {', '.join(sources)}\n")
    
    alerts = scrape_all_sources(sources)
    print(f"✅ Total alerts from all sources: {len(alerts)}\n")
    
    # Group by source
    by_source = {}
    for alert in alerts:
        source = alert['source']
        by_source[source] = by_source.get(source, 0) + 1
    
    print("Breakdown by source:")
    for source, count in by_source.items():
        print(f"  {source}: {count} alerts")
    
    # Show formatted text (first 500 chars)
    print("\n" + "="*70)
    print("Formatted Text Output (RAG-ready)")
    print("="*70)
    text = format_alerts_as_text(alerts[:2])  # First 2 alerts
    print(text[:500] + "..." if len(text) > 500 else text)
    
    return len(alerts) > 0


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 Bio-Watcher Real Scraper Test Suite")
    print("="*70)
    print("\nTesting connection to real medical data sources...")
    print("This may take 30-60 seconds\n")
    
    results = {}
    
    # Test each source
    print("\n[1/5] Testing WHO...")
    results['WHO'] = test_who()
    
    print("\n[2/5] Testing FDA...")
    results['FDA'] = test_fda()
    
    print("\n[3/5] Testing CDC...")
    results['CDC'] = test_cdc()
    
    print("\n[4/5] Testing Mock Site...")
    results['MOCK'] = test_mock()
    
    print("\n[5/5] Testing Multi-Source...")
    results['MULTI'] = test_multi_source()
    
    # Summary
    print("\n" + "="*70)
    print("📊 Test Results Summary")
    print("="*70)
    
    for source, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{source:10s} {status}")
    
    total_pass = sum(results.values())
    total_tests = len(results)
    
    print(f"\n{total_pass}/{total_tests} tests passed")
    
    if results['WHO'] and results['FDA']:
        print("\n✅ Real data scraping is WORKING!")
        print("   You can use WHO and FDA as live sources in production")
    else:
        print("\n⚠️  Some real sources failed (this might be normal)")
        print("   Websites may be down or have changed their HTML structure")
    
    print("\n💡 To use real sources in your system:")
    print("   Update .env file:")
    print("   EXTERNAL_NEWS_SOURCES=WHO,FDA,MOCK:http://localhost:5000/alerts")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
