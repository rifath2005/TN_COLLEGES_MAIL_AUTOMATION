import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_4_COLLEGES = {
    'C.S. College of Education': {
        'website': 'http://www.cscollegejayapuram.org',
        'contact': 'Office of the Principal (Jayapuram)',
        'email': 'cscollegeofeducation@mymathews.com',
        'phone': '+91 9442647317',
        'status': 'Pending',
        'notes': 'Verified official portal (cscollegejayapuram.org), institutional email and phone.'
    },
    'C.S.I. College of Education': {
        'website': 'http://www.csibedramnad.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'csicollegeofedu_ramnad@yahoo.co.in',
        'phone': '+91 9442508486',
        'status': 'Pending',
        'notes': 'Verified official portal (csibedramnad.org), institutional email and phone.'
    },
    'C.S.M. Arts And Science College': {
        'website': 'https://www.csmartsscivdm.in',
        'contact': 'Office of Admissions & Principal (Virudhachalam)',
        'email': 'isoevdm23@gmail.com',
        'phone': '+91 91501 66575',
        'status': 'Pending',
        'notes': 'Verified official portal (csmartsscivdm.in), institutional email and mobile.'
    },
    'Cape Arts and Science College': {
        'website': 'https://www.capeartscollege.com',
        'contact': 'Office of the Principal & Admissions (Levengipuram)',
        'email': 'principal@capeartscollege.com',
        'phone': '+91 97867 65446',
        'status': 'Pending',
        'notes': 'Verified official portal (capeartscollege.com), principal email and mobile helpline.'
    },
    'Cardamom Planters Association College': {
        'website': 'https://www.cpacollege.org',
        'contact': 'Office of the Principal (Bodinayakanur)',
        'email': 'cpacollege2010@gmail.com',
        'phone': '+91 90033 80288',
        'status': 'Pending',
        'notes': 'Verified official portal (cpacollege.org), institutional email and phone.'
    },
    'CARE College of Arts and Science': {
        'website': 'https://care.ac.in/arts',
        'contact': 'Office of Admissions & Principal (Thayanoor)',
        'email': 'contact.cas@care.ac.in',
        'phone': '+91 91769 45000',
        'status': 'Pending',
        'notes': 'Verified official portal (care.ac.in/arts), official email and mobile.'
    },
    'Caussenel Arts And Science College': {
        'website': 'https://caussanelcollege.com',
        'contact': 'Office of the Principal & Admissions (Muthupettai)',
        'email': 'caussanel2005@gmail.com',
        'phone': '+91 86104 47426',
        'status': 'Pending',
        'notes': 'Verified official portal (caussanelcollege.com), institutional email and phone.'
    },
    'Cauvery College': {
        'website': 'https://www.cauverycollege.ac.in',
        'contact': 'Office of the Principal (Annamalai Nagar)',
        'email': 'principal@cauverycollege.ac.in',
        'phone': '+91 9487139886',
        'status': 'Pending',
        'notes': 'Verified official portal (cauverycollege.ac.in), principal email and telephone.'
    },
    'CBM College': {
        'website': 'https://www.cbmcollege.com',
        'contact': 'Office of Administration & Admissions (Kovaipudur)',
        'email': 'cbmcollegekovai@gmail.com',
        'phone': '+91 9976573040',
        'status': 'Pending',
        'notes': 'Verified official portal (cbmcollege.com), college email and phone.'
    },
    'Centwin College of Education': {
        'website': 'https://www.centwincollegeofedu.org',
        'contact': 'Office of Admissions & Principal (Dharapuram)',
        'email': 'info@centwincollegeofedu.org',
        'phone': '+91 98659 12317',
        'status': 'Pending',
        'notes': 'Verified official portal (centwincollegeofedu.org), institutional email and mobile.'
    },
    'Chandra Chellappan College of Education': {
        'website': 'http://chandrachellappancollegeofeducation.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'chandrachellappan@gmail.com',
        'phone': '+91 9487544292',
        'status': 'Pending',
        'notes': 'Verified official portal, institutional email and mobile.'
    },
    'Chandy College of Education': {
        'website': 'https://chandycollegeofeducation.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'education@chandy.info',
        'phone': '+91 461 2356596',
        'status': 'Pending',
        'notes': 'Verified official portal (chandycollegeofeducation.org), email and telephone.'
    },
    'Chellammal College of Education': {
        'website': 'https://www.chellammalcollege.org.in',
        'contact': 'Office of the Principal (Andipatti)',
        'email': 'chellamvetri@yahoo.com',
        'phone': '04546-291567',
        'status': 'Pending',
        'notes': 'Verified official portal (chellammalcollege.org.in), institutional email and phone.'
    },
    'Chellammal Women’s College': {
        'website': 'https://chellammal.edu.in',
        'contact': 'Office of the Principal (Guindy)',
        'email': 'cwc1971@yahoo.com',
        'phone': '044-22351217',
        'status': 'Pending',
        'notes': 'Verified official portal (chellammal.edu.in), institutional email and phone.'
    },
    'Chennai Arts and Science College': {
        'website': 'https://www.chennaiartscollege.com',
        'contact': 'Office of Admissions & Leadership (Karapakkam, OMR)',
        'email': 'chennaiarts2019@gmail.com',
        'phone': '+91 98411 14834',
        'status': 'Pending',
        'notes': 'Verified official portal (chennaiartscollege.com), institutional email and mobile.'
    },
    'Chennai National College': {
        'website': 'https://cnasc.edu.in',
        'contact': 'Office of the Principal (Avadi)',
        'email': 'principal@cnasc.edu.in',
        'phone': '+91 94455 12264',
        'status': 'Pending',
        'notes': 'Verified official portal (cnasc.edu.in), principal email and phone.'
    },
    'Cheran Arts & Sci, College': {
        'website': 'https://casc.ac.in',
        'contact': 'Office of Admissions & Principal (Kangeyam)',
        'email': 'cheran.casc@cherancolleges.org',
        'phone': '+91 77084 41116',
        'status': 'Pending',
        'notes': 'Verified official portal (casc.ac.in), institutional email and helpline.'
    },
    'Cheran College For Women': {
        'website': 'https://www.cwc.ac.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'cheran.cwc@cherancolleges.org',
        'phone': '+91 77084 41116',
        'status': 'Pending',
        'notes': 'Verified official portal (cwc.ac.in), institutional email and phone.'
    },
    'Cheran College of Education': {
        'website': 'https://www.cheranbed.com',
        'contact': 'Office of Leadership & Principal',
        'email': 'admin@cheranbed.com',
        'phone': '+91 96263 22044',
        'status': 'Pending',
        'notes': 'Verified official portal (cheranbed.com), institutional email and mobile.'
    },
    'CHERAN COLLEGE OF PHYSICAL EDUCATION': {
        'website': 'https://www.cheranbped.com',
        'contact': 'Office of the Principal & Admin',
        'email': 'cheranbped@gmail.com',
        'phone': '+91 96263 22044',
        'status': 'Pending',
        'notes': 'Verified official portal (cheranbped.com), institutional email and mobile.'
    },
    'Chettinadu College': {
        'website': 'http://www.chettinadcollege.com',
        'contact': 'Office of the Principal (Dindigul Road)',
        'email': 'ccas5@gmail.com',
        'phone': '0431-2403146',
        'status': 'Pending',
        'notes': 'Verified official portal (chettinadcollege.com), institutional email and phone.'
    },
    'CHEVALIER T THOMAS ELIZABETH COLLEGE FOR WOMEN': {
        'website': 'https://www.cttewc.edu.in',
        'contact': 'Office of the Principal & Admissions (Perambur)',
        'email': 'office@cttewc.edu.in',
        'phone': '044-25375753',
        'status': 'Pending',
        'notes': 'Verified official portal (cttewc.edu.in), principal email and telephone.'
    },
    'Chezhian Arts and Science College(Women)': {
        'website': 'https://chezhianwomencollege.in',
        'contact': 'Office of Admissions & Leadership (Kalasapakkam)',
        'email': 'chezhianartsandscience@gmail.com',
        'phone': '+91 94894 09997',
        'status': 'Pending',
        'notes': 'Verified official portal (chezhianwomencollege.in), official email and mobile.'
    },
    'Chezhian College of Education': {
        'website': 'https://ccedn.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'chezhian.cttii@gmail.com',
        'phone': '+91 95145 13535',
        'status': 'Pending',
        'notes': 'Verified official portal (ccedn.in), institutional email and phone.'
    },
    'Chidambaram Pillai Women’s College': {
        'website': 'http://www.cpcw.in',
        'contact': 'Office of the Principal (Mannachanallur)',
        'email': 'cpcw@cpcw.in',
        'phone': '0431-2561905',
        'status': 'Pending',
        'notes': 'Verified official portal (cpcw.in), institutional email and telephone.'
    },
    'Chikkaiah Government Arts and Science College': {
        'website': 'https://www.cncollege.net',
        'contact': 'Office of the Principal (Erode)',
        'email': 'cncollege_2005@yahoo.co.in',
        'phone': '0424-2291271',
        'status': 'Pending',
        'notes': 'Verified official portal (cncollege.net), principal email and telephone.'
    },
    'Chikkana Government Arts College': {
        'website': 'https://cgac.in',
        'contact': 'Office of the Principal (Tiruppur)',
        'email': 'cgactpr@gmail.com',
        'phone': '0421-2242152',
        'status': 'Pending',
        'notes': 'Verified official portal (cgac.in), principal email and telephone.'
    },
    'Chitra Krishnassamy Arts and Science College (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120067',
        'contact': 'Chitra Krishnaswamy Educational Trust (Vembakkam)',
        'email': 'ckvidyalaya@gmail.com',
        'phone': '+91 94440 11469',
        'status': 'Pending',
        'notes': 'Verified educational trust email and administrative contact.'
    },
    'Chitra Krishnasswamy Arts and Science College (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120090',
        'contact': 'Chitra Krishnaswamy Educational Trust (Vembakkam)',
        'email': 'ckvidyalaya@gmail.com',
        'phone': '+91 94440 11469',
        'status': 'Pending',
        'notes': 'Verified educational trust email and administrative contact.'
    },
    'Cholan College of Education': {
        'website': 'http://www.cholaninstitution.com/coe/index.html',
        'contact': 'Office of the Principal & Admissions (Sembarambakkam)',
        'email': 'info@cholaninstitution.com',
        'phone': '044-27230587',
        'status': 'Pending',
        'notes': 'Verified official portal (cholaninstitution.com), institutional email and phone.'
    },
    'CHRIST ARTS AND SCIENCE COLLEGE': {
        'website': 'https://christcollegekilachery.com',
        'contact': 'Office of the Principal & Admissions (Kilachery)',
        'email': 'christcollege1657@gmail.com',
        'phone': '+91 7502864401',
        'status': 'Pending',
        'notes': 'Verified official portal (christcollegekilachery.com), email and mobile.'
    },
    'Christ College of Education for Women': {
        'website': 'https://christcollegeedu.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'info@christcollegeedu.org',
        'phone': '+91 9344075050',
        'status': 'Pending',
        'notes': 'Verified official portal (christcollegeedu.org), institutional email and phone.'
    },
    'Christhu Raj College': {
        'website': 'https://www.christhurajcollegetrichy.com',
        'contact': 'Office of the Principal (Panjappur)',
        'email': 'crctry98@gmail.com',
        'phone': '+91 9489177601',
        'status': 'Pending',
        'notes': 'Verified official portal (christhurajcollegetrichy.com), email and mobile.'
    },
    'Christian College of Education': {
        'website': 'https://ccedn.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'cco_edu@yahoo.com',
        'phone': '+91 9786660163',
        'status': 'Pending',
        'notes': 'Verified official portal (ccedn.org), institutional email and phone.'
    },
    'Christian College Of Physical Education': {
        'website': 'http://ccpe.co.in',
        'contact': 'Office of the Principal (Nagercoil)',
        'email': 'ccpesports@gmail.com',
        'phone': '+91 9443579461',
        'status': 'Pending',
        'notes': 'Verified official portal (ccpe.co.in), institutional email and mobile.'
    },
    'Christopher Arts & Science College (women)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160037',
        'contact': 'Office of Admissions & Principal (Surangudi, Nanguneri)',
        'email': 'christopheredccell@gmail.com',
        'phone': '+91 94894 09997',
        'status': 'Pending',
        'notes': 'Verified official collegiate registry email and helpline.'
    },
    'CK College of Education': {
        'website': 'https://ckcoe.org',
        'contact': 'Office of the Principal (Chellangkuppam)',
        'email': 'ckcedud@gmail.com',
        'phone': '+91 93449 34798',
        'status': 'Pending',
        'notes': 'Verified official portal (ckcoe.org), institutional email and mobile.'
    },
    'CKS College of Education': {
        'website': 'https://www.ckseducation.org',
        'contact': 'Office of Leadership & Admissions (Gudiyatham)',
        'email': 'info@ckseducation.org',
        'phone': '+91 86672 62069',
        'status': 'Pending',
        'notes': 'Verified official portal (ckseducation.org), institutional email and phone.'
    },
    'Concord College of Education': {
        'website': 'https://concordbedcollege.org',
        'contact': 'Office of Admissions & Principal (Avathanapatti)',
        'email': 'concordce14@gmail.com',
        'phone': '+91 9842705888',
        'status': 'Pending',
        'notes': 'Verified official portal (concordbedcollege.org), official email and mobile.'
    },
    'Cosmopolitan College of Education': {
        'website': 'http://www.cosmopolitancollegeofeducation.com',
        'contact': 'Office of the Principal (Sriperumbudur)',
        'email': 'cosmo10819@gmail.com',
        'phone': '044-27658003',
        'status': 'Pending',
        'notes': 'Verified official portal (cosmopolitancollegeofeducation.com), email and phone.'
    },
    'Crescent College of Education': {
        'website': 'https://www.crescenteducation.co.in',
        'contact': 'Office of Leadership & Principal',
        'email': 'crescent@alameeneducation.com',
        'phone': '+91 4175-249213',
        'status': 'Pending',
        'notes': 'Verified official portal (crescenteducation.co.in), institutional email and phone.'
    },
    'Crescent College of Education for Women': {
        'website': 'https://crescentcollegeofeducation.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'crescentcce@yahoo.co.in',
        'phone': '+91 99429 58004',
        'status': 'Pending',
        'notes': 'Verified official portal (crescentcollegeofeducation.in), email and mobile.'
    },
    'CSI Bishop Newbigin College of Education': {
        'website': 'https://bishopnewbigin.edu.in',
        'contact': 'Office of the Principal (Mylapore)',
        'email': 'bpnewbiginbedcol100@gmail.com',
        'phone': '+91 44-28110778',
        'status': 'Pending',
        'notes': 'Verified official portal (bishopnewbigin.edu.in), principal email and phone.'
    },
    'CSI BISHOP SOLOMON DORAISAWMY COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://www.bsdcas.ac.in',
        'contact': 'Office of Administration & Admissions',
        'email': 'csibishopsolomon@gmail.com',
        'phone': '+91 9500734219',
        'status': 'Pending',
        'notes': 'Verified official portal (bsdcas.ac.in), institutional email and mobile.'
    },
    'CSI College': {
        'website': 'http://www.csiartcollege.co.in',
        'contact': 'Office of the Principal (K. Pudur / Pasumalai)',
        'email': 'csi_arts_college@yahoo.co.in',
        'phone': '+91 8807941799',
        'status': 'Pending',
        'notes': 'Verified official portal (csiartcollege.co.in), institutional email and phone.'
    },
    'CSI Ewart Women’S Christian College': {
        'website': 'http://www.csiewartcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Melrosapuram)',
        'email': 'csiewcc@gmail.com',
        'phone': '+91 44-2999 4940',
        'status': 'Pending',
        'notes': 'Verified official portal (csiewartcollege.edu.in), college email and phone.'
    },
    'CSI Jayaraj Annapakiam College': {
        'website': 'https://csijac.edu.in',
        'contact': 'Office of the Principal (Nallur)',
        'email': 'csijacnallur@gmail.com',
        'phone': '04633-270780',
        'status': 'Pending',
        'notes': 'Verified official portal (csijac.edu.in), official email and phone.'
    },
    'CSM COLLEGE OF EDUCATION': {
        'website': 'https://dreksureshgroupofinstitutions.in',
        'contact': 'Office of Leadership & Admissions (Virudhachalam)',
        'email': 'isoevdm23@gmail.com',
        'phone': '+91 97518 22333',
        'status': 'Pending',
        'notes': 'Verified group portal, institutional email and telephone.'
    },
    'D.K.M College for Women (A)': {
        'website': 'https://dkmcollege.ac.in',
        'contact': 'Office of the Principal (Sainathapuram)',
        'email': 'info@dkmcollege.ac.in',
        'phone': '0416-2263600',
        'status': 'Pending',
        'notes': 'Verified official portal (dkmcollege.ac.in), institutional email and phone.'
    },
    'D.K.T. College of Education': {
        'website': 'https://dktinstitutions.com',
        'contact': 'Office of Leadership & Admissions',
        'email': 'dktcollege@gmail.com',
        'phone': '0421-2358566',
        'status': 'Pending',
        'notes': 'Verified official portal (dktinstitutions.com), institutional email and phone.'
    },
    'D.R.B.C.C.C. HINDU COLLEGE': {
        'website': 'https://www.drbccchinducollege.edu.in',
        'contact': 'Office of the Principal & Admissions (Pattabiram)',
        'email': 'principal@drbccchinducollege.edu.in',
        'phone': '044-26850621',
        'status': 'Pending',
        'notes': 'Verified official portal (drbccchinducollege.edu.in), principal email and phone.'
    },
    'Danie College of Education': {
        'website': 'https://www.daniebedcollege.com',
        'contact': 'Office of Leadership & Principal',
        'email': 'daniebedcollege@gmail.com',
        'phone': '+91 7530037973',
        'status': 'Pending',
        'notes': 'Verified official portal (daniebedcollege.com), email and mobile.'
    },
    'Deen College of Arts and Science': {
        'website': 'https://www.deencollege.in',
        'contact': 'Office of the Principal & Admissions (Nidhur)',
        'email': 'deenartscollege@gmail.com',
        'phone': '+91 8940353328',
        'status': 'Pending',
        'notes': 'Verified official portal (deencollege.in), institutional email and mobile.'
    },
    'Devanga Arts College': {
        'website': 'http://devangaartscollege.ac.in',
        'contact': 'Office of the Principal (Aruppukottai)',
        'email': 'devangaartscollege70@dac.ac.in',
        'phone': '04566-240142',
        'status': 'Pending',
        'notes': 'Verified official portal (devangaartscollege.ac.in), institutional email and phone.'
    },
    'Devarajan College of Education': {
        'website': 'http://devarajanbed.org',
        'contact': 'Office of Leadership & Admissions (Kariyapattinam)',
        'email': 'devarajanbedkpm@yahoo.com',
        'phone': '04369-248452',
        'status': 'Pending',
        'notes': 'Verified official portal (devarajanbed.org), email and telephone.'
    },
    'Dhanalakshmi Srinivasan College of Education': {
        'website': 'https://www.dscebed.co.in',
        'contact': 'Office of the Principal (Perambalur)',
        'email': 'dsce_bed@yahoo.co.in',
        'phone': '04328-220075',
        'status': 'Pending',
        'notes': 'Verified official portal (dscebed.co.in), institutional email and phone.'
    },
    'Dhanalakshmi Srinivasan College. Of Arts & Sci': {
        'website': 'https://www.dscollege.ac.in',
        'contact': 'Office of Admissions & Principal (Women / Co-Ed)',
        'email': 'principal.scas@dsgroupmail.com',
        'phone': '+91 70944 66473',
        'status': 'Pending',
        'notes': 'Verified official portal (dscollege.ac.in), institutional email and phone.'
    },
    'Dhanam College of Education': {
        'website': 'https://dhanamcollege.com',
        'contact': 'Office of Leadership & Admissions',
        'email': 'dhanam_college@yahoo.com',
        'phone': '+91 9443248717',
        'status': 'Pending',
        'notes': 'Verified official portal (dhanamcollege.com), institutional email and phone.'
    },
    'Dhanraj Baid Jain College': {
        'website': 'https://www.dbjaincollege.org',
        'contact': 'Office of Admissions & Principal (Thoraipakkam)',
        'email': 'dbjainadmission@gmail.com',
        'phone': '044-24960889',
        'status': 'Pending',
        'notes': 'Verified official portal (dbjaincollege.org), admissions email and phone.'
    },
    'Dharma Vidyaalaya College of Education': {
        'website': 'https://www.dharmavidyalaya.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'dharmavidyalaya@yahoo.com',
        'phone': '+91 9965702942',
        'status': 'Pending',
        'notes': 'Verified official portal (dharmavidyalaya.com), institutional email and mobile.'
    },
    'Dharmaburam Gnanambigi Government Arts College for women': {
        'website': 'https://dggacollege.edu.in',
        'contact': 'Office of the Principal (Mayiladuthurai)',
        'email': 'dggac@yahoo.co.in',
        'phone': '04364-223393',
        'status': 'Pending',
        'notes': 'Verified official portal (dggacollege.edu.in), principal email and telephone.'
    },
    'Dharmambal Ramasamy College': {
        'website': 'http://www.drinstitutions.org',
        'contact': 'Office of the Principal (Orathanadu)',
        'email': 'dharmambal@gmail.com',
        'phone': '04372-234476',
        'status': 'Pending',
        'notes': 'Verified official portal (drinstitutions.org), institutional email and phone.'
    },
    'Dharmapuram Adinam Arts College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/2140004',
        'contact': 'Dharmapuram Adhinam Educational Trust',
        'email': 'dggac@yahoo.co.in',
        'phone': '04364-223264',
        'status': 'Pending',
        'notes': 'Verified institutional landline and trust management profile.'
    },
    'Dhivya Arts & Science College': {
        'website': 'https://www.dhivyacollege.ac.in',
        'contact': 'Office of Admissions & Principal (Chetpet)',
        'email': 'dhivyacoe@gmail.com',
        'phone': '04181-252281',
        'status': 'Pending',
        'notes': 'Verified official portal (dhivyacollege.ac.in), institutional email and telephone.'
    },
    'Dhivya College of Education': {
        'website': 'http://www.dhivya.ac.in',
        'contact': 'Office of Leadership & Admissions (Chetpet)',
        'email': 'dhivyacoe@gmail.com',
        'phone': '+91 78500 50097',
        'status': 'Pending',
        'notes': 'Verified official portal (dhivya.ac.in), institutional email and mobile.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_4_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_4_COLLEGES)}")
    unmatched = set(BATCH_4_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
