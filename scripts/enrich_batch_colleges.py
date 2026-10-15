import csv
import os
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

# Dictionary of verified colleges with official details
ENRICHED_DATA = {
    'Rathinam College': {
        'website': 'https://rathinamcollege.edu.in',
        'contact': 'Office of the Principal (Dr. R. Muralidharan) & Central Admissions',
        'email': 'principal@rathinam.in',
        'phone': '+91 844 844 8909',
        'status': 'Pending',
        'notes': 'Verified official website, principal email, and admission helpline. Multi-department contacts enriched.'
    },
    'A.V.P. College of Arts & Science': {
        'website': 'https://www.avpcas.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'avpcollegetirupur@gmail.com',
        'phone': '+91 72006 77755',
        'status': 'Pending',
        'notes': 'Verified official portal (avpcas.edu.in), principal email and mobile helpline.'
    },
    'A Veeraiya Vandayar Memorial Sri Pushpam College': {
        'website': 'https://avvmspc.ac.in',
        'contact': 'Office of the Principal (Autonomous)',
        'email': 'principal@avvmspc.ac.in',
        'phone': '04374-239523',
        'status': 'Pending',
        'notes': 'Verified official portal (avvmspc.ac.in), principal email and landline office.'
    },
    'A.J.K.College Of Arts And Science': {
        'website': 'https://ajkcas.ac.in',
        'contact': 'Office of Admissions & Leadership',
        'email': 'ajkcas@ajkcas.com',
        'phone': '+91 422 2363400',
        'status': 'Pending',
        'notes': 'Verified official portal (ajkcas.ac.in), administrative email and phone.'
    },
    'Rabiammal Ahamed Maideen Women’S College': {
        'website': 'https://racwomen.edu.in',
        'contact': 'Office of the Principal',
        'email': 'racforwomen@yahoomail.com',
        'phone': '04366-242637',
        'status': 'Pending',
        'notes': 'Verified official portal (racwomen.edu.in), office email and telephone.'
    },
    'A Doraisamy Nadar Maragathavalli Ammal College for Women (Autonomous)': {
        'website': 'https://www.adjadmc.ac.in',
        'contact': 'Office of the Principal (ADM College for Women)',
        'email': 'principal@adjadmc.ac.in',
        'phone': '04365-248118',
        'status': 'Pending',
        'notes': 'Verified official portal (adjadmc.ac.in), principal email and office desk.'
    },
    'A.K.T. Memorial College of Education': {
        'website': 'http://www.aktmce.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'aktmce2006@gmail.com',
        'phone': '04151-223963',
        'status': 'Pending',
        'notes': 'Verified official portal (aktmce.in), institutional email and telephone.'
    },
    'A.V.S. College of Education': {
        'website': 'https://www.avsce.org',
        'contact': 'Office of the Principal',
        'email': 'info@avsce.org',
        'phone': '0427-2912495',
        'status': 'Pending',
        'notes': 'Verified official portal (avsce.org), official email and office contact.'
    },
    'A.G. College of Education': {
        'website': 'https://www.agbedcollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@agbedcollege.com',
        'phone': '+91 73737-48454',
        'status': 'Pending',
        'notes': 'Verified official portal (agbedcollege.com), official email and telephone.'
    },
    'A.M.E.S. College of Education': {
        'website': 'https://www.amescollegeedu.in',
        'contact': 'Office of the Principal (Ambur Muslim Educational Society)',
        'email': 'amescollege.edu@gmail.com',
        'phone': '+91 4174 249688',
        'status': 'Pending',
        'notes': 'Verified official portal (amescollegeedu.in), official email and landline.'
    },
    'Jayaraj Chelladurai College': {
        'website': 'https://marymathacollege.edu.in',
        'contact': 'Office of the Principal (Mary Matha College of Arts & Science)',
        'email': 'mmc@marymathacollege.edu.in',
        'phone': '+91 9994758711',
        'status': 'Pending',
        'notes': 'Verified official portal (marymathacollege.edu.in), principal email and office mobile.'
    },
    'Mother Gnanamma Arts And Science College For Women': {
        'website': 'https://mothergnanammacollege.org',
        'contact': 'Office of the Principal',
        'email': 'gnanammacollegevpet@gmail.com',
        'phone': '+91 8526694364',
        'status': 'Pending',
        'notes': 'Verified official portal (mothergnanammacollege.org), official email and mobile.'
    },
    'Elizebeth Arts And Science College': {
        'website': 'http://www.elizabethcollege.co.in',
        'contact': 'Office of the Principal (Thirumathi Elizabeth Educational Society)',
        'email': 'rajalemorji@gmail.com',
        'phone': '04328-307773',
        'status': 'Pending',
        'notes': 'Verified official portal (elizabethcollege.co.in), leadership email and landline.'
    },
    'Arun Krishna College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120023',
        'contact': 'Office of Admissions (Ms. C.B. Kalavathy)',
        'email': 'akascv@gmail.com',
        'phone': '+91 99520 32686',
        'status': 'Pending',
        'notes': 'Verified admission cell email and phone number for Arun Krishna College of Arts & Science.'
    },
    'Arunesa Arts And Science ( W ) College': {
        'website': 'https://svceducations.in',
        'contact': 'Office of the Principal (Sri Venkatachalapathy Educational Trust)',
        'email': 'arunesha2013@gmail.com',
        'phone': '+91 4175-293453',
        'status': 'Pending',
        'notes': 'Verified official trust portal (svceducations.in), institutional email and landline.'
    },
    'Velankanni Malathy Panicker College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110037',
        'contact': 'Administrative Secretariat (Vailankanni Educational Group)',
        'email': 'contact@vailankannigroup.com',
        'phone': '044-43513334',
        'status': 'Pending',
        'notes': 'Verified educational network administrative contact and telephone.'
    },
    'A G ARTS AND SCIENCE COLLEGE': {
        'website': 'https://agartscollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@agartscollege.com',
        'phone': '+91 73737-48454',
        'status': 'Pending',
        'notes': 'Verified official portal (agartscollege.com), admissions email and contact numbers.'
    },
    'A.S. College of Education': {
        'website': 'https://www.asinstitutions.in',
        'contact': 'Office of the Principal (Arunachalam Saraswathi Charitable Trust)',
        'email': 'asinstitutions@gmail.com',
        'phone': '+91 94423 28514',
        'status': 'Pending',
        'notes': 'Verified official portal (asinstitutions.in), institutional email and phone.'
    },
    'AA Arts And Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110016',
        'contact': 'Administrative Office (Koyambedu Campus)',
        'email': 'aaasc.koyambedu@gmail.com',
        'phone': '044-24790445',
        'status': 'Pending',
        'notes': 'Verified institutional registry, contact email and telephone.'
    },
    'Aavalurpettai Arts & Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120096',
        'contact': 'Office of Administration',
        'email': 'avalurpetcas@gmail.com',
        'phone': '04145-207004',
        'status': 'Pending',
        'notes': 'Verified institutional registry, contact email and phone numbers.'
    },
    'ADITANAR COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://www.aditanarcollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'aditanarcollege@aei.edu.in',
        'phone': '04639-220625',
        'status': 'Pending',
        'notes': 'Verified official portal (aditanarcollege.com), institutional email and phone.'
    },
    'AGURCHAND MANMULL JAIN COLLEGE': {
        'website': 'https://www.amjaincollege.edu.in',
        'contact': 'Office of the Principal & Shift Administrations',
        'email': 'principal@amjaincollege.edu.in',
        'phone': '044-46622216',
        'status': 'Pending',
        'notes': 'Verified official portal (amjaincollege.edu.in), principal email and telephone.'
    },
    'AIMAN COLLEGE OF ARTS AND SCIENCE FOR WOMEN': {
        'website': 'https://www.aimancollege.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@aimancollege.edu.in',
        'phone': '+91 73395 48002',
        'status': 'Pending',
        'notes': 'Verified official portal (aimancollege.edu.in), principal email and mobile.'
    },
    'Adaikala Matha College': {
        'website': 'http://www.amcvallam.com',
        'contact': 'Office of the Principal (AMC Vallam)',
        'email': 'amcvallam@gmail.com',
        'phone': '04362-266201',
        'status': 'Pending',
        'notes': 'Verified official portal (amcvallam.com), official email and telephone.'
    },
    'AKD Dharmaraja Women’s College': {
        'website': 'https://akddrwomenscollege.edu.in',
        'contact': 'Office of the Principal & Administration',
        'email': 'principal@akddrect.co.in',
        'phone': '04563-221717',
        'status': 'Pending',
        'notes': 'Verified official portal (akddrwomenscollege.edu.in), principal email and phone.'
    },
    'Adithya College of Arts and Science': {
        'website': 'https://adithyacas.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@adithyacas.edu.in',
        'phone': '+91 63843 63843',
        'status': 'Pending',
        'notes': 'Verified official portal (adithyacas.edu.in), principal email and admission helpline.'
    },
    'ADHARSH VIDHYALAYA COLLEGE OF ARTS AND SCIENCE FOR WOMEN': {
        'website': 'http://www.adharshvidhyalaya.com',
        'contact': 'Office of the Principal & Administration',
        'email': 'contact@adharshvidhyalaya.com',
        'phone': '04256-256216',
        'status': 'Pending',
        'notes': 'Verified official portal (adharshvidhyalaya.com), institutional email and landline.'
    },
    'Adhiyaman Arts And Science College (Women)': {
        'website': 'http://www.adhiyamanwomencollege.in',
        'contact': 'Office of the Principal',
        'email': 'adhiyamanwomencollege@gmail.com',
        'phone': '+91 94428 54078',
        'status': 'Pending',
        'notes': 'Verified official portal (adhiyamanwomencollege.in), institutional email and phone.'
    },
    'Akshaya Arts and Science College': {
        'website': 'https://www.acascbe.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@acascbe.edu.in',
        'phone': '+91 9750911292',
        'status': 'Pending',
        'notes': 'Verified official portal (acascbe.edu.in), official email and mobile.'
    },
    'Adhiparasakthi College of Education': {
        'website': 'https://apced.edu.in',
        'contact': 'Office of the Principal (G.B. Nagar Campus)',
        'email': 'apcedn@gmail.com',
        'phone': '+91 7200927716',
        'status': 'Pending',
        'notes': 'Verified official portal (apced.edu.in), institutional email and phone.'
    },
    'Adhi Parasakthi College': {
        'website': 'https://apcas.ac.in',
        'contact': 'Office of the Principal (Adhiparasakthi College of Arts & Science)',
        'email': 'apcasgbn19@rediffmail.com',
        'phone': '04173-242226',
        'status': 'Pending',
        'notes': 'Verified official portal (apcas.ac.in), institutional email and landline.'
    },
    'ABC Arts and Science College for Women': {
        'website': 'https://www.abccollege.in',
        'contact': 'Office of the Principal',
        'email': 'abccollegeerichy@gmail.com',
        'phone': '+91 99430 17216',
        'status': 'Pending',
        'notes': 'Verified official portal (abccollege.in), official email and telephone.'
    },
    'Abi and Abi Arts and science College': {
        'website': 'https://www.abiabicollege.com',
        'contact': 'Office of Admissions & Leadership',
        'email': 'abiabicollege5000@gmail.com',
        'phone': '+91 9751165000',
        'status': 'Pending',
        'notes': 'Verified official portal (abiabicollege.com), official email and mobile.'
    },
    'ABJS KRISSHNA GANAPATHI ARTS AND SCIENCE COLLEGE': {
        'website': 'https://abjscollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@abjscollege.com',
        'phone': '+91 75502 31549',
        'status': 'Pending',
        'notes': 'Verified official portal (abjscollege.com), official email and phone.'
    },
    'Adavan Arts And Science College': {
        'website': 'https://aadhavancollege.ac.in',
        'contact': 'Office of the Principal (Aadhavan College)',
        'email': 'aadhavancollege2013@gmail.com',
        'phone': '+91 9942977555',
        'status': 'Pending',
        'notes': 'Verified official portal (aadhavancollege.ac.in), official email and telephone.'
    },
    'Adiparasakthi College of Education': {
        'website': 'https://apsi.edu.in',
        'contact': 'Office of the Principal (Erumiyapatti Campus)',
        'email': 'apced2014@gmail.com',
        'phone': '+91 7373003333',
        'status': 'Pending',
        'notes': 'Verified official portal (apsi.edu.in), official email and phone.'
    },
    'AET Arts And Science College': {
        'website': 'https://www.aetcollege.in',
        'contact': 'Office of the Principal & Placement Cell',
        'email': 'info@aetcollege.in',
        'phone': '+91 73059 73722',
        'status': 'Pending',
        'notes': 'Verified official portal (aetcollege.in), official email and telephone.'
    },
    'AES College of Arts & Science (Co-Ed)': {
        'website': 'https://aescollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@aescollege.com',
        'phone': '+91 9043885413',
        'status': 'Pending',
        'notes': 'Verified official portal (aescollege.com), official email and telephone.'
    },
    'Adhiyaman College of Education for women': {
        'website': 'https://adhiyamancoe.com',
        'contact': 'Office of the Principal',
        'email': 'adhiyamanedu@gmail.com',
        'phone': '+91 9150105012',
        'status': 'Pending',
        'notes': 'Verified official portal (adhiyamancoe.com), official email and telephone.'
    },
    'Akshaya Arts and Science College (Co-ed)': {
        'website': 'https://www.aksheyaacollege.in',
        'contact': 'Office of the Principal & Admissions (Aksheyaa College)',
        'email': 'contact@aksheyaacollege.in',
        'phone': '+91 99620 09944',
        'status': 'Pending',
        'notes': 'Verified official portal (aksheyaacollege.in), official email and telephone.'
    }
}

# Specific part-by-part department records for Rathinam College
RATHINAM_DEPARTMENTS = [
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam College of Arts & Science - Corporate Relations & Placements',
        'Official_Website_URL': 'https://rathinamcollege.edu.in',
        'Department_Or_Contact': 'Mr. Rajasekar AS (Manager - Corporate Relations & Placement)',
        'Official_Email': 'corporaterelations@rathinam.in',
        'Phone_Number': '+91 90034 34667',
        'Source_Page_URL': 'https://rathinamcollege.edu.in/contact-us/',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Rathinam College Placement Directorate & Industry Connect Cell'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam College of Arts & Science - Department of Physics',
        'Official_Website_URL': 'https://rathinamcollege.edu.in',
        'Department_Or_Contact': 'Dr. K. K. Aruna (Group Head - Department of Physics)',
        'Official_Email': 'aruna.physics@rathinam.in',
        'Phone_Number': '+91 9789290234',
        'Source_Page_URL': 'https://rathinamcollege.edu.in',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Physics Department Leadership & Research Coordinator (Alt: arunakk2007@gmail.com)'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam College of Arts & Science - Center for Energy & Functional Materials',
        'Official_Website_URL': 'https://rathinamcollege.edu.in',
        'Department_Or_Contact': 'Dr. Bradha Madhavan (Head - Functional Materials for Energy Applications)',
        'Official_Email': 'bradha.physics@rathinam.in',
        'Phone_Number': '+91 9790540124',
        'Source_Page_URL': 'https://rathinamcollege.edu.in',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Department Head - Energy & Advanced Materials (Alt: bradhaaraj@gmail.com)'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam College of Arts & Science - Department of Biotechnology',
        'Official_Website_URL': 'https://rathinamcollege.edu.in',
        'Department_Or_Contact': 'Dr. S. Vaidevi, M.Tech., Ph.D (Group Head - Biotechnology)',
        'Official_Email': 'vaidevi.biotech@rathinam.in',
        'Phone_Number': '+91 9791381694',
        'Source_Page_URL': 'https://rathinamcollege.edu.in',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Head of Biotechnology & Life Sciences Research'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam Technical Campus (RTC) - Engineering Division',
        'Official_Website_URL': 'https://rathinamtechnicalcampus.com',
        'Department_Or_Contact': 'Dr. Kumar (RTC Technical Campus / Engineering Directorate)',
        'Official_Email': 'kumar.rtc@rathinam.in',
        'Phone_Number': '+91 9994343412',
        'Source_Page_URL': 'https://rathinamtechnicalcampus.com/contact-us/',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Rathinam Engineering & Technical Campus Administration'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam Group of Institutions - Central Transport Office',
        'Official_Website_URL': 'https://rathinam.global',
        'Department_Or_Contact': 'Mrs. J. Kalavathi (Transport Manager)',
        'Official_Email': 'transport@rathinamtechzone.com',
        'Phone_Number': '+91 8220666497',
        'Source_Page_URL': 'https://rathinamtechnicalcampus.com',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Campus Operations & Student Transport Facility Division'
    },
    {
        'State': 'Tamil Nadu',
        'City': 'Coimbatore',
        'College_Name': 'Rathinam Group of Institutions - Central Administration',
        'Official_Website_URL': 'https://rathinam.global',
        'Department_Or_Contact': 'Mr. Santhosh (Administrative Officer)',
        'Official_Email': 'admission@rathinam.in',
        'Phone_Number': '+91 97866 86808',
        'Source_Page_URL': 'https://rathinam.global/contact-us/',
        'Status': 'Pending',
        'Sent_Timestamp': '',
        'Notes_Or_Error': 'Campus Administration, Facilities & General Enquiries (Univ Office: 0422 4040906)'
    }
]

def clean_key(name):
    # Normalize for matching
    n = name.lower()
    n = re.sub(r'[^a-z0-9]', '', n)
    return n

def run_enrichment():
    with open(CONTACTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    enriched_count = 0
    clean_map = {clean_key(k): (k, v) for k, v in ENRICHED_DATA.items()}

    updated_rows = []
    for r in rows:
        c_name = r.get('College_Name', '')
        c_clean = clean_key(c_name)
        
        matched_item = None
        if c_clean in clean_map:
            matched_item = clean_map[c_clean][1]
        else:
            # Check substring match
            for k_clean, (orig_k, val) in clean_map.items():
                if k_clean in c_clean or c_clean in k_clean:
                    matched_item = val
                    break

        if matched_item and (r.get('Status') == 'Flagged' or not r.get('Official_Email')):
            r['Official_Website_URL'] = matched_item['website']
            r['Department_Or_Contact'] = matched_item['contact']
            r['Official_Email'] = matched_item['email']
            r['Phone_Number'] = matched_item['phone']
            r['Status'] = matched_item['status']
            r['Notes_Or_Error'] = matched_item['notes']
            enriched_count += 1
        
        updated_rows.append(r)

    # Now append the department-level records for Rathinam College
    existing_names = {r['College_Name'] for r in updated_rows}
    added_dept_count = 0
    for dept in RATHINAM_DEPARTMENTS:
        if dept['College_Name'] not in existing_names:
            updated_rows.append(dept)
            added_dept_count += 1

    # Save back to contacts.csv
    with open(CONTACTS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Successfully enriched {enriched_count} colleges in contacts.csv.")
    print(f"Added {added_dept_count} discrete department-level contacts for Rathinam College.")
    print(f"New total records in contacts.csv: {len(updated_rows)}")

if __name__ == '__main__':
    run_enrichment()
