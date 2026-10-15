import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_6_COLLEGES = {
    'Fatima College': {
        'website': 'https://www.fatimacollegemdu.org',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@fatimacollegemdu.org',
        'phone': '0452-2668016',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (fatimacollegemdu.org), institutional email and phone.'
    },
    'G. Venkataswamy Naidu College': {
        'website': 'https://www.gvncollege.org',
        'contact': 'Office of the Principal & Admissions (Kovilpatti)',
        'email': 'gvncollegeoffice@gvncollege.edu.in',
        'phone': '+91 83009 20389',
        'status': 'Pending',
        'notes': 'Verified official portal (gvncollege.org), institutional email and phone.'
    },
    'G.E.T. B.Ed College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220023',
        'contact': 'Office of Admissions & Principal (Paradarami)',
        'email': 'getbedcollege@gmail.com',
        'phone': '+91 97876 99040',
        'status': 'Pending',
        'notes': 'Verified official educational registry, institutional email and mobile.'
    },
    'G.K. College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220011',
        'contact': 'Office of the Principal (Cheyyar)',
        'email': 'Not publicly listed from official sources',
        'phone': 'Not publicly listed from official sources',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, contact details not publicly listed from official sources.'
    },
    'G.R.D. College of Education': {
        'website': 'https://www.grdcollege.org',
        'contact': 'Office of Admissions & Leadership',
        'email': 'grdcollege3@gmail.com',
        'phone': '+91 98408 87454',
        'status': 'Pending',
        'notes': 'Verified official portal (grdcollege.org), institutional email and mobile.'
    },
    'G.R.T. College of Education': {
        'website': 'https://www.grtcoe.com',
        'contact': 'Office of Admissions & Principal (Tiruttani)',
        'email': 'grtcoe@grt.edu.in',
        'phone': '+91 89399 92763',
        'status': 'Pending',
        'notes': 'Verified official portal (grtcoe.com), institutional email and mobile.'
    },
    'G.V.C. College of Education': {
        'website': 'http://www.gvccollege.com',
        'contact': 'Office of Admissions & Principal (Arcot)',
        'email': 'gvcbedcollege@gmail.com',
        'phone': '+91 86082 08440',
        'status': 'Pending',
        'notes': 'Verified official portal (gvccollege.com), verified email and mobile.'
    },
    'Ganapathi Seethai Ammal College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/2140003',
        'contact': 'Office of Admissions & Principal (Manamadurai)',
        'email': 'gsa_ganapathi@yahoo.co.in',
        'phone': '04574-261292',
        'status': 'Pending',
        'notes': 'Verified via university affiliation and TNDCE directory, official email and phone.'
    },
    'Ganapathy College of Education': {
        'website': 'https://www.ganapathybed.edu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'principal@ganapathybed.edu.in',
        'phone': '+91 90800 82641',
        'status': 'Pending',
        'notes': 'Verified official portal (ganapathybed.edu.in), principal email and phone.'
    },
    'Gandhi Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150035',
        'contact': 'Office of Admissions & Principal (Sathyamangalam)',
        'email': 'gandhisathy@gmail.com',
        'phone': '+91 94879 96606',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, contact email and mobile.'
    },
    'Gandhi Arts and Science College for women': {
        'website': 'http://www.gandhicollege.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'gandhicas@gmail.com',
        'phone': '+91 98402 89788',
        'status': 'Pending',
        'notes': 'Verified official portal (gandhicollege.ac.in), institutional email and phone.'
    },
    'Gandhi College of Education': {
        'website': 'http://www.gandhiinstitutions.org',
        'contact': 'Office of Admissions & Principal',
        'email': 'gcesathy@gmail.com',
        'phone': '+91 94437 34801',
        'status': 'Pending',
        'notes': 'Verified official portal (gandhiinstitutions.org), institutional email and mobile.'
    },
    'Ganesar Senthamil College': {
        'website': 'https://ganesarcollege.edu.in',
        'contact': 'Office of the Principal & Admissions (Melasivapuri)',
        'email': 'ganesarcollege1909@gmail.com',
        'phone': '04333-247218',
        'status': 'Pending',
        'notes': 'Verified official portal (ganesarcollege.edu.in), institutional email and phone.'
    },
    'Ganesh College of Education': {
        'website': 'http://www.ganeshbedcollege.org',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principalganesh@gmail.com',
        'phone': '0427-2911019',
        'status': 'Pending',
        'notes': 'Verified official portal (ganeshbedcollege.org), principal email and phone.'
    },
    'Geetha Jeevan Arts and Science College': {
        'website': 'https://www.gjasc.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'geethajeevancollege@gmail.com',
        'phone': '+91 94434 82904',
        'status': 'Pending',
        'notes': 'Verified official portal (gjasc.ac.in), institutional email and phone.'
    },
    'GEM Gates Arts And Science College': {
        'website': 'http://www.gemgatescollege.com',
        'contact': 'Office of Admissions & Principal (Attur)',
        'email': 'gemgates05@gmail.com',
        'phone': '+91 75985 58222',
        'status': 'Pending',
        'notes': 'Verified official portal (gemgatescollege.com), verified email and mobile.'
    },
    'Global Arts and Science College (Women)': {
        'website': 'https://globalartscollege.in',
        'contact': 'Office of Admissions & Principal (Veppur)',
        'email': 'globalartscollegevellore@gmail.com',
        'phone': '+91 94431 32622',
        'status': 'Pending',
        'notes': 'Verified official portal (globalartscollege.in), institutional email and mobile.'
    },
    'Global College of Arts and Science (Co-ed)': {
        'website': 'https://gcoas.in',
        'contact': 'Office of Admissions & Principal (Ammaiyappan)',
        'email': 'globalcollegetvr@gmail.com',
        'phone': '+91 93634 65025',
        'status': 'Pending',
        'notes': 'Verified official portal (gcoas.in), institutional email and phone.'
    },
    'Gnanamani College of Education': {
        'website': 'https://gnanamani.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@gnanamani.ac.in',
        'phone': '+91 75982 93888',
        'status': 'Pending',
        'notes': 'Verified official portal (gnanamani.ac.in), institutional email and helpline.'
    },
    'GNANAMANI INTEGRATED COLLEGE OF EDUCATION': {
        'website': 'https://gnanamani.ac.in',
        'contact': 'Office of Admissions & Leadership',
        'email': 'ao@gnanamani.ac.in',
        'phone': '+91 75982 93999',
        'status': 'Pending',
        'notes': 'Verified official portal (gnanamani.ac.in), administrative email and helpline.'
    },
    'Gobi Arts &amp; Science College': {
        'website': 'https://www.gascgobi.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'gobiartscollege@gascgobi.ac.in',
        'phone': '04285-240147',
        'status': 'Pending',
        'notes': 'Verified official portal (gascgobi.ac.in), institutional email and phone.'
    },
    'Gojan College of Teacher Education': {
        'website': 'http://www.teachereducation.gojaneducation.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'neelanrajan8@gmail.com',
        'phone': '044-26311043',
        'status': 'Pending',
        'notes': 'Verified official portal (teachereducation.gojaneducation.com), institutional email and phone.'
    },
    'Gonzaga College ofArts and Science Women': {
        'website': 'https://www.gonzagacollege.edu.in',
        'contact': 'Office of Admissions & Principal (Elathagiri)',
        'email': 'college.gonzaga@gmail.com',
        'phone': '+91 83001 59015',
        'status': 'Pending',
        'notes': 'Verified official portal (gonzagacollege.edu.in), verified email and mobile.'
    },
    'Good Samaritan College of Education': {
        'website': 'https://www.gscedu.org',
        'contact': 'Office of Admissions & Principal (Mayiladuthurai)',
        'email': 'info@gscedu.org',
        'phone': '+91 97897 14002',
        'status': 'Pending',
        'notes': 'Verified official portal (gscedu.org), institutional email and phone.'
    },
    'Good Shepherd College of Education': {
        'website': 'https://www.goodshepherd.ac.in',
        'contact': 'Office of Admissions & Principal (Nagercoil)',
        'email': 'goodshepherdedn@gmail.com',
        'phone': '+91 94425 60433',
        'status': 'Pending',
        'notes': 'Verified official portal (goodshepherd.ac.in), verified email and mobile.'
    },
    'Governent Arts College For Women': {
        'website': 'https://www.gcwk.ac.in',
        'contact': 'Office of the Principal (Kumbakonam)',
        'email': 'principal@gcwk.ac.in',
        'phone': '0435-2420153',
        'status': 'Pending',
        'notes': 'Verified official portal (gcwk.ac.in), principal email and landline.'
    },
    'Government Arts College For Men': {
        'website': 'https://www.gacmenkrishnagiri.org',
        'contact': 'Office of the Principal & Admissions (Krishnagiri)',
        'email': 'principalgacmen@gmail.com',
        'phone': '04343-292270',
        'status': 'Pending',
        'notes': 'Verified official portal (gacmenkrishnagiri.org), principal email and phone.'
    },
    'Government Arts College(Autonomus)': {
        'website': 'https://gacbe.ac.in',
        'contact': 'Office of the Principal & Admissions (Coimbatore)',
        'email': 'govtartscoimbatore18@gmail.com',
        'phone': '0422-2222212',
        'status': 'Pending',
        'notes': 'Verified official portal (gacbe.ac.in), institutional email and phone.'
    },
    'Government College Of Education': {
        'website': 'https://www.gcekpm.ac.in',
        'contact': 'Office of Admissions & Principal (Komarapalayam)',
        'email': 'gcekpm@gmail.com',
        'phone': '04288-260085',
        'status': 'Pending',
        'notes': 'Verified official portal (gcekpm.ac.in), institutional email and phone.'
    },
    'Government College Of Education For Women': {
        'website': 'https://www.gcewcbe.ac.in',
        'contact': 'Office of Admissions & Leadership (Coimbatore)',
        'email': 'gcewcbe@gmail.com',
        'phone': '0422-2397616',
        'status': 'Pending',
        'notes': 'Verified official portal (gcewcbe.ac.in), official college email and phone.'
    },
    'Government Thirumagal Mills College': {
        'website': 'http://www.gtmc.edu.in',
        'contact': 'Office of the Principal & Admissions (Gudiyattam)',
        'email': 'principal@gtmc.edu.in',
        'phone': '04171-220162',
        'status': 'Pending',
        'notes': 'Verified official portal (gtmc.edu.in), principal email and phone.'
    },
    'Governmentt Arts and Science College': {
        'website': 'https://www.gasm.org.in',
        'contact': 'Office of the Principal (Mudukulathur)',
        'email': 'gascmku@gmail.com',
        'phone': '04576-290012',
        'status': 'Pending',
        'notes': 'Verified official portal (gasm.org.in), institutional email and phone.'
    },
    'Govindammal Aditanar College for Women': {
        'website': 'https://www.gacw.in',
        'contact': 'Office of the Principal & Admissions (Tiruchendur)',
        'email': 'gacw@aei.edu.in',
        'phone': '04639-242184',
        'status': 'Pending',
        'notes': 'Verified official portal (gacw.in), verified institutional email and phone.'
    },
    'Govt Arts and Science College': {
        'website': 'https://www.kgasc.co.in',
        'contact': 'Office of Admissions & Principal (Karambakudi)',
        'email': 'principal@kgasc.co.in',
        'phone': '04322-290818',
        'status': 'Pending',
        'notes': 'Verified official portal (kgasc.co.in), principal email and phone.'
    },
    'Grace College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220025',
        'contact': 'Office of Admissions & Principal (Vandavasi)',
        'email': 'Not publicly listed from official sources',
        'phone': '04181-252657',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, contact phone 04181-252657.'
    },
    'Grised Arts & Science College': {
        'website': 'https://christcollegekilachery.com',
        'contact': 'Office of Admissions & Principal (Kilachery)',
        'email': 'christcollege1657@gmail.com',
        'phone': '+91 75028 64401',
        'status': 'Pending',
        'notes': 'Verified official portal (christcollegekilachery.com), institutional email and mobile.'
    },
    'GTN Arts College': {
        'website': 'https://www.gtnartscollege.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'principal@gtnartscollege.ac.in',
        'phone': '+91 73977 83313',
        'status': 'Pending',
        'notes': 'Verified official portal (gtnartscollege.ac.in), principal email and mobile helpline.'
    },
    'Guru Shree Shanthi Vijai Jain College [W]': {
        'website': 'https://gssjcollege.org',
        'contact': 'Office of Admissions & Principal (Vepery)',
        'email': 'gsscollege@gmail.com',
        'phone': '+91 44 25322257',
        'status': 'Pending',
        'notes': 'Verified official portal (gssjcollege.org), college email and phone.'
    },
    'Guru Shree Shanthivijai Jain Arts and Science College': {
        'website': 'https://www.gssjaincollege.in',
        'contact': 'Office of Admissions & Principal (Nellikuppam)',
        'email': 'contactgssjaincollege@gmail.com',
        'phone': '+91 63813 02426',
        'status': 'Pending',
        'notes': 'Verified official portal (gssjaincollege.in), verified email and mobile.'
    },
    'Hajee Karutha Rowther Howdia College': {
        'website': 'https://www.hkrhc.ac.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@hkrhc.ac.in',
        'phone': '04554-265225',
        'status': 'Pending',
        'notes': 'Verified official portal (hkrhc.ac.in), principal email and phone.'
    },
    'Haji S.M.S.Shaik Jalaludeen B.Ed. College': {
        'website': 'https://hajismscollege.org',
        'contact': 'Office of Admissions & Leadership (Adirampattinam)',
        'email': 'smsadirai@gmail.com',
        'phone': '+91 94427 10464',
        'status': 'Pending',
        'notes': 'Verified official portal (hajismscollege.org), contact email and phone.'
    },
    'Hindustan College of Arts And Science': {
        'website': 'https://hcaschennai.edu.in',
        'contact': 'Office of Admissions & Principal (Padur)',
        'email': 'hcasadmin@gmail.com',
        'phone': '+91 97898 85555',
        'status': 'Pending',
        'notes': 'Verified official portal (hcaschennai.edu.in), administration email and helpline.'
    },
    'Hindusthan College of Arts &amp; Science': {
        'website': 'https://www.hicas.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'hicas@hindusthan.net',
        'phone': '+91 98431 33333',
        'status': 'Pending',
        'notes': 'Verified official portal (hicas.ac.in), institutional email and hotline.'
    },
    'Hindusthan College of Education': {
        'website': 'https://www.hindusthan.net',
        'contact': 'Office of Admissions & Leadership',
        'email': 'bed@hindusthan.net',
        'phone': '+91 98431 33333',
        'status': 'Pending',
        'notes': 'Verified official portal (hindusthan.net), institutional email and phone.'
    },
    'Hindusthan College of Science and commerce': {
        'website': 'https://www.hisac.ac.in',
        'contact': 'Office of Admissions & Principal (Ingur)',
        'email': 'admission@hindusthan.net',
        'phone': '+91 90037 53332',
        'status': 'Pending',
        'notes': 'Verified official portal (hisac.ac.in), admissions email and helpline.'
    },
    'Holy Cross Arts &amp; Science College ( Women)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120084',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'hccollege2009@gmail.com',
        'phone': '+91 99940 20309',
        'status': 'Pending',
        'notes': 'Verified official portal & affiliation, institutional email and phone.'
    },
    'Holy Cross College': {
        'website': 'https://www.holycrossngl.edu.in',
        'contact': 'Office of the Principal & Admissions (Nagercoil)',
        'email': 'holycrossngc@yahoo.com',
        'phone': '+91 94421 61473',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (holycrossngl.edu.in), principal email and phone.'
    },
    'Holy Cross College of Education': {
        'website': 'http://www.holycrosscedu.com',
        'contact': 'Office of Admissions & Leadership (Trichy)',
        'email': 'holycrosscedu@gmail.com',
        'phone': '+91 90035 33273',
        'status': 'Pending',
        'notes': 'Verified official portal (holycrosscedu.com), verified email and phone.'
    },
    'Holy Cross Home Science College': {
        'website': 'https://www.hchsc.edu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'hchomesciencecollege@gmail.com',
        'phone': '0461-2328294',
        'status': 'Pending',
        'notes': 'Verified official portal (hchsc.edu.in), institutional email and phone.'
    },
    'Cheiyadu Ammal Arts And Science College': {
        'website': 'https://saasc10.com',
        'contact': 'Office of Admissions & Principal (Syed Ammal)',
        'email': 'info@saasc10.com',
        'phone': '+91 94428 58320',
        'status': 'Pending',
        'notes': 'Verified official portal (saasc10.com), contact email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_6_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_6_COLLEGES)}")
    unmatched = set(BATCH_6_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
