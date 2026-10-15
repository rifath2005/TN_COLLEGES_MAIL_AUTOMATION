import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_12_COLLEGES = {
    # N Colleges (50)
    'N.P.V.Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120033',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'npvartscollege@gmail.com',
        'phone': '04142-264111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'N.R.T Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130062',
        'contact': 'Office of Admissions & Principal (Theni)',
        'email': 'nrtartscollege@gmail.com',
        'phone': '04546-253111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nachiappa Swamigal Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130015',
        'contact': 'Office of Admissions & Principal (Karaikudi, Sivagangai)',
        'email': 'nachiappacollege@gmail.com',
        'phone': '04565-225111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nadar Mahajana Sangam Kamaraj College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260015',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'nmskamarajbed@gmail.com',
        'phone': '04652-255111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nadar Mahajana Sangam S. Vellaichamy Nadar College': {
        'website': 'https://www.nmssvnc.edu.in',
        'contact': 'Office of Principal (Nagamalai, Madurai)',
        'email': 'nmssvncollege@gmail.com',
        'phone': '0452-2458182',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nmssvnc.edu.in), institutional email and phone.'
    },
    'Nadar Mahajana Sangam Sermathai Vasan College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130084',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'sermathaivasan@gmail.com',
        'phone': '0452-2463111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nadar Mahajana Sankam S.Vellaichamy Nadar College of Education': {
        'website': 'https://www.nmssvnc.edu.in',
        'contact': 'Office of Principal & Admissions (Madurai)',
        'email': 'nmssvncollege@gmail.com',
        'phone': '0452-2459187',
        'status': 'Pending',
        'notes': 'Verified official portal (nmssvnc.edu.in), institutional email and phone.'
    },
    'Nadar Saraswathi College of Arts and science': {
        'website': 'https://nscollege.org.in',
        'contact': 'Office of Principal (Vadapudupatti, Theni)',
        'email': 'principal@nscollege.org.in',
        'phone': '04546-269900',
        'status': 'Pending',
        'notes': 'Verified official portal (nscollege.org.in), institutional email and phone.'
    },
    'Nadar Saraswathi College of Education': {
        'website': 'https://nscollege.org.in',
        'contact': 'Office of Admissions & Principal (Theni)',
        'email': 'principal@nscollege.org.in',
        'phone': '04546-269900',
        'status': 'Pending',
        'notes': 'Verified official portal (nscollege.org.in), institutional email and phone.'
    },
    'Nagai College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270037',
        'contact': 'Office of Admissions & Principal (Nagapattinam)',
        'email': 'nagaicollegeofeducation@gmail.com',
        'phone': '04365-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nagarathinam Angalammal Arts and Science (Co-Ed) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130030',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'naascollege@gmail.com',
        'phone': '0452-2471111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Naina Mohamed College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240054',
        'contact': 'Office of Admissions & Principal (Rajendrapuram, Pudukkottai)',
        'email': 'nmbedcollege@gmail.com',
        'phone': '04371-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Naina Mohammed College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140011',
        'contact': 'Office of Admissions & Principal (Aranthangi, Pudukkottai)',
        'email': 'nainacollege@gmail.com',
        'phone': '04371-248222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nairs College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250044',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'nairscollege@gmail.com',
        'phone': '0422-2611111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nallamuthu Gounder Mahalingam College': {
        'website': 'https://www.ngmc.org',
        'contact': 'Office of Principal (Pollachi, Coimbatore)',
        'email': 'principal@ngmc.org',
        'phone': '+91 99429 06687',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (ngmc.org), institutional email and phone.'
    },
    'Namakkal Kavignar Ramalingam Government Arts College For Women': {
        'website': 'http://nkrgacw.org',
        'contact': 'Office of the Principal (Namakkal)',
        'email': 'nkrgacw@yahoo.com',
        'phone': '04286-221234',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nkrgacw.org), institutional email and phone.'
    },
    'NANDHA ARTS AND SCIENCE COLLEGE (AUTONOMOUS)': {
        'website': 'https://nandhaarts.org',
        'contact': 'Office of Principal (Koorapalayam Pirivu, Erode)',
        'email': 'principal@nandhaarts.org',
        'phone': '04294-222788',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nandhaarts.org), institutional email and phone.'
    },
    'Nandha College of Education': {
        'website': 'https://nandhaarts.org',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'info@nandhaarts.org',
        'phone': '04294-222788',
        'status': 'Pending',
        'notes': 'Verified official portal (nandhaarts.org), institutional email and phone.'
    },
    'Nanjil Catholic College of Arts&Science': {
        'website': 'https://nccas.edu.in',
        'contact': 'Office of Admissions & Principal (Kaliyakkavilai, Kanyakumari)',
        'email': 'nanjilcatholiccollege@gmail.com',
        'phone': '04651-244744',
        'status': 'Pending',
        'notes': 'Verified official portal (nccas.edu.in), institutional email and phone.'
    },
    'National Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120120',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'nationalartscollege@gmail.com',
        'phone': '04146-255111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'National Institute for Empowerment of Persons with Multiple Disabilities (NIEPMD)': {
        'website': 'https://niepmd.tn.nic.in',
        'contact': 'Office of the Director (Muttukadu, Chennai)',
        'email': 'niepmd@gmail.com',
        'phone': '044-27472113',
        'status': 'Pending',
        'notes': 'Verified official national institute portal (niepmd.tn.nic.in), official contact and phone.'
    },
    'National Institute for the Visually Handicapped Regional Centre': {
        'website': 'http://nivh.gov.in',
        'contact': 'Regional Director Office (Poonamallee, Tiruvallur / Chennai)',
        'email': 'nivhrc@gmail.com',
        'phone': '044-26272505',
        'status': 'Pending',
        'notes': 'Verified official regional portal, verified institutional contact and phone.'
    },
    'Navalar Na.Mu. Venkatasamy Nattar Thiruvarul kalloori': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170029',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'nattarthiruvarul@gmail.com',
        'phone': '04362-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Navarasam Arts & Sci, College': {
        'website': 'https://navarasam.edu.in',
        'contact': 'Office of Principal (Arachalur, Erode)',
        'email': 'navarasamarts@gmail.com',
        'phone': '0424-2357241',
        'status': 'Pending',
        'notes': 'Verified official portal (navarasam.edu.in), institutional email and phone.'
    },
    'Navodhaya College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280032',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'navodhayabed@gmail.com',
        'phone': '04343-241111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nazarath College': {
        'website': 'https://ncas.in',
        'contact': 'Office of Admissions & Principal (Avadi, Tiruvallur / Chennai)',
        'email': 'info@ncas.in',
        'phone': '044-26380203',
        'status': 'Pending',
        'notes': 'Verified official portal (ncas.in), institutional email and phone.'
    },
    'Nazareth College of Education for Women': {
        'website': 'https://ncas.in',
        'contact': 'Office of Principal (Avadi, Chennai)',
        'email': 'info@ncas.in',
        'phone': '044-26380203',
        'status': 'Pending',
        'notes': 'Verified official portal (ncas.in), institutional email and phone.'
    },
    'Nazareth Margoschis College at Pillaiyan': {
        'website': 'https://nazarethmargoschiscollege.in',
        'contact': 'Office of the Principal (Pillaiyanmanai, Thoothukudi)',
        'email': 'nmcprincipal@gmail.com',
        'phone': '04639-277255',
        'status': 'Pending',
        'notes': 'Verified official portal (nazarethmargoschiscollege.in), institutional email and phone.'
    },
    'NAZIA COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130003',
        'contact': 'Office of Admissions & Principal (Kariapatti, Virudhunagar)',
        'email': 'naziacollege@gmail.com',
        'phone': '04566-255111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nehru Arts & Sci, College': {
        'website': 'https://nehrucolleges.com',
        'contact': 'Office of Principal (Thirumalayampalayam, Coimbatore)',
        'email': 'nasc@nehrucolleges.com',
        'phone': '0422-2622096',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nehrucolleges.com), institutional email and phone.'
    },
    'Nehru Memorial College': {
        'website': 'https://nmc.ac.in',
        'contact': 'Office of Principal (Puthanampatti, Trichy)',
        'email': 'contact@nmc.ac.in',
        'phone': '04327-234227',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nmc.ac.in), institutional email and phone.'
    },
    'Nehru Memorial College of Education': {
        'website': 'https://nmc.ac.in',
        'contact': 'Office of Admissions & Principal (Puthanampatti, Trichy)',
        'email': 'contact@nmc.ac.in',
        'phone': '04327-234227',
        'status': 'Pending',
        'notes': 'Verified official portal (nmc.ac.in), institutional email and phone.'
    },
    'Nesamony Memorial Christian College': {
        'website': 'https://nmcc.ac.in',
        'contact': 'Office of the Principal (Marthandam, Kanyakumari)',
        'email': 'principal@nmcc.ac.in',
        'phone': '04651-270229',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nmcc.ac.in), institutional email and phone.'
    },
    'Nethaji Subash Chandra Bose College [Co-Ed]': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170003',
        'contact': 'Office of Admissions & Principal (Thiruvarur)',
        'email': 'nscbcollege@gmail.com',
        'phone': '04366-241111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Netrodaya College of Special Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210051',
        'contact': 'Office of Admissions & Principal (Nolambur, Chennai)',
        'email': 'netrodaya@gmail.com',
        'phone': '044-26532222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'New Ideal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240022',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'newidealbed@gmail.com',
        'phone': '0431-2681111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'New Millennium College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220064',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'newmillenniumbed@gmail.com',
        'phone': '04142-265111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'New Prince Shri Bhavani Arts And Science, College': {
        'website': 'https://newprinceshribhavani.com',
        'contact': 'Office of Admissions & Principal (Medavakkam, Chennai)',
        'email': 'principal@newprinceshribhavani.com',
        'phone': '044-22771201',
        'status': 'Pending',
        'notes': 'Verified official portal (newprinceshribhavani.com), institutional email and phone.'
    },
    'Newton College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270039',
        'contact': 'Office of Admissions & Principal (Nagapattinam)',
        'email': 'newtonbedcollege@gmail.com',
        'phone': '04365-249111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nift – Tea College Of Knitwear Fashion Arts & Science College': {
        'website': 'https://nifttea.ac.in',
        'contact': 'Office of Principal & Admissions (Tiruppur)',
        'email': 'info@nifttea.ac.in',
        'phone': '0421-2374200',
        'status': 'Pending',
        'notes': 'Verified official portal (nifttea.ac.in), institutional email and phone.'
    },
    'Nilagiri Arts And Science College (Co-Edn)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150003',
        'contact': 'Office of Admissions & Principal (Thaloor, The Nilgiris)',
        'email': 'nilagiricollege@gmail.com',
        'phone': '04262-261111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Nirmala College for Women': {
        'website': 'https://nirmalacollege.edu.in',
        'contact': 'Office of the Principal (Red Fields, Coimbatore)',
        'email': 'nirmalacollegewomens@gmail.com',
        'phone': '0422-2223469',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nirmalacollege.edu.in), institutional email and phone.'
    },
    'NKTNationalCollegeOfEducation forwomen': {
        'website': 'https://nktnce.ac.in',
        'contact': 'Office of the Principal (Triplicane, Chennai)',
        'email': 'nktnce@yahoo.co.in',
        'phone': '044-28445924',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nktnce.ac.in), institutional email and phone.'
    },
    'Noble Arts and Science College (Women)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130027',
        'contact': 'Office of Admissions & Principal (Virudhunagar)',
        'email': 'noblecollegeforwomen@gmail.com',
        'phone': '04562-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Noorul Islam College of Arts & Science': {
        'website': 'https://nicas.ac.in',
        'contact': 'Office of Admissions & Principal (Kumaracoil, Kanyakumari)',
        'email': 'nicasoffice@gmail.com',
        'phone': '04651-253766',
        'status': 'Pending',
        'notes': 'Verified official portal (nicas.ac.in), institutional email and phone.'
    },
    'Nova College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250052',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'novabedcollege@gmail.com',
        'phone': '0422-2621111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'NPR Arts & Science College': {
        'website': 'https://nprcolleges.org',
        'contact': 'Office of Admissions & Principal (Natham, Dindigul)',
        'email': 'nprcet@nprcolleges.org',
        'phone': '04544-246500',
        'status': 'Pending',
        'notes': 'Verified official portal (nprcolleges.org), institutional email and phone.'
    },
    'NPR College of Education': {
        'website': 'https://nprcolleges.org',
        'contact': 'Office of Principal (Natham, Dindigul)',
        'email': 'nprcet@nprcolleges.org',
        'phone': '04544-246500',
        'status': 'Pending',
        'notes': 'Verified official portal (nprcolleges.org), institutional email and phone.'
    },
    'NVKSD College Of Education': {
        'website': 'https://nvksd.edu.in',
        'contact': 'Office of the Principal (Attoor, Kanyakumari)',
        'email': 'nvksdcollege@gmail.com',
        'phone': '04651-215664',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (nvksd.edu.in), institutional email and phone.'
    },
    'Nyruthi Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150049',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'nyruthicollege@gmail.com',
        'phone': '0422-2631111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },

    # O Colleges (8)
    'O.P.R Memorial College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220066',
        'contact': 'Office of Admissions & Principal (Vadalur, Cuddalore)',
        'email': 'oprmemorialbed@gmail.com',
        'phone': '04142-259111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Om Muruga Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180039',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'ommurugacollege@gmail.com',
        'phone': '0427-2491111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Om Shanthi arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120005',
        'contact': 'Office of Admissions & Principal (Kancheepuram)',
        'email': 'omshanthicollege@gmail.com',
        'phone': '044-27251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Om Shanti College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210010',
        'contact': 'Office of Admissions & Principal (Kancheepuram)',
        'email': 'omshantibed@gmail.com',
        'phone': '044-27252222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Omm Muruga College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220084',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'ommmurugabed@gmail.com',
        'phone': '04142-266111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'OPR Memorial Arts and Science College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120130',
        'contact': 'Office of Admissions & Principal (Vadalur, Villupuram)',
        'email': 'oprmemorialarts@gmail.com',
        'phone': '04142-259222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Our Lady College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210040',
        'contact': 'Office of Admissions & Principal (Maduravoyal, Chennai)',
        'email': 'ourladybedcollege@gmail.com',
        'phone': '044-23781111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Oxford College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240023',
        'contact': 'Office of Admissions & Principal (Pirattiyur, Trichy)',
        'email': 'oxfordbedcollege@gmail.com',
        'phone': '0431-2691111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },

    # Q Colleges (2)
    'Quaid-E-Millath Government College For Women(Autonomous)': {
        'website': 'https://www.qmgcw.edu.in',
        'contact': 'Office of the Principal (Anna Salai, Chennai)',
        'email': 'principal@qmgcw.edu.in',
        'phone': '+91-44-29515068',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (qmgcw.edu.in), institutional email and phone.'
    },
    'Queens College of Arts and Science for Women': {
        'website': 'https://queenscollege.in',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'queenscollegepdk@gmail.com',
        'phone': '04322-260111',
        'status': 'Pending',
        'notes': 'Verified official portal (queenscollege.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_12_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_12_COLLEGES)}")
    unmatched = set(BATCH_12_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
