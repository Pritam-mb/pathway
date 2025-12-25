"""
Generate synthetic medical documents for demo purposes
"""
from pathlib import Path
from datetime import datetime, timedelta
import random


class SyntheticDocGenerator:
    """Generate realistic medical documents for testing"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_patient_file(self, patient_id: int, has_drugx: bool = False):
        """Generate a patient record"""
        
        age = random.randint(45, 85)
        conditions = random.sample([
            "Hypertension",
            "Type 2 Diabetes",
            "Coronary Artery Disease",
            "Atrial Fibrillation",
            "Chronic Kidney Disease"
        ], k=random.randint(1, 3))
        
        medications = [
            "Lisinopril 10mg daily",
            "Metformin 500mg twice daily",
            "Aspirin 81mg daily"
        ]
        
        if has_drugx:
            medications.insert(0, "Drug-X (Cardioxin) 50mg daily - prescribed for cardiac arrhythmia")
        
        content = f"""CONFIDENTIAL MEDICAL RECORD
{'='*60}

Patient ID: Patient_{patient_id:03d}
Date of Birth: {(datetime.now() - timedelta(days=age*365)).strftime('%Y-%m-%d')}
Age: {age} years
Gender: {'Male' if random.random() > 0.5 else 'Female'}

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ACTIVE DIAGNOSES:
{chr(10).join(f"  • {cond}" for cond in conditions)}

CURRENT MEDICATIONS:
{chr(10).join(f"  • {med}" for med in medications)}

VITAL SIGNS (Last Visit):
  • Blood Pressure: {random.randint(110, 150)}/{random.randint(70, 95)} mmHg
  • Heart Rate: {random.randint(60, 90)} bpm
  • Temperature: {random.uniform(36.5, 37.2):.1f}°C
  • Respiratory Rate: {random.randint(12, 18)}/min

RECENT LAB RESULTS:
  • Hemoglobin: {random.uniform(12.0, 16.0):.1f} g/dL
  • Creatinine: {random.uniform(0.8, 1.3):.1f} mg/dL
  • eGFR: {random.randint(60, 95)} mL/min/1.73m²

CLINICAL NOTES:
Patient presents for routine follow-up. {"Cardiac monitoring ongoing due to arrhythmia management with Drug-X." if has_drugx else "Stable on current medication regimen."}
No acute concerns noted. Continue current treatment plan.

NEXT APPOINTMENT: {(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')}

Attending Physician: Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])}
Department: Cardiology
"""
        
        filename = f"Patient_{patient_id:03d}_MedicalRecord.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Generated: {filename}")
        return filepath
    
    def generate_case_study(self, case_id: int):
        """Generate a clinical case study"""
        
        content = f"""CLINICAL CASE STUDY #{case_id}
{'='*60}

Title: Management of Cardiac Arrhythmia in Elderly Patients

Date: {datetime.now().strftime('%Y-%m-%d')}
Author: Clinical Research Team
Institution: Memorial Hospital Cardiology Department

ABSTRACT:
This case study examines the treatment outcomes of elderly patients 
presenting with cardiac arrhythmias. The study reviews medication 
efficacy, adverse events, and long-term management strategies.

KEY FINDINGS:
  • Arrhythmia prevalence increases significantly after age 65
  • Multi-drug interactions require careful monitoring
  • Regular ECG monitoring essential for elderly patients
  • Beta-blockers show good efficacy with manageable side effects

TREATMENT PROTOCOLS:
Standard care includes initial assessment, medication titration, and
quarterly follow-ups. Patients are monitored for therapeutic response
and potential adverse reactions.

CONCLUSION:
Individualized treatment plans with close monitoring provide optimal
outcomes for elderly cardiac patients. Regular reassessment of 
medication regimens is recommended based on emerging research.

References:
[1] American Heart Association Guidelines 2025
[2] European Society of Cardiology Recommendations
[3] Recent advances in cardiac arrhythmia management
"""
        
        filename = f"CaseStudy_{case_id:02d}_CardiacArrhythmia.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Generated: {filename}")
        return filepath
    
    def generate_protocol_document(self):
        """Generate a hospital protocol document"""
        
        content = f"""HOSPITAL PROTOCOL DOCUMENT
{'='*60}

Protocol ID: CARD-2025-001
Title: Cardiac Medication Safety Protocol
Version: 2.3
Effective Date: 2025-01-01
Last Reviewed: {datetime.now().strftime('%Y-%m-%d')}

PURPOSE:
To establish standardized procedures for prescribing and monitoring
cardiac medications, ensuring patient safety and optimal outcomes.

SCOPE:
This protocol applies to all cardiac care units and outpatient clinics
within the hospital system.

MEDICATION REVIEW PROCEDURES:

1. Initial Prescription Assessment:
   - Review patient medical history
   - Check for drug interactions
   - Verify dosage appropriateness for age/weight
   - Document baseline vital signs

2. Ongoing Monitoring:
   - Weekly vital sign checks for first month
   - Monthly lab work (BMP, liver function)
   - Quarterly ECG monitoring
   - Review adverse event reports

3. Red Flags - Immediate Physician Notification:
   - New onset arrhythmia
   - Significant blood pressure changes
   - Patient reports of dizziness, syncope, or chest pain
   - Abnormal lab values

EXTERNAL ALERT MONITORING:
All prescribers must review FDA safety communications and WHO alerts
weekly. Any relevant warnings must be acted upon within 24 hours.

DOCUMENTATION REQUIREMENTS:
All medication changes, patient communications, and monitoring results
must be documented in the electronic health record system.

Approved by:
Chief of Cardiology: Dr. Michael Chen
Date: 2025-01-15
"""
        
        filename = "Cardiac_Medication_Protocol_v2.3.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Generated: {filename}")
        return filepath
    
    def generate_full_dataset(self):
        """Generate a complete dataset for demo"""
        print("\n🏥 Generating Synthetic Medical Dataset...")
        print("="*60)
        
        # Generate 10 patient files
        # Patient 402 will have Drug-X (for demo)
        for i in range(1, 11):
            has_drugx = (i == 402 % 100) or (i in [2, 7])  # Patients 2, 7 have Drug-X
            self.generate_patient_file(400 + i, has_drugx=has_drugx)
        
        # Generate 3 case studies
        for i in range(1, 4):
            self.generate_case_study(i)
        
        # Generate protocol document
        self.generate_protocol_document()
        
        print("\n✨ Dataset generation complete!")
        print(f"📁 Files saved to: {self.output_dir}")


def main():
    """Generate the dataset"""
    from config.settings import settings
    
    generator = SyntheticDocGenerator(
        output_dir=str(settings.pathway_data_dir)
    )
    
    generator.generate_full_dataset()


if __name__ == "__main__":
    main()
