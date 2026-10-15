import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_3_COLLEGES = {
    'A.C.R Arts and Science College for Women': {
        'website': 'https://www.drmgrcarts.edu.in',
        'contact': 'Office of Admissions & Leadership (Arni Campus)',
        'email': 'drmgrcartsprincipal@gmail.com',
        'phone': '04173-228375',
        'status': 'Pending',
        'notes': 'Verified institutional office (Chockalingam / ACR Group), official email and phone.'
    },
    'A.V.P. College of Arts & Science': {
        'website': 'https://www.avpcas.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'avpcollegetirupur@gmail.com',
        'phone': '+91 72006 77755',
        'status': 'Pending',
        'notes': 'Verified official portal (avpcas.edu.in), principal email and mobile helpline.'
    },
    'Annai Arts & Sci [Co-Ed]': {
        'website': 'https://annaicolleges.com',
        'contact': 'Office of the Principal (Kumbakonam)',
        'email': 'principal@annaicollege.com',
        'phone': '+91 99441 44645',
        'status': 'Pending',
        'notes': 'Verified official portal (annaicolleges.com), principal email and helpline.'
    },
    'Annai Therasa Arts & Science College': {
        'website': 'https://atasctkm.com',
        'contact': 'Office of the Principal (Thirukazhukundram / Salem Extension)',
        'email': 'atasctkm97@gmail.com',
        'phone': '+91 9384662520',
        'status': 'Pending',
        'notes': 'Verified official portal (atasctkm.com), principal email and mobile.'
    },
    'Aravindar Arts And Science College (Co-Edn)': {
        'website': 'http://aravindharcollegeofeducation.com',
        'contact': 'Office of the Principal & Admissions (Kalasapakkam)',
        'email': 'aravindharcoe@gmail.com',
        'phone': '+91 9994979968',
        'status': 'Pending',
        'notes': 'Verified educational trust portal, official email and mobile.'
    },
    'Arunachala College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280036',
        'contact': 'Office of Leadership & Admissions',
        'email': 'arunachalacollege@gmail.com',
        'phone': '+91 9244900191',
        'status': 'Pending',
        'notes': 'Verified institutional email and contact helpline.'
    },
    'Arunai College of Education': {
        'website': 'https://www.arunaibedtvm.in',
        'contact': 'Office of the Principal (Pallikonda Pattu)',
        'email': 'arunaibedcollege@gmail.com',
        'phone': '04175-298026',
        'status': 'Pending',
        'notes': 'Verified official portal (arunaibedtvm.in), official email and phone.'
    },
    'Arunamalai College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280037',
        'contact': 'Office of the Principal (Mannargudi)',
        'email': 'arunamalai.bed@gmail.com',
        'phone': '+91 9442402156',
        'status': 'Pending',
        'notes': 'Verified institutional email and official phone.'
    },
    'Arungarai Amman Arts And Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140026',
        'contact': 'Office of the Principal (Chinna Dharapuram)',
        'email': 'aacas@rediffmail.com',
        'phone': '+91 94432 37320',
        'status': 'Pending',
        'notes': 'Verified institutional email and administrative contact.'
    },
    'Asan Arts and Science college (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140034',
        'contact': 'Office of the Principal & Admissions (Sukkaliyur)',
        'email': 'acaaskarur@gmail.com',
        'phone': '+91 84285 08090',
        'status': 'Pending',
        'notes': 'Verified university affiliation email and mobile helpline.'
    },
    'Asan Memorial College': {
        'website': 'https://amcas.in',
        'contact': 'Office of Admissions & Principal (Jaladampet)',
        'email': 'info.amcas@asaneducation.com',
        'phone': '+91 93848 23699',
        'status': 'Pending',
        'notes': 'Verified official portal (amcas.in), institutional email and phone.'
    },
    'ASSEFA COLLEGE OF EDUCATION': {
        'website': 'http://www.assefa-sss.org',
        'contact': 'Office of Leadership & Admissions (Peraiyur)',
        'email': 'sssassefa@sancharnet.in',
        'phone': '+91 9942518393',
        'status': 'Pending',
        'notes': 'Verified official trust portal (assefa-sss.org), official email and phone.'
    },
    'Athoor Cooperative Arts and Science College': {
        'website': 'http://www.tncu.tn.gov.in',
        'contact': 'Tamil Nadu Cooperative Union (TNCU Admin Desk)',
        'email': 'tncu.chennai@gmail.com',
        'phone': '044-28364843',
        'status': 'Pending',
        'notes': 'Unit of Tamil Nadu Cooperative Union (TNCU). Direct campus contact routed via TNCU headquarters.'
    },
    'Auxilium Arts and Science College for Women': {
        'website': 'https://www.aascw.ac.in',
        'contact': 'Office of Admissions & Principal (Chittampatti)',
        'email': 'info@aascw.ac.in',
        'phone': '+91 94878 42386',
        'status': 'Pending',
        'notes': 'Verified official portal (aascw.ac.in), institutional email and mobile.'
    },
    'Auxilium College Of Arts And Science': {
        'website': 'http://www.auxiliumcollege.ac.in',
        'contact': 'Office of the Principal & Admissions (Regunathapuram)',
        'email': 'auxiregu@gmail.com',
        'phone': '+91 9487842387',
        'status': 'Pending',
        'notes': 'Verified official portal (auxiliumcollege.ac.in), official email and phone.'
    },
    'Auxilium College of Education': {
        'website': 'https://www.auxiliumbedvellore.edu.in',
        'contact': 'Office of the Principal (Katpadi)',
        'email': 'vlrauxiliumbed12@gmail.com',
        'phone': '+91 9342213916',
        'status': 'Pending',
        'notes': 'Verified official portal (auxiliumbedvellore.edu.in), email and mobile.'
    },
    'Auxilium College of Education for Women': {
        'website': 'http://acer.edu.in',
        'contact': 'Office of Leadership & Admissions (Regunathapuram)',
        'email': 'auxiliumed@gmail.com',
        'phone': '04322-254355',
        'status': 'Pending',
        'notes': 'Verified official portal (acer.edu.in), official email and landline.'
    },
    'Avalurpet Arts and Science College': {
        'website': 'https://www.avalurpetcollege.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'info@avalurpetcollege.in',
        'phone': '+91 93446 65153',
        'status': 'Pending',
        'notes': 'Verified official portal (avalurpetcollege.in), official email and phone.'
    },
    'Avichi Arts and Science College': {
        'website': 'https://avichicollege.edu.in',
        'contact': 'Office of Admissions & Principal (Virugambakkam)',
        'email': 'admissions@avichicollege.edu.in',
        'phone': '+91 9600164070',
        'status': 'Pending',
        'notes': 'Verified official portal (avichicollege.edu.in), admissions email and contact.'
    },
    'Avinasi Gounder Mariammal College of Education': {
        'website': 'http://www.agmcoe.ac.in',
        'contact': 'Office of the Principal (Kollampalayam)',
        'email': 'agmcoe@gmail.com',
        'phone': '0424-2401078',
        'status': 'Pending',
        'notes': 'Verified official portal (agmcoe.ac.in), institutional email and phone.'
    },
    'AVS Arts and Science (Co-Ed) College': {
        'website': 'https://www.avscollege.ac.in',
        'contact': 'Office of the Principal (Ramalingapuram)',
        'email': 'principal@avscollege.ac.in',
        'phone': '+91 94427 00205',
        'status': 'Pending',
        'notes': 'Verified official portal (avscollege.ac.in), principal email and mobile.'
    },
    'AVS COLLEGE OF ARTS & SCIENCE(AUTONOMOUS)': {
        'website': 'https://www.avscollege.ac.in',
        'contact': 'Office of Admissions & Leadership (Ramalingapuram)',
        'email': 'principal@avscollege.ac.in',
        'phone': '+91 94427 00205',
        'status': 'Pending',
        'notes': 'Verified official portal (avscollege.ac.in), principal email and mobile.'
    },
    'Ayira Vaisya College of Education': {
        'website': 'http://www.avbedpmk.com',
        'contact': 'Office of the Principal (Paramakudi)',
        'email': 'avbed11701@gmail.com',
        'phone': '+91 7539944994',
        'status': 'Pending',
        'notes': 'Verified official portal (avbedpmk.com), institutional email and phone.'
    },
    'Ayya Nadar Janaki Ammal College (Autonomous)': {
        'website': 'http://www.anjaconline.org',
        'contact': 'Office of the Principal (Sivakasi)',
        'email': 'principal@anjaconline.org',
        'phone': '04562-254100',
        'status': 'Pending',
        'notes': 'Verified official portal (anjaconline.org), principal email and phone.'
    },
    'Ayyan Thiruvalluvar Arts & Sci, College [Co-Ed]': {
        'website': 'https://atcas.in',
        'contact': 'Office of Admissions & Principal (Punjai Puliampatti)',
        'email': 'ayyanthiruvalluvarcollege@gmail.com',
        'phone': '+91 95853 36000',
        'status': 'Pending',
        'notes': 'Verified official portal (atcas.in), institutional email and mobile.'
    },
    'B.Padmanabha Jeyanthimala College': {
        'website': 'https://bpjcollege.com',
        'contact': 'Office of the Principal & Admissions (Srimushnam)',
        'email': 'bpjcollegesrm@gmail.com',
        'phone': '+91 81899 99519',
        'status': 'Pending',
        'notes': 'Verified official portal (bpjcollege.com), college email and mobile.'
    },
    'B.T.K. College of Education': {
        'website': 'http://www.btkbed.com',
        'contact': 'Office of the Principal (Viralimalai)',
        'email': 'btkbedcollege@yahoo.in',
        'phone': '+91 9047668049',
        'status': 'Pending',
        'notes': 'Verified official portal (btkbed.com), institutional email and phone.'
    },
    'Balagan Saraswathi Arts and Science Women College': {
        'website': 'https://balagansaraswathicollege.edu.in',
        'contact': 'Office of Administration & Principal (Mukkudal)',
        'email': 'admin@balagansaraswathiinstitution.org',
        'phone': '04634-213319',
        'status': 'Pending',
        'notes': 'Verified official portal (balagansaraswathicollege.edu.in), email and telephone.'
    },
    'Bapuji Memorial College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280041',
        'contact': 'NOVA Educational Trust / Campus Office',
        'email': 'bapujicollegebed@gmail.com',
        'phone': '04651-237774',
        'status': 'Pending',
        'notes': 'Verified institutional landline and campus management profile.'
    },
    'Best Arts And Science College': {
        'website': 'http://bestcollegesirkali.com',
        'contact': 'Office of Admissions & Principal (Sirkali)',
        'email': 'bestcollegesirkali@gmail.com',
        'phone': '+91 9489177264',
        'status': 'Pending',
        'notes': 'Verified official portal (bestcollegesirkali.com), institutional email and mobile.'
    },
    'Best College of Education': {
        'website': 'http://bcedu.in',
        'contact': 'Office of the Principal (Ayoob Trust)',
        'email': 'estcemyl@gmail.com',
        'phone': '04364-249115',
        'status': 'Pending',
        'notes': 'Verified official portal (bcedu.in), institutional email and phone.'
    },
    'Bethany Navajeevan College of Education': {
        'website': 'https://www.bethanycollegeofeducation.edu.in',
        'contact': 'Office of Leadership & Principal (Vencode)',
        'email': 'bethanynavajeevanb.ed@gmail.com',
        'phone': '+91 94867 60044',
        'status': 'Pending',
        'notes': 'Verified official portal (bethanycollegeofeducation.edu.in), official email and mobile.'
    },
    'Bethesda College of Education': {
        'website': 'https://www.bethesda-education.org',
        'contact': 'Office of the Principal (Bethelpuram)',
        'email': 'bethesdacollegeb.ed@gmail.com',
        'phone': '+91 94423 65761',
        'status': 'Pending',
        'notes': 'Verified official portal (bethesda-education.org), email and mobile.'
    },
    'Bethlahem College of Education': {
        'website': 'https://www.bethlahem-bed.org',
        'contact': 'Office of Admissions & Principal (Karungal)',
        'email': 'bethlahem05@yahoo.com',
        'phone': '+91 94890 58360',
        'status': 'Pending',
        'notes': 'Verified official portal (bethlahem-bed.org), email and phone.'
    },
    'Bhaktavatsalam Memorial College [W]': {
        'website': 'https://www.bmc.ac.in',
        'contact': 'Office of the Principal (Korattur)',
        'email': 'bmcchennai@yahoo.co.in',
        'phone': '044-26872891',
        'status': 'Pending',
        'notes': 'Verified official portal (bmc.ac.in), institutional email and phone.'
    },
    'Bharat College of Education': {
        'website': 'http://www.bharatcollegeofeducation.com',
        'contact': 'Office of the Principal (Kosapet)',
        'email': 'bharatheadoffice@gmail.com',
        'phone': '+91 9442924555',
        'status': 'Pending',
        'notes': 'Verified official portal (bharatcollegeofeducation.com), head office email and mobile.'
    },
    'Bharat Ratna Dr.A.P.J.Abdul Kalam Government Arts and Science College': {
        'website': 'https://www.drapjgascrmm.in',
        'contact': 'Office of the Principal (Rameswaram)',
        'email': 'drabdulkalamgasc@gmail.com',
        'phone': '04573-290301',
        'status': 'Pending',
        'notes': 'Verified official portal (drapjgascrmm.in), official institutional email and landline.'
    },
    'Bharat Ratna Puratchi Thalaivar Dr. M.G.R.Government Arts and Science College': {
        'website': 'https://www.gascpalacode.org',
        'contact': 'Office of the Principal (Palacode)',
        'email': 'gascpalacode2017@gmail.com',
        'phone': '04348-296105',
        'status': 'Pending',
        'notes': 'Verified official portal (gascpalacode.org), institutional email and landline.'
    },
    'Bharath College of Education': {
        'website': 'https://www.bharathcollegetvr.com',
        'contact': 'Office of Leadership & Admissions (Ammaiyappan)',
        'email': 'bharathgroupofcolleges@gmail.com',
        'phone': '+91 94433 33283',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathcollegetvr.com), group email and mobile.'
    },
    'Bharath College Of Sci': {
        'website': 'https://www.bharathcollege.in',
        'contact': 'Office of Admissions & Principal (Trichy Road)',
        'email': 'info@bharathcollege.in',
        'phone': '+91 80155 05295',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathcollege.in), admissions email and helpline.'
    },
    'Bharath Institute of Education': {
        'website': 'https://www.bharathinstitute.com',
        'contact': 'Office of Admissions & Principal (Elathur)',
        'email': 'admissions@bharathinstitute.com',
        'phone': '+91 94863 53185',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathinstitute.com), admissions email and phone.'
    },
    'Bharath Vidya mandir Arts and science College': {
        'website': 'https://bvmartscollege.com',
        'contact': 'Office of the Principal (Thandrampet)',
        'email': 'bvmcollegetpet@gmail.com',
        'phone': '+91 86086 08787',
        'status': 'Pending',
        'notes': 'Verified official portal (bvmartscollege.com), college email and mobile.'
    },
    'Bharathi Arts & Science College for Women': {
        'website': 'https://www.bharathieduins.org',
        'contact': 'Office of Admissions & Leadership (Thatchur)',
        'email': 'bwascollege@gmail.com',
        'phone': '+91 9994598449',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathieduins.org), institutional email and phone.'
    },
    'Bharathi College of Education': {
        'website': 'https://www.bharathicollegeofeducation.in',
        'contact': 'Office of the Principal (Maravaneri)',
        'email': 'info@bharathicollegeofeducation.in',
        'phone': '+91 99442 66060',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathicollegeofeducation.in), institutional email and mobile.'
    },
    'Bharathi Vidhyalaya College of Education': {
        'website': 'https://www.bharathitrust.com',
        'contact': 'Office of the Principal (Tirugokarnam)',
        'email': 'info@bharathividyalaya.org',
        'phone': '04322-220746',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathitrust.com), institutional email and telephone.'
    },
    'Bharathi Vidyalaya Arts and Science College for Woman': {
        'website': 'https://www.sbcoll.edu.in',
        'contact': 'Office of Admissions & Principal (Kaikurichi)',
        'email': 'ribharathicollege@gmail.com',
        'phone': '+91 9942228013',
        'status': 'Pending',
        'notes': 'Verified official portal (sbcoll.edu.in), institutional email and mobile.'
    },
    'Bharathi Vidyalaya College of Education(Women)': {
        'website': 'https://www.bharathitrust.com',
        'contact': 'Office of Leadership & Admissions (Tirugokarnam)',
        'email': 'info@bharathividyalaya.org',
        'phone': '04322-228931',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathitrust.com), institutional email and telephone.'
    },
    'Bharathi Womens College(Autonomous)': {
        'website': 'https://bwc.edu.in',
        'contact': 'Office of the Principal (Broadway)',
        'email': 'principal@bwc.edu.in',
        'phone': '044-25286411',
        'status': 'Pending',
        'notes': 'Verified official portal (bwc.edu.in), principal email and telephone.'
    },
    'Bharathidasan College': {
        'website': 'https://www.bcas.ac.in',
        'contact': 'Office of Admissions & Principal (Ellispettai)',
        'email': 'info@bcas.ac.in',
        'phone': '+91 93848 12271',
        'status': 'Pending',
        'notes': 'Verified official portal (bcas.ac.in), institutional email and mobile.'
    },
    'Bharathiyar Arts & Sci, College': {
        'website': 'https://bascw.ac.in',
        'contact': 'Office of Admissions & Principal (Deviyakurichi)',
        'email': 'bharathiyar1997@gmail.com',
        'phone': '+91 94427 00889',
        'status': 'Pending',
        'notes': 'Verified official portal (bascw.ac.in), institutional email and telephone.'
    },
    'Bharathiyar College of Education': {
        'website': 'http://www.bharathiyarcollege.com',
        'contact': 'Office of the Principal (Mandavai)',
        'email': 'bedmkm@yahoo.com',
        'phone': '+91 9843929070',
        'status': 'Pending',
        'notes': 'Verified official portal (bharathiyarcollege.com), institutional email and mobile.'
    },
    'Bhavani College of Education': {
        'website': 'http://www.bhavani-ced.com',
        'contact': 'Office of Leadership & Admissions (K.N. Pettai)',
        'email': 'bhavani.college@yahoo.in',
        'phone': '+91 6383730115',
        'status': 'Pending',
        'notes': 'Verified official portal (bhavani-ced.com), institutional email and phone.'
    },
    'Billgates College of Education': {
        'website': 'http://billgateseducation.org',
        'contact': 'Office of the Principal (Gingee)',
        'email': 'dominicpv@yahoo.com',
        'phone': '+91 9444011469',
        'status': 'Pending',
        'notes': 'Verified official portal (billgateseducation.org), management email and phone.'
    },
    'Bishop Agniswamy College of Education': {
        'website': 'https://baceducation.org',
        'contact': 'Office of the Principal (Muttom)',
        'email': 'baceducationmuttom@gmail.com',
        'phone': '+91 9943350117',
        'status': 'Pending',
        'notes': 'Verified official portal (baceducation.org), email and mobile.'
    },
    'Bishop Ambrose College': {
        'website': 'https://www.bishopambrosecollege.in',
        'contact': 'Office of the Principal (Sungam Bypass)',
        'email': 'bishopambrosecollege1@gmail.com',
        'phone': '0422-2316731',
        'status': 'Pending',
        'notes': 'Verified official portal (bishopambrosecollege.in), official email and phone.'
    },
    'Bishop Appasamy College of Education': {
        'website': 'https://csibaced.ac.in',
        'contact': 'Office of Admissions & Principal (BACED)',
        'email': 'info@csibaced.ac.in',
        'phone': '+91 90420 23703',
        'status': 'Pending',
        'notes': 'Verified official portal (csibaced.ac.in), institutional email and mobile.'
    },
    'Bishop Appasamy College': {
        'website': 'https://csibacas.edu.in',
        'contact': 'Office of the Principal & Admissions (Race Course)',
        'email': 'csibacas@gmail.com',
        'phone': '+91 7598619705',
        'status': 'Pending',
        'notes': 'Verified official portal (csibacas.edu.in), institutional email and helpline.'
    },
    'Bishop Caldwell College': {
        'website': 'http://bishopcaldwellcollege.com',
        'contact': 'Office of the Principal (Maravanmadam)',
        'email': 'caldwellcoll@yahoo.in',
        'phone': '0461-2271868',
        'status': 'Pending',
        'notes': 'Verified official portal (bishopcaldwellcollege.com), official email and phone.'
    },
    'Bishop Heber College': {
        'website': 'https://bhc.edu.in',
        'contact': 'Office of the Principal (Autonomous, Puthur)',
        'email': 'principal@bhc.edu.in',
        'phone': '+91 431 2770136',
        'status': 'Pending',
        'notes': 'Verified official portal (bhc.edu.in), principal email and telephone.'
    },
    'Bishop Packiam Arokiaswamy College of Education': {
        'website': 'https://www.bpacollegeofeducation.in',
        'contact': 'Office of Leadership & Admissions (Vamban)',
        'email': 'bpacollegeofeducation@gmail.com',
        'phone': '+91 91595 11604',
        'status': 'Pending',
        'notes': 'Verified official portal (bpacollegeofeducation.in), email and mobile.'
    },
    'Bishop Thorp College': {
        'website': 'https://bishopthorp.in',
        'contact': 'Office of the Principal (Dharapuram)',
        'email': 'bishopthorp@rediffmail.com',
        'phone': '+91 9443181097',
        'status': 'Pending',
        'notes': 'Verified official portal (bishopthorp.in), institutional email and mobile.'
    },
    'Blessy College of Education': {
        'website': 'https://blessycollegeofeducation.com',
        'contact': 'Office of the Principal (Chidambaram)',
        'email': 'blessybed@gmail.com',
        'phone': '+91 9994647744',
        'status': 'Pending',
        'notes': 'Verified official portal (blessycollegeofeducation.com), institutional email and mobile.'
    },
    'Bon Secours Arts and Science (Women) College': {
        'website': 'https://bonsecoursdindigul.edu.in',
        'contact': 'Office of the Principal & Admissions (Begambur)',
        'email': 'bonsecours.dindigul@gmail.com',
        'phone': '+91 99437 36742',
        'status': 'Pending',
        'notes': 'Verified official portal (bonsecoursdindigul.edu.in), email and phone.'
    },
    'BON SECOURS ARTS AND SCIENCE COLLEGE FOR WOMEN': {
        'website': 'http://bonsecourscollegeveppadai.edu.in',
        'contact': 'Office of the Principal & Admissions (Veppadai)',
        'email': 'bonssalem@gmail.com',
        'phone': '+91 86106 81129',
        'status': 'Pending',
        'notes': 'Verified official portal (bonsecourscollegeveppadai.edu.in), official email and mobile.'
    },
    'Bon Secours College for Women(Autonomous)': {
        'website': 'https://www.bonsecourscollege.edu.in',
        'contact': 'Office of the Principal & Admin (Vilar Bypass)',
        'email': 'bonsecourscollege02@gmail.com',
        'phone': '+91 78458 62322',
        'status': 'Pending',
        'notes': 'Verified official portal (bonsecourscollege.edu.in), institutional email and phone.'
    },
    'Bon Secours College of Education': {
        'website': 'http://www.bonsecoursedu.org.in',
        'contact': 'Office of Leadership & Principal',
        'email': 'bonsecourscollege02@gmail.com',
        'phone': '04362-257647',
        'status': 'Pending',
        'notes': 'Verified official portal (bonsecoursedu.org.in), institutional email and phone.'
    },
    'Brilliant College of Education': {
        'website': 'https://brilliantcoe.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'bcettp@gmail.com',
        'phone': '+91 8489030407',
        'status': 'Pending',
        'notes': 'Verified official portal (brilliantcoe.com), institutional email and mobile.'
    },
    'BWDA College Of Arts And Science': {
        'website': 'https://bwdacollege-in.bwda.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'bwdaascollege@gmail.com',
        'phone': '04147-241412',
        'status': 'Pending',
        'notes': 'Verified official portal (bwdacollege-in.bwda.in), institutional email and phone.'
    },
    'C M Annamalai College of Education': {
        'website': 'https://www.cmacollegeofedu.com',
        'contact': 'Office of the Principal & Admissions (Adhivaragapuram)',
        'email': 'info@cmacollegeofedu.com',
        'phone': '+91 95853 65959',
        'status': 'Pending',
        'notes': 'Verified official portal (cmacollegeofedu.com), official email and mobile.'
    },
    'C. Abdul Hakeem College': {
        'website': 'https://cahc.edu.in',
        'contact': 'Office of the Principal (Autonomous, Melvisharam)',
        'email': 'contactus@cahc.edu.in',
        'phone': '+91 4172 266487',
        'status': 'Pending',
        'notes': 'Verified official portal (cahc.edu.in), official email and telephone.'
    },
    'C. Kandaswami Naidu College For Men': {
        'website': 'https://cknc.edu.in',
        'contact': 'Office of the Principal (Anna Nagar East)',
        'email': 'ckncprincipal@gmail.com',
        'phone': '044-26262970',
        'status': 'Pending',
        'notes': 'Verified official portal (cknc.edu.in), principal email and telephone.'
    },
    'C. Kandaswami Naidu College for Women': {
        'website': 'https://ckncollegeforwomen.org',
        'contact': 'Office of the Principal (Semmandalam)',
        'email': 'cknccuddalore@gmail.com',
        'phone': '04142-230408',
        'status': 'Pending',
        'notes': 'Verified official portal (ckncollegeforwomen.org), principal email and telephone.'
    },
    'C.M.Annamalai Arts and Science (Women) College': {
        'website': 'https://www.cmacollegeofedu.com',
        'contact': 'Office of Leadership & Admissions (Adhivaragapuram)',
        'email': 'info@cmacollegeofedu.com',
        'phone': '+91 95853 65959',
        'status': 'Pending',
        'notes': 'Verified official portal (cmacollegeofedu.com), official email and mobile.'
    },
    'C.M.S. College of Education': {
        'website': 'https://cmscollegeofeducation.in',
        'contact': 'Office of Leadership & Admissions (Ganapathy)',
        'email': 'cmscollegeofeducation08@gmail.com',
        'phone': '+91 9363635508',
        'status': 'Pending',
        'notes': 'Verified official portal (cmscollegeofeducation.in), institutional email and mobile.'
    },
    'C.S Jain College of Education': {
        'website': 'https://csjaincollegeofeducation.com',
        'contact': 'Office of the Principal & Admissions (Srimushnam)',
        'email': 'csjainbed@gmail.com',
        'phone': '+91 9442378241',
        'status': 'Pending',
        'notes': 'Verified official portal (csjaincollegeofeducation.com), institutional email and mobile.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_3_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_3_COLLEGES)}")
    unmatched = set(BATCH_3_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
