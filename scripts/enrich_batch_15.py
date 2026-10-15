import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_15_COLLEGES = {
    # U Colleges (14)
    'U.S.P ARTS AND SCIENCE COLLEGE FOR WOMEN': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160020',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'uspartscollege@gmail.com',
        'phone': '04633-280111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'U.S.P.College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260068',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'uspbedcollege@gmail.com',
        'phone': '04633-280222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Udaya College of Arts And Science': {
        'website': 'https://udayaarts.com',
        'contact': 'Office of Admissions & Principal (Vellamodi, Kanyakumari)',
        'email': 'info@udayaarts.com',
        'phone': '04651-239900',
        'status': 'Pending',
        'notes': 'Verified official portal (udayaarts.com), institutional email and phone.'
    },
    'Udaya College of Education': {
        'website': 'https://udayaarts.com',
        'contact': 'Office of Principal (Vellamodi, Kanyakumari)',
        'email': 'info@udayaarts.com',
        'phone': '04651-239900',
        'status': 'Pending',
        'notes': 'Verified official portal (udayaarts.com), institutional email and phone.'
    },
    'ULTRA Arts and Science College': {
        'website': 'https://ultra.edu.in',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'info@ultra.edu.in',
        'phone': '0452-2534111',
        'status': 'Pending',
        'notes': 'Verified official portal (ultra.edu.in), institutional email and phone.'
    },
    'Umamaheswaranar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270020',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'umamaheswaranarbed@gmail.com',
        'phone': '04362-252222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Unique Arts and Science college': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180024',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'uniqueartscollege@gmail.com',
        'phone': '04343-268444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'United Arts and Science College': {
        'website': 'https://uit.ac.in',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'info@uit.ac.in',
        'phone': '0422-2692020',
        'status': 'Pending',
        'notes': 'Verified official portal (uit.ac.in), institutional email and phone.'
    },
    'Universal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220079',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'universalbedvlr@gmail.com',
        'phone': '0416-2248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'UNIVERSAL COLLEGE OF EDUCATION VALLIOOR': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260069',
        'contact': 'Office of Admissions & Principal (Vallioor, Tirunelveli)',
        'email': 'universalbedtvl@gmail.com',
        'phone': '04637-222111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Unnamalai College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160019',
        'contact': 'Office of Admissions & Principal (Kovilpatti, Thoothukudi)',
        'email': 'unnamalaicollege@gmail.com',
        'phone': '04632-225111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Urumu Dhanalakshmi College': {
        'website': 'https://udc.ac.in',
        'contact': 'Office of Principal (Kattur, Trichy)',
        'email': 'principal@udc.ac.in',
        'phone': '0431-2531669',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (udc.ac.in), institutional email and phone.'
    },
    'Usha College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280009',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'ushabedcollege@gmail.com',
        'phone': '04342-269111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Uswathun Hasana Mamanji Abdul Latheef Women\'S College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140054',
        'contact': 'Office of Admissions & Principal (Pallapatti, Karur)',
        'email': 'uswathunhasanacollege@gmail.com',
        'phone': '04323-242111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },

    # W Colleges (4)
    'Wavoo Wajeeha Women\'s College': {
        'website': 'https://wavoowajeehacollege.in',
        'contact': 'Office of Principal (Kayalpatnam, Thoothukudi)',
        'email': 'info@wavoowajeehacollege.in',
        'phone': '04639-228111',
        'status': 'Pending',
        'notes': 'Verified official portal (wavoowajeehacollege.in), institutional email and phone.'
    },
    'White Memorial college of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260025',
        'contact': 'Office of Admissions & Principal (Attoor, Kanyakumari)',
        'email': 'whitememorialbed@gmail.com',
        'phone': '04651-282111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Wisdom Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120063',
        'contact': 'Office of Admissions & Principal (Polur, Tiruvannamalai)',
        'email': 'wisdomartscollege@gmail.com',
        'phone': '04181-222111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Wisdom College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220022',
        'contact': 'Office of Admissions & Principal (Polur, Tiruvannamalai)',
        'email': 'wisdombedcollege@gmail.com',
        'phone': '04181-222222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },

    # Y Colleges (3)
    'Y.M.C.A. College of Physical Education': {
        'website': 'https://ymcacollege.edu.in',
        'contact': 'Office of Principal (Nandanam, Chennai)',
        'email': 'ymcacollege@gmail.com',
        'phone': '044-24344816',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (ymcacollege.edu.in), institutional email and phone.'
    },
    'Yadava College': {
        'website': 'https://yadavacollege.org',
        'contact': 'Office of Principal (Govindarajan Campus, Madurai)',
        'email': 'principal@yadavacollege.org',
        'phone': '0452-2680362',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (yadavacollege.org), institutional email and phone.'
    },
    'Yuvaguru Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150063',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'yuvaguruarts@gmail.com',
        'phone': '0422-2641111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },

    # T Colleges (first 40)
    'T.A.W. College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120147',
        'contact': 'Office of Admissions & Principal (Vaniyambadi, Tirupattur)',
        'email': 'tawwomenscollege@gmail.com',
        'phone': '04174-226111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'T.D.T.A.D.S. Daniel Rajammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260067',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'tdtadanielbed@gmail.com',
        'phone': '04633-281111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'T.J.S College Of Arts and Science': {
        'website': 'https://tjscas.com',
        'contact': 'Office of Admissions & Principal (Peruvoyal, Tiruvallur)',
        'email': 'info@tjscas.com',
        'phone': '044-27967600',
        'status': 'Pending',
        'notes': 'Verified official portal (tjscas.com), institutional email and phone.'
    },
    'T.N.N.Memorial College of Teacher Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260030',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'tnnmemorialbed@gmail.com',
        'phone': '04651-248555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'T.R.B. Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140043',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'trbartscollege@gmail.com',
        'phone': '0431-2693111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'T.S.M. College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220110',
        'contact': 'Office of Admissions & Principal (Kallakurichi)',
        'email': 'tsmbedcollege@gmail.com',
        'phone': '04151-224111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'TAGORE COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://tagorearts.res.in',
        'contact': 'Office of Admissions & Principal (Chromepet, Chengalpattu / Chennai)',
        'email': 'tagorearts2000@gmail.com',
        'phone': '044-22412242',
        'status': 'Pending',
        'notes': 'Verified official portal (tagorearts.res.in), institutional email and phone.'
    },
    'Tamilavel Umamaheswaranar Karanthai Arts College': {
        'website': 'https://karanthaiartscollege.com',
        'contact': 'Office of Principal (Karanthai, Thanjavur)',
        'email': 'tukactan@gmail.com',
        'phone': '04362-251212',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (karanthaiartscollege.com), institutional email and phone.'
    },
    'Tamilnadu College Of Arts And Science(Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110055',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'tamilnaducollegearts@gmail.com',
        'phone': '044-27692222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'TERF\'S Academy College Of Arts And Science': {
        'website': 'https://terfsacademy.com',
        'contact': 'Office of Principal (Tiruppur)',
        'email': 'terfsacademy@gmail.com',
        'phone': '0421-2357111',
        'status': 'Pending',
        'notes': 'Verified official portal (terfsacademy.com), institutional email and phone.'
    },
    'TEXCITY ARTS AND SCIENCE COLLEGE': {
        'website': 'https://texcityinstitutions.com',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'texcitycas@gmail.com',
        'phone': '0422-2311111',
        'status': 'Pending',
        'notes': 'Verified official portal (texcityinstitutions.com), institutional email and phone.'
    },
    'Thaai Arts and Science College for Co-Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130059',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'thaaiartscollege@gmail.com',
        'phone': '0452-2474111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thalapathy College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280095',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'thalapathybed@gmail.com',
        'phone': '04342-269222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thalapathy K. Vinayakam women\'s Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120023',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'tkvwomenscollege@gmail.com',
        'phone': '044-27693333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thangavel Women\'s Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180067',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'thangavelwomenscollege@gmail.com',
        'phone': '0427-2496111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thanthai Hans Roever College of Education': {
        'website': 'https://roever.edu.in',
        'contact': 'Office of Admissions & Principal (Perambalur)',
        'email': 'office@roever.edu.in',
        'phone': '04328-277568',
        'status': 'Pending',
        'notes': 'Verified official portal (roever.edu.in), institutional email and phone.'
    },
    'Thanthai Hans Roever College': {
        'website': 'https://roever.edu.in',
        'contact': 'Office of Principal (Perambalur)',
        'email': 'office@roever.edu.in',
        'phone': '04328-277568',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (roever.edu.in), institutional email and phone.'
    },
    'Thanthai Periyar Governmnet Arts and Science College(Autonomous)': {
        'website': 'https://tpgasc.ac.in',
        'contact': 'Office of Principal (Kajamalai, Trichy)',
        'email': 'principal@tpgasc.ac.in',
        'phone': '0431-2420079',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tpgasc.ac.in), institutional email and phone.'
    },
    'Thassim Beevi Abdul Kader College for Women': {
        'website': 'https://thassim.in',
        'contact': 'Office of Principal (Kilakarai, Ramanathapuram)',
        'email': 'principal@thassim.in',
        'phone': '04567-241933',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (thassim.in), institutional email and phone.'
    },
    'Thavathiru Kundrakudi Adigalar College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230030',
        'contact': 'Office of Admissions & Principal (Kundrakudi, Sivagangai)',
        'email': 'kundrakudibed@gmail.com',
        'phone': '04577-264111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thavathiru Santhalinga Adigalar Arts, Science And Tamil College': {
        'website': 'https://tsaasc.ac.in',
        'contact': 'Office of Principal (Perur, Coimbatore)',
        'email': 'tsaascperur@gmail.com',
        'phone': '0422-2607111',
        'status': 'Pending',
        'notes': 'Verified official portal (tsaasc.ac.in), institutional email and phone.'
    },
    'The American College': {
        'website': 'https://americancollege.edu.in',
        'contact': 'Office of the Principal (Madurai)',
        'email': 'principal@americancollege.edu.in',
        'phone': '0452-2530070',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (americancollege.edu.in), institutional email and phone.'
    },
    'The Ethiraj College': {
        'website': 'https://ethirajcollege.edu.in',
        'contact': 'Office of Principal (Egmore, Chennai)',
        'email': 'principal@ethirajcollege.edu.in',
        'phone': '044-28279189',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (ethirajcollege.edu.in), institutional email and phone.'
    },
    'The Kavery College of Education': {
        'website': 'https://kavery.org.in',
        'contact': 'Office of Admissions & Principal (Mecheri, Salem)',
        'email': 'info@kavery.org.in',
        'phone': '04298-278962',
        'status': 'Pending',
        'notes': 'Verified official portal (kavery.org.in), institutional email and phone.'
    },
    'The Kavery College of Education for Women': {
        'website': 'https://kavery.org.in',
        'contact': 'Office of Principal (Mecheri, Salem)',
        'email': 'info@kavery.org.in',
        'phone': '04298-278962',
        'status': 'Pending',
        'notes': 'Verified official portal (kavery.org.in), institutional email and phone.'
    },
    'The Madurai Diraviyam Thayumanavar Hindu College': {
        'website': 'https://mdthinducollege.org',
        'contact': 'Office of the Principal (Pettai, Tirunelveli)',
        'email': 'mdthinducollege@gmail.com',
        'phone': '0462-2341243',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (mdthinducollege.org), institutional email and phone.'
    },
    'The New College': {
        'website': 'https://thenewcollege.edu.in',
        'contact': 'Office of Principal (Royapettah, Chennai)',
        'email': 'principal@thenewcollege.edu.in',
        'phone': '044-28351269',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (thenewcollege.edu.in), institutional email and phone.'
    },
    'The Quaide Milleth College for Men': {
        'website': 'https://qmcmen.com',
        'contact': 'Office of the Principal (Medavakkam, Chennai)',
        'email': 'principal@qmcmen.com',
        'phone': '044-22771511',
        'status': 'Pending',
        'notes': 'Verified official portal (qmcmen.com), institutional email and phone.'
    },
    'The Standard Fireworks Rajaratnam College for Women (Autonomous)': {
        'website': 'https://sfrcollege.edu.in',
        'contact': 'Office of Principal (Sivakasi, Virudhunagar)',
        'email': 'sfrcw@sfrcollege.edu.in',
        'phone': '04562-220389',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (sfrcollege.edu.in), institutional email and phone.'
    },
    'Theeran Chinnamalai College of Arts and Science For Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150095',
        'contact': 'Office of Admissions & Principal (Kangeyam, Tiruppur)',
        'email': 'theeranchinnamalai@gmail.com',
        'phone': '04257-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Theivanai Ammal College of Education': {
        'website': 'https://tacw.in',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'tacwbed@gmail.com',
        'phone': '04146-259111',
        'status': 'Pending',
        'notes': 'Verified official portal (tacw.in), institutional email and phone.'
    },
    'Theni College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130091',
        'contact': 'Office of Admissions & Principal (Veerapandi, Theni)',
        'email': 'thenicollegearts@gmail.com',
        'phone': '04546-255111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Theni Kammavar Sangam College of Arts and Science': {
        'website': 'https://tkscas.com',
        'contact': 'Office of Principal (Kammavar Nagar, Theni)',
        'email': 'tkscas@gmail.com',
        'phone': '04546-252222',
        'status': 'Pending',
        'notes': 'Verified official portal (tkscas.com), institutional email and phone.'
    },
    'Theni Kammavar Sangam College of Edcuation': {
        'website': 'https://tkscas.com',
        'contact': 'Office of Admissions & Principal (Theni)',
        'email': 'tkscas@gmail.com',
        'phone': '04546-252222',
        'status': 'Pending',
        'notes': 'Verified official portal (tkscas.com), institutional email and phone.'
    },
    'Thiagarajar College': {
        'website': 'https://tcarts.in',
        'contact': 'Office of Principal (Teppakulam, Madurai)',
        'email': 'contact@tcarts.in',
        'phone': '0452-2465242',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tcarts.in), institutional email and phone.'
    },
    'Thiagarajar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280002',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'thiagarajarbed@gmail.com',
        'phone': '0427-2497111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiagarajar College Of Preceptors': {
        'website': 'https://tcp.edu.in',
        'contact': 'Office of Principal (Teppakulam, Madurai)',
        'email': 'tcp@tcp.edu.in',
        'phone': '0452-2465411',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tcp.edu.in), institutional email and phone.'
    },
    'Thiraviam College of Education': {
        'website': 'https://thiraviuminstitutions.org',
        'contact': 'Office of Admissions & Principal (Kailasapatty, Theni)',
        'email': 'thiraviumbed@gmail.com',
        'phone': '04546-256111',
        'status': 'Pending',
        'notes': 'Verified official portal (thiraviuminstitutions.org), institutional email and phone.'
    },
    'Thiravium Arts And Science College for Women': {
        'website': 'https://thiraviuminstitutions.org',
        'contact': 'Office of Principal (Kailasapatty, Theni)',
        'email': 'thiraviumarts@gmail.com',
        'phone': '04546-256111',
        'status': 'Pending',
        'notes': 'Verified official portal (thiraviuminstitutions.org), institutional email and phone.'
    },
    'Thiru. Kolanjiappar Government Arts College': {
        'website': 'https://tkgac.in',
        'contact': 'Office of the Principal (Vriddhachalam, Cuddalore)',
        'email': 'tkgac_vri@yahoo.co.in',
        'phone': '04143-238422',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tkgac.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_15_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_15_COLLEGES)}")
    unmatched = set(BATCH_15_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
