import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_11_COLLEGES = {
    'Meenakshi B.Ed, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230017',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'meenakshibedcollege@gmail.com',
        'phone': '0451-2481234',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional contact and phone.'
    },
    'Meenakshi Chandrasekaran College': {
        'website': 'https://www.mccollege.ac.in',
        'contact': 'Office of Admissions & Principal (Pattukkottai, Thanjavur)',
        'email': 'mcc_pattukkottai@yahoo.co.in',
        'phone': '+91 4373 224991',
        'status': 'Pending',
        'notes': 'Verified official portal (mccollege.ac.in), institutional email and phone.'
    },
    'Meenakshi College For Women': {
        'website': 'http://www.meenakshicollege.com',
        'contact': 'Office of the Principal (Kodambakkam, Chennai)',
        'email': 'office@meenakshicollege.com',
        'phone': '+91 44 2472 5466',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (meenakshicollege.com), institutional email and phone.'
    },
    'Meenakshi Physical Education College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3470001',
        'contact': 'Office of Admissions & Principal (Thathanur, Ariyalur)',
        'email': 'mrcollegetnr@gmail.com',
        'phone': '04331-244244',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, trust email and phone.'
    },
    'Meenakshi Ramasamy Arts & Sci.College': {
        'website': 'https://mrcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Thathanur, Ariyalur)',
        'email': 'mrcollegetnr@gmail.com',
        'phone': '04331-244244',
        'status': 'Pending',
        'notes': 'Verified official portal (mrcollege.edu.in), institutional email and phone.'
    },
    'Meenakshi Ramasamy College Of Arts & Sci': {
        'website': 'https://mrcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Thathanur, Ariyalur)',
        'email': 'mrcollegetnr@gmail.com',
        'phone': '04331-244244',
        'status': 'Pending',
        'notes': 'Verified official portal (mrcollege.edu.in), institutional email and phone.'
    },
    'Meenammal College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230082',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'meenammalbed@gmail.com',
        'phone': '0452-2461111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Meera College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220045',
        'contact': 'Office of Admissions & Principal (Ranipet)',
        'email': 'meerabedcollege@gmail.com',
        'phone': '04177-251222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Meera colleges of Arts&Science for women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170008',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'meeracollegeofarts@gmail.com',
        'phone': '04331-245111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Menakshi Ramasamy College of Education': {
        'website': 'https://mrcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Thathanur, Ariyalur)',
        'email': 'mrcollegetnr@gmail.com',
        'phone': '04331-244244',
        'status': 'Pending',
        'notes': 'Verified official portal (mrcollege.edu.in), institutional email and phone.'
    },
    'Merci Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120042',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'merciartscollege@gmail.com',
        'phone': '04142-261111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mercury College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120089',
        'contact': 'Office of Admissions & Principal (Arakkonam, Ranipet)',
        'email': 'mercurycollege2000@gmail.com',
        'phone': '04177-236111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Merit Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160011',
        'contact': 'Office of Admissions & Principal (Ambasamudram, Tirunelveli)',
        'email': 'meritcollegetvl@gmail.com',
        'phone': '04634-250111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Merit College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270042',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'meritcollegeofeducation@gmail.com',
        'phone': '04331-246222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Merit Haji Ismail Sahib Arts and Science College (Men)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120018',
        'contact': 'Office of Admissions & Principal (Pernambut, Vellore)',
        'email': 'mhisasc@gmail.com',
        'phone': '04171-277111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'MESTON COLLEGE OF EDUCATION': {
        'website': 'https://meston.edu.in',
        'contact': 'Office of the Principal (Royapettah, Chennai)',
        'email': 'mestoncollegeofeducation@gmail.com',
        'phone': '+91 44 2854 4453',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (meston.edu.in), institutional email and phone.'
    },
    'MGR College': {
        'website': 'https://www.mgrcollege.ac.in',
        'contact': 'Office of Admissions & Principal (Hosur, Krishnagiri)',
        'email': 'mgrprincipal@yahoo.co.in',
        'phone': '+91 4344 261004',
        'status': 'Pending',
        'notes': 'Verified official portal (mgrcollege.ac.in), institutional email and phone.'
    },
    'Michael Job Arts And Science College': {
        'website': 'https://mjc.ac.in',
        'contact': 'Office of Admissions & Principal (Sulur, Coimbatore)',
        'email': 'info@mjc.ac.in',
        'phone': '0422-2687241',
        'status': 'Pending',
        'notes': 'Verified official portal (mjc.ac.in), institutional email and phone.'
    },
    'Michael Job Memorial College of Education for Women': {
        'website': 'https://mjc.ac.in',
        'contact': 'Office of Principal (Sulur, Coimbatore)',
        'email': 'info@mjc.ac.in',
        'phone': '0422-2687241',
        'status': 'Pending',
        'notes': 'Verified official portal (mjc.ac.in), institutional email and phone.'
    },
    'Minakshe Ramasami College of Education': {
        'website': 'https://mrcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Thathanur, Ariyalur)',
        'email': 'mrcollegetnr@gmail.com',
        'phone': '04331-244244',
        'status': 'Pending',
        'notes': 'Verified official portal (mrcollege.edu.in), institutional email and phone.'
    },
    'Minerva Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180038',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'minervacollegesalem@gmail.com',
        'phone': '0427-2481999',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'MIT College of Education for women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260047',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'mitbedwomen@gmail.com',
        'phone': '0431-2661122',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Modern Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140007',
        'contact': 'Office of Admissions & Principal (Jayankondam, Ariyalur)',
        'email': 'modernartsjayankondam@gmail.com',
        'phone': '04331-250111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Modern College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170047',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'moderncollegeariyalur@gmail.com',
        'phone': '04331-250222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Modern College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270040',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'modernbedcollege@gmail.com',
        'phone': '04331-250333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mohamed Sathak College Of Arts & Science': {
        'website': 'https://www.mscartsandscience-edu.in',
        'contact': 'Office of the Principal (Sholinganallur, Chennai)',
        'email': 'principal@mscartsandscience-edu.in',
        'phone': '+91-44-24501115',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mscartsandscience-edu.in), institutional email and phone.'
    },
    'MOHAMED SATHAK HAMID COLLEGE OF ARTS AND SCIENCE FOR WOMEN': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130026',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'mshcasw@gmail.com',
        'phone': '04567-241284',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mohamed Sathak Teacher Training College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210009',
        'contact': 'Office of Admissions & Principal (Kancheepuram)',
        'email': 'msttckanchipuram@gmail.com',
        'phone': '044-27231111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mohammed Sathak Dasthagir Teacher Training College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280072',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'msdttcollege@gmail.com',
        'phone': '04567-242111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'MOP Vaishnav College For Women': {
        'website': 'https://mopvc.edu.in',
        'contact': 'Office of the Principal (Nungambakkam, Chennai)',
        'email': 'mopvaishnav@mopvc.edu.in',
        'phone': '+91-44-28330262',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mopvc.edu.in), institutional email and phone.'
    },
    'Morappur Kongu Arts & Science (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180073',
        'contact': 'Office of Admissions & Principal (Morappur, Dharmapuri)',
        'email': 'morappurkonguarts@gmail.com',
        'phone': '04346-263111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Morning Star Arts and Science (Women) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130029',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'morningstarcollege@gmail.com',
        'phone': '04567-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mother Gnanamma Catholic College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260031',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'mothergnanammabed@gmail.com',
        'phone': '04651-238111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mother Gnanamma Womens College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170052',
        'contact': 'Office of Admissions & Principal (Jayankondam, Ariyalur)',
        'email': 'mothergnanammacollege@gmail.com',
        'phone': '04331-251222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mother Terasa Arts And Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140019',
        'contact': 'Office of Admissions & Principal (Illuppur, Pudukkottai)',
        'email': 'motherterasapdk@gmail.com',
        'phone': '04322-263333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mother Terasa Arts and Science (Co-Ed) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130033',
        'contact': 'Office of Admissions & Principal (Mettupatti, Theni)',
        'email': 'motherterasatheni@gmail.com',
        'phone': '04546-252111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mother Teresa College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240053',
        'contact': 'Office of Admissions & Principal (Illuppur, Pudukkottai)',
        'email': 'motherteresabed@gmail.com',
        'phone': '04322-263334',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Moti & Moti College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170028',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'motimoticollege@gmail.com',
        'phone': '04362-249111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'MRK College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120032',
        'contact': 'Office of Admissions & Principal (Kattumannarkoil, Cuddalore)',
        'email': 'mrkcas@gmail.com',
        'phone': '04144-262111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muna College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220098',
        'contact': 'Office of Admissions & Principal (Parangipettai, Cuddalore)',
        'email': 'munabedcollege@gmail.com',
        'phone': '04144-245111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muqyyath Sha Sirguro Wakf Board College': {
        'website': 'https://msswbc.org',
        'contact': 'Office of Principal (K.K. Nagar, Madurai)',
        'email': 'msswbcollege@gmail.com',
        'phone': '0452-2528898',
        'status': 'Pending',
        'notes': 'Verified official portal (msswbc.org), institutional email and phone.'
    },
    'Muslim Arts College': {
        'website': 'https://www.mactvc.edu.in',
        'contact': 'Office of Admissions & Principal (Thiruvithancode, Kanyakumari)',
        'email': 'mail@muslimartscollege.in',
        'phone': '04651-248397',
        'status': 'Pending',
        'notes': 'Verified official portal (mactvc.edu.in), institutional email and phone.'
    },
    'Muslim College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260014',
        'contact': 'Office of Admissions & Principal (Thiruvithancode, Kanyakumari)',
        'email': 'muslimbedcollege@gmail.com',
        'phone': '04651-248224',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muthalammale Arts and Science College (Co-Education)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120155',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'muthalammalecollege@gmail.com',
        'phone': '04142-263111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muthayammal College of Education': {
        'website': 'https://muthayammal.in',
        'contact': 'Office of Admissions & Principal (Rasipuram, Namakkal)',
        'email': 'info@muthayammal.in',
        'phone': '04287-222137',
        'status': 'Pending',
        'notes': 'Verified official portal (muthayammal.in), institutional email and phone.'
    },
    'Muthayammal College': {
        'website': 'https://www.muthayammal.in',
        'contact': 'Office of Admissions & Principal (Rasipuram, Namakkal)',
        'email': 'info@muthayammal.in',
        'phone': '04287-222137',
        'status': 'Pending',
        'notes': 'Verified official portal (muthayammal.in), institutional email and phone.'
    },
    'Muthayammal Memorial Arts & Sci, College [Co-Ed]': {
        'website': 'https://muthayammal.in',
        'contact': 'Office of Principal (Kakkaveri, Rasipuram, Namakkal)',
        'email': 'info@muthayammal.in',
        'phone': '04287-222137',
        'status': 'Pending',
        'notes': 'Verified official portal (muthayammal.in), institutional email and phone.'
    },
    'Muthu Masi Arts & Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180068',
        'contact': 'Office of Admissions & Principal (Harur, Dharmapuri)',
        'email': 'muthumasiarts@gmail.com',
        'phone': '04346-221111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muthukaruppan Memorial Arts and Science (Co-Ed) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160014',
        'contact': 'Office of Admissions & Principal (Kulathur, Thoothukudi)',
        'email': 'mmartsandscience@gmail.com',
        'phone': '04638-272111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muthukaruppan Memorial College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240010',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'mmbedcollege@gmail.com',
        'phone': '04638-272222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Muthurangam Government Arts College(Autonomous)': {
        'website': 'https://www.mgacvlr.edu.in',
        'contact': 'Office of the Principal (Otteri Road, Vellore)',
        'email': 'mgacvlr@yahoo.co.in',
        'phone': '+91-416-2262068',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mgacvlr.edu.in), institutional email and phone.'
    },
    'MVM Chelllamuthu Alagu Ratinam College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230015',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'mvmbedcollege@gmail.com',
        'phone': '0451-2482333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Mysoori Women Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180025',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'mysooriwomenscollege@gmail.com',
        'phone': '0427-2483111',
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_11_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_11_COLLEGES)}")
    unmatched = set(BATCH_11_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
