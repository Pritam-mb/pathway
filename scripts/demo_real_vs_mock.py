"""
Quick demo: Shows real WHO/FDA data alongside mock alerts
Perfect for hackathon presentation
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.pathway_engine.real_scrapers import (
    WHOOutbreakScraper,
    FDADrugSafetyScraper,
    MockSiteScraper
)
import time


def show_real_data_demo():
    """Quick demo showing real vs mock data"""
    
    print("\n" + "="*70)
    print("🏥 BIO-WATCHER: Real vs Mock Data Demo")
    print("="*70)
    
    # 1. Show Mock Site (Your controllable demo)
    print("\n[1/3] 🎭 YOUR MOCK SITE (Controllable)")
    print("-" * 70)
    mock = MockSiteScraper("http://localhost:5000/alerts")
    html = mock.fetch_content()
    if html:
        alerts = mock.parse(html)
        if alerts:
            print(f"✅ Found {len(alerts)} alerts (YOU control these!)")
            for alert in alerts:
                print(f"   • {alert['title']}: {alert['description'][:60]}...")
        else:
            print("   No alerts (baseline state - you can trigger them!)")
    else:
        print("   ⚠️  Mock site not running on port 5000")
        print("   Run: python backend/mock_site/app.py")
    
    time.sleep(1)
    
    # 2. Show WHO (Real live data)
    print("\n[2/3] 🌍 WHO DISEASE OUTBREAKS (Real Live Data)")
    print("-" * 70)
    print("Fetching from https://www.who.int/emergencies/disease-outbreak-news ...")
    who = WHOOutbreakScraper()
    html = who.fetch_content()
    if html:
        alerts = who.parse(html)
        if alerts:
            print(f"✅ Found {len(alerts)} REAL outbreak alerts")
            print("\nLatest WHO alerts:")
            for i, alert in enumerate(alerts[:3], 1):
                print(f"\n   {i}. {alert['title']}")
                print(f"      Date: {alert['date']}")
                print(f"      URL: {alert['url']}")
        else:
            print("   No alerts parsed (WHO may have changed their HTML)")
    else:
        print("   ❌ Could not fetch WHO (check internet)")
    
    time.sleep(1)
    
    # 3. Show FDA (Real live data)
    print("\n[3/3] 💊 FDA DRUG SAFETY (Real Live Data)")
    print("-" * 70)
    print("Fetching from https://www.fda.gov/drugs/drug-safety-and-availability ...")
    fda = FDADrugSafetyScraper()
    html = fda.fetch_content()
    if html:
        alerts = fda.parse(html)
        if alerts:
            print(f"✅ Found {len(alerts)} REAL drug safety alerts")
            print("\nLatest FDA alerts:")
            for i, alert in enumerate(alerts[:3], 1):
                print(f"\n   {i}. {alert['title']}")
                print(f"      Date: {alert['date']}")
                print(f"      URL: {alert['url']}")
        else:
            print("   No alerts parsed (FDA may have changed their HTML)")
    else:
        print("   ❌ Could not fetch FDA (check internet)")
    
    # Summary
    print("\n" + "="*70)
    print("📊 DEMO SUMMARY")
    print("="*70)
    print("\n✅ You now have:")
    print("   1. Mock site - Controllable for reliable demos")
    print("   2. WHO scraper - Real outbreak data")
    print("   3. FDA scraper - Real drug safety warnings")
    print("\n💡 For your hackathon:")
    print("   • Use MOCK for primary demo (you control it)")
    print("   • Show WHO/FDA as bonus (proves it works with real data)")
    print("   • Explain: 'In production, this runs 24/7 on real sources'")
    print("\n🚀 To enable in your system:")
    print("   Edit .env file:")
    print("   EXTERNAL_NEWS_SOURCES=WHO,FDA,MOCK:http://localhost:5000/alerts")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        show_real_data_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted\n")
