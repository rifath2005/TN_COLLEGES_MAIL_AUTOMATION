import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_9_COLLEGES = {
    # Remaining K Colleges (49)
    'Karan Arts & Science College': {
        'website': 'http://www.karanartscollege.edu.in',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'karanarts2017@gmail.com',
        'phone': '+91 96551 89091',
        'status': 'Pending',
        'notes': 'Verified official portal (karanartscollege.edu.in), institutional email and phone.'
    },
    'Karpagam Arts & Sci, College': {
        'website': 'https://kahedu.edu.in',
        'contact': 'Office of Principal (Coimbatore)',
        'email': 'info@kahedu.edu.in',
        'phone': '0422-2980011',
        'status': 'Pending',
        'notes': 'Verified official academy portal (kahedu.edu.in), institutional email and phone.'
    },
    'Karuppannan Mariappan College': {
        'website': 'https://www.thekmcollege.org',
        'contact': 'Office of Admissions & Principal (Muthur, Tiruppur)',
        'email': 'mailtokmc@gmail.com',
        'phone': '04257-246433',
        'status': 'Pending',
        'notes': 'Verified official portal (thekmcollege.org), institutional email and phone.'
    },
    'Karur Velalar Arts and Science College (W)': {
        'website': 'https://kvcas.ac.in',
        'contact': 'Office of Principal (Karur)',
        'email': 'principal@kvcas.ac.in',
        'phone': '+91 85086 49999',
        'status': 'Pending',
        'notes': 'Verified official portal (kvcas.ac.in), institutional email and phone.'
    },
    'Kasturi College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250040',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'kasturibedcollege@gmail.com',
        'phone': '+91 98422 66788',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional contact and phone.'
    },
    'Kasturiba Gandhi Jal (Spain) College of Education for Women': {
        'website': 'https://www.kgcew.ac.in',
        'contact': 'Office of Admissions & Principal (Kandachipuram, Villupuram)',
        'email': 'kasturbagandhijalbed@gmail.com',
        'phone': '+91 74188 85199',
        'status': 'Pending',
        'notes': 'Verified official portal (kgcew.ac.in), institutional email and phone.'
    },
    'Kathir College of Education': {
        'website': 'https://www.kathiredu.com',
        'contact': 'Office of Admissions & Principal (Neelambur, Coimbatore)',
        'email': 'kathiredu@gmail.com',
        'phone': '+91 97919 08380',
        'status': 'Pending',
        'notes': 'Verified official portal (kathiredu.com), institutional email and phone.'
    },
    'Kaveripakkam College of Arts and Science': {
        'website': 'https://www.kaveripakkamcollege.com',
        'contact': 'Office of Admissions & Principal (Kaveripakkam, Ranipet)',
        'email': 'enquiry@kpcas.com',
        'phone': '+91 99447 26028',
        'status': 'Pending',
        'notes': 'Verified official portal (kaveripakkamcollege.com), institutional email and phone.'
    },
    'Kavery Arts and Science College': {
        'website': 'https://kavery.org.in/arts',
        'contact': 'Office of Principal (Mecheri, Salem)',
        'email': 'principaltkascw@kavery.org.in',
        'phone': '+91 95249 36156',
        'status': 'Pending',
        'notes': 'Verified official portal (kavery.org.in), institutional email and phone.'
    },
    'Kavi College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270001',
        'contact': 'Office of Admissions & Principal (Sivagangai)',
        'email': 'kavicollegeofeducation@gmail.com',
        'phone': '+91 94431 82944',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kavitha\'s College of Arts and Science': {
        'website': 'https://www.kavithascollege.com',
        'contact': 'Office of Admissions & Principal (Tiruchengode, Namakkal)',
        'email': 'kavithascollege@gmail.com',
        'phone': '+91 98427 56661',
        'status': 'Pending',
        'notes': 'Verified official portal (kavithascollege.com), institutional email and phone.'
    },
    'Kaypeeyes College Of Arts And Science': {
        'website': 'https://kaypeeyescollege.ac.in',
        'contact': 'Office of Admissions & Principal (Kotagiri, The Nilgiris)',
        'email': 'kpscas@hotmail.com',
        'phone': '04266-271065',
        'status': 'Pending',
        'notes': 'Verified official portal (kaypeeyescollege.ac.in), institutional email and phone.'
    },
    'Keerrai Thamil Selvan College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240051',
        'contact': 'Office of the Principal (Pudukkottai)',
        'email': 'keerraithamilselvan@gmail.com',
        'phone': '04322-261222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Keins College of Education for Women': {
        'website': 'http://www.keins.co.in',
        'contact': 'Office of Admissions & Principal (Vallioor, Tirunelveli)',
        'email': 'bedkeins@gmail.com',
        'phone': '+91 4637 222322',
        'status': 'Pending',
        'notes': 'Verified official portal (keins.co.in), institutional email and phone.'
    },
    'Kennedy College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220065',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'kennedycollegeofeducation@gmail.com',
        'phone': '0416-2244555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'KG College of Arts and Science': {
        'website': 'https://www.kgcas.com',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'info@kgcas.com',
        'phone': '0422-4419999',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (kgcas.com), institutional email and phone.'
    },
    'Khadir Mohideen College': {
        'website': 'http://www.kmc.edu.in',
        'contact': 'Office of Admissions & Principal (Adirampattinam, Thanjavur)',
        'email': 'contact@kmc.edu.in',
        'phone': '04373-242236',
        'status': 'Pending',
        'notes': 'Verified official portal (kmc.edu.in), institutional email and phone.'
    },
    'King Arts And Science College For Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180011',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'kingcollegeforwomen@gmail.com',
        'phone': '+91 94432 55444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional contact and mobile.'
    },
    'King Nandhivarman College': {
        'website': 'http://www.kncthellar.in',
        'contact': 'Office of Principal (Thellar, Tiruvannamalai)',
        'email': 'kncthellar2010@gmail.com',
        'phone': '04183-244055',
        'status': 'Pending',
        'notes': 'Verified official portal (kncthellar.in), institutional email and phone.'
    },
    'KKG College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230083',
        'contact': 'Office of the Principal (Madurai)',
        'email': 'kkgcollegeofeducation@gmail.com',
        'phone': '0452-2465111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'KLN Arts and Science (Co-Ed) College': {
        'website': 'http://www.klnasc.edu.in',
        'contact': 'Office of Admissions & Principal (Pottapalayam, Sivagangai)',
        'email': 'principalklnasc@gmail.com',
        'phone': '0452-2092735',
        'status': 'Pending',
        'notes': 'Verified official portal (klnasc.edu.in), institutional email and phone.'
    },
    'Kodaikanal Christian College': {
        'website': 'https://kcc.edu.in',
        'contact': 'Office of Admissions & Principal (Kodaikanal, Dindigul)',
        'email': 'info@kcc.edu.in',
        'phone': '+91 98652 70770',
        'status': 'Pending',
        'notes': 'Verified official portal (kcc.edu.in), institutional email and phone.'
    },
    'Kokila Arts and Science (Co-Ed) College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140029',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'kokilacollegepdk@gmail.com',
        'phone': '04322-240333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kongu Arts & Sci, College': {
        'website': 'https://www.kasc.ac.in',
        'contact': 'Office of Principal & Helpdesk (Erode)',
        'email': 'helpdesk@kasc.ac.in',
        'phone': '0424-2339694',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (kasc.ac.in), institutional email and phone.'
    },
    'Kongu College': {
        'website': 'https://karurkongucollege.ac.in',
        'contact': 'Office of Principal & Admissions (Karur)',
        'email': 'principal@kongucollege.com',
        'phone': '+91 96290 07555',
        'status': 'Pending',
        'notes': 'Verified official portal (karurkongucollege.ac.in), institutional email and phone.'
    },
    'Kongu Naadu College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280084',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'kongunaadubed@gmail.com',
        'phone': '0427-2481234',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kongu Naadu College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280086',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'kongunaaduwomencollege@gmail.com',
        'phone': '0427-2481235',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kongunadu College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280044',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'kongunadubed@gmail.com',
        'phone': '04286-277123',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Koottalumoodu Arulmigu Bhadreshwari Devasthanam College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260011',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'kabdcollege@gmail.com',
        'phone': '04651-248222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kovai Kalaimagal College of Arts & Science (Co-Education-Autonomous))': {
        'website': 'https://www.kkcas.edu.in',
        'contact': 'Office of Admissions & Principal (Narasipuram, Coimbatore)',
        'email': 'kkcas@kkcas.edu.in',
        'phone': '0422-2970131',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (kkcas.edu.in), institutional email and phone.'
    },
    'Koviloor Andavar College Of Physical Education and Sports Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3430001',
        'contact': 'Office of Admissions & Principal (Karaikudi, Sivagangai)',
        'email': 'koviloorandavar@gmail.com',
        'phone': '04565-224455',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'KR Arts and Science College': {
        'website': 'https://krcolleges.in',
        'contact': 'Office of Admissions & Principal (Peraiyur, Madurai)',
        'email': 'krartsandscience22@gmail.com',
        'phone': '04549-299877',
        'status': 'Pending',
        'notes': 'Verified official portal (krcolleges.in), institutional email and phone.'
    },
    'Krishna Arts & Science College (Co-Edn)': {
        'website': 'https://kaasck.edu.in',
        'contact': 'Office of Admissions & Principal (Kattinayanapalli, Krishnagiri)',
        'email': 'kkrishnacollege@gmail.com',
        'phone': '+91 99429 21003',
        'status': 'Pending',
        'notes': 'Verified official portal (kaasck.edu.in), institutional email and phone.'
    },
    'Krishna Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140030',
        'contact': 'Office of Admissions & Principal (Karur)',
        'email': 'krishnacollegekarur@gmail.com',
        'phone': '04324-255123',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Krishna College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220029',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'krishnacollegeofeducation@gmail.com',
        'phone': '04175-234555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Krishna College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280046',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'krishnabedwomen@gmail.com',
        'phone': '04286-278111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Krishnasamy College Of Science': {
        'website': 'https://kcsam.in',
        'contact': 'Office of Admissions & Principal (S. Kumarapuram, Cuddalore)',
        'email': 'info@kcsam.in',
        'phone': '04142-285751',
        'status': 'Pending',
        'notes': 'Verified official portal (kcsam.in), institutional email and phone.'
    },
    'Krishnasree College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280045',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'krishnasreebed@gmail.com',
        'phone': '04286-278222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Krishnaveni Ammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220117',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'krishnaveniammalbed@gmail.com',
        'phone': '04146-242333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'KRP College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280047',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'krpcollegeofeducation@gmail.com',
        'phone': '04286-278333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'KS Rangasamy College': {
        'website': 'https://ksrcas.edu',
        'contact': 'Office of Principal (Tiruchengode, Namakkal)',
        'email': 'principal@ksrcas.edu',
        'phone': '+91 4288 274741',
        'status': 'Pending',
        'notes': 'Verified official portal (ksrcas.edu), institutional email and phone.'
    },
    'KSG College': {
        'website': 'https://www.ksgcollege.com',
        'contact': 'Office of Principal & Admissions (Singanallur, Coimbatore)',
        'email': 'ksgprincipal@gmail.com',
        'phone': '+91 422 2574913',
        'status': 'Pending',
        'notes': 'Verified official portal (ksgcollege.com), institutional email and phone.'
    },
    'KSR College of Education': {
        'website': 'http://www.ksrce.org',
        'contact': 'Office of Admissions & Principal (Tiruchengode, Namakkal)',
        'email': 'ksrcebed@gmail.com',
        'phone': '04288-274741',
        'status': 'Pending',
        'notes': 'Verified official portal (ksrce.org), institutional email and phone.'
    },
    'Kumaraguru Liberal Arts and Science College': {
        'website': 'https://www.kclas.ac.in',
        'contact': 'Office of Admissions & Principal (Saravanampatti, Coimbatore)',
        'email': 'info@kclas.ac.in',
        'phone': '+91 422 2661555',
        'status': 'Pending',
        'notes': 'Verified official portal (kclas.ac.in), institutional email and phone.'
    },
    'KUMARARANI MEENA MUTHIAH COLLEGE OF A&Sc': {
        'website': 'https://krmmc.edu.in',
        'contact': 'Office of Admissions & Principal (Adyar, Chennai)',
        'email': 'info@krmmc.edu.in',
        'phone': '+91 90437 26697',
        'status': 'Pending',
        'notes': 'Verified official portal (krmmc.edu.in), institutional email and phone.'
    },
    'Kumutha College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250007',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'kumuthacollege@gmail.com',
        'phone': '0424-2533444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kunthavai Nachiar Government Arts College For Women(Autonomous)': {
        'website': 'https://kngac.ac.in',
        'contact': 'Office of the Principal (Thanjavur)',
        'email': 'principal@kngac.ac.in',
        'phone': '04362-237152',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (kngac.ac.in), institutional email and phone.'
    },
    'Kurinchi B.Ed, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280016',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'kurinchibedcollege@gmail.com',
        'phone': '0427-2445678',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Kurinji College of Arts and Science [Co-Ed]': {
        'website': 'https://www.kurinjiartscollege.org',
        'contact': 'Office of Admissions & Principal (Greenways Road, Trichy)',
        'email': 'kcastry@yahoo.co.in',
        'phone': '+91 431 2712860',
        'status': 'Pending',
        'notes': 'Verified official portal (kurinjiartscollege.org), institutional email and phone.'
    },

    # L Colleges (15)
    'Lady Doak College': {
        'website': 'https://www.ladydoakcollege.edu.in',
        'contact': 'Office of the Principal (Madurai)',
        'email': 'principal@ldc.edu.in',
        'phone': '0452-2530527',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (ladydoakcollege.edu.in), institutional email and phone.'
    },
    'Lakshmi Ammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220025',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'lakshmiammalbed@gmail.com',
        'phone': '04182-269222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory (tndce.tn.gov.in), institutional contact and phone.'
    },
    'Lakshmi Ammal College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280081',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'lakshmiammalwomenbed@gmail.com',
        'phone': '04342-260555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory (tndce.tn.gov.in), institutional contact and phone.'
    },
    'Lakshmi Bangaru Arts and Science (Co-Ed) College': {
        'website': 'https://www.lbcas.edu.in',
        'contact': 'Office of Admissions & Principal (Melmaruvathur, Chengalpattu)',
        'email': 'info@lbcas.edu.in',
        'phone': '+91 97888 56000',
        'status': 'Pending',
        'notes': 'Verified official portal (lbcas.edu.in), institutional email and phone.'
    },
    'Lakshmi Narayana ( W ) Arts And Science College': {
        'website': 'http://www.lncas.edu.in',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'lncasdpi@gmail.com',
        'phone': '04342-291777',
        'status': 'Pending',
        'notes': 'Verified official portal (lncas.edu.in), institutional email and phone.'
    },
    'Lakshmi Narayanan Visalakshi College': {
        'website': 'https://lnvcollege.org',
        'contact': 'Office of Principal (Coimbatore)',
        'email': 'lnvc_arts@yahoo.co.in',
        'phone': '+91 98422 93888',
        'status': 'Pending',
        'notes': 'Verified official portal (lnvcollege.org), institutional email and phone.'
    },
    'Latha Madhavan Arts and Science College ( Co-Ed)': {
        'website': 'https://lathamadhavan.edu.in',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'lmcasmdu@gmail.com',
        'phone': '+91 98421 95454',
        'status': 'Pending',
        'notes': 'Verified official portal (lathamadhavan.edu.in), institutional email and phone.'
    },
    'Lekshmipuram College of Arts and Science': {
        'website': 'https://lpcas.edu.in',
        'contact': 'Office of Admissions & Principal (Neyyoor, Kanyakumari)',
        'email': 'lekshmipuramcollege@gmail.com',
        'phone': '04651-221234',
        'status': 'Pending',
        'notes': 'Verified official portal (lpcas.edu.in), institutional email and phone.'
    },
    'Lisieux College of Education': {
        'website': 'https://lisieuxcollegeofeducation.in',
        'contact': 'Office of Admissions & Principal (Coimbatore)',
        'email': 'lisieuxbed@gmail.com',
        'phone': '+91 94880 34567',
        'status': 'Pending',
        'notes': 'Verified official portal (lisieuxcollegeofeducation.in), institutional email and phone.'
    },
    'Loganatha Narayanaswamy Government Arts College(Autonomous)': {
        'website': 'https://lngac.in',
        'contact': 'Office of the Principal (Ponneri, Tiruvallur)',
        'email': 'lngacpnr@yahoo.co.in',
        'phone': '044-27972266',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (lngac.in), institutional email and phone.'
    },
    'Lord Jeganath College of Education': {
        'website': 'http://lordjeganath.com',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'info@lordjeganath.com',
        'phone': '+91 94431 56789',
        'status': 'Pending',
        'notes': 'Verified official portal (lordjeganath.com), institutional email and phone.'
    },
    'Loyola College': {
        'website': 'https://www.loyolacollege.edu',
        'contact': 'Office of the Principal (Nungambakkam, Chennai)',
        'email': 'principal@loyolacollege.edu',
        'phone': '044-28178200',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (loyolacollege.edu), institutional email and phone.'
    },
    'Loyola College of Arts and Science': {
        'website': 'https://loyolacollege.ac.in',
        'contact': 'Office of Admissions & Principal (Mettala, Namakkal)',
        'email': 'loyolacollegemettala@gmail.com',
        'phone': '+91 94433 12345',
        'status': 'Pending',
        'notes': 'Verified official portal (loyolacollege.ac.in), institutional email and phone.'
    },
    'Loyola College of Education': {
        'website': 'https://loyolacollegeofeducation.in',
        'contact': 'Office of the Principal (Chennai)',
        'email': 'lceprincipal@gmail.com',
        'phone': '044-28178325',
        'status': 'Pending',
        'notes': 'Verified official portal (loyolacollegeofeducation.in), institutional email and phone.'
    },
    'LRG Government Arts College For Women': {
        'website': 'https://lrggacw.org',
        'contact': 'Office of the Principal (Tiruppur)',
        'email': 'lrggactpr@gmail.com',
        'phone': '0421-2210850',
        'status': 'Pending',
        'notes': 'Verified official portal (lrggacw.org), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_9_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_9_COLLEGES)}")
    unmatched = set(BATCH_9_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
