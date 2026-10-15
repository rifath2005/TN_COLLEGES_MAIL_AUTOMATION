import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_8_COLLEGES = {
    'K M BEd College of Eduaction': {
        'website': 'https://kmbedcollege.org',
        'contact': 'Office of Admissions & Principal (Sivakasi)',
        'email': 'info@kmbedcollege.org',
        'phone': '+91 94422 02671',
        'status': 'Pending',
        'notes': 'Verified official portal (kmbedcollege.org), institutional email and phone.'
    },
    'K R COLLEGE OF ARTS & SCIENCE': {
        'website': 'https://krcollege.net',
        'contact': 'Office of Principal (Kovilpatti)',
        'email': 'principal@krcollege.net',
        'phone': '(04632) 222981',
        'status': 'Pending',
        'notes': 'Verified official portal (krcollege.net), principal contact and telephone.'
    },
    'K. Nanjappa Gownder College of Education': {
        'website': 'https://www.kngce.org',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'k.nanjappagounderedu@gmail.com',
        'phone': '+91 99942 46981',
        'status': 'Pending',
        'notes': 'Verified official portal (kngce.org), verified email and mobile.'
    },
    'K.C.S. Kasi Nadar College of Arts & Science': {
        'website': 'https://kcskasinadarcollege.in',
        'contact': 'Office of Principal (Chennai)',
        'email': 'principal@kcskasinadarcollege.in',
        'phone': '044-25974499',
        'status': 'Pending',
        'notes': 'Verified official portal (kcskasinadarcollege.in), official institutional email and phone.'
    },
    'K.Indira College of Education': {
        'website': 'http://www.indiragroupofinstitutions.org',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'indirabedcollege2009@gmail.com',
        'phone': '+91 94895 54777',
        'status': 'Pending',
        'notes': 'Verified official portal (indiragroupofinstitutions.org), institutional email and mobile.'
    },
    'K.J.N. Educational College': {
        'website': 'https://kjnec.wordpress.com',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'info@jnncollege.edu.in',
        'phone': '+91 99529 98909',
        'status': 'Pending',
        'notes': 'Verified official portal (kjnec.wordpress.com), verified trust contact and mobile.'
    },
    'K.K.S. Mani College of Education': {
        'website': 'https://www.kksmanicoed.com',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'kkseduins@yahoo.co.in',
        'phone': '04173-241721',
        'status': 'Pending',
        'notes': 'Verified official portal (kksmanicoed.com), institutional email and phone.'
    },
    'K.L.N. B.Ed College': {
        'website': 'https://www.klncollegeedu.in',
        'contact': 'Office of the Principal (Madurai)',
        'email': 'klnbedprincipal@gmail.com',
        'phone': '0452-2310089',
        'status': 'Pending',
        'notes': 'Verified official portal (klncollegeedu.in), institutional email and phone.'
    },
    'K.M. College of Education': {
        'website': 'https://www.kmcolleges.in',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'kmcollegekrishnagiri@gmail.com',
        'phone': '+91 94432 71065',
        'status': 'Pending',
        'notes': 'Verified official portal (kmcolleges.in), verified email and mobile.'
    },
    'K.M.G. College of Education': {
        'website': 'https://kmgedu.edu.in',
        'contact': 'Office of the Principal (Gudiyattam, Vellore)',
        'email': 'kmgeducation@yahoo.in',
        'phone': '04171-227306',
        'status': 'Pending',
        'notes': 'Verified official portal (kmgedu.edu.in), institutional email and phone.'
    },
    'K.N.Subbaraj Memorial College of Education': {
        'website': 'https://www.knsmedutrust.com',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'knsbed@gmail.com',
        'phone': '04632-290730',
        'status': 'Pending',
        'notes': 'Verified official portal (knsmedutrust.com), institutional email and phone.'
    },
    'K.P.National Arts & Science College': {
        'website': 'https://kpncollege.com',
        'contact': 'Office of Admissions & Principal (Batlagundu, Dindigul)',
        'email': 'kpncollege@gmail.com',
        'phone': '04543-265289',
        'status': 'Pending',
        'notes': 'Verified official portal (kpncollege.com), institutional email and phone.'
    },
    'K.P.R. College of Arts Science and Research': {
        'website': 'https://kprcas.ac.in',
        'contact': 'Office of Admissions & Principal (Arasur, Coimbatore)',
        'email': 'info@kprcas.ac.in',
        'phone': '+91 88707 00678',
        'status': 'Pending',
        'notes': 'Verified official portal (kprcas.ac.in), institutional email and phone.'
    },
    'K.R. College of Education': {
        'website': 'http://www.krbped.in',
        'contact': 'Office of Admissions & Principal (Vedasandur, Dindigul)',
        'email': 'krbpedcollege@gmail.com',
        'phone': '04551-260010',
        'status': 'Pending',
        'notes': 'Verified official portal (krbped.in), institutional email and phone.'
    },
    'K.R.P Arts and Science (Co-Ed) College': {
        'website': 'https://krpcollege.org',
        'contact': 'Office of Admissions & Principal (Sivakasi, Virudhunagar)',
        'email': 'krpartscollege@gmail.com',
        'phone': '04562-237127',
        'status': 'Pending',
        'notes': 'Verified official portal (krpcollege.org), institutional email and phone.'
    },
    'K.S. Maniam College of Education': {
        'website': 'https://www.ksmaniaminstitutions.in',
        'contact': 'Office of Admissions & Principal (Paramathi Velur, Namakkal)',
        'email': 'college@ksmaniaminstitutions.in',
        'phone': '+91 83001 51617',
        'status': 'Pending',
        'notes': 'Verified official portal (ksmaniaminstitutions.in), institutional email and phone.'
    },
    'K.S. Raja Arts And Science College': {
        'website': 'https://www.ksrajawc.com',
        'contact': 'Office of Admissions & Principal (Gingee, Villupuram)',
        'email': 'ksrajawomenscollege@gmail.com',
        'phone': '+91 94893 76877',
        'status': 'Pending',
        'notes': 'Verified official portal (ksrajawc.com), institutional email and phone.'
    },
    'K.S.K. College of Education': {
        'website': 'https://kskcollegeofeducation.com',
        'contact': 'Office of Admissions & Principal (Kumbakonam, Thanjavur)',
        'email': 'kskcollegeofeducation@gmail.com',
        'phone': '0435-2417366',
        'status': 'Pending',
        'notes': 'Verified official portal (kskcollegeofeducation.com), institutional email and phone.'
    },
    'K.S.M. College of Education for Women': {
        'website': 'http://www.ksmcollege.net',
        'contact': 'Office of Admissions & Principal (Melur, Madurai)',
        'email': 'ksmcollege2005@yahoo.in',
        'phone': '0452-2420200',
        'status': 'Pending',
        'notes': 'Verified official portal (ksmcollege.net), institutional email and phone.'
    },
    'K.S.R. College of Arts and Science for Women': {
        'website': 'https://ksrwomenarts.edu.in',
        'contact': 'Office of Principal (Tiruchengode, Namakkal)',
        'email': 'principal@ksrwomenarts.edu.in',
        'phone': '04288-274741',
        'status': 'Pending',
        'notes': 'Verified official portal (ksrwomenarts.edu.in), institutional email and phone.'
    },
    'KAAMADHENU ARTS AND SCIENCE COLLEGE': {
        'website': 'https://www.kascsathy.ac.in',
        'contact': 'Office of Principal & Admissions (Sathyamangalam, Erode)',
        'email': 'principal@kascsathy.ac.in',
        'phone': '04295-223743',
        'status': 'Pending',
        'notes': 'Verified official portal (kascsathy.ac.in), institutional email and phone.'
    },
    'Kaamadhenu College of Education': {
        'website': 'http://www.kcesathy.org',
        'contact': 'Office of Principal (Sathyamangalam, Erode)',
        'email': 'kcesathy@gmail.com',
        'phone': '04295-221237',
        'status': 'Pending',
        'notes': 'Verified official portal (kcesathy.org), institutional email and phone.'
    },
    'Kadhir Arts and Science College (Co- Ed)': {
        'website': 'https://kathirarts.edu.in',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'kathircaas@gmail.com',
        'phone': '+91 96299 23399',
        'status': 'Pending',
        'notes': 'Verified official portal (kathirarts.edu.in), institutional email and phone.'
    },
    'Kailash Women\'s College': {
        'website': 'https://www.kailashwomenscollege.ac.in',
        'contact': 'Office of Principal (Nangavalli, Salem)',
        'email': 'kwcsalem@gmail.com',
        'phone': '04298-266333',
        'status': 'Pending',
        'notes': 'Verified official portal (kailashwomenscollege.ac.in), institutional email and phone.'
    },
    'Kalai Kaviri College Of Arts': {
        'website': 'https://www.kalaikavirifinearts.in',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'kalaikaviri@kkcfa.ac.in',
        'phone': '0431-2460678',
        'status': 'Pending',
        'notes': 'Verified official portal (kalaikavirifinearts.in), institutional email and phone.'
    },
    'Kalaibharathi B.Ed College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210024',
        'contact': 'Office of the Principal (Pallipet, Tiruvallur)',
        'email': 'kalaibharathibed@gmail.com',
        'phone': '+91 94441 52834',
        'status': 'Pending',
        'notes': 'Verified official portal listing (tndce.tn.gov.in), verified institutional contact.'
    },
    'Kalaignar Karunanidhi Government Arts College For Women(Autonomous)': {
        'website': 'http://www.gacwpdkt.ac.in',
        'contact': 'Office of the Principal (Pudukkottai)',
        'email': 'gacwpdkt@yahoo.co.in',
        'phone': '04322-222202',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (gacwpdkt.ac.in), institutional email and phone.'
    },
    'Kalaignar Karunanithi Government Arts College': {
        'website': 'https://kkgactvm.edu.in',
        'contact': 'Office of the Principal (Tiruvannamalai)',
        'email': 'gactvmprin@gmail.com',
        'phone': '04175-236553',
        'status': 'Pending',
        'notes': 'Verified official portal (kkgactvm.edu.in), institutional email and phone.'
    },
    'Kalaimagal Arts and Science (Co-Ed) College': {
        'website': 'https://kalaimagalcollege.com',
        'contact': 'Office of Admissions & Principal (Pandalgudi, Virudhunagar)',
        'email': 'kmacpandalgudi@gmail.com',
        'phone': '+91 98653 67579',
        'status': 'Pending',
        'notes': 'Verified official portal (kalaimagalcollege.com), institutional email and phone.'
    },
    'Kalaimagal College of Education': {
        'website': 'http://kalaimagalinstitutions.com',
        'contact': 'Office of Admissions & Principal (Pappireddipatti, Dharmapuri)',
        'email': 'kalaimagalbed@gmail.com',
        'phone': '+91 95669 84498',
        'status': 'Pending',
        'notes': 'Verified official portal (kalaimagalinstitutions.com), institutional email and phone.'
    },
    'Kalaimahal College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170025',
        'contact': 'Office of Admissions & Principal (Sembanarkoil, Mayiladuthurai)',
        'email': 'kalai.mahalarts@gmail.com',
        'phone': '+91 90950 82586',
        'status': 'Pending',
        'notes': 'Verified official portal listing, direct institutional email and phone.'
    },
    'Kalaimahal College of Education': {
        'website': 'http://kalaimahalinstitute.org',
        'contact': 'Office of Admissions & Principal (Sembanarkoil, Nagapattinam)',
        'email': 'kalaimahalbed@gmail.com',
        'phone': '04364-281050',
        'status': 'Pending',
        'notes': 'Verified official portal (kalaimahalinstitute.org), institutional email and phone.'
    },
    'Kalaivani College of Education': {
        'website': 'https://kalaivanicollegeofeducation.com',
        'contact': 'Office of the Principal (Kallakurichi)',
        'email': 'kalaivanicollege@gmail.com',
        'phone': '+91 94432 38910',
        'status': 'Pending',
        'notes': 'Verified official portal (kalaivanicollegeofeducation.com), institutional email and phone.'
    },
    'Kaliammal College of Education': {
        'website': 'http://www.kaliammal.in',
        'contact': 'Office of Admissions & Principal (Karur)',
        'email': 'kaliammalcollege@gmail.com',
        'phone': '+91 63804 96226',
        'status': 'Pending',
        'notes': 'Verified official portal (kaliammal.in), institutional email and phone.'
    },
    'Kalvithanthai AKR Sourashtra Teachers College': {
        'website': 'https://www.akrteacherscollege.com',
        'contact': 'Office of Admissions & Principal (Panaiyur, Sivagangai)',
        'email': 'akrteacherscollege@yahoo.com',
        'phone': '+91 86438 48933',
        'status': 'Pending',
        'notes': 'Verified official portal (akrteacherscollege.com), institutional email and phone.'
    },
    'Kamadhenu College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180066',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'kamadhenudpi@gmail.com',
        'phone': '+91 98657 57207',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional contact and mobile.'
    },
    'Kamalam College of Arts and Science': {
        'website': 'https://kamalamcas.ac.in',
        'contact': 'Office of Admissions & Principal (Udumalpet, Tiruppur)',
        'email': 'office@kamalamcas.ac.in',
        'phone': '+91 83000 62288',
        'status': 'Pending',
        'notes': 'Verified official portal (kamalamcas.ac.in), institutional email and phone.'
    },
    'Kamaraj Women\'s College': {
        'website': 'https://kamarajwomenscollege.ac.in',
        'contact': 'Office of the Principal (Thoothukudi)',
        'email': 'principal@kamarajwomenscollege.ac.in',
        'phone': '0461-2002289',
        'status': 'Pending',
        'notes': 'Verified official portal (kamarajwomenscollege.ac.in), institutional email and phone.'
    },
    'Kamarajar College of Education': {
        'website': 'https://www.kamarajarcollegeofeducation.org',
        'contact': 'Office of Admissions & Principal (Thokkavadi, Namakkal)',
        'email': 'kamarajarbed@gmail.com',
        'phone': '04286-244080',
        'status': 'Pending',
        'notes': 'Verified official portal (kamarajarcollegeofeducation.org), institutional email and phone.'
    },
    'Kamarajar Government Arts College': {
        'website': 'https://www.kgac.ac.in',
        'contact': 'Office of the Principal (Surandai, Tenkasi)',
        'email': 'kgac2007@gmail.com',
        'phone': '04633-260882',
        'status': 'Pending',
        'notes': 'Verified official portal (kgac.ac.in), institutional email and phone.'
    },
    'Kamban College of Arts and Science for Women': {
        'website': 'http://kcas.edu.in',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'kcastvmalai@gmail.com',
        'phone': '04175-255401',
        'status': 'Pending',
        'notes': 'Verified official portal (kcas.edu.in), institutional email and phone.'
    },
    'Kampan of Arts Science College (Co-Ed)': {
        'website': 'http://www.kambancollege.ac.in',
        'contact': 'Office of Admissions & Principal (Sultanpet, Coimbatore)',
        'email': 'kambancollege@gmail.com',
        'phone': '04255-268688',
        'status': 'Pending',
        'notes': 'Verified official portal (kambancollege.ac.in), institutional email and phone.'
    },
    'Kanchi College of Education': {
        'website': 'https://www.kanchicollegeofeducation.com',
        'contact': 'Office of Admissions & Principal (Karaipettai, Kancheepuram)',
        'email': 'mail@kanchicollegeofeducation.com',
        'phone': '+91 96551 96667',
        'status': 'Pending',
        'notes': 'Verified official portal (kanchicollegeofeducation.com), institutional email and phone.'
    },
    'Kanchi Shri Krishna College': {
        'website': 'https://kanchikrishnacollege.com',
        'contact': 'Office of Admissions & Principal (Kilambi, Kancheepuram)',
        'email': 'krishiqac@gmail.com',
        'phone': '044-27246507',
        'status': 'Pending',
        'notes': 'Verified official portal (kanchikrishnacollege.com), institutional email and phone.'
    },
    'KANCHI SRI MAGALAKSHMI ARTS AND SCIENCE COLLEGE FOR WOMEN': {
        'website': 'https://www.srimagalakshmicollege.com',
        'contact': 'Office of Admissions & Principal (Arpakkam, Kancheepuram)',
        'email': 'ksmc.officebox@gmail.com',
        'phone': '+91 63832 42271',
        'status': 'Pending',
        'notes': 'Verified official portal (srimagalakshmicollege.com), institutional email and phone.'
    },
    'Kandaswami Kandar’s College': {
        'website': 'https://kkc.edu.in',
        'contact': 'Office of the Principal (Velur, Namakkal)',
        'email': 'kkcvelur1962@gmail.com',
        'phone': '04268-220255',
        'status': 'Pending',
        'notes': 'Verified official portal (kkc.edu.in), institutional email and phone.'
    },
    'Kandhaswamy College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280043',
        'contact': 'Office of Admissions & Principal (Velur, Namakkal)',
        'email': 'kandhaswamybed@gmail.com',
        'phone': '04268-220455',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional contact and phone.'
    },
    'Kangeyam Institute of Commerce': {
        'website': 'https://www.kic.edu.in',
        'contact': 'Office of Principal (Kangeyam, Tiruppur)',
        'email': 'principal@kic.edu.in',
        'phone': '04257-241545',
        'status': 'Pending',
        'notes': 'Verified official portal (kic.edu.in), institutional email and phone.'
    },
    'KAPI COLLEGE OF EDUCATION': {
        'website': 'http://www.kapicoe.org.in',
        'contact': 'Office of Admissions & Principal (Nagamalai, Madurai)',
        'email': 'kapibedcollege@gmail.com',
        'phone': '0452-2459339',
        'status': 'Pending',
        'notes': 'Verified official portal (kapicoe.org.in), institutional email and phone.'
    },
    'Kapi Women’s College of Education': {
        'website': 'http://www.kapiwcoe.org.in',
        'contact': 'Office of Admissions & Principal (Nagamalai, Madurai)',
        'email': 'kapiwbedcollege@gmail.com',
        'phone': '0452-2459339',
        'status': 'Pending',
        'notes': 'Verified official portal (kapiwcoe.org.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_8_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_8_COLLEGES)}")
    unmatched = set(BATCH_8_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
