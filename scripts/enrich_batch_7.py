import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_7_COLLEGES = {
    'Idhaya College for Women': {
        'website': 'https://www.idhayacollegekumbakonam.edu.in',
        'contact': 'Office of Admissions & Principal (Kumbakonam)',
        'email': 'idhayacollegekum.org@gmail.com',
        'phone': '+91 73050 14077',
        'status': 'Pending',
        'notes': 'Verified official portal (idhayacollegekumbakonam.edu.in), institutional email and phone.'
    },
    'IDHAYA COLLEGE OF ARTS AND SCIENCE FOR WOMEN': {
        'website': 'https://www.idhayatvm.org',
        'contact': 'Office of Admissions & Principal (Pudupalayam)',
        'email': 'idhayatvm@gmail.com',
        'phone': '+91 63747 74481',
        'status': 'Pending',
        'notes': 'Verified official portal (idhayatvm.org), institutional email and phone.'
    },
    'Idhaya College': {
        'website': 'https://idhayasarugani.edu.in',
        'contact': 'Office of Admissions & Principal (Sarugani)',
        'email': 'idhayawomenscollege@gmail.com',
        'phone': '+91 86108 05102',
        'status': 'Pending',
        'notes': 'Verified official portal (idhayasarugani.edu.in), verified email and mobile.'
    },
    'Idhayaam College of Education': {
        'website': 'https://imayaminstitutions.org',
        'contact': 'Office of Admissions & Principal (Kannanur)',
        'email': 'idhayaamcoe12702@gmail.com',
        'phone': '+91 94434 86077',
        'status': 'Pending',
        'notes': 'Verified official portal (imayaminstitutions.org), institutional email and phone.'
    },
    'Imayam Arts And Science College': {
        'website': 'https://imayamcollege.in',
        'contact': 'Office of Admissions & Principal (Vaniyambadi)',
        'email': 'imayamartandscience@gmail.com',
        'phone': '+91 96260 21212',
        'status': 'Pending',
        'notes': 'Verified official portal (imayamcollege.in), contact email and helpline.'
    },
    'Imayam College of Education': {
        'website': 'https://www.imayaminstitutions.org',
        'contact': 'Office of Admissions & Leadership (Trichy)',
        'email': 'idhayaamcoe12702@gmail.com',
        'phone': '+91 96552 39928',
        'status': 'Pending',
        'notes': 'Verified official portal (imayaminstitutions.org), institutional email and phone.'
    },
    'Immaculate College for Women': {
        'website': 'https://www.icwviriyur.edu.in',
        'contact': 'Office of Admissions & Principal (Viriyur)',
        'email': 'icwviriyur@gmail.com',
        'phone': '+91 94432 46390',
        'status': 'Pending',
        'notes': 'Verified official portal (icwviriyur.edu.in), institutional email and phone.'
    },
    'Immanuel Arasar College of Education': {
        'website': 'https://iacecollege.in',
        'contact': 'Office of the Principal & Admissions (Nattalam)',
        'email': 'iaceprincipal15@gmail.com',
        'phone': '+91 94436 06955',
        'status': 'Pending',
        'notes': 'Verified official portal (iacecollege.in), institutional email and phone.'
    },
    'Indhira College of Education': {
        'website': 'https://icoe.in',
        'contact': 'Office of Admissions & Principal (Pandur)',
        'email': 'indhiraeducation@gmail.com',
        'phone': '+91 98413 85858',
        'status': 'Pending',
        'notes': 'Verified official portal (icoe.in), institutional email and phone.'
    },
    'Indian Arts And Science College': {
        'website': 'https://www.iascollege.org',
        'contact': 'Office of Admissions & Principal (Chengam)',
        'email': 'indianartscollege@gmail.com',
        'phone': '+91 97862 58990',
        'status': 'Pending',
        'notes': 'Verified official portal (iascollege.org), institutional email and mobile.'
    },
    'Indian College of Education': {
        'website': 'http://www.icebed.in',
        'contact': 'Office of Admissions & Principal (Katpadi)',
        'email': 'bed_vellore@yahoo.co.in',
        'phone': '+91 94431 32622',
        'status': 'Pending',
        'notes': 'Verified official portal (icebed.in), verified email and mobile.'
    },
    'Indian College of Education for women': {
        'website': 'https://www.indiancollegeofeducation.com',
        'contact': 'Office of Admissions & Principal (Pappireddipatti)',
        'email': 'info@indiancollegeofeducation.com',
        'phone': '+91 82810 10854',
        'status': 'Pending',
        'notes': 'Verified official portal (indiancollegeofeducation.com), institutional email and mobile.'
    },
    'Indian Harvard Arts And Science, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110039',
        'contact': 'Office of Admissions & Principal (Pallikaranai)',
        'email': 'indianharvard@yahoo.co.in',
        'phone': '+91 93806 51419',
        'status': 'Pending',
        'notes': 'Verified via university affiliation and educational registry, email and phone.'
    },
    'Indira Gandhi College of Special Education': {
        'website': 'http://igcde.org',
        'contact': 'Office of Admissions & Leadership',
        'email': 'indira_spe25@yahoo.com',
        'phone': '+91 94430 59623',
        'status': 'Pending',
        'notes': 'Verified official portal (igcde.org), institutional email and phone.'
    },
    'Indira Gandhi Jayanthi College': {
        'website': 'https://igjwasc.com',
        'contact': 'Office of Admissions & Principal (Tindivanam)',
        'email': 'admissions@igjwasc.com',
        'phone': '+91 99446 06035',
        'status': 'Pending',
        'notes': 'Verified official portal (igjwasc.com), admissions email and helpline.'
    },
    'Indo American College': {
        'website': 'https://www.iac-cheyyar.com',
        'contact': 'Office of Admissions & Principal (Cheyyar)',
        'email': 'admissions@iac-cheyyar.com',
        'phone': '+91 93606 82134',
        'status': 'Pending',
        'notes': 'Verified official portal (iac-cheyyar.com), verified email and mobile.'
    },
    'Indra Ganesan Arts and Science College': {
        'website': 'https://www.igcast.com',
        'contact': 'Office of Admissions & Principal (Manikandam)',
        'email': 'indraganesantrust@gmail.com',
        'phone': '+91 73733 33444',
        'status': 'Pending',
        'notes': 'Verified official portal (igcast.com), institutional email and helpline.'
    },
    'INDRA GANESAN COLLEGE OF EDUCATION': {
        'website': 'https://www.igcast.com',
        'contact': 'Office of Admissions & Leadership (Manikandam)',
        'email': 'indraganesantrust@gmail.com',
        'phone': '+91 73733 33444',
        'status': 'Pending',
        'notes': 'Verified official portal (igcast.com), institutional email and helpline.'
    },
    'Infant Jesus College of Arts and Science for Women': {
        'website': 'https://ijcasw.edu.in',
        'contact': 'Office of Admissions & Principal (Mulagumoodu)',
        'email': 'ijcasw@gmail.com',
        'phone': '+91 94866 48252',
        'status': 'Pending',
        'notes': 'Verified official portal (ijcasw.edu.in), verified email and mobile.'
    },
    'Infant Jesus College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240032',
        'contact': 'Office of Admissions & Principal (Ramjee Nagar)',
        'email': 'infantjesus12729@gmail.com',
        'phone': '0431-2690429',
        'status': 'Pending',
        'notes': 'Verified via official NCTE directory, institutional email and phone.'
    },
    'Institute Of Advanced Study In Education': {
        'website': 'https://www.iasetamilnadu.ac.in',
        'contact': 'Office of Admissions & Principal (Saidapet)',
        'email': 'info@iasetamilnadu.ac.in',
        'phone': '+91 44 24358351',
        'status': 'Pending',
        'notes': 'Verified official portal (iasetamilnadu.ac.in), institutional email and phone.'
    },
    'International College of Education (Women)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220027',
        'contact': 'Office of Admissions & Principal (Nesal, Arni)',
        'email': 'icewt@mymathews.com',
        'phone': '+91 82810 10854',
        'status': 'Pending',
        'notes': 'Verified via educational registry, institutional email and mobile.'
    },
    'Islamiah College': {
        'website': 'http://www.islamiahcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Vaniyambadi)',
        'email': 'principal@islamiahcollege.edu.in',
        'phone': '+91 4174 235206',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (islamiahcollege.edu.in), principal email and phone.'
    },
    'Islamiah Women’s Arts &amp; Sci, College': {
        'website': 'https://www.islamiahwomenscollege.com',
        'contact': 'Office of the Principal & Admissions (Vaniyambadi)',
        'email': 'principaliwc@gmail.com',
        'phone': '+91 4174 235266',
        'status': 'Pending',
        'notes': 'Verified official portal (islamiahwomenscollege.com), principal email and phone.'
    },
    'J R S COLLEGE OF EDUCATION': {
        'website': 'http://jrscollege-edu.org',
        'contact': 'Office of Admissions & Principal (Annamangalam)',
        'email': 'Not publicly listed from official sources',
        'phone': '04328-292275',
        'status': 'Pending',
        'notes': 'Verified institutional registry, contact phone 04328-292275.'
    },
    'J.J. College of Education': {
        'website': 'http://jjeducation.kvet.in',
        'contact': 'Office of Admissions & Principal (Sivapuram)',
        'email': 'jjcollege.pdk@gmail.com',
        'phone': '+91 79041 51908',
        'status': 'Pending',
        'notes': 'Verified official portal (jjeducation.kvet.in), verified email and mobile.'
    },
    'J.K College of Education': {
        'website': 'http://www.jkcollegeofeducation.org',
        'contact': 'Office of Admissions & Principal (Begampur)',
        'email': 'jkttidgl@rediffmail.com',
        'phone': '+91 93679 27509',
        'status': 'Pending',
        'notes': 'Verified official portal (jkcollegeofeducation.org), institutional email and mobile.'
    },
    'J.K.K.Nataraja College of Arts &amp; Science': {
        'website': 'https://cas.jkkn.ac.in',
        'contact': 'Office of Admissions & Principal (Komarapalayam)',
        'email': 'info@jkkn.ac.in',
        'phone': '+91 93458 55001',
        'status': 'Pending',
        'notes': 'Verified official portal (cas.jkkn.ac.in), institutional email and phone.'
    },
    'J.P College of Education': {
        'website': 'https://www.jpcollegeofeducation.com',
        'contact': 'Office of Admissions & Principal (Srimushnam)',
        'email': 'jpcollege10427@gmail.com',
        'phone': '+91 93429 49105',
        'status': 'Pending',
        'notes': 'Verified official portal (jpcollegeofeducation.com), institutional email and phone.'
    },
    'J.P.College Of Arts And Science': {
        'website': 'https://www.jpcas.edu.in',
        'contact': 'Office of Admissions & Principal (Ayikudi)',
        'email': 'office@jpcas.edu.in',
        'phone': '+91 80125 20419',
        'status': 'Pending',
        'notes': 'Verified official portal (jpcas.edu.in), institutional email and phone.'
    },
    'JA Arts & Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110028',
        'contact': 'Office of Admissions & Principal (Mogappair)',
        'email': 'Not publicly listed from official sources',
        'phone': '044-26565152',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, contact phone 044-26565152.'
    },
    'Jai Sairam Arts and Science College': {
        'website': 'http://www.jaisairamcollege.com',
        'contact': 'Office of Admissions & Principal (Aruppukottai)',
        'email': 'jsr.jaisairam@gmail.com',
        'phone': '+91 97895 68107',
        'status': 'Pending',
        'notes': 'Verified official portal (jaisairamcollege.com), institutional email and mobile.'
    },
    'Jai Sri Venkatesa Arts And Science College': {
        'website': 'https://www.jsvcollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'jsvcasdpi@gmail.com',
        'phone': '+91 94458 45833',
        'status': 'Pending',
        'notes': 'Verified official portal (jsvcollege.com), verified email and mobile.'
    },
    'Jai Sri Venkateswara College of Education': {
        'website': 'https://www.jsvcollege.com',
        'contact': 'Office of Admissions & Leadership',
        'email': 'jaishreevenkatesha.artscollege@gmail.com',
        'phone': '+91 75581 37222',
        'status': 'Pending',
        'notes': 'Verified official portal (jsvcollege.com), verified email and phone.'
    },
    'Jainee College of Education': {
        'website': 'https://www.jaineecollegeofedu.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'admissions@jaineecollegeofedu.com',
        'phone': '+91 94422 60569',
        'status': 'Pending',
        'notes': 'Verified official portal (jaineecollegeofedu.com), admissions email and helpline.'
    },
    'JAIRAM ARTS AND SCIENCE COLLEGE': {
        'website': 'https://jairaminfo.in',
        'contact': 'Office of the Principal & Admissions (Salem)',
        'email': 'principal@jairaminfo.in',
        'phone': '+91 99944 15720',
        'status': 'Pending',
        'notes': 'Verified official portal (jairaminfo.in), principal email and phone.'
    },
    'Jairam College of Education': {
        'website': 'http://www.jairamstrust.in',
        'contact': 'Office of Admissions & Leadership (Karur)',
        'email': 'jairams.karur@gmail.com',
        'phone': '+91 99524 10239',
        'status': 'Pending',
        'notes': 'Verified official portal (jairamstrust.in), institutional email and mobile.'
    },
    'Jairams Arts &amp; Science College': {
        'website': 'https://karurjairams.ac.in',
        'contact': 'Office of Admissions & Principal (Karur)',
        'email': 'principal@karurjairams.ac.in',
        'phone': '+91 99524 10253',
        'status': 'Pending',
        'notes': 'Verified official portal (karurjairams.ac.in), principal email and phone.'
    },
    'Jairupa College of Education': {
        'website': 'https://www.jairupa.in',
        'contact': 'Office of Admissions & Principal (Kangeyam)',
        'email': 'jairupa2007@gmail.com',
        'phone': '+91 93619 43344',
        'status': 'Pending',
        'notes': 'Verified official portal (jairupa.in), institutional email and mobile.'
    },
    'Jamal Mohamed College of Teacher Education': {
        'website': 'https://www.jmc.edu/B.Ed',
        'contact': 'Office of Admissions & Leadership (Trichy)',
        'email': 'princi_bed@yahoo.com',
        'phone': '0431-2333135',
        'status': 'Pending',
        'notes': 'Verified official portal (jmc.edu/B.Ed), institutional email and phone.'
    },
    'Jamal Mohammed College': {
        'website': 'https://www.jmc.edu',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'princi@jmc.edu',
        'phone': '0431-2331135',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (jmc.edu), principal email and phone.'
    },
    'Jamia Darussalam Arabic College': {
        'website': 'https://jdsacollege.in',
        'contact': 'Office of Admissions & Principal (Oomerabad)',
        'email': 'jamiaoomerabad@gmail.com',
        'phone': '+91 63857 01904',
        'status': 'Pending',
        'notes': 'Verified official portal (jdsacollege.in), institutional email and phone.'
    },
    'Jawahar Science College': {
        'website': 'https://www.jsc104.net',
        'contact': 'Office of Admissions & Principal (Neyveli)',
        'email': 'admin@jsc104.net',
        'phone': '04142-265814',
        'status': 'Pending',
        'notes': 'Verified official portal (jsc104.net), administrative email and phone.'
    },
    'Jawaharlal Nehru Women&#039;s College': {
        'website': 'https://jncw.in',
        'contact': 'Office of Admissions & Principal (Ulundurpet)',
        'email': 'jcwomen@gmail.com',
        'phone': '+91 93619 09060',
        'status': 'Pending',
        'notes': 'Verified official portal (jncw.in), institutional email and phone.'
    },
    'Jaya Arts and Science College for Women': {
        'website': 'https://jayagc.org',
        'contact': 'Office of Admissions (Thiruninravur)',
        'email': 'admission@jayagc.org',
        'phone': '+91 88074 50450',
        'status': 'Pending',
        'notes': 'Verified official portal (jayagc.org), admissions email and helpline.'
    },
    'Jaya College Of Arts &amp; Science (Co-Ed)': {
        'website': 'https://www.jcas.ac.in',
        'contact': 'Office of Admissions & Principal (Thiruninravur)',
        'email': 'info@jcas.ac.in',
        'phone': '+91 85310 77777',
        'status': 'Pending',
        'notes': 'Verified official portal (jcas.ac.in), institutional email and phone.'
    },
    'Jaya College of Education': {
        'website': 'http://www.jayacollegeofeducation.com',
        'contact': 'Office of Admissions & Leadership (Thiruninravur)',
        'email': 'info@jayacollegeofeducation.com',
        'phone': '044-26344282',
        'status': 'Pending',
        'notes': 'Verified official portal (jayacollegeofeducation.com), institutional email and phone.'
    },
    'JAYAGOVIND HARIGOPAL AGARWAL AGARSEN': {
        'website': 'https://www.agarsencollege.com',
        'contact': 'Office of Admissions & Principal (Madhavaram)',
        'email': 'contact@agarsencollege.com',
        'phone': '+91 89255 02753',
        'status': 'Pending',
        'notes': 'Verified official portal (agarsencollege.com), institutional email and helpline.'
    },
    'Jayalakshmi Narayanaswami College of Education': {
        'website': 'https://www.jncedu.in',
        'contact': 'Office of Admissions & Principal (Tharamani)',
        'email': 'jnceducation@gmail.com',
        'phone': '+91 73055 85596',
        'status': 'Pending',
        'notes': 'Verified official portal (jncedu.in), institutional email and phone.'
    },
    'Jayam Arts and Science College': {
        'website': 'https://jac.ac.in',
        'contact': 'Office of Admissions & Principal (Nallanur)',
        'email': 'principal@jac.ac.in',
        'phone': '+91 94899 14800',
        'status': 'Pending',
        'notes': 'Verified official portal (jac.ac.in), principal email and mobile.'
    },
    'Jayam College of Education': {
        'website': 'http://www.jayamcoledn.com',
        'contact': 'Office of Admissions & Principal (Kilpennathur)',
        'email': 'jayambedcollege@gmail.com',
        'phone': '+91 99941 87033',
        'status': 'Pending',
        'notes': 'Verified official portal (jayamcoledn.com), verified email and mobile.'
    },
    'Jayanthi College of Education': {
        'website': 'http://jayanthicollege.in',
        'contact': 'Office of Admissions & Principal (Arulpuram)',
        'email': 'jayanthicollege@gmail.com',
        'phone': '+91 94421 06944',
        'status': 'Pending',
        'notes': 'Verified official portal (jayanthicollege.in), institutional email and phone.'
    },
    'Jayaraj Annapackiam College': {
        'website': 'https://www.annejac.ac.in',
        'contact': 'Office of the Principal (Periyakulam)',
        'email': 'principal@annejac.ac.in',
        'phone': '04546-231482',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (annejac.ac.in), principal email and phone.'
    },
    'Jayarani Arts and Science(Women)College': {
        'website': 'https://www.jcs.edu.in',
        'contact': 'Office of Admissions & Principal (Nethimedu)',
        'email': 'info@jcs.edu.in',
        'phone': '+91 91500 99240',
        'status': 'Pending',
        'notes': 'Verified official portal (jcs.edu.in), institutional email and phone.'
    },
    'Jayasanthi B.Ed. College': {
        'website': 'https://www.jayasanthibedcollege.com',
        'contact': 'Office of Admissions & Principal (Anthiyur)',
        'email': 'jayasanthibedcollege@gmail.com',
        'phone': '04256-290759',
        'status': 'Pending',
        'notes': 'Verified official portal (jayasanthibedcollege.com), institutional email and phone.'
    },
    'JCT College of Arts and Science': {
        'website': 'https://www.jct.ac.in',
        'contact': 'Office of Admissions & Principal (Pichanur)',
        'email': 'info@jct.ac.in',
        'phone': '+91 93614 88801',
        'status': 'Pending',
        'notes': 'Verified official portal (jct.ac.in), institutional email and helpline.'
    },
    'JENNEY&#039;S COLLEGE OF EDUCATION': {
        'website': 'https://jenneysedu.in',
        'contact': 'Office of Admissions & Principal (Ramjee Nagar)',
        'email': 'jcetrichy@gmail.com',
        'phone': '+91 63698 38741',
        'status': 'Pending',
        'notes': 'Verified official portal (jenneysedu.in), verified email and mobile.'
    },
    'Jeppiaar College of Arts and Science': {
        'website': 'https://jeppiaararts.in',
        'contact': 'Office of Admissions & Principal (Padur)',
        'email': 'admin@jeppiaararts.in',
        'phone': '+91 73700 87008',
        'status': 'Pending',
        'notes': 'Verified official portal (jeppiaararts.in), administrative email and phone.'
    },
    'Jesu Arts and Science College': {
        'website': 'https://www.jgroupseducational.com',
        'contact': 'Office of Admissions & Principal (Alangudi)',
        'email': 'princissba@bdu.ac.in',
        'phone': 'Not publicly listed from official sources',
        'status': 'Pending',
        'notes': 'Verified via university affiliation and registry, official email listed.'
    },
    'JJ College. Of Arts &amp; Sci': {
        'website': 'https://jjcoll.in',
        'contact': 'Office of Admissions & Principal (Sivapuram)',
        'email': 'jjcollege.pdkt@gmail.com',
        'phone': '+91 79041 51908',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (jjcoll.in), verified email and mobile.'
    },
    'JKK Nattraja College of Education': {
        'website': 'https://edu.jkkn.ac.in',
        'contact': 'Office of Admissions & Principal (Komarapalayam)',
        'email': 'education@jkkn.ac.in',
        'phone': '+91 93458 55001',
        'status': 'Pending',
        'notes': 'Verified official portal (edu.jkkn.ac.in), institutional email and phone.'
    },
    'JNN Arts and Science College (Women)': {
        'website': 'https://www.jnncollege.edu.in',
        'contact': 'Office of Admissions & Principal (Kannigaipair)',
        'email': 'info@jnncollege.edu.in',
        'phone': '+91 96000 57121',
        'status': 'Pending',
        'notes': 'Verified official portal (jnncollege.edu.in), institutional email and phone.'
    },
    'John Bosco Arts And Science College': {
        'website': 'http://www.johnbosco.ac.in',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'chairmanjbc@gmail.com',
        'phone': '044-27600611',
        'status': 'Pending',
        'notes': 'Verified official portal (johnbosco.ac.in), institutional email and phone.'
    },
    'John Dewey College of Arts and Science for Women': {
        'website': 'https://www.johndeweywomenscollege.com',
        'contact': 'Office of Admissions & Principal (Panruti)',
        'email': 'johndeweywomencollege@gmail.com',
        'phone': '+91 72009 47378',
        'status': 'Pending',
        'notes': 'Verified official portal (johndeweywomenscollege.com), verified email and mobile.'
    },
    'JOSEPH ARTS AND SCIENCE COLLEGE': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120092',
        'contact': 'Office of Admissions & Principal (Thirunavalur)',
        'email': 'josephcollege2011@gmail.com',
        'phone': '+91 94440 59986',
        'status': 'Pending',
        'notes': 'Verified via university affiliation and educational registry, verified email and mobile.'
    },
    'Jothis College': {
        'website': 'https://www.jothiscollege.org',
        'contact': 'Office of Admissions & Principal (Katpadi)',
        'email': 'jothiscollege@gmail.com',
        'phone': '+91 86670 98528',
        'status': 'Pending',
        'notes': 'Verified official portal (jothiscollege.org), verified email and mobile.'
    },
    'JSR College of Education': {
        'website': 'https://www.jsrcollege.co.in',
        'contact': 'Office of Admissions & Principal (Madathukulam)',
        'email': 'Not publicly listed from official sources',
        'phone': 'Not publicly listed from official sources',
        'status': 'Pending',
        'notes': 'Verified institutional registry, details not publicly listed from official sources.'
    },
    'Justice Basheer Ahmed Sayeed College for Women': {
        'website': 'https://www.jbascollege.edu.in',
        'contact': 'Office of the Principal & Admissions (Teynampet)',
        'email': 'jbascollege@gmail.com',
        'phone': '+91 44 24364152',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (jbascollege.edu.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_7_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_7_COLLEGES)}")
    unmatched = set(BATCH_7_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
