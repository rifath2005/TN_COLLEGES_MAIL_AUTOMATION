import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_2_COLLEGES = {
    # Previously verified 38 batch
    'Akshaya College of Education': {
        'website': 'http://www.akshayacollegeofeducation.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'akshayacollegeofeduction@gmail.com',
        'phone': '+91 7010731906',
        'status': 'Pending',
        'notes': 'Verified official portal (akshayacollegeofeducation.com), institutional email and phone.'
    },
    'Al Ameen Arts & Science College': {
        'website': 'https://www.alameeneducation.in',
        'contact': 'Office of the Principal & Admin',
        'email': 'info@alameeneducation.co.in',
        'phone': '+91 97877 29203',
        'status': 'Pending',
        'notes': 'Verified official portal (alameeneducation.in), institutional email and contact.'
    },
    'Al-Ameen College of Education': {
        'website': 'https://www.alameeneducation.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'info@alameeneducation.co.in',
        'phone': '+91 97877 29203',
        'status': 'Pending',
        'notes': 'Verified official portal (alameeneducation.in), institutional email and contact.'
    },
    'Al-Amir College of Education': {
        'website': 'http://alamir.in',
        'contact': 'Office of the Principal',
        'email': 'alamirbededu12@gmail.com',
        'phone': '+91 9489278391',
        'status': 'Pending',
        'notes': 'Verified official portal (alamir.in), institutional email and mobile.'
    },
    'Aladi Aruna College of Liberal Arts and Science': {
        'website': 'https://www.aladiarunaliberalartscollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'aladiarunaliberalarts@gmail.com',
        'phone': '+91 95857 13337',
        'status': 'Pending',
        'notes': 'Verified official portal (aladiarunaliberalartscollege.com), principal email and mobile.'
    },
    'Alagappa Government Arts College': {
        'website': 'https://www.agacollege.in',
        'contact': 'Office of the Principal',
        'email': 'agackkdi@yahoo.com',
        'phone': '04565-224521',
        'status': 'Pending',
        'notes': 'Verified official portal (agacollege.in), office email and telephone.'
    },
    "Al'Ameen Arts & Science College for Women": {
        'website': 'https://www.aascw.in',
        'contact': 'Office of the Principal & Admin',
        'email': 'office@aascw.in',
        'phone': '+91 96262 63356',
        'status': 'Pending',
        'notes': 'Verified official portal (aascw.in), administrative email and helpline.'
    },
    'All Saints College of Education': {
        'website': 'https://allsaintscollegeofeducation.edu.in',
        'contact': 'Office of the Principal',
        'email': 'allsaintscollegeofeducation@gmail.com',
        'phone': '+91 4651 236888',
        'status': 'Pending',
        'notes': 'Verified official portal (allsaintscollegeofeducation.edu.in), email and landline.'
    },
    'Alpha Arts & Science College': {
        'website': 'https://alphagroup.edu/arts-science/',
        'contact': 'Office of Admissions & Principal (Porur Campus)',
        'email': 'aasc@alphagroup.edu',
        'phone': '+91 44 24762368',
        'status': 'Pending',
        'notes': 'Verified official portal (alphagroup.edu), official email and phone.'
    },
    'Alpha Arts & Sci, College': {
        'website': 'https://alphagroup.edu/arts-science/',
        'contact': 'Office of Admissions & Principal (Porur Campus)',
        'email': 'aasc@alphagroup.edu',
        'phone': '+91 44 24762368',
        'status': 'Pending',
        'notes': 'Verified official portal (alphagroup.edu), official email and phone.'
    },
    'Amala College of Education': {
        'website': 'http://bedcollege.amala.ac.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'info@amala.ac.in',
        'phone': '+91 94427 00844',
        'status': 'Pending',
        'notes': 'Verified official portal (amala.ac.in), institutional email and mobile.'
    },
    'Ambai Arts College': {
        'website': 'https://www.ambaiartscollege.org',
        'contact': 'Office of the Principal',
        'email': 'aartscollege@gmail.com',
        'phone': '04634-250375',
        'status': 'Pending',
        'notes': 'Verified official portal (ambaiartscollege.org), institutional email and phone.'
    },
    'Ambari Arts and Science College for Women': {
        'website': 'https://www.ambariartscollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'admissions@ambariartscollege.com',
        'phone': '+91 93634 65475',
        'status': 'Pending',
        'notes': 'Verified official portal (ambariartscollege.com), admissions email and helpline.'
    },
    'Ambiga College of Arts and Science for Women': {
        'website': 'https://ambigacollege.com',
        'contact': 'Office of the Principal',
        'email': 'ambigacollege@gmail.com',
        'phone': '0452-2535613',
        'status': 'Pending',
        'notes': 'Verified official portal (ambigacollege.com), institutional email and phone.'
    },
    'Amirtha College of Education': {
        'website': 'https://amritacetpt.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@amritacetpt.in',
        'phone': '+91 9443626540',
        'status': 'Pending',
        'notes': 'Verified official portal (amritacetpt.in), institutional email and mobile.'
    },
    'Amirtham College of Education': {
        'website': 'https://amirthameducational.org',
        'contact': 'Office of the Principal',
        'email': 'amirthameducation@ymail.com',
        'phone': '+91 98402 47719',
        'status': 'Pending',
        'notes': 'Verified official portal (amirthameducational.org), institutional email and phone.'
    },
    'Amman Arts And Science College': {
        'website': 'http://www.ammanacas.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'ammanartscollege@gmail.com',
        'phone': '+91 9965509185',
        'status': 'Pending',
        'notes': 'Verified official portal (ammanacas.com), institutional email and mobile.'
    },
    'Amman College of Education': {
        'website': 'http://www.ammancolleges.org',
        'contact': 'Office of the Principal',
        'email': 'ammanbedcollege@yahoo.com',
        'phone': '+91 99655 09185',
        'status': 'Pending',
        'notes': 'Verified official portal (ammancolleges.org), institutional email and mobile.'
    },
    'Anand Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120092',
        'contact': 'Office of Administration',
        'email': 'admin@anand-college.com',
        'phone': '+91 9789312200',
        'status': 'Pending',
        'notes': 'Verified institutional email and administrative helpline.'
    },
    'Ananda College': {
        'website': 'https://anandacollege.in',
        'contact': 'Office of the Principal',
        'email': 'anandacollegeoffice@gmail.com',
        'phone': '04561-261412',
        'status': 'Pending',
        'notes': 'Verified official portal (anandacollege.in), institutional office email and phone.'
    },
    'Anandhan Memorial Arts and Science College': {
        'website': 'https://anandhancollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'anandhancollege2024@gmail.com',
        'phone': '+91 94433 79664',
        'status': 'Pending',
        'notes': 'Verified official portal (anandhancollege.com), official email and mobile.'
    },
    'Anbu Arts And Science College': {
        'website': 'https://www.anbu.ac.in',
        'contact': 'Office of the Principal',
        'email': 'anbucollegekpm@gmail.com',
        'phone': '04288-263181',
        'status': 'Pending',
        'notes': 'Verified official portal (anbu.ac.in), institutional email and phone.'
    },
    'ANDAVAR COLLEGE OF EDUCATION': {
        'website': 'http://www.andavarei.org',
        'contact': 'Office of the Principal',
        'email': 'andavarcoe@gmail.com',
        'phone': '04365-245600',
        'status': 'Pending',
        'notes': 'Verified official portal (andavarei.org), institutional email and phone.'
    },
    'Angappa College of Arts and Science': {
        'website': 'https://angappacollege.ac.in',
        'contact': 'Office of the Principal',
        'email': 'principal@angappacollege.ac.in',
        'phone': '0422-2610007',
        'status': 'Pending',
        'notes': 'Verified official portal (angappacollege.ac.in), principal email and phone.'
    },
    'Angel College of Education': {
        'website': 'https://www.acetn.ac.in',
        'contact': 'Office of the Principal',
        'email': 'angelbed2008@gmail.com',
        'phone': '+91 91500-76727',
        'status': 'Pending',
        'notes': 'Verified official portal (acetn.ac.in), official email and helpline.'
    },
    'Angels College of Education': {
        'website': 'https://www.angelsnkl.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'angels.nkl@gmail.com',
        'phone': '04286-266833',
        'status': 'Pending',
        'notes': 'Verified official portal (angelsnkl.org), official email and telephone.'
    },
    'Anna Arivagam College of Education': {
        'website': 'http://www.annaarivagam.com',
        'contact': 'Office of Administration & Principal',
        'email': 'aahsspochampalli@gmail.com',
        'phone': '+91 9443252388',
        'status': 'Pending',
        'notes': 'Verified official portal (annaarivagam.com), institutional email and mobile.'
    },
    'Anna Vinayagar Arts and Science': {
        'website': 'https://www.annavinayagarcollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'annavinayagarartscollege@gmail.com',
        'phone': '+91 94423 66415',
        'status': 'Pending',
        'notes': 'Verified official portal (annavinayagarcollege.com), official email and mobile.'
    },
    'Anna Vinayagar College of Education': {
        'website': 'https://annavinayagaredu.com',
        'contact': 'Office of Leadership & Admissions',
        'email': 'annavinayagar@gmail.com',
        'phone': '04652-252328',
        'status': 'Pending',
        'notes': 'Verified official portal (annavinayagaredu.com), institutional email and phone.'
    },
    'Annai College of Arts and Science': {
        'website': 'https://annaicolleges.com',
        'contact': 'Office of the Principal',
        'email': 'principal@annaicollege.com',
        'phone': '+91 99441 44645',
        'status': 'Pending',
        'notes': 'Verified official portal (annaicolleges.com), principal email and helpline.'
    },
    'Annai College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280017',
        'contact': 'Office of the Principal',
        'email': 'annaice05@yahoo.com',
        'phone': '+91 4292-245484',
        'status': 'Pending',
        'notes': 'Verified institutional email and official phone.'
    },
    'Annai College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280053',
        'contact': 'Office of Leadership & Admissions',
        'email': 'annaicollegetheni@gmail.com',
        'phone': '04554-253162',
        'status': 'Pending',
        'notes': 'Verified institutional email and telephone contact.'
    },
    'Annai Fathima Arts And Science College': {
        'website': 'http://www.annaifathimacollege.edu.in',
        'contact': 'Office of the Principal',
        'email': 'info@annaifathimacollege.edu.in',
        'phone': '04549-284528',
        'status': 'Pending',
        'notes': 'Verified official portal (annaifathimacollege.edu.in), official email and phone.'
    },
    'Annai Fathima College of Education': {
        'website': 'http://www.annaifathimacollege.edu.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'info@annaifathimacollege.edu.in',
        'phone': '+91 82200 08005',
        'status': 'Pending',
        'notes': 'Verified official portal (annaifathimacollege.edu.in), official email and helpline.'
    },
    "Annai Hajira Women's College": {
        'website': 'https://www.annaihajirawomenscollege.ac.in',
        'contact': 'Office of the Principal',
        'email': 'principal@annaihajirawomenscollege.ac.in',
        'phone': '0462-2353066',
        'status': 'Pending',
        'notes': 'Verified official portal (annaihajirawomenscollege.ac.in), principal email and phone.'
    },
    'Annai India College of Education': {
        'website': 'https://www.annaicolleges.in',
        'contact': 'Office of Administration & Admissions',
        'email': 'annaitrustdpi@gmail.com',
        'phone': '+91 94865 77717',
        'status': 'Pending',
        'notes': 'Verified official portal (annaicolleges.in), trust email and mobile.'
    },
    'Annai JKK Sampoorani Ammal College of Education': {
        'website': 'https://jkkm.info',
        'contact': 'Office of Administration (JKK Nattraja Group)',
        'email': 'info@jkkm.net',
        'phone': '+91 8012189135',
        'status': 'Pending',
        'notes': 'Verified official portal (jkkm.info), group email and contact.'
    },
    'Annai Ayesha Arts and Science College': {
        'website': 'https://www.annaiayeshacollege.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@annaiayeshacollege.in',
        'phone': '+91 8144547666',
        'status': 'Pending',
        'notes': 'Verified official portal (annaiayeshacollege.in), institutional email and helpline.'
    },
    'Annai Arts And Science College': {
        'website': 'https://www.annaicolleges.in',
        'contact': 'Office of Administration & Admissions',
        'email': 'annaitrustdpi@gmail.com',
        'phone': '+91 94865 77717',
        'status': 'Pending',
        'notes': 'Verified official portal (annaicolleges.in), trust email and mobile.'
    },

    # Additional early batch items
    'Aavalurpettai Arts & Science College': {
        'website': 'https://www.avalurpetcollege.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@avalurpetcollege.in',
        'phone': '+91 93446 65153',
        'status': 'Pending',
        'notes': 'Verified official portal (avalurpetcollege.in), official email and mobile.'
    },
    'AES College of Arts & Science': {
        'website': 'https://aescollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'Info@aescollege.com',
        'phone': '+91 9043885413',
        'status': 'Pending',
        'notes': 'Verified official portal (aescollege.com), official email and mobile helpline.'
    },
    'Aksheyaa College of Arts and Science': {
        'website': 'https://www.aksheyaacollege.in',
        'contact': 'Office of Admissions & Leadership',
        'email': 'aksheyaaartsscience@gmail.com',
        'phone': '+91 99620 09944',
        'status': 'Pending',
        'notes': 'Verified official portal (aksheyaacollege.in), official email and mobile.'
    },
    'Amritalaya College of Education': {
        'website': 'https://www.amritalayacoe.com',
        'contact': 'Office of Leadership & Admissions',
        'email': 'amritalayace@gmail.com',
        'phone': '+91 94430 36091',
        'status': 'Pending',
        'notes': 'Verified official portal (amritalayacoe.com), official email and mobile.'
    },
    'Pasumpon Muthuramalinga Thevar College': {
        'website': 'https://www.pmtcollege.edu.in',
        'contact': 'Office of the Principal (Melaneelithanallur)',
        'email': 'pmtcollege1970@gmail.com',
        'phone': '+91 9443587152',
        'status': 'Pending',
        'notes': 'Verified official portal (pmtcollege.edu.in), institutional email and mobile.'
    },

    # Batch 46 through 105
    'Annai Katheeja Arts And Science (Women) College': {
        'website': 'https://annaikhadeeja.com',
        'contact': 'Office of the Principal & Admissions (Annai Khadeeja)',
        'email': 'annaikhadeeja2012@gmail.com',
        'phone': '+91 7708901134',
        'status': 'Pending',
        'notes': 'Verified official portal (annaikhadeeja.com), official email and mobile helpline.'
    },
    'Annai Madha College of Education': {
        'website': 'http://www.annaimadhaeducation.com',
        'contact': 'Office of Leadership & Admissions',
        'email': 'annaimadha@gmail.com',
        'phone': '+91 7339210010',
        'status': 'Pending',
        'notes': 'Verified official portal (annaimadhaeducation.com), institutional email and mobile.'
    },
    'ANNAI MATHAMMAL SHEELA COLLEGE OF EDUCATION': {
        'website': 'http://www.amsedu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'amsbednkl@gmail.com',
        'phone': '+91 9442700548',
        'status': 'Pending',
        'notes': 'Verified official portal (amsedu.in), official email and phone.'
    },
    'Annai Meenakshi College of Education': {
        'website': 'https://annaimeenakshicollege.com',
        'contact': 'Office of Admissions & Principal (Puliangudi)',
        'email': 'annaimeenaedu@gmail.com',
        'phone': '+91 9443381380',
        'status': 'Pending',
        'notes': 'Verified official portal (annaimeenakshicollege.com), official email and mobile.'
    },
    'Annai Scholastica Arts and Science College(Women)': {
        'website': 'https://annaischolasticacollege.ac.in',
        'contact': 'Office of the Principal & Admissions (Pamban)',
        'email': 'annaischolasticacollege@gmail.com',
        'phone': '+91 95977 00634',
        'status': 'Pending',
        'notes': 'Verified official portal (annaischolasticacollege.ac.in), official email and mobile.'
    },
    'Annai Teresa College of Education': {
        'website': 'https://www.annaiteresacollegeofedu.com',
        'contact': 'Office of Leadership & Principal (Ariyakudi)',
        'email': 'annaiteresa47@yahoo.com',
        'phone': '04565-221477',
        'status': 'Pending',
        'notes': 'Verified official portal (annaiteresacollegeofedu.com), official email and telephone.'
    },
    'Annai Therasa Arts And Science, College': {
        'website': 'https://atasctkm.com',
        'contact': 'Office of the Principal (Thirukazhukundram)',
        'email': 'atasctkm97@gmail.com',
        'phone': '+91 9384662520',
        'status': 'Pending',
        'notes': 'Verified official portal (atasctkm.com), principal email and mobile.'
    },
    "Annai Veilankanni's College For Women": {
        'website': 'https://avcas.annaiveilankannis.com',
        'contact': 'Office of the Principal & Admissions (Saidapet)',
        'email': 'mail4avc@gmail.com',
        'phone': '+91 92821 44444',
        'status': 'Pending',
        'notes': 'Verified official portal (avcas.annaiveilankannis.com), institutional email and phone.'
    },
    'Annai Veilankannis College of Education': {
        'website': 'https://avced.annaiveilankannis.com',
        'contact': 'Office of Leadership & Admissions (Nedungundram)',
        'email': 'info@annaiveilankannis.com',
        'phone': '+91 9444454222',
        'status': 'Pending',
        'notes': 'Verified official portal (avced.annaiveilankannis.com), institutional email and phone.'
    },
    'Annai Velankanni Arts & Science College': {
        'website': 'https://avasctnj.edu.in',
        'contact': 'Office of the Principal & Admin (Bishop Sundaram Campus)',
        'email': 'info@avasctnj.edu.in',
        'phone': '04362-230434',
        'status': 'Pending',
        'notes': 'Verified official portal (avasctnj.edu.in), official office email and landline.'
    },
    'Annai Velankanni College': {
        'website': 'http://annaicollege.edu.in',
        'contact': 'Office of the Principal (Tholayavattam)',
        'email': 'annaivelankannioffice@gmail.com',
        'phone': '+91 9486935270',
        'status': 'Pending',
        'notes': 'Verified official portal (annaicollege.edu.in), office email and telephone.'
    },
    'Annai Violet Arts & Science College': {
        'website': 'https://violetcollege.in',
        'contact': 'Office of Admissions & Principal (Ambattur)',
        'email': 'annaiviolet@gmail.com',
        'phone': '044-26861611',
        'status': 'Pending',
        'notes': 'Verified official portal (violetcollege.in), institutional email and phone.'
    },
    "Annai Women's College": {
        'website': 'https://www.annaiwomenscollege.com',
        'contact': 'Office of Admissions & Leadership (Punnamchatram)',
        'email': 'annaiwomenskarur@gmail.com',
        'phone': '+91 98424 99576',
        'status': 'Pending',
        'notes': 'Verified official portal (annaiwomenscollege.com), official email and mobile.'
    },
    'Annammal College Of Education For Women': {
        'website': 'https://annammal.org',
        'contact': 'Office of the Principal',
        'email': 'annammals@yahoo.com',
        'phone': '+91 93632 25852',
        'status': 'Pending',
        'notes': 'Verified official portal (annammal.org), institutional email and phone.'
    },
    'ANR Arts and Science College': {
        'website': 'https://www.anrcas.edu.in',
        'contact': 'Office of Administration & Admissions (A.N. Radhakrishnan College)',
        'email': 'admin@anrcas.edu.in',
        'phone': '+91 8939804020',
        'status': 'Pending',
        'notes': 'Verified official portal (anrcas.edu.in), administration email and telephone.'
    },
    'Ansaldo College of Education': {
        'website': 'https://www.ansaldobed.org',
        'contact': 'Office of the Principal (Chetpet)',
        'email': 'ansaldochetpet@gmail.com',
        'phone': '+91 9790091975',
        'status': 'Pending',
        'notes': 'Verified official portal (ansaldobed.org), institutional email and phone.'
    },
    'Anugraha Institute of Social Sciences & Research Centre': {
        'website': 'https://anugrahacollege.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'anugrahacollege.edu@gmail.com',
        'phone': '+91 9487945223',
        'status': 'Pending',
        'notes': 'Verified official portal (anugrahacollege.edu.in), official email and helpline.'
    },
    'APC Mahalaxmi College For Women': {
        'website': 'http://apcmcollege.ac.in',
        'contact': 'Office of the Principal',
        'email': 'principal@apcmcollege.ac.in',
        'phone': '+91 6369673530',
        'status': 'Pending',
        'notes': 'Verified official portal (apcmcollege.ac.in), principal email and helpline.'
    },
    'Apollo Arts and Science College (Co-Ed)': {
        'website': 'https://apolloartsandsciencecollegechennai.ac.in',
        'contact': 'Office of Admissions & Leadership (Guduvanchery)',
        'email': 'info@apolloartsandsciencecollegechennai.ac.in',
        'phone': '+91 90136 12345',
        'status': 'Pending',
        'notes': 'Verified official portal (apolloartsandsciencecollegechennai.ac.in), email and helpline.'
    },
    'Apollo Arts And Science College Chennai': {
        'website': 'https://apolloartsandsciencecollegechennai.ac.in',
        'contact': 'Office of Administration & Principal',
        'email': 'apolloartschennai@gmail.com',
        'phone': '+91 93846 98262',
        'status': 'Pending',
        'notes': 'Verified official portal (apolloartsandsciencecollegechennai.ac.in), email and contact.'
    },
    'Apollo Arts and Science College North Chennai': {
        'website': 'https://apolloartsandsciencecollege.ac.in',
        'contact': 'Office of Admissions (Poonamallee Campus)',
        'email': 'info@apolloartsandsciencecollege.ac.in',
        'phone': '+91 90135 12345',
        'status': 'Pending',
        'notes': 'Verified official portal (apolloartsandsciencecollege.ac.in), email and helpline.'
    },
    'Apollo College of Education': {
        'website': 'https://apollocollegeofeducation.ac.in',
        'contact': 'Office of Leadership & Principal (Sriperumbudur)',
        'email': 'info@apollocollegeofeducation.ac.in',
        'phone': '+91 97899 91522',
        'status': 'Pending',
        'notes': 'Verified official portal (apollocollegeofeducation.ac.in), email and mobile.'
    },
    'Arakkonam Arts and Science College': {
        'website': 'https://www.jaasc.in',
        'contact': 'Office of the Principal (Jaya Arakkonam Arts and Science College)',
        'email': 'akmcollege@gmail.com',
        'phone': '+91 9942990235',
        'status': 'Pending',
        'notes': 'Verified official portal (jaasc.in), college email and phone.'
    },
    'Arasan Ganesan College of Preceptors': {
        'website': 'https://www.agcp.co.in',
        'contact': 'Office of the Principal (Sivakasi)',
        'email': 'agcpsvks@yahoo.in',
        'phone': '+91 9842182235',
        'status': 'Pending',
        'notes': 'Verified official portal (agcp.co.in), institutional email and phone.'
    },
    'Arasu Arts and Science College (Women)': {
        'website': 'https://arasuwomenscollege.com',
        'contact': 'Office of Admissions & Principal (Manmangalam)',
        'email': 'info@arasuwomenscollege.com',
        'phone': '+91 9994300304',
        'status': 'Pending',
        'notes': 'Verified official portal (arasuwomenscollege.com), email and helpline.'
    },
    'ARASU COLLEGE OF EDUCATION FOR WOMEN': {
        'website': 'https://www.arasubed.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'arasucollege@gmail.com',
        'phone': '+91 9367136195',
        'status': 'Pending',
        'notes': 'Verified official portal (arasubed.in), institutional email and phone.'
    },
    'Aravindhar College of Education': {
        'website': 'http://aravindharcollegeofeducation.com',
        'contact': 'Office of the Principal & Admissions (Kalasapakkam)',
        'email': 'aravindharcoe@gmail.com',
        'phone': '+91 9994979968',
        'status': 'Pending',
        'notes': 'Verified official portal (aravindharcollegeofeducation.com), email and phone.'
    },
    'ARC Viswanathan College': {
        'website': 'https://arcviswanathancollege.org',
        'contact': 'Office of the Principal (Sitharkadu)',
        'email': 'arcvc.myl3@gmail.com',
        'phone': '04364-259500',
        'status': 'Pending',
        'notes': 'Verified official portal (arcviswanathancollege.org), email and telephone.'
    },
    'Arcot Lutheran Church College of Education': {
        'website': 'https://alccollegeofeducation.ac.in',
        'contact': 'Office of the Principal (Nellikuppam)',
        'email': 'alc.collegeofeducation@gmail.com',
        'phone': '04142-271550',
        'status': 'Pending',
        'notes': 'Verified official portal (alccollegeofeducation.ac.in), institutional email and phone.'
    },
    "Arcot Sri Mahalakshmi Women's College of Education": {
        'website': 'https://asmwc.in',
        'contact': 'Office of Leadership & Admissions (Villapakkam)',
        'email': 'asmwc.college@gmail.com',
        'phone': '+91 9489316923',
        'status': 'Pending',
        'notes': 'Verified official portal (asmwc.in), institutional email and phone.'
    },
    'Arcot Sri Mahalakshmi Women’s College (Autonomous)': {
        'website': 'https://asmwc.in',
        'contact': 'Office of the Principal & Admissions (Villapakkam)',
        'email': 'asmwc.college@gmail.com',
        'phone': '+91 9489316923',
        'status': 'Pending',
        'notes': 'Verified official portal (asmwc.in), institutional email and phone.'
    },
    'Aries Arts And Science College For Women': {
        'website': 'http://ariescolleges.com',
        'contact': 'Office of Administration & Principal (Vadalur)',
        'email': 'vdl_aries548@yahoo.co.in',
        'phone': '04142-259859',
        'status': 'Pending',
        'notes': 'Verified trust portal (ariescolleges.com), institutional email and phone.'
    },
    'Arignar Anna College': {
        'website': 'https://www.arignarannacollege.com',
        'contact': 'Office of the Principal (Aralvaimozhi)',
        'email': 'anna.college@yahoo.com',
        'phone': '04652-263122',
        'status': 'Pending',
        'notes': 'Verified official portal (arignarannacollege.com), principal email and landline.'
    },
    'ARIGNAR ANNA COLLEGE(ARTS & SCIENCE)': {
        'website': 'https://www.aackrishnagiri.in',
        'contact': 'Office of Admissions & Principal (Polupalli)',
        'email': 'mail@aackrishnagiri.in',
        'phone': '+91 74185 12020',
        'status': 'Pending',
        'notes': 'Verified official portal (aackrishnagiri.in), institutional email and phone.'
    },
    'Arignar Anna Government Arts College': {
        'website': 'http://aagacnkl.edu.in',
        'contact': 'Office of the Principal (Namakkal)',
        'email': 'principal@aagacnkl.edu.in',
        'phone': '04286-266323',
        'status': 'Pending',
        'notes': 'Verified official portal (aagacnkl.edu.in), principal email and telephone.'
    },
    'Arignar Anna Government Arts College For Women': {
        'website': 'https://www.aagacw.com',
        'contact': 'Office of the Principal (Walajapet)',
        'email': 'principalgacwwal@gmail.com',
        'phone': '04172-230813',
        'status': 'Pending',
        'notes': 'Verified official portal (aagacw.com), principal email and telephone.'
    },
    'Arignar Anna Governmet Arts College': {
        'website': 'http://www.aagacattur.org.in',
        'contact': 'Office of the Principal (Attur)',
        'email': 'aagacattur@yahoo.co.in',
        'phone': '04282-235001',
        'status': 'Pending',
        'notes': 'Verified official portal (aagacattur.org.in), institutional email and phone.'
    },
    'Arputha College': {
        'website': 'https://arputhacollege.org',
        'contact': 'Office of the Principal & Admissions (Vamban)',
        'email': 'arputhacollege@gmail.com',
        'phone': '+91 9486259221',
        'status': 'Pending',
        'notes': 'Verified official portal (arputhacollege.org), institutional email and mobile.'
    },
    'Arul Anandar College': {
        'website': 'https://aactni.edu.in',
        'contact': 'Office of the Principal (Autonomous, Karumathur)',
        'email': 'principal@aactni.edu.in',
        'phone': '+91 78457 41893',
        'status': 'Pending',
        'notes': 'Verified official portal (aactni.edu.in), principal email and mobile helpline.'
    },
    'Arul College of Education': {
        'website': 'http://aeteducation.org',
        'contact': 'Office of the Principal (Ulundurpet)',
        'email': 'allimuthu.p@gmail.com',
        'phone': '+91 9003376455',
        'status': 'Pending',
        'notes': 'Verified official portal (aeteducation.org), management email and mobile.'
    },
    'Arulmigu Arthanareeswarar Arts and Science College': {
        'website': 'https://aaasc.ac.in',
        'contact': 'Office of the Principal (Tiruchengode)',
        'email': 'aaascollege2021@gmail.com',
        'phone': '+91 98658 68126',
        'status': 'Pending',
        'notes': 'Verified official portal (aaasc.ac.in), institutional email and mobile.'
    },
    'Arulmigu Kalasalingam College of Education': {
        'website': 'http://www.akceducation.org',
        'contact': 'Office of the Principal (Krishnankoil)',
        'email': 'akceducation@rediffmail.com',
        'phone': '+91 9976644228',
        'status': 'Pending',
        'notes': 'Verified official portal (akceducation.org), institutional email and phone.'
    },
    'Arulmigu Kalasalingam College': {
        'website': 'https://www.akcas.in',
        'contact': 'Office of Admissions & Principal (Krishnankoil)',
        'email': 'akcas_98@yahoo.co.in',
        'phone': '+91 9442164044',
        'status': 'Pending',
        'notes': 'Verified official portal (akcas.in), institutional email and phone.'
    },
    'ARULMIGU KAPALEESWARAR ARTS AND SCIENCE COLLEGE': {
        'website': 'https://akasccollege.edu.in',
        'contact': 'Office of Administration & Principal (Kolathur)',
        'email': 'akascoffice2021@gmail.com',
        'phone': '044-22568848',
        'status': 'Pending',
        'notes': 'Verified official portal (akasccollege.edu.in), institutional email and phone.'
    },
    'Arulmigu Meenakshi Amman College of Education': {
        'website': 'https://www.amacedu.edu.in',
        'contact': 'Office of Admissions & Principal (Uthiramerur)',
        'email': 'admin@amacedu.edu.in',
        'phone': '+91 90420 73453',
        'status': 'Pending',
        'notes': 'Verified official portal (amacedu.edu.in), admin email and mobile.'
    },
    'Arulmigu Palani Andavar Arts College': {
        'website': 'https://www.apcac.edu.in',
        'contact': 'Office of the Principal (Palani)',
        'email': 'apacac_men@yahoo.co.in',
        'phone': '04545-251288',
        'status': 'Pending',
        'notes': 'Verified official portal (apcac.edu.in), institutional email and phone.'
    },
    'ARULMIGU PALANIANDAVAR ARTS AND SCIENCE COLLEGE FOR WOMEN': {
        'website': 'https://www.apacwomen.ac.in',
        'contact': 'Office of the Principal & Helpdesk (Palani)',
        'email': 'apacwprincipal@gmail.com',
        'phone': '04545-255711',
        'status': 'Pending',
        'notes': 'Verified official portal (apacwomen.ac.in), principal email and landline.'
    },
    'Arulmigu Palaniandavar College of Arts and Culture': {
        'website': 'https://www.apcac.edu.in',
        'contact': 'Office of the Principal (Palani)',
        'email': 'apacac_men@yahoo.co.in',
        'phone': '04545-251288',
        'status': 'Pending',
        'notes': 'Verified official portal (apcac.edu.in), institutional email and phone.'
    },
    'Arulmigu Pannirupidi Ayyan College': {
        'website': 'https://www.apacollege.org',
        'contact': 'Office of the Principal & Admissions (Vagaikulam)',
        'email': 'apaprincipal@gmail.com',
        'phone': '+91 75982 19947',
        'status': 'Pending',
        'notes': 'Verified official portal (apacollege.org), principal email and mobile.'
    },
    'Arulmigu Subramania Swamy Arts and Science College': {
        'website': 'https://www.assascollege.org',
        'contact': 'Office of the Principal & Admissions (Vilathikulam)',
        'email': 'assasc.vkm21@gmail.com',
        'phone': '+91 8838689782',
        'status': 'Pending',
        'notes': 'Verified official portal (assascollege.org), official email and mobile.'
    },
    'Arulmigu Subramaniaswamy Government Arts College': {
        'website': 'https://ssgac.ac.in',
        'contact': 'Office of the Principal (Tiruttani)',
        'email': 'pssgactrt@gmail.com',
        'phone': '044-27885212',
        'status': 'Pending',
        'notes': 'Verified official portal (ssgac.ac.in), principal email and phone.'
    },
    'Arumugam Nallamani College of Education': {
        'website': 'http://www.nallamanimadurai.in',
        'contact': 'Office of the Principal (Madurai North)',
        'email': 'nallamanimadurai@gmail.com',
        'phone': '+91 9842136390',
        'status': 'Pending',
        'notes': 'Verified official portal (nallamanimadurai.in), institutional email and mobile.'
    },
    'Arumugam Pillai Seethai Ammal College': {
        'website': 'https://apsacollege.com',
        'contact': 'Office of the Principal (Tiruppattur)',
        'email': 'principal@apsacollege.com',
        'phone': '04577-266142',
        'status': 'Pending',
        'notes': 'Verified official portal (apsacollege.com), principal email and telephone.'
    },
    'Arumugam Pillai Seethai Ammal College of Education': {
        'website': 'https://www.apsacoedu.com',
        'contact': 'Office of Leadership & Admissions (Tiruppattur)',
        'email': 'secretary@apsacoedu.com',
        'phone': '+91 9442265029',
        'status': 'Pending',
        'notes': 'Verified official portal (apsacoedu.com), leadership email and mobile.'
    },
    'Arumugham Palaniguru Arts and Science (Women) College': {
        'website': 'https://apcollege.co.in',
        'contact': 'Office of the Principal (Rajapalayam)',
        'email': 'college@arumuga.com',
        'phone': '+91 98949 35299',
        'status': 'Pending',
        'notes': 'Verified official portal (apcollege.co.in), institutional email and mobile.'
    },
    'Arun College of Education': {
        'website': 'http://aruncedu.org',
        'contact': 'Office of Leadership & Admissions (Vallam)',
        'email': 'aruncedu@gmail.com',
        'phone': '+91 73730 66317',
        'status': 'Pending',
        'notes': 'Verified official portal (aruncedu.org), institutional email and mobile.'
    },
    'Aruna Vidya Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120078',
        'contact': 'Office of Administration & Principal',
        'email': 'vigneshvaran.p@gmail.com',
        'phone': '+91 9677804004',
        'status': 'Pending',
        'notes': 'Verified institutional email and administrative mobile helpline.'
    },
    'Arunachala Arts and Science (Women) College': {
        'website': 'https://www.arunachalaartscollege.com',
        'contact': 'Office of Admissions & Principal (Vellichanthai)',
        'email': 'arunachalaartscollege@gmail.com',
        'phone': '+91 9489672664',
        'status': 'Pending',
        'notes': 'Verified official portal (arunachalaartscollege.com), official email and mobile.'
    }
}

def clean_key(name):
    # Unescape HTML entities first (e.g. &amp;, &#039;)
    n = html.unescape(name).lower()
    # Remove non-alphanumeric
    n = re.sub(r'[^a-z0-9]', '', n)
    return n

def run():
    with open(CONTACTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Initial total rows: {len(rows)}")
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_2_COLLEGES.items()}

    matched_keys = set()
    enriched_count = 0

    for idx, r in enumerate(rows):
        # Fix specific truncated row if needed:
        if r.get('College_Name') == 'P' and '2160006' in r.get('Source_Page_URL', ''):
            r['College_Name'] = 'Pasumpon Muthuramalinga Thevar College, Melaneelithanallur'
            r['City'] = 'Thenkasi'
            r['Official_Website_URL'] = 'https://www.pmtcollege.edu.in'
            r['Department_Or_Contact'] = 'Office of the Principal'
            r['Official_Email'] = 'pmtcollege1970@gmail.com'
            r['Phone_Number'] = '+91 9443587152'
            r['Status'] = 'Pending'
            r['Notes_Or_Error'] = 'Verified official portal (pmtcollege.edu.in), institutional email and mobile.'
            enriched_count += 1
            matched_keys.add('Pasumpon Muthuramalinga Thevar College')
            continue

        c_name = r.get('College_Name', '')
        c_clean = clean_key(c_name)

        matched_item = None
        matched_k_name = None

        if c_clean in clean_map:
            matched_k_name, matched_item = clean_map[c_clean]
        else:
            # Safe substring match: only if length is at least 6 characters
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

    # Write updated rows back
    with open(CONTACTS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully enriched {enriched_count} records in contacts.csv.")
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_2_COLLEGES)}")
    unmatched = set(BATCH_2_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
