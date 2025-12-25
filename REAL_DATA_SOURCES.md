# 🌐 Real Medical Data Sources

Your Bio-Watcher system now supports **real-time scraping** from actual WHO/FDA/CDC websites!

## 🎯 What's New

You can now monitor:
- ✅ **WHO Disease Outbreak News** - Live global health threats
- ✅ **FDA Drug Safety Communications** - Real drug warnings
- ✅ **CDC Health Alert Network** - US health alerts
- ✅ **Mock Site** - Controllable demo source

## 🚀 Quick Start

### Test Real Scrapers
```powershell
python scripts/test_real_scrapers.py
```

This will:
1. Connect to WHO, FDA, CDC websites
2. Parse latest alerts from each
3. Show you what data is available
4. Verify scrapers are working

### Enable Real Sources

**Option 1: Add to Mock (Recommended for Demo)**
```bash
# .env file
EXTERNAL_NEWS_SOURCES=WHO,FDA,MOCK:http://localhost:5000/alerts
```

**Option 2: Real Sources Only (Production)**
```bash
# .env file
EXTERNAL_NEWS_SOURCES=WHO,FDA,CDC
```

**Option 3: Mock Only (Safe Demo)**
```bash
# .env file
EXTERNAL_NEWS_SOURCES=MOCK:http://localhost:5000/alerts
```

## 📊 Available Sources

### 🌍 WHO - Disease Outbreak News
- **URL**: https://www.who.int/emergencies/disease-outbreak-news
- **Updates**: Daily (when outbreaks occur)
- **Data**: Ebola, cholera, novel viruses, disease clusters
- **Format**: HTML article list
- **Reliability**: ⭐⭐⭐⭐⭐

### 💊 FDA - Drug Safety Communications
- **URL**: https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications
- **Updates**: Weekly/as-needed
- **Data**: Drug recalls, safety warnings, adverse events
- **Format**: HTML list
- **Reliability**: ⭐⭐⭐⭐⭐

### 🏥 CDC - Health Alert Network
- **URL**: https://emergency.cdc.gov/han/index.asp
- **Updates**: Real-time during emergencies
- **Data**: Public health alerts, investigation notices
- **Format**: HTML table
- **Reliability**: ⭐⭐⭐⭐

### 🎭 Mock Site (Your Demo Server)
- **URL**: http://localhost:5000/alerts
- **Updates**: On-demand via API
- **Data**: Controlled test scenarios
- **Format**: Custom HTML
- **Reliability**: ⭐⭐⭐⭐⭐ (you control it!)

## 🛠️ How It Works

### Scraper Architecture
```python
# Each source has a specialized scraper
WHOOutbreakScraper → Parses WHO HTML → Extracts alerts
FDADrugSafetyScraper → Parses FDA HTML → Extracts warnings
CDCHealthAlertScraper → Parses CDC HTML → Extracts notices
MockSiteScraper → Parses your site → Extracts test data
```

### Data Flow
```
WHO/FDA/CDC Website
     ↓ (HTTP request every 10s)
HTML Parser (BeautifulSoup)
     ↓ (extract structured data)
Alert Objects (title, date, description, URL)
     ↓ (format as text)
RAG System (Pathway indexes)
     ↓ (semantic search)
Agent (analyzes + generates alerts)
```

## 🎪 Demo Strategies

### Strategy 1: Controlled Demo (Recommended)
**Use**: Mock site for primary demo
**Add**: WHO/FDA as bonus feature
**Advantage**: Reliable, repeatable, impressive

```bash
EXTERNAL_NEWS_SOURCES=MOCK:http://localhost:5000/alerts,WHO
```

**Script**:
1. Show mock alert triggering (controllable)
2. Show WHO feed in background (real data!)
3. Explain: "In production, this runs 24/7 on real WHO/FDA"

### Strategy 2: Pure Real Data
**Use**: Only WHO/FDA/CDC
**Advantage**: Most impressive (actual live data)
**Risk**: Sites might not update during your demo

```bash
EXTERNAL_NEWS_SOURCES=WHO,FDA,CDC
```

**Script**:
1. Show live WHO alerts being indexed
2. Query system: "What are current WHO outbreaks?"
3. System retrieves real WHO data
4. Explain: "This is live - refreshing every 10 seconds"

### Strategy 3: Hybrid Approach
**Use**: Both mock and real
**Advantage**: Best of both worlds

```bash
EXTERNAL_NEWS_SOURCES=WHO,FDA,MOCK:http://localhost:5000/alerts
```

**Script**:
1. Show system monitoring WHO + FDA in background
2. Trigger mock alert to demonstrate instant response
3. Query real WHO data to show multi-source capability

## 🧪 Testing Real Sources

### Test Individual Scrapers
```python
from backend.pathway_engine.real_scrapers import WHOOutbreakScraper

scraper = WHOOutbreakScraper()
html = scraper.fetch_content()
alerts = scraper.parse(html)

print(f"Found {len(alerts)} WHO alerts")
for alert in alerts[:3]:
    print(f"- {alert['title']}")
```

### Test Multi-Source
```python
from backend.pathway_engine.real_scrapers import scrape_all_sources

sources = ["WHO", "FDA", "CDC"]
alerts = scrape_all_sources(sources)

print(f"Total: {len(alerts)} alerts from all sources")
```

### Run Full Test Suite
```powershell
python scripts/test_real_scrapers.py
```

Expected output:
```
🌍 WHO: ✅ Found 5 outbreak alerts
💊 FDA: ✅ Found 5 safety alerts
🏥 CDC: ✅ Found 5 health alerts
🎭 MOCK: ✅ Found 2 mock alerts

📊 Total: 17 alerts from all sources
```

## ⚠️ Important Notes

### Rate Limiting
- WHO/FDA/CDC are public sites - no API keys needed
- Be respectful: default 10-second refresh is reasonable
- Don't decrease below 5 seconds

### Reliability
- **WHO/FDA/CDC**: Pages may change format (scrapers might break)
- **Mock Site**: 100% reliable (you control it)
- **For Hackathon**: Use mock as primary, real as bonus

### Legal/Ethical
- ✅ All sites are public, no authentication required
- ✅ Medical data is public health information
- ✅ Scraping for non-commercial research is generally OK
- ⚠️ For production: Consider official APIs (WHO has one)

### HTML Parsing
The scrapers use **BeautifulSoup** with fallback patterns:
- If WHO changes their HTML class names, scraper still tries generic tags
- Parsers are defensive (won't crash if structure changes)
- Worst case: Returns empty list (doesn't break system)

## 🎯 Configuration Examples

### For Your Hackathon Demo
```bash
# .env
EXTERNAL_NEWS_SOURCES=MOCK:http://localhost:5000/alerts,WHO

# Why:
# - Mock gives you control for demo triggers
# - WHO adds credibility with real data
# - FDA/CDC optional (more is not always better for demo)
```

### For Production Deployment
```bash
# .env
EXTERNAL_NEWS_SOURCES=WHO,FDA,CDC

# Why:
# - All major sources covered
# - No mock site in production
# - Real data 24/7
```

### For Development/Testing
```bash
# .env
EXTERNAL_NEWS_SOURCES=MOCK:http://localhost:5000/alerts

# Why:
# - Fast, reliable, controllable
# - No internet dependency
# - Repeatable tests
```

## 🔍 Troubleshooting

### "Failed to fetch WHO content"
- Check internet connection
- WHO site might be down (rare)
- Try: `curl https://www.who.int/emergencies/disease-outbreak-news`

### "Found 0 WHO alerts"
- HTML structure may have changed
- Scraper needs updating
- Use mock site as fallback

### Slow Performance
- Real scrapers add 1-2 seconds per source
- Solution: Use fewer sources or increase poll interval
- Mock site is instant

## 📈 Next Steps

1. **Test scrapers**: Run `python scripts/test_real_scrapers.py`
2. **Choose strategy**: Pick demo approach (mock only, hybrid, or all real)
3. **Update .env**: Configure `EXTERNAL_NEWS_SOURCES`
4. **Practice demo**: Trigger events, query live data, show reasoning
5. **Prepare backup**: If WHO fails during demo, fall back to mock

## 💡 Pro Tips

### For Impressive Demo
1. Open WHO website in browser tab
2. Show your system dashboard
3. Point to alert on WHO page
4. Query your system: "What WHO outbreaks are active?"
5. System returns the SAME data
6. Explain: "This was ingested automatically 10 seconds ago"

### For Technical Depth
1. Show the scraper code: [real_scrapers.py](backend/pathway_engine/real_scrapers.py)
2. Explain BeautifulSoup HTML parsing
3. Show alert formatting: `format_alerts_as_text()`
4. Demonstrate multi-source: WHO + FDA + Mock simultaneously

### For Q&A
**Q**: "What if WHO changes their HTML?"
**A**: "We have defensive parsing with fallbacks, plus mock site ensures system keeps working. In production, we'd add monitoring and auto-alerts if scrapers break."

**Q**: "Is this legal?"
**A**: "Yes - all public health data, publicly accessible, non-commercial use. WHO even encourages sharing outbreak information for public safety."

**Q**: "How real-time is this?"
**A**: "10-second polling. Could use webhooks or RSS feeds for true push notifications in production."

---

**You now have a system that works with REAL medical data!** 🎉

Choose your demo strategy, test the scrapers, and you're ready to show a working real-time clinical intelligence system.
