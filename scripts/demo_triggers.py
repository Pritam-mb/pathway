"""
Demo Trigger Scripts - Simulate real-time events
"""
import requests
import time
from pathlib import Path
import shutil


def trigger_external_alert():
    """
    Trigger a critical alert on the mock WHO site.
    Simulates an external data change that Pathway will detect.
    """
    print("\n" + "="*60)
    print("🌐 TRIGGERING EXTERNAL ALERT")
    print("="*60)
    
    try:
        response = requests.post("http://localhost:5000/api/trigger_warning")
        
        if response.status_code == 200:
            print("✅ External alert triggered successfully!")
            print("\n📋 Alert Content:")
            alert = response.json().get('alert', {})
            print(f"   Title: {alert.get('title')}")
            print(f"   Source: {alert.get('source')}")
            print(f"   Date: {alert.get('date')}")
            print(f"\n   {alert.get('content')}")
            
            print("\n⚡ Pathway engine should detect this change within 10-30 seconds...")
            return True
        else:
            print(f"❌ Failed to trigger alert: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the mock site is running: python backend/mock_site/app.py")
        return False


def add_new_patient_document():
    """
    Drop a new patient lab results document into the watched folder.
    Simulates internal document update that Pathway will detect.
    """
    print("\n" + "="*60)
    print("📄 ADDING NEW PATIENT DOCUMENT")
    print("="*60)
    
    from config.settings import settings
    
    # Create a new lab results document
    content = f"""URGENT LAB RESULTS
{'='*60}

Patient ID: Patient_402
Test Date: 2025-12-25
Report Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

CARDIAC ENZYME PANEL:
  • Troponin I: 0.08 ng/mL (ELEVATED - Normal <0.04)
  • CK-MB: 28 U/L (ELEVATED - Normal <25)
  • BNP: 450 pg/mL (ELEVATED - Normal <100)

ECG FINDINGS:
  • Irregular rhythm noted
  • Possible atrial fibrillation
  • QT interval: 485ms (PROLONGED)

CLINICAL SIGNIFICANCE:
⚠️ URGENT: These findings suggest cardiac stress and possible 
medication-related QT prolongation. Immediate physician review required.

Current medications include Drug-X (Cardioxin), which is known to 
affect cardiac conduction. Consider medication review in light of 
these abnormal findings.

RECOMMENDATIONS:
1. Immediate cardiology consultation
2. Review all cardiac medications
3. Consider Drug-X discontinuation or dose adjustment
4. Repeat ECG in 24 hours

Reported by: Clinical Laboratory
Contact: Lab Extension 4567
"""
    
    # Save to watched directory
    filename = f"Patient_402_URGENT_LabResults_{int(time.time())}.txt"
    filepath = settings.pathway_data_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ New document added: {filename}")
    print(f"📁 Location: {filepath}")
    print("\n⚡ Pathway engine should detect this file immediately...")
    
    return filepath


def reset_demo():
    """Reset the demo to initial state"""
    print("\n" + "="*60)
    print("🔄 RESETTING DEMO TO BASELINE")
    print("="*60)
    
    # Reset mock site alerts
    try:
        response = requests.post("http://localhost:5000/api/reset")
        if response.status_code == 200:
            print("✅ Mock site reset to baseline")
        else:
            print("⚠️ Could not reset mock site")
    except:
        print("⚠️ Mock site not running")
    
    # Clean up urgent lab files
    from config.settings import settings
    
    urgent_files = list(settings.pathway_data_dir.glob("*URGENT*.txt"))
    for file in urgent_files:
        file.unlink()
        print(f"✅ Removed: {file.name}")
    
    print("\n✨ Demo reset complete!")


def run_full_demo():
    """
    Run the complete demo sequence with timing.
    """
    print("\n" + "="*70)
    print("🎬 STARTING BIO-WATCHER LIVE DEMO SEQUENCE")
    print("="*70)
    
    print("\n📊 Initial State: System monitoring...")
    print("   Safety Score: ✅ 95/100 (Green)")
    print("   Active Alerts: None")
    
    input("\nPress ENTER to trigger external alert...")
    
    # Step 1: External alert
    trigger_external_alert()
    print("\n⏳ Waiting 15 seconds for agent to process...")
    time.sleep(15)
    
    input("\nPress ENTER to add new patient document...")
    
    # Step 2: Internal document
    add_new_patient_document()
    print("\n⏳ Waiting 10 seconds for agent to process...")
    time.sleep(10)
    
    print("\n" + "="*70)
    print("✨ DEMO COMPLETE!")
    print("="*70)
    print("\nExpected Results:")
    print("  1. Agent detected external WHO alert about Drug-X")
    print("  2. Agent cross-referenced with patient records")
    print("  3. Agent found Patient_402 prescribed Drug-X")
    print("  4. Agent detected urgent lab results showing cardiac issues")
    print("  5. Safety score dropped to CRITICAL")
    print("  6. Alert generated for immediate physician review")
    print("\n🎯 This demonstrates real-time agentic reasoning with live data!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/demo_triggers.py alert    - Trigger external alert")
        print("  python scripts/demo_triggers.py doc      - Add patient document")
        print("  python scripts/demo_triggers.py reset    - Reset to baseline")
        print("  python scripts/demo_triggers.py full     - Run full demo sequence")
    else:
        command = sys.argv[1]
        
        if command == "alert":
            trigger_external_alert()
        elif command == "doc":
            add_new_patient_document()
        elif command == "reset":
            reset_demo()
        elif command == "full":
            run_full_demo()
        else:
            print(f"Unknown command: {command}")
