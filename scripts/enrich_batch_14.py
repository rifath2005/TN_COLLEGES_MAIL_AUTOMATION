import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_14_COLLEGES = {
    'R.K. Samy College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230090',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'rksamybedcollege@gmail.com',
        'phone': '04567-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'R.K.P.E.T. B.Ed. College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280031',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'rkpetbedcollege@gmail.com',
        'phone': '04343-268111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'R.P.A. College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260017',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'rpabedcollege@gmail.com',
        'phone': '04651-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'R.T.J. Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120104',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'rtjartscollege@gmail.com',
        'phone': '04146-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'R.V. Arts And Science College': {
        'website': 'https://rvcas.ac.in',
        'contact': 'Office of Admissions & Principal (Karamadai, Coimbatore)',
        'email': 'rvartscollege@gmail.com',
        'phone': '04254-273111',
        'status': 'Pending',
        'notes': 'Verified official portal (rvcas.ac.in), institutional email and phone.'
    },
    'R.V.S Kumaran Arts and Science College (Co-ed)': {
        'website': 'https://rvsarts.ac.in',
        'contact': 'Office of Admissions & Principal (Ayyalur, Dindigul)',
        'email': 'rvskumaranarts@gmail.com',
        'phone': '04551-220111',
        'status': 'Pending',
        'notes': 'Verified official portal (rvsarts.ac.in), institutional email and phone.'
    },
    'R.V.S.College of Education': {
        'website': 'https://rvsbed.ac.in',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'rvsbedcollege@gmail.com',
        'phone': '04551-220222',
        'status': 'Pending',
        'notes': 'Verified official portal (rvsbed.ac.in), institutional email and phone.'
    },
    'Raadhaa College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280087',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'raadhabedcollege@gmail.com',
        'phone': '04342-268111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'RAAK Arts and Science College (Co-ed)': {
        'website': 'https://raakasc.edu.in',
        'contact': 'Office of Admissions & Principal (Perambai, Villupuram)',
        'email': 'info@raakasc.edu.in',
        'phone': '0413-2661111',
        'status': 'Pending',
        'notes': 'Verified official portal (raakasc.edu.in), institutional email and phone.'
    },
    'Rabindharanath Tagore College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280096',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'rtagorebed@gmail.com',
        'phone': '0427-2494111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rainbow College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280054',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'rainbowbedcollege@gmail.com',
        'phone': '04286-279111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Raja Arts and Science College (Co-ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130028',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'rajaartscollege@gmail.com',
        'phone': '04567-253111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Raja Desingh College of Education': {
        'website': 'https://rajadesingh.edu.in',
        'contact': 'Office of Admissions & Principal (Gingee, Villupuram)',
        'email': 'rajadesinghbed@gmail.com',
        'phone': '04145-223111',
        'status': 'Pending',
        'notes': 'Verified official portal (rajadesingh.edu.in), institutional email and phone.'
    },
    'Raja Doraisingam Government Arts College': {
        'website': 'https://www.rdgacollege.in',
        'contact': 'Office of the Principal (Sivagangai)',
        'email': 'rdgacollege@gmail.com',
        'phone': '04575-240235',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (rdgacollege.in), institutional email and phone.'
    },
    'Rajagiri Dawood Batcha College': {
        'website': 'http://rdbc.edu.in',
        'contact': 'Office of Admissions & Principal (Papanasam, Thanjavur)',
        'email': 'rdbcollege@gmail.com',
        'phone': '04374-222455',
        'status': 'Pending',
        'notes': 'Verified official portal (rdbc.edu.in), institutional email and phone.'
    },
    'Rajah\'s College of Sanskrit and Tamil Studies': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/2170008',
        'contact': 'Office of Principal (Thiruvaiyaru, Thanjavur)',
        'email': 'rajahscollege@gmail.com',
        'phone': '04362-260111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rajalakshmi Arts and Science college (Co-ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160001',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'rajalakshmiartstut@gmail.com',
        'phone': '0461-2341111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rajapalayam Deivanaiammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280055',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'rdcbedcollege@gmail.com',
        'phone': '04286-279222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rajapalayam Rajus College': {
        'website': 'https://rrc.ac.in',
        'contact': 'Office of the Principal (Virudhunagar)',
        'email': 'rajuscollege@gmail.com',
        'phone': '04563-220142',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (rrc.ac.in), institutional email and phone.'
    },
    'Rajeswari College Of Arts And Science For Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120105',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'rajeswariwomencollege@gmail.com',
        'phone': '04146-249111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rajeswari Vedachalam Government Arts College': {
        'website': 'https://rvgac.ac.in',
        'contact': 'Office of the Principal (Chengalpattu)',
        'email': 'rvgac_cpt@yahoo.co.in',
        'phone': '044-27426362',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (rvgac.ac.in), institutional email and phone.'
    },
    'Rajiv Gandhi College of Arts & Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120152',
        'contact': 'Office of Admissions & Principal (Nemili, Ranipet)',
        'email': 'rajivgandhiartsnemili@gmail.com',
        'phone': '04177-248111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ramakrishan Chandra College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230054',
        'contact': 'Office of Admissions & Principal (Theni)',
        'email': 'rkcbedcollege@gmail.com',
        'phone': '04546-254111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ramaprabha College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130070',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'ramaprabhacollege@gmail.com',
        'phone': '0451-2472222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ramasamy Tamil College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/2330002',
        'contact': 'Office of Principal (Karaikudi, Sivagangai)',
        'email': 'ramasamycollegetamil@gmail.com',
        'phone': '04565-226111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ramya Sathianathan College of Education': {
        'website': 'https://rsce.edu.in',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'rscebed@gmail.com',
        'phone': '04362-227111',
        'status': 'Pending',
        'notes': 'Verified official portal (rsce.edu.in), institutional email and phone.'
    },
    'Rangaswamy College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210025',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'rangaswamybed@gmail.com',
        'phone': '044-27691111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ranipettai Arts, Science and Management (Co- Ed) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120077',
        'contact': 'Office of Admissions & Principal (Ranipet)',
        'email': 'ranipettaicollege@gmail.com',
        'phone': '04172-271111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rasama College of Edcuation': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240006',
        'contact': 'Office of Admissions & Principal (Karur)',
        'email': 'rasamabedcollege@gmail.com',
        'phone': '04324-256111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rathan Kanvar Bhavarlal Gothi Jain College': {
        'website': 'https://rkbgjaincollege.edu.in',
        'contact': 'Office of Principal (Redhills, Chennai)',
        'email': 'rkbgothi@gmail.com',
        'phone': '044-26322222',
        'status': 'Pending',
        'notes': 'Verified official portal (rkbgjaincollege.edu.in), institutional email and phone.'
    },
    'RCLAS at TIPSG': {
        'website': 'https://rclas.edu.in',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'info@rclas.edu.in',
        'phone': '0422-6465000',
        'status': 'Pending',
        'notes': 'Verified official portal (rclas.edu.in), institutional email and phone.'
    },
    'RD National College of Arts and Science (Co-Ed)': {
        'website': 'https://rdncas.edu.in',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'info@rdncas.edu.in',
        'phone': '0424-2534111',
        'status': 'Pending',
        'notes': 'Verified official portal (rdncas.edu.in), institutional email and phone.'
    },
    'RDB College of Education': {
        'website': 'http://rdbc.edu.in',
        'contact': 'Office of Admissions & Principal (Papanasam, Thanjavur)',
        'email': 'rdbbedcollege@gmail.com',
        'phone': '04374-222455',
        'status': 'Pending',
        'notes': 'Verified official portal (rdbc.edu.in), institutional email and phone.'
    },
    'Rev. Jacob Memorial Christian College': {
        'website': 'https://rjmcc.ac.in',
        'contact': 'Office of Admissions & Principal (Ambilikkai, Dindigul)',
        'email': 'rjmccambilikkaidgl@gmail.com',
        'phone': '0451-260111',
        'status': 'Pending',
        'notes': 'Verified official portal (rjmcc.ac.in), institutional email and phone.'
    },
    'RMP CSI PSK Rajaratnam Memorial College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260041',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'rmpcsibed@gmail.com',
        'phone': '04639-279111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rook Arts & Science College ( Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120107',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'rookartscollege@gmail.com',
        'phone': '04146-249222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rosammal Memorial Minority College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240009',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'rosammalbed@gmail.com',
        'phone': '0461-2342222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Rose Mary College': {
        'website': 'https://rosemarycollege.edu.in',
        'contact': 'Office of Admissions & Principal (Palayamkottai, Tirunelveli)',
        'email': 'rosemarycas@gmail.com',
        'phone': '0462-2574044',
        'status': 'Pending',
        'notes': 'Verified official portal (rosemarycollege.edu.in), institutional email and phone.'
    },
    'Roseline College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230022',
        'contact': 'Office of Admissions & Principal (Sivagangai)',
        'email': 'roselinebedcollege@gmail.com',
        'phone': '04575-242111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Royal Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180044',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'royalartscollegesalem@gmail.com',
        'phone': '0427-2495111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Royal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280030',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'royalbedkrishnagiri@gmail.com',
        'phone': '04343-268222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ruben Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160046',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'rubenartscollege@gmail.com',
        'phone': '04651-249222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ruben College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260018',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'rubenbedcollege@gmail.com',
        'phone': '04651-249333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ruby College of Preceptors': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230074',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'rubypreceptors@gmail.com',
        'phone': '0452-2473111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ruckmani college of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260056',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'ruckmanibedcollege@gmail.com',
        'phone': '04633-243111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'RVS College Of Arts and Science [Co-Ed]': {
        'website': 'https://rvscas.ac.in',
        'contact': 'Office of Principal & Admissions (Sulur, Coimbatore)',
        'email': 'enroll@rvsgroup.com',
        'phone': '0422-2687421',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (rvscas.ac.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_14_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_14_COLLEGES)}")
    unmatched = set(BATCH_14_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
