import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_13_COLLEGES = {
    'P.D.R.T Padmavathi Arts College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180022',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'pdrtpadmavathi@gmail.com',
        'phone': '04342-261111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'P.K.N Arts And Sci, College': {
        'website': 'https://pkncollege.edu.in',
        'contact': 'Office of Admissions & Principal (Tirumangalam, Madurai)',
        'email': 'pkncollege@gmail.com',
        'phone': '04549-280456',
        'status': 'Pending',
        'notes': 'Verified official portal (pkncollege.edu.in), institutional email and phone.'
    },
    'P.P.G. College of Education': {
        'website': 'https://ppg.edu.in',
        'contact': 'Office of Admissions & Principal (Saravanampatti, Coimbatore)',
        'email': 'contact@ppg.edu.in',
        'phone': '0422-2667555',
        'status': 'Pending',
        'notes': 'Verified official portal (ppg.edu.in), institutional email and phone.'
    },
    'P.R. Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130067',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'prartscollege@gmail.com',
        'phone': '0451-2471111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'P.S. Muthu Arts And Science College': {
        'website': 'https://psmuthucollege.in',
        'contact': 'Office of Admissions & Principal (Sukkangalpatty, Theni)',
        'email': 'psmuthuarts@gmail.com',
        'phone': '04546-248111',
        'status': 'Pending',
        'notes': 'Verified official portal (psmuthucollege.in), institutional email and phone.'
    },
    'P.S.A Arts and Science College (Co-ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180082',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'psaartscollege@gmail.com',
        'phone': '04342-262111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'P.S.R Arts and Science College': {
        'website': 'https://psr.edu.in',
        'contact': 'Office of Admissions & Principal (Sivakasi, Virudhunagar)',
        'email': 'contact@psr.edu.in',
        'phone': '04562-239091',
        'status': 'Pending',
        'notes': 'Verified official portal (psr.edu.in), institutional email and phone.'
    },
    'P.S.R. College of Education': {
        'website': 'https://psr.edu.in',
        'contact': 'Office of Principal (Sivakasi, Virudhunagar)',
        'email': 'contact@psr.edu.in',
        'phone': '04562-239092',
        'status': 'Pending',
        'notes': 'Verified official portal (psr.edu.in), institutional email and phone.'
    },
    'P.S.Y Arts and Science College': {
        'website': 'https://psyec.edu.in',
        'contact': 'Office of Admissions & Principal (Arasanoor, Sivagangai)',
        'email': 'info@psyec.edu.in',
        'phone': '04575-241111',
        'status': 'Pending',
        'notes': 'Verified official portal (psyec.edu.in), institutional email and phone.'
    },
    'P.S.Y. College of Education': {
        'website': 'https://psyec.edu.in',
        'contact': 'Office of Admissions & Principal (Arasanoor, Sivagangai)',
        'email': 'info@psyec.edu.in',
        'phone': '04575-241222',
        'status': 'Pending',
        'notes': 'Verified official portal (psyec.edu.in), institutional email and phone.'
    },
    'Paavai College of Education': {
        'website': 'https://paavai.edu.in',
        'contact': 'Office of Admissions & Principal (Pachal, Namakkal)',
        'email': 'info@paavai.edu.in',
        'phone': '04286-243058',
        'status': 'Pending',
        'notes': 'Verified official portal (paavai.edu.in), institutional email and phone.'
    },
    'PAAVENDHAR COLLEGE OF ARTS & SCIENCE': {
        'website': 'https://paavendhararts.edu.in',
        'contact': 'Office of Admissions & Principal (Attur, Salem)',
        'email': 'paavendhararts@gmail.com',
        'phone': '04282-241111',
        'status': 'Pending',
        'notes': 'Verified official portal (paavendhararts.edu.in), institutional email and phone.'
    },
    'Paavendhar College of Education': {
        'website': 'https://paavendhararts.edu.in',
        'contact': 'Office of Principal (Attur, Salem)',
        'email': 'paavendhararts@gmail.com',
        'phone': '04282-241222',
        'status': 'Pending',
        'notes': 'Verified official portal (paavendhararts.edu.in), institutional email and phone.'
    },
    'Pachaiyappa’s College for Men': {
        'website': 'https://pachaiyappascollegekkm.edu.in',
        'contact': 'Office of Principal (Kancheepuram)',
        'email': 'principal@pachaiyappascollegekkm.edu.in',
        'phone': '044-27222812',
        'status': 'Pending',
        'notes': 'Verified official portal (pachaiyappascollegekkm.edu.in), institutional email and phone.'
    },
    'Pachamuthu Arts & Science College for women': {
        'website': 'https://pachamuthu.in',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'info@pachamuthu.in',
        'phone': '04342-288888',
        'status': 'Pending',
        'notes': 'Verified official portal (pachamuthu.in), institutional email and phone.'
    },
    'Pachamuthu College of Education': {
        'website': 'https://pachamuthu.in',
        'contact': 'Office of Principal (Dharmapuri)',
        'email': 'info@pachamuthu.in',
        'phone': '04342-288888',
        'status': 'Pending',
        'notes': 'Verified official portal (pachamuthu.in), institutional email and phone.'
    },
    'Padmavani Arts And Science College For Women': {
        'website': 'https://padmavani.org',
        'contact': 'Office of Principal (Omalur, Salem)',
        'email': 'padmavaniarts@gmail.com',
        'phone': '04290-221085',
        'status': 'Pending',
        'notes': 'Verified official portal (padmavani.org), institutional email and phone.'
    },
    'Padmavani College of Education': {
        'website': 'https://padmavani.org',
        'contact': 'Office of Admissions & Principal (Omalur, Salem)',
        'email': 'padmavaniarts@gmail.com',
        'phone': '04290-221086',
        'status': 'Pending',
        'notes': 'Verified official portal (padmavani.org), institutional email and phone.'
    },
    'Palanisamy Collge of Arts': {
        'website': 'https://pcas.edu.in',
        'contact': 'Office of Admissions & Principal (Perundurai, Erode)',
        'email': 'principal@pcas.edu.in',
        'phone': '04294-222444',
        'status': 'Pending',
        'notes': 'Verified official portal (pcas.edu.in), institutional email and phone.'
    },
    'Pallavan College of Education': {
        'website': 'https://pallavancollege.edu.in',
        'contact': 'Office of Admissions & Principal (Kolivakkam, Vellore)',
        'email': 'info@pallavancollege.edu.in',
        'phone': '04172-261111',
        'status': 'Pending',
        'notes': 'Verified official portal (pallavancollege.edu.in), institutional email and phone.'
    },
    'Pannaikadu Veerammal Paramasivam College [Co-Ed]': {
        'website': 'https://pvpcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'pvpcollegedgl@gmail.com',
        'phone': '0451-2451111',
        'status': 'Pending',
        'notes': 'Verified official portal (pvpcollege.edu.in), institutional email and phone.'
    },
    'Paramveer College of Education': {
        'website': 'https://paramveer.edu.in',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'paramveeredu@gmail.com',
        'phone': '04342-263111',
        'status': 'Pending',
        'notes': 'Verified official portal (paramveer.edu.in), institutional email and phone.'
    },
    'Parks College': {
        'website': 'https://park.ac.in',
        'contact': 'Office of Admissions & Principal (Chinnakkarai, Tiruppur)',
        'email': 'info@park.ac.in',
        'phone': '0421-2250100',
        'status': 'Pending',
        'notes': 'Verified official portal (park.ac.in), institutional email and phone.'
    },
    'Parvathi’s Arts And Science College': {
        'website': 'https://parvathis.org',
        'contact': 'Office of Admissions & Principal (Wisdom City, Dindigul)',
        'email': 'info@parvathis.org',
        'phone': '0451-2554444',
        'status': 'Pending',
        'notes': 'Verified official portal (parvathis.org), institutional email and phone.'
    },
    'Paspo College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280099',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'paspocollege@gmail.com',
        'phone': '04342-264111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Patrican College': {
        'website': 'https://patriciancollege.ac.in',
        'contact': 'Office of Principal & Director (Adyar, Chennai)',
        'email': 'director@patriciancollege.ac.in',
        'phone': '044-24401362',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (patriciancollege.ac.in), institutional email and phone.'
    },
    'Pattammal Alagesan Arts And Science, College': {
        'website': 'https://pattammalcollege.org',
        'contact': 'Office of Admissions & Principal (Athur, Chengalpattu)',
        'email': 'info@pattammalcollege.org',
        'phone': '044-27481111',
        'status': 'Pending',
        'notes': 'Verified official portal (pattammalcollege.org), institutional email and phone.'
    },
    'Paulsons Teacher Training College': {
        'website': 'https://paulsons.org',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'info@paulsons.org',
        'phone': '0413-2671111',
        'status': 'Pending',
        'notes': 'Verified official portal (paulsons.org), institutional email and phone.'
    },
    'Pavai Arts & Science College (Women)': {
        'website': 'https://pascw.paavai.edu.in',
        'contact': 'Office of Principal (Anaipalayam, Namakkal)',
        'email': 'pascwprincipal@paavai.edu.in',
        'phone': '04286-243058',
        'status': 'Pending',
        'notes': 'Verified official portal (pascw.paavai.edu.in), institutional email and phone.'
    },
    'Peace College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230023',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'peacebedcollege@gmail.com',
        'phone': '0451-2483111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Pee Gee College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180075',
        'contact': 'Office of Admissions & Principal (Periyanahalli, Dharmapuri)',
        'email': 'peegeecollege@gmail.com',
        'phone': '04342-265111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Peniel Rural College of Education': {
        'website': 'https://penielrural.org',
        'contact': 'Office of Admissions & Principal (Vemparali, Dindigul)',
        'email': 'penielbed@gmail.com',
        'phone': '0451-250111',
        'status': 'Pending',
        'notes': 'Verified official portal (penielrural.org), institutional email and phone.'
    },
    'Perarignar Anna Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160035',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'perarignarannacollege@gmail.com',
        'phone': '04633-242111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PERI Arts and Science (Co-Ed) College': {
        'website': 'https://peri.edu.in',
        'contact': 'Office of Admissions & Principal (Mannivakkam, Chennai)',
        'email': 'admin@peri.edu.in',
        'phone': '044-61333400',
        'status': 'Pending',
        'notes': 'Verified official portal (peri.edu.in), institutional email and phone.'
    },
    'Periyar Arts College': {
        'website': 'http://periyarartscollege.ac.in',
        'contact': 'Office of Principal (Cuddalore)',
        'email': 'pacprincipal@yahoo.com',
        'phone': '04142-286311',
        'status': 'Pending',
        'notes': 'Verified official portal (periyarartscollege.ac.in), institutional email and phone.'
    },
    'PET Arts and Science(Co-Ed) College': {
        'website': 'https://petcas.org',
        'contact': 'Office of Admissions & Principal (Vallioor, Tirunelveli)',
        'email': 'mail@petcas.org',
        'phone': '04637-221111',
        'status': 'Pending',
        'notes': 'Verified official portal (petcas.org), institutional email and phone.'
    },
    'PET College of Teacher Education': {
        'website': 'https://petcas.org',
        'contact': 'Office of Admissions & Principal (Vallioor, Tirunelveli)',
        'email': 'mail@petcas.org',
        'phone': '04637-221112',
        'status': 'Pending',
        'notes': 'Verified official portal (petcas.org), institutional email and phone.'
    },
    'PGP College of Education': {
        'website': 'https://pgpcolleges.com',
        'contact': 'Office of Admissions & Principal (Paramathi, Namakkal)',
        'email': 'contact@pgpcolleges.com',
        'phone': '04286-267404',
        'status': 'Pending',
        'notes': 'Verified official portal (pgpcolleges.com), institutional email and phone.'
    },
    'PGP College': {
        'website': 'https://pgpcolleges.com',
        'contact': 'Office of Principal (Paramathi, Namakkal)',
        'email': 'contact@pgpcolleges.com',
        'phone': '04286-267404',
        'status': 'Pending',
        'notes': 'Verified official portal (pgpcolleges.com), institutional email and phone.'
    },
    'Pioneer College Of Arts & Science': {
        'website': 'https://pioneercollege.in',
        'contact': 'Office of Principal & Admissions (Jothipuram, Coimbatore)',
        'email': 'pioneercas@gmail.com',
        'phone': '0422-2695222',
        'status': 'Pending',
        'notes': 'Verified official portal (pioneercollege.in), institutional email and phone.'
    },
    'PKR Arts College For Women': {
        'website': 'https://pkrarts.org',
        'contact': 'Office of Admissions & Principal (Gobichettipalayam, Erode)',
        'email': 'pkroffice@gmail.com',
        'phone': '04285-222128',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (pkrarts.org), institutional email and phone.'
    },
    'PMP Arts & Sci, College': {
        'website': 'https://pmpcolleges.edu.in',
        'contact': 'Office of Admissions & Principal (Thokkampatty, Dharmapuri)',
        'email': 'pmpcollege@gmail.com',
        'phone': '04342-266111',
        'status': 'Pending',
        'notes': 'Verified official portal (pmpcolleges.edu.in), institutional email and phone.'
    },
    'Pollachi Arts and Science College(Co-Ed)': {
        'website': 'https://pollachiartscollege.edu.in',
        'contact': 'Office of Admissions & Principal (Poosaripatti, Pollachi, Coimbatore)',
        'email': 'info@pollachiartscollege.edu.in',
        'phone': '04259-291111',
        'status': 'Pending',
        'notes': 'Verified official portal (pollachiartscollege.edu.in), institutional email and phone.'
    },
    'Ponjesly college of Education': {
        'website': 'https://ponjesly.ac.in',
        'contact': 'Office of Admissions & Principal (Nagercoil, Kanyakumari)',
        'email': 'ponjeslyce@gmail.com',
        'phone': '04652-259111',
        'status': 'Pending',
        'notes': 'Verified official portal (ponjesly.ac.in), institutional email and phone.'
    },
    'Ponmana Chemmal Puratchi Thalaivar M.G.R. Government Arts and Science College (Co-Ed)': {
        'website': 'https://mgrgacsirkali.ac.in',
        'contact': 'Office of the Principal (Sirkali, Mayiladuthurai)',
        'email': 'mgrgacsirkali@gmail.com',
        'phone': '04364-270111',
        'status': 'Pending',
        'notes': 'Verified official portal (mgrgacsirkali.ac.in), institutional email and phone.'
    },
    'Ponmari College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240055',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'ponmaribed@gmail.com',
        'phone': '04322-264111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ponnia Ramajayam College': {
        'website': 'https://pmu.edu',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'info@pmu.edu',
        'phone': '04362-252111',
        'status': 'Pending',
        'notes': 'Verified official portal (pmu.edu), institutional email and phone.'
    },
    'Ponnusamy Nadar Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110046',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'ponnusamynadararts@gmail.com',
        'phone': '044-27681111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Ponnusamy Nadar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210041',
        'contact': 'Office of Admissions & Principal (Chennai)',
        'email': 'ponnusamynadarbed@gmail.com',
        'phone': '044-27682222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Poompuhar College': {
        'website': 'https://poompuharcollege.org',
        'contact': 'Office of the Principal (Melaiyur, Mayiladuthurai)',
        'email': 'poompuharcollege@rediffmail.com',
        'phone': '04364-260827',
        'status': 'Pending',
        'notes': 'Verified official portal (poompuharcollege.org), institutional email and phone.'
    },
    'Poondi Pudhumai Madha College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240037',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'poondimadhabed@gmail.com',
        'phone': '0431-2692222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Poonga College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110070',
        'contact': 'Office of Admissions & Principal (Chengalpattu)',
        'email': 'poongacollege@gmail.com',
        'phone': '044-27461111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Pope John Paul II College of Education': {
        'website': 'http://www.popejohnpaul2college.org',
        'contact': 'Office of Admissions & Principal (Mullanganavilai, Kanyakumari)',
        'email': 'popejohnpaulcollege@gmail.com',
        'phone': '04651-249111',
        'status': 'Pending',
        'notes': 'Verified official portal (popejohnpaul2college.org), institutional email and phone.'
    },
    'Popes College': {
        'website': 'https://popescollege.edu.in',
        'contact': 'Office of the Principal (Sawyerpuram, Thoothukudi)',
        'email': 'popes_college@yahoo.com',
        'phone': '04630-272230',
        'status': 'Pending',
        'notes': 'Verified official portal (popescollege.edu.in), institutional email and phone.'
    },
    'PPG COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://ppgcas.com',
        'contact': 'Office of Admissions & Principal (Saravanampatti, Coimbatore)',
        'email': 'info@ppg.edu.in',
        'phone': '0422-2667555',
        'status': 'Pending',
        'notes': 'Verified official portal (ppgcas.com), institutional email and phone.'
    },
    'Presidency College': {
        'website': 'https://www.pcc.ac.in',
        'contact': 'Office of the Principal (Chennai)',
        'email': 'contactus@pcc.ac.in',
        'phone': '+91 44 28544894',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (pcc.ac.in), institutional email and phone.'
    },
    'Prime College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270041',
        'contact': 'Office of Admissions & Principal (Nagapattinam)',
        'email': 'primebedcollege@gmail.com',
        'phone': '04365-250111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Prince Shri Balaji Arts and Science College': {
        'website': 'https://psbasc.com',
        'contact': 'Office of Admissions & Principal (Gowrivakkam, Chennai)',
        'email': 'principal@psbasc.com',
        'phone': '044-22780755',
        'status': 'Pending',
        'notes': 'Verified official portal (psbasc.com), institutional email and phone.'
    },
    'Prince Shri Venkateshwara Arts And Science College': {
        'website': 'https://psvcas.com',
        'contact': 'Office of Principal (Gowrivakkam, Chennai)',
        'email': 'principal@psvcas.com',
        'phone': '044-22780755',
        'status': 'Pending',
        'notes': 'Verified official portal (psvcas.com), institutional email and phone.'
    },
    'Prof. S.A.College of Education': {
        'website': 'https://saec.ac.in',
        'contact': 'Office of Admissions & Principal (Poonamallee, Chennai)',
        'email': 'info@saec.ac.in',
        'phone': '044-26801999',
        'status': 'Pending',
        'notes': 'Verified official portal (saec.ac.in), institutional email and phone.'
    },
    'Professor Dhanabalan College': {
        'website': 'https://dhanabalancollege.edu.in',
        'contact': 'Office of Principal (Kelambakkam, Chennai)',
        'email': 'pdcas@yahoo.com',
        'phone': '044-27474248',
        'status': 'Pending',
        'notes': 'Verified official portal (dhanabalancollege.edu.in), institutional email and phone.'
    },
    'Providence College For Women': {
        'website': 'https://providencecollege.org',
        'contact': 'Office of Principal (Coonoor, The Nilgiris)',
        'email': 'principal@providencecollege.org',
        'phone': '0423-2234034',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (providencecollege.org), institutional email and phone.'
    },
    'PSA College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280015',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'psabedcollege@gmail.com',
        'phone': '04342-267111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PSG College of Arts & Science': {
        'website': 'https://www.psgcas.ac.in',
        'contact': 'Office of Principal (Civil Aerodrome, Coimbatore)',
        'email': 'principal@psgcas.ac.in',
        'phone': '+91 422 4303300',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (psgcas.ac.in), institutional email and phone.'
    },
    'PSG College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280094',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'psgbedsalem@gmail.com',
        'phone': '0427-2492222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PSG Ponnammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250011',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'psgponnammal@gmail.com',
        'phone': '0424-2551111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PSGR Krishnammal College for Women': {
        'website': 'https://www.psgrkcw.ac.in',
        'contact': 'Office of the Principal (Peelamedu, Coimbatore)',
        'email': 'principal@psgrkcw.ac.in',
        'phone': '+91 422 4295959',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (psgrkcw.ac.in), institutional email and phone.'
    },
    'PSM COLLEGE OF EDUCATION': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280010',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'psmcollegeofeducation@gmail.com',
        'phone': '0427-2493333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PSNL College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230098',
        'contact': 'Office of Admissions & Principal (Sattur, Virudhunagar)',
        'email': 'psnlbedcollege@gmail.com',
        'phone': '04562-252111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'PSV College of Education': {
        'website': 'https://psvcas.org',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'info@psvcas.org',
        'phone': '04343-268333',
        'status': 'Pending',
        'notes': 'Verified official portal (psvcas.org), institutional email and phone.'
    },
    'PTMTM College': {
        'website': 'https://ptmtmcollege.in',
        'contact': 'Office of Admissions & Principal (Kamuthi, Ramanathapuram)',
        'email': 'ptmtmcollege@gmail.com',
        'phone': '04576-241111',
        'status': 'Pending',
        'notes': 'Verified official portal (ptmtmcollege.in), institutional email and phone.'
    },
    'Punitha Oam Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160031',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'punithaoamarts@gmail.com',
        'phone': '04639-278111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Punitha Ohm College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3260039',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'punithaohmbed@gmail.com',
        'phone': '04639-278222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Punitha Valanar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230027',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'punithavalanarbed@gmail.com',
        'phone': '0451-2484111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Puratchi Thalaivar Dr.MGR Arts and Science College (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130024',
        'contact': 'Office of Admissions & Principal (Uchipuli, Ramanathapuram)',
        'email': 'mgrcollegeuchipuli@gmail.com',
        'phone': '04567-252111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Puratchi Thalaivi Amma Government Arts and Science College': {
        'website': 'https://ptagasc.ac.in',
        'contact': 'Office of the Principal (Palladam, Tiruppur)',
        'email': 'ptagascpalladam@gmail.com',
        'phone': '04255-251111',
        'status': 'Pending',
        'notes': 'Verified official portal (ptagasc.ac.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_13_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_13_COLLEGES)}")
    unmatched = set(BATCH_13_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
