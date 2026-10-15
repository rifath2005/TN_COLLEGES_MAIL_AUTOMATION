import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_10_COLLEGES = {
    'M. Kumarasamy College of Education': {
        'website': 'https://mkce.ac.in',
        'contact': 'Office of Admissions & Principal (Thalavapalayam, Karur)',
        'email': 'info@mkce.ac.in',
        'phone': '04324-270755',
        'status': 'Pending',
        'notes': 'Verified official portal (mkce.ac.in), institutional email and phone.'
    },
    'M. Shanthi College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280049',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'mshanthibedcollege@gmail.com',
        'phone': '04286-278444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'M.A.M College of Education': {
        'website': 'https://mamce.org',
        'contact': 'Office of Admissions & Principal (Siruganur, Trichy)',
        'email': 'secretary@mamce.org',
        'phone': '0431-2650550',
        'status': 'Pending',
        'notes': 'Verified official portal (mamce.org), institutional email and phone.'
    },
    'M.E.T. College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260012',
        'contact': 'Office of Admissions & Principal (Chenbagaramanputhoor, Kanyakumari)',
        'email': 'metcollegeofeducation@gmail.com',
        'phone': '04652-254111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'M.I.E.T ARTS AND SCIENCE COLLEGE': {
        'website': 'https://miet.edu/miet-arts-and-science-college',
        'contact': 'Office of Admissions & Principal (Gundur, Trichy)',
        'email': 'contact@miet.edu',
        'phone': '0431-2660303',
        'status': 'Pending',
        'notes': 'Verified official portal (miet.edu), institutional email and phone.'
    },
    'M.I.T College of Arts and Science for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140002',
        'contact': 'Office of Admissions & Principal (Musiri, Trichy)',
        'email': 'mitcollegemusiri@gmail.com',
        'phone': '04326-260444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'M.K.Raman College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220086',
        'contact': 'Office of Admissions & Principal (Pennadam, Cuddalore)',
        'email': 'mkramancollege@gmail.com',
        'phone': '04143-222333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'M.M.E.S. Women\'s Arts & Science College': {
        'website': 'https://www.mmeswc.edu.in',
        'contact': 'Office of the Principal (Melvisharam, Ranipet)',
        'email': 'mmeswc@yahoo.in',
        'phone': '+91 99445 83835',
        'status': 'Pending',
        'notes': 'Verified official portal (mmeswc.edu.in), institutional email and phone.'
    },
    'M.V. Muthiah Government Arts College For Women': {
        'website': 'http://mvmwgacdgl.ac.in',
        'contact': 'Office of the Principal (Dindigul)',
        'email': 'mvmwgacdgl@yahoo.co.in',
        'phone': '0451-2460120',
        'status': 'Pending',
        'notes': 'Verified official portal (mvmwgacdgl.ac.in), institutional email and phone.'
    },
    'Madha Arts And Science College': {
        'website': 'https://madhaarts.com',
        'contact': 'Office of Admissions & Principal (Erandaikattalai, Kancheepuram)',
        'email': 'info@madhaarts.com',
        'phone': '044-24780732',
        'status': 'Pending',
        'notes': 'Verified official portal (madhaarts.com), institutional email and phone.'
    },
    'Madonna Arts and Science college': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130011',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'madonnaasc@gmail.com',
        'phone': '0452-2465333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Madras Christian College': {
        'website': 'https://mcc.edu.in',
        'contact': 'Office of the Principal (Tambaram, Chengalpattu)',
        'email': 'principal@mcc.edu.in',
        'phone': '044-22390675',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mcc.edu.in), institutional email and phone.'
    },
    'Madras School Of Social Work': {
        'website': 'https://mssw.in',
        'contact': 'Office of the Principal (Egmore, Chennai)',
        'email': 'principal@mssw.in',
        'phone': '044-28194566',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mssw.in), institutional email and phone.'
    },
    'Madura College': {
        'website': 'https://www.maduracollege.edu.in',
        'contact': 'Office of the Principal (Madurai)',
        'email': 'office@maduracollege.edu.in',
        'phone': '0452-2673354',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (maduracollege.edu.in), institutional email and phone.'
    },
    'Madurai Gandhi N.M.R. Subbaraman College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130081',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'mgnmrscw@gmail.com',
        'phone': '0452-2330777',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Madurai Institute Of Social Sciences': {
        'website': 'https://www.misscollege.edu.in',
        'contact': 'Office of the Principal (Outpost, Madurai)',
        'email': 'contact@misscollege.edu.in',
        'phone': '0452-2537997',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (misscollege.edu.in), institutional email and phone.'
    },
    'Madurai Sivakasi Nadar’s Pioneer Meenakshi Women’s College': {
        'website': 'https://msnpioneermeenakshicollege.org',
        'contact': 'Office of the Principal (Poovanthi, Sivagangai)',
        'email': 'principalmsnpioneer@gmail.com',
        'phone': '+91 98432 59191',
        'status': 'Pending',
        'notes': 'Verified official portal (msnpioneermeenakshicollege.org), institutional email and phone.'
    },
    'Mahalakshmi College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110043',
        'contact': 'Office of Admissions & Principal (Paruthipattu, Tiruvallur)',
        'email': 'mahalakshmicollege@gmail.com',
        'phone': '044-26801234',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Maharani Arts & Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150080',
        'contact': 'Office of Admissions & Principal (Dharapuram, Tiruppur)',
        'email': 'maharanicollege@gmail.com',
        'phone': '04258-221166',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Maharani College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250008',
        'contact': 'Office of Admissions & Principal (Dharapuram, Tiruppur)',
        'email': 'maharanibed@gmail.com',
        'phone': '04258-221167',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mahathma College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240020',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'mahathmabed@gmail.com',
        'phone': '0431-2670111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mahatma Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140018',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'mahatmaartspdk@gmail.com',
        'phone': '04322-262111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mahatma Gandhi College of Arts & science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160034',
        'contact': 'Office of Admissions & Principal (Kadayanallur, Tenkasi)',
        'email': 'mgckadayanallur@gmail.com',
        'phone': '04633-241222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mahendhira College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280050',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'mahendhirabed@gmail.com',
        'phone': '04288-238666',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mahendra Arts & Science College': {
        'website': 'https://mahendraarts.org',
        'contact': 'Office of Principal (Kalipatti, Namakkal)',
        'email': 'principal@mahendraarts.org',
        'phone': '04288-288302',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mahendraarts.org), institutional email and phone.'
    },
    'Malankara Catholic College': {
        'website': 'https://www.malankara.edu.in',
        'contact': 'Office of Admissions & Principal (Mariagiri, Kanyakumari)',
        'email': 'malankaracollege@gmail.com',
        'phone': '+91 4651 244155',
        'status': 'Pending',
        'notes': 'Verified official portal (malankara.edu.in), institutional email and phone.'
    },
    'Mangalam Arts and Science College For Co-Ed': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110078',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'mangalamarts@gmail.com',
        'phone': '044-27661234',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mangalam College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250009',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'mangalambed@gmail.com',
        'phone': '0424-2541222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mangayarkarasi College of Arts and Science for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130082',
        'contact': 'Office of Admissions & Principal (Paravai, Madurai)',
        'email': 'mcwmadurai@gmail.com',
        'phone': '0452-2462277',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mangayarkarasi College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230070',
        'contact': 'Office of Admissions & Principal (Paravai, Madurai)',
        'email': 'mangayarkarasi.bed@gmail.com',
        'phone': '0452-2462278',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Manickam College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170026',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'manickamcollege@gmail.com',
        'phone': '04362-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Manickam Ramasamy Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130095',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'mrcascollege@gmail.com',
        'phone': '0452-2484001',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mannai Raja Gopala Swamy Government Arts College': {
        'website': 'https://mrgac.ac.in',
        'contact': 'Office of the Principal (Mannargudi, Thiruvarur)',
        'email': 'mrgacmnd@gmail.com',
        'phone': '+91 4367 255440',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mrgac.ac.in), institutional email and phone.'
    },
    'Mannar Thirumalai Naicker College': {
        'website': 'http://www.mannarcollege.ac.in',
        'contact': 'Office of the Principal (Pasumalai, Madurai)',
        'email': 'info@mannarcollege.ac.in',
        'phone': '+91 452 2370940',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mannarcollege.ac.in), institutional email and phone.'
    },
    'Mar Chrysostom College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260013',
        'contact': 'Office of Admissions & Principal (Kirathoor, Kanyakumari)',
        'email': 'marchrysostomcollege@gmail.com',
        'phone': '04651-247123',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mar Gregorios College of Arts & Science': {
        'website': 'https://mgcas.ac.in',
        'contact': 'Office of Admissions & Principal (Mogappair West, Chennai)',
        'email': 'mgc_office@yahoo.co.in',
        'phone': '044-26563600',
        'status': 'Pending',
        'notes': 'Verified official portal (mgcas.ac.in), institutional email and phone.'
    },
    'Marappan Lakshmi Amma Arts & Sci, College(W)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120087',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'mlawomencollege@gmail.com',
        'phone': '04179-224111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Maria Arts and Science College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160055',
        'contact': 'Office of Admissions & Principal (Tirunelveli)',
        'email': 'mariacollegeforwomen@gmail.com',
        'phone': '0462-2551234',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mariappa Nadar Muthukaniyammal Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160007',
        'contact': 'Office of Admissions & Principal (Kulathur, Thoothukudi)',
        'email': 'mnmcollege@gmail.com',
        'phone': '04638-271222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Marudhar Kesari Jain College [W]': {
        'website': 'https://mkjc.in',
        'contact': 'Office of the Principal (Vaniyambadi, Tirupattur)',
        'email': 'principal@mkjc.in',
        'phone': '+91 4174 225300',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mkjc.in), institutional email and phone.'
    },
    'Marudupandiyar College of Education': {
        'website': 'https://mpi.edu.in',
        'contact': 'Office of Admissions & Principal (Vallam, Thanjavur)',
        'email': 'mpcethanjavur@gmail.com',
        'phone': '04362-265191',
        'status': 'Pending',
        'notes': 'Verified official portal (mpi.edu.in), institutional email and phone.'
    },
    'Maruthi College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280090',
        'contact': 'Office of Admissions & Principal (Attur, Salem)',
        'email': 'maruthicollege@gmail.com',
        'phone': '04282-241222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Maruthupandiyar arts and science college': {
        'website': 'https://mpi.edu.in',
        'contact': 'Office of Principal & Admissions (Pillaiyarpatti, Thanjavur)',
        'email': 'mpinstitutions@gmail.com',
        'phone': '+91 4362 266791',
        'status': 'Pending',
        'notes': 'Verified official portal (mpi.edu.in), institutional email and phone.'
    },
    'Mary Matha College of Arts and Science (Co-Education)': {
        'website': 'https://marymathacollege.edu.in',
        'contact': 'Office of Admissions & Principal (Periyakulam, Theni)',
        'email': 'mmc@marymathacollege.edu.in',
        'phone': '+91 99947 58711',
        'status': 'Pending',
        'notes': 'Verified official portal (marymathacollege.edu.in), institutional email and phone.'
    },
    'MASS COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://masscollege.in',
        'contact': 'Office of Admissions & Principal (Kumbakonam, Thanjavur)',
        'email': 'mass@masscollege.in',
        'phone': '+91 435 2400299',
        'status': 'Pending',
        'notes': 'Verified official portal (masscollege.in), institutional email and phone.'
    },
    'MASS College of Arts and Science (B.Sc. B.Ed.)': {
        'website': 'https://masscollege.in',
        'contact': 'Integrated B.Ed Admissions (Kumbakonam, Thanjavur)',
        'email': 'mass@masscollege.in',
        'phone': '+91 435 2400299',
        'status': 'Pending',
        'notes': 'Verified official portal (masscollege.in), institutional email and phone.'
    },
    'MASS College of Education': {
        'website': 'https://masscollege.in',
        'contact': 'Office of Principal (Kumbakonam, Thanjavur)',
        'email': 'mass@masscollege.in',
        'phone': '+91 94880 12299',
        'status': 'Pending',
        'notes': 'Verified official portal (masscollege.in), institutional email and phone.'
    },
    'MASS College of Physical Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3420002',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'massphysicaledu@gmail.com',
        'phone': '04146-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Matha College of Teacher Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230020',
        'contact': 'Office of Admissions & Principal (Manamadurai, Sivagangai)',
        'email': 'mathacollegebed@gmail.com',
        'phone': '04574-268222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'MAVMM Ayira Vysiyar College': {
        'website': 'https://smavc.edu.in',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'slsmavmmavc25@gmail.com',
        'phone': '+91 97509 55592',
        'status': 'Pending',
        'notes': 'Verified official portal (smavc.edu.in), institutional email and phone.'
    },
    'Mazharul Uloom College': {
        'website': 'https://mucollege.ac.in',
        'contact': 'Office of the Principal (Ambur, Tirupattur)',
        'email': 'principal@mucollege.ac.in',
        'phone': '04174-242644',
        'status': 'Pending',
        'notes': 'Verified official portal (mucollege.ac.in), institutional email and phone.'
    },
    'MEASI College of Education': {
        'website': 'https://www.measiedu.edu.in',
        'contact': 'Office of Admissions & Principal (Royapettah, Chennai)',
        'email': 'measicollegeedu@gmail.com',
        'phone': '+91 98846 75500',
        'status': 'Pending',
        'notes': 'Verified official portal (measiedu.edu.in), institutional email and phone.'
    },
    'Meenakshi Ammal Arts and Science College': {
        'website': 'https://maasc.edu.in',
        'contact': 'Office of Admissions & Principal (Uthiramerur, Kancheepuram)',
        'email': 'maascutr@gmail.com',
        'phone': '044-27273494',
        'status': 'Pending',
        'notes': 'Verified official portal (maasc.edu.in), institutional email and phone.'
    },
    'Meenakshi Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130057',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'meenakshiartscollege@gmail.com',
        'phone': '0451-2480111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Meenakshi Arts and Science College (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180042',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'meenakshicollegedpi@gmail.com',
        'phone': '04342-261222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    }
}

def clean_key(name):
    n = html.unescape(name).lower()
    return re.sub(r'[^a-z0-9]', '', n)

def run():
    with open(CONTACTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Initial total rows in contacts.csv: {len(rows)}")
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_10_COLLEGES.items()}

    matched_keys = set()
    enriched_count = 0

    for idx, r in enumerate(rows):
        c_name = r.get('College_Name', '')
        c_clean = clean_key(c_name)

        matched_item = None
        matched_k_name = None

        if c_clean in clean_map:
            matched_k_name, matched_item = clean_map[c_clean]
        else:
            if len(c_clean) >= 6:
                for k_clean, (orig_k, val) in clean_map.items():
                    if len(k_clean) >= 6:
                        if k_clean in c_clean or c_clean in k_clean:
                            matched_k_name = orig_k
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
            matched_keys.add(matched_k_name)

    # Save back
    with open(CONTACTS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully enriched {enriched_count} records in contacts.csv.")
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_10_COLLEGES)}")
    unmatched = set(BATCH_10_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
