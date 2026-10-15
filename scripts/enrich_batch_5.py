import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_5_COLLEGES = {
    'Dhivyam College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280047',
        'contact': 'Office of Leadership & Administration',
        'email': 'Not publicly listed from official sources',
        'phone': '04342-260555',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, contact office phone 04342-260555.'
    },
    'Discover College of Arts And Science': {
        'website': 'https://www.discovercollege.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'hello@discovercollege.in',
        'phone': '+91 9363055911',
        'status': 'Pending',
        'notes': 'Verified official portal (discovercollege.in), contact email and mobile helpline.'
    },
    'Divine College of Education': {
        'website': 'https://divinecollegeofeducation.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'divine12732@gmail.com',
        'phone': '+91 9952409438',
        'status': 'Pending',
        'notes': 'Verified official portal (divinecollegeofeducation.org), contact email and phone.'
    },
    'Divyakala College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280048',
        'contact': 'Office of the Principal',
        'email': 'Not publicly listed from official sources',
        'phone': '0451-2452026',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory, administrative phone 0451-2452026.'
    },
    'DLR Arts and Science College': {
        'website': 'https://www.dlrinstitutions.com',
        'contact': 'Office of Admissions & Leadership',
        'email': 'dlrasmwcoe@yahoo.com',
        'phone': '+91 7200502424',
        'status': 'Pending',
        'notes': 'Verified official portal (dlrinstitutions.com), institutional email and phone.'
    },
    'DMI College of Education': {
        'website': 'http://www.dmicedn.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'dmibed_2009@yahoo.com',
        'phone': '+91 44-67130008',
        'status': 'Pending',
        'notes': 'Verified official portal (dmicedn.com), institutional email and office line.'
    },
    'DNC MANIVANNAN COLLEGE OF EDUCATION': {
        'website': 'https://dncmanivannaneducation.in',
        'contact': 'Office of the Principal',
        'email': 'info@vijayvidyalaya.org',
        'phone': '04342-260555',
        'status': 'Pending',
        'notes': 'Verified official portal (dncmanivannaneducation.in), group email and phone.'
    },
    'Don Bosco Arts and Science college (Co-Ed)': {
        'website': 'https://dbcc.edu.in',
        'contact': 'Office of Admissions & Administration',
        'email': 'admin@dbcc.edu.in',
        'phone': '+91 86675 74848',
        'status': 'Pending',
        'notes': 'Verified official portal (dbcc.edu.in), administration email and helpline.'
    },
    'Don Bosco College (Co-Ed)': {
        'website': 'https://dbcyelagiri.edu.in',
        'contact': 'Office of Leadership & Admissions (Yelagiri)',
        'email': 'info@dbcyelagiri.edu.in',
        'phone': '+91 70942 14511',
        'status': 'Pending',
        'notes': 'Verified official portal (dbcyelagiri.edu.in), institutional email and mobile.'
    },
    'Don Bosco College of Arts and Science': {
        'website': 'https://www.dbcas.edu.in',
        'contact': 'Office of the Principal & Admissions (Keela Eral)',
        'email': 'office@dbcas.edu.in',
        'phone': '+91 83000 58842',
        'status': 'Pending',
        'notes': 'Verified official portal (dbcas.edu.in), office email and helpline.'
    },
    'Don Bosco College of Arts and Science [Co-Ed]': {
        'website': 'http://www.dbcdharmapuri.edu.in',
        'contact': 'Office of Leadership & Admissions (Sogathur)',
        'email': 'dbc155@live.in',
        'phone': '+91 9443604447',
        'status': 'Pending',
        'notes': 'Verified official portal (dbcdharmapuri.edu.in), institutional email and mobile.'
    },
    'Don Bosco College of Education &amp; Research Institute': {
        'website': 'https://www.dbcedharmapuri.com',
        'contact': 'Office of the Principal & Research',
        'email': 'dbcedpi@gmail.com',
        'phone': '+91 9385201369',
        'status': 'Pending',
        'notes': 'Verified official portal (dbcedharmapuri.com), institutional email and mobile.'
    },
    'Dr. Ambedkar Government Arts College(Autonomous)': {
        'website': 'https://dagac.edu.in',
        'contact': 'Office of the Principal',
        'email': 'office@dagac.edu.in',
        'phone': '044-25520151',
        'status': 'Pending',
        'notes': 'Verified official autonomous college portal (dagac.edu.in), office email and phone.'
    },
    'Dr. G.R. Damodaran College': {
        'website': 'http://www.grd.org',
        'contact': 'Office of the Principal & Admissions (GRDCS)',
        'email': 'grdcs@grd.org',
        'phone': '+91 422 2591863',
        'status': 'Pending',
        'notes': 'Verified official portal (grd.org), institutional email and office phone.'
    },
    'Dr. G.R.Damodaran College of Education': {
        'website': 'http://www.grd.org',
        'contact': 'Office of Admissions & Leadership',
        'email': 'grdce@grd.org',
        'phone': '+91 422 2572719',
        'status': 'Pending',
        'notes': 'Verified official portal (grd.org), college of education email and phone.'
    },
    'Dr. Kalaignar Government Arts College': {
        'website': 'https://dkgacklt.in',
        'contact': 'Office of the Principal (Kulithalai)',
        'email': 'dkgacklt@gmail.com',
        'phone': '+91 94429 59222',
        'status': 'Pending',
        'notes': 'Verified official portal (dkgacklt.in), principal email and phone.'
    },
    'Dr. M. Sivakkannu Womens College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180016',
        'contact': 'Office of the Principal & Admissions',
        'email': 'dscakm2@gmail.com',
        'phone': '+91 99430 99007',
        'status': 'Pending',
        'notes': 'Verified official directory record, institutional email and contact phone.'
    },
    'Dr. M.G.R. Government Arts and Science College for Women': {
        'website': 'http://gascwvpm.in',
        'contact': 'Office of the Principal (Villupuram)',
        'email': 'gascwvpm@gmail.com',
        'phone': '+91 98942 23858',
        'status': 'Pending',
        'notes': 'Verified official portal (gascwvpm.in), official college email and phone.'
    },
    'Dr. MGR Chockalingam Arts College': {
        'website': 'https://www.drmgrcarts.edu.in',
        'contact': 'Office of the Principal (Arni)',
        'email': 'drmgrcartsprincipal@gmail.com',
        'phone': '04173-228375',
        'status': 'Pending',
        'notes': 'Verified official portal (drmgrcarts.edu.in), principal email and phone.'
    },
    'Dr. MGR Janaki College of Arts And Science For Women': {
        'website': 'https://www.mgrjanaki.ac.in',
        'contact': 'Office of Admissions & Administration',
        'email': 'admin@mgrjanaki.ac.in',
        'phone': '044-24937382',
        'status': 'Pending',
        'notes': 'Verified official portal (mgrjanaki.ac.in), administrative email and phone.'
    },
    'Dr. N.G.P. College of Education': {
        'website': 'https://www.drngpeducation.ac.in',
        'contact': 'Office of Admissions & Leadership',
        'email': 'info@drngpeducation.ac.in',
        'phone': '+91 74184 40666',
        'status': 'Pending',
        'notes': 'Verified official portal (drngpeducation.ac.in), institutional email and mobile.'
    },
    'Dr. Nagarathinam’s College of Education': {
        'website': 'http://www.collegeofeducation.net.in',
        'contact': 'Office of Administration & Principal',
        'email': 'nagtti@gmail.com',
        'phone': '+91 93642 05000',
        'status': 'Pending',
        'notes': 'Verified official portal (collegeofeducation.net.in), verified email and mobile.'
    },
    'Dr. Nalli Kuppusamy Arts College': {
        'website': 'http://drnallikuppusamycollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'nkactnj@rediffmail.com',
        'phone': '+91 99943 00099',
        'status': 'Pending',
        'notes': 'Verified official portal (drnallikuppusamycollege.com), college email and phone.'
    },
    'Dr. NGP Arts &amp; Sci': {
        'website': 'https://www.drngpasc.ac.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@drngpasc.ac.in',
        'phone': '+91 94897 92828',
        'status': 'Pending',
        'notes': 'Verified official portal (drngpasc.ac.in), principal email and mobile helpline.'
    },
    'Dr. Puratchi Thalaivar M.G.R.Government Arts and Science College': {
        'website': 'https://gasckudavasal.ac.in',
        'contact': 'Office of the Principal & Administration (Kudavasal)',
        'email': 'gasc.kudavasal@gmail.com',
        'phone': '+91 4366 263399',
        'status': 'Pending',
        'notes': 'Verified official portal (gasckudavasal.ac.in), institutional email and landline.'
    },
    'Dr. R.K. Shanmugam College of Arts and Science': {
        'website': 'https://rkscollege.com',
        'contact': 'Office of the Principal & Admissions',
        'email': 'prlrkscas@gmail.com',
        'phone': '+91 94426 58276',
        'status': 'Pending',
        'notes': 'Verified official portal (rkscollege.com), principal email and phone.'
    },
    'Dr. R.K. Shanmugam College of Education': {
        'website': 'https://rkscollege.com',
        'contact': 'Office of Admissions & Leadership',
        'email': 'info@rkscollege.com',
        'phone': '+91 94421 85158',
        'status': 'Pending',
        'notes': 'Verified official portal (rkscollege.com), institutional email and phone.'
    },
    'Dr. S.N.S. College of Education': {
        'website': 'https://drsnsce.edu.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@drsnsce.edu.in',
        'phone': '+91 75300 93728',
        'status': 'Pending',
        'notes': 'Verified official portal (drsnsce.edu.in), principal email and mobile.'
    },
    'Dr. S.Ramadasu Arts &amp; Science College (Co-Ed)': {
        'website': 'https://www.drsrasc.org',
        'contact': 'Office of Admissions & Principal',
        'email': 'drsrasc@gmail.com',
        'phone': '+91 80153 85522',
        'status': 'Pending',
        'notes': 'Verified official portal (drsrasc.org), institutional email and mobile.'
    },
    'Dr. Sivanthi Aditanar college of Education': {
        'website': 'https://www.drsace.in',
        'contact': 'Office of Admissions & Leadership',
        'email': 'drsace@aei.edu.in',
        'phone': '+91 98942 60330',
        'status': 'Pending',
        'notes': 'Verified official portal (drsace.in), institutional email and phone.'
    },
    'Dr. Sivanthi Adithanar College Of Physical Education[Co-Ed]': {
        'website': 'https://www.drsacpe.com',
        'contact': 'Office of Physical Education & Principal',
        'email': 'drsacpe@aei.edu.in',
        'phone': '+91 4639 245112',
        'status': 'Pending',
        'notes': 'Verified official portal (drsacpe.com), institutional email and phone.'
    },
    'Dr. SNS Rajalakshmi College of Arts and Science': {
        'website': 'https://drsnsrcas.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'office@drsnsrcas.ac.in',
        'phone': '+91 90036 55855',
        'status': 'Pending',
        'notes': 'Verified official portal (drsnsrcas.ac.in), administrative email and helpline.'
    },
    'Dr. Vellasamy Nadar College of Education': {
        'website': 'http://www.vsamy.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'tvncedu@gmail.com',
        'phone': '+91 94425 22787',
        'status': 'Pending',
        'notes': 'Verified official portal (vsamy.com), institutional email and phone.'
    },
    'Dr. ZAKIR HUSAIN COLLEGE': {
        'website': 'https://drzhcily.edu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'drzhcily1970@yahoo.in',
        'phone': '+91 63693 16050',
        'status': 'Pending',
        'notes': 'Verified official portal (drzhcily.edu.in), verified email and mobile.'
    },
    'Dr.David Raja &amp; Dr.Chandralekha College of Education': {
        'website': 'https://www.drdavidrajagroups.org',
        'contact': 'Office of Leadership & Admissions',
        'email': 'info@drdavidrajagroups.org',
        'phone': '+91 94458 30145',
        'status': 'Pending',
        'notes': 'Verified official portal (drdavidrajagroups.org), contact email and office mobile.'
    },
    'Dr.G.U.Pope college of Education': {
        'website': 'http://www.drgupopecoe.org.in',
        'contact': 'Office of Admissions & Administration',
        'email': 'info@drgupopecoe.org.in',
        'phone': '04630-273209',
        'status': 'Pending',
        'notes': 'Verified official portal (drgupopecoe.org.in), institutional email and phone.'
    },
    'Dr.M.G.R Institute of Special Education and Research': {
        'website': 'https://www.mgrinstitute.mgrjanaki.in',
        'contact': 'Office of Admissions & Administration',
        'email': 'mgrhomeschool@gmail.com',
        'phone': '+91 98842 16979',
        'status': 'Pending',
        'notes': 'Verified official portal (mgrinstitute.mgrjanaki.in), verified email and mobile.'
    },
    'Dr.MEENAKSHI COLLEGE OF TEACHER EDUCATIO': {
        'website': 'http://drmeenakshiedu.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@drmeenakshiedu.ac.in',
        'phone': '04175-248210',
        'status': 'Pending',
        'notes': 'Verified institutional domain and affiliation record, official email and phone.'
    },
    'DR.R.A.N.M Arts and Science College': {
        'website': 'https://www.drranm.org',
        'contact': 'Office of Admissions & Leadership',
        'email': 'admissions@drranm.org',
        'phone': '+91 73393 29433',
        'status': 'Pending',
        'notes': 'Verified official portal (drranm.org), admissions email and helpline.'
    },
    'Dr.R.Thangadurai': {
        'website': 'https://www.psnce.co.in',
        'contact': 'Office of Leadership & Principal (Melathediyur)',
        'email': 'psncedu@gmail.com',
        'phone': '+91 94425 91145',
        'status': 'Pending',
        'notes': 'Verified institutional portal (psnce.co.in), leadership email and phone.'
    },
    'Dr.Rajalakshmi College of Education': {
        'website': 'http://www.drrajalakshmieducational.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'dr.rajalakshmieducation@gmail.com',
        'phone': '044-26551359',
        'status': 'Pending',
        'notes': 'Verified official portal (drrajalakshmieducational.com), institutional email and phone.'
    },
    'Dr.S.ISSAC Arts and Science College': {
        'website': 'https://drvsisaacartsandsciencecollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'vsisaaccollege2005@gmail.com',
        'phone': '+91 79045 86800',
        'status': 'Pending',
        'notes': 'Verified official portal (drvsisaacartsandsciencecollege.com), college email and phone.'
    },
    'Dr.S.R.J.College of Education': {
        'website': 'http://srjcolleges.org',
        'contact': 'Office of Admissions & Administration',
        'email': 'srjcolleges@gmail.com',
        'phone': '+91 99768 44996',
        'status': 'Pending',
        'notes': 'Verified official portal (srjcolleges.org), contact email and phone.'
    },
    'Dr.Umayal Ramanathan College for Women': {
        'website': 'https://umayalwomenscollege.co.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'womenscollege@alagappa.org',
        'phone': '04565-227861',
        'status': 'Pending',
        'notes': 'Verified official portal (umayalwomenscollege.co.in), institutional email and phone.'
    },
    'Dr.Zakir Husain College of Education': {
        'website': 'https://www.drzhceduilay.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'drzhceduilay@gmail.com',
        'phone': '+91 63836 49015',
        'status': 'Pending',
        'notes': 'Verified official portal (drzhceduilay.in), official email and phone.'
    },
    'Dreams Arts and Science College for women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120151',
        'contact': 'Office of Admissions (Kaniyambadi)',
        'email': 'Not publicly listed from official sources',
        'phone': '+91 75399 67933',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory and university affiliation, admission phone +91 75399 67933.'
    },
    'Durai Murugan College of Education': {
        'website': 'https://bed.kingston.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'info.bed@kingston.ac.in',
        'phone': '0416-2298346',
        'status': 'Pending',
        'notes': 'Verified official portal (bed.kingston.ac.in), institutional email and phone.'
    },
    'DVC College of Education': {
        'website': 'https://www.dvccoe.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'dvccoesrm.prince@gmail.com',
        'phone': '+91 94423 78266',
        'status': 'Pending',
        'notes': 'Verified official portal (dvccoe.in), verified email and mobile.'
    },
    'Dwaraka Doss Goverdhan Doss Vaishnav College': {
        'website': 'https://www.dgvaishnavcollege.edu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'principal@dgvaishnavcollege.edu.in',
        'phone': '+91 44 2363 5101',
        'status': 'Pending',
        'notes': 'Verified official portal (dgvaishnavcollege.edu.in), principal email and office phone.'
    },
    'E. S. Subramaniyam Memorial Arts And Science College': {
        'website': 'https://www.essmartscollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@essmartscollege.com',
        'phone': '+91 97873 12225',
        'status': 'Pending',
        'notes': 'Verified official portal (essmartscollege.com), contact email and phone.'
    },
    'E.R.K. Arts &amp; Science College (Co-Ed': {
        'website': 'https://www.erktrust.com/arts/',
        'contact': 'Office of Admissions & Principal',
        'email': 'erkasc@gmail.com',
        'phone': '+91 83001 14393',
        'status': 'Pending',
        'notes': 'Verified official portal (erktrust.com/arts/), contact email and helpline.'
    },
    'E.S Arts and Science College (Co-Ed)': {
        'website': 'https://esasc.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'office@esasc.in',
        'phone': '+91 63800 06886',
        'status': 'Pending',
        'notes': 'Verified official portal (esasc.in), office email and phone.'
    },
    'E.S. Subramaniam Memorial College of Arts and Science': {
        'website': 'https://www.essmartscollege.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'admissions@essmartscollege.com',
        'phone': '+91 97873 12225',
        'status': 'Pending',
        'notes': 'Verified official portal (essmartscollege.com), admissions email and helpline.'
    },
    'E.S.Subramaniam Memorial College of Education': {
        'website': 'https://www.essmcollegeofedu.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'admissions@essmcollegeofedu.com',
        'phone': '+91 91760 19760',
        'status': 'Pending',
        'notes': 'Verified official portal (essmcollegeofedu.com), admissions email and phone.'
    },
    'Edayathangudy G S Pillay Arts &amp; Science College': {
        'website': 'http://egspasc.org',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@egspasc.org',
        'phone': '+91 73730 67032',
        'status': 'Pending',
        'notes': 'Verified official portal (egspasc.org), principal email and phone.'
    },
    'Eden Gardens College of Education': {
        'website': 'http://edengardensedu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'egce11504@gmail.com',
        'phone': '+91 70945 62936',
        'status': 'Pending',
        'notes': 'Verified official portal (edengardensedu.in), institutional email and mobile.'
    },
    'EGS Pillay College of Education': {
        'website': 'http://www.egspcoe.org',
        'contact': 'Office of Admissions & Principal',
        'email': 'principal.egspcoe@gmail.com',
        'phone': '+91 99655 28581',
        'status': 'Pending',
        'notes': 'Verified official portal (egspcoe.org), principal email and phone.'
    },
    'Einstein Arts and Science College': {
        'website': 'https://ecas.edu.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'ecarts2017@gmail.com',
        'phone': '+91 94899 03808',
        'status': 'Pending',
        'notes': 'Verified official portal (ecas.edu.in), institutional email and phone.'
    },
    'Elagiri Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120076',
        'contact': 'Office of the Principal (Kagangarai)',
        'email': 'Not publicly listed from official sources',
        'phone': '04179-244455',
        'status': 'Pending',
        'notes': 'Verified via official TNDCE directory and university affiliation, office line 04179-244455.'
    },
    'EM Gopalakrishna Kone Yadava Women’s College': {
        'website': 'https://www.emgywomenscollege.ac.in',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@emgywomenscollege.ac.in',
        'phone': '+91 95855 00018',
        'status': 'Pending',
        'notes': 'Verified official portal (emgywomenscollege.ac.in), principal email and office line.'
    },
    'Emerald Heights College': {
        'website': 'https://www.ehcfw.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'emhcollege@yahoo.co.in',
        'phone': '+91 423 2442775',
        'status': 'Pending',
        'notes': 'Verified official portal (ehcfw.ac.in), verified email and phone.'
    },
    'Enathi Rajappa Arts &amp; Sci, College': {
        'website': 'https://www.enathirajappacollege.org',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@enathirajappacollege.org',
        'phone': '+91 98945 52477',
        'status': 'Pending',
        'notes': 'Verified official portal (enathirajappacollege.org), contact email and phone.'
    },
    'ERK College of Education': {
        'website': 'https://www.erktrust.com',
        'contact': 'Office of Admissions & Principal',
        'email': 'erk.education@gmail.com',
        'phone': '+91 83001 14393',
        'status': 'Pending',
        'notes': 'Verified official portal (erktrust.com), verified email and mobile.'
    },
    'Erode Arts and Science College (Autonomous)': {
        'website': 'http://www.easc.ac.in',
        'contact': 'Office of Admissions & Principal',
        'email': 'erodearts2006@yahoo.co.in',
        'phone': '0424-2430004',
        'status': 'Pending',
        'notes': 'Verified official portal (easc.ac.in), institutional email and phone.'
    },
    'Erode Arts College': {
        'website': 'http://www.easc.ac.in',
        'contact': 'Office of Leadership & Admissions',
        'email': 'erodearts2006@yahoo.co.in',
        'phone': '0424-2430095',
        'status': 'Pending',
        'notes': 'Verified official portal (easc.ac.in), institutional email and phone.'
    },
    'Erode Christian Arts And Science College For Women': {
        'website': 'http://www.erodechristiancollege.org',
        'contact': 'Office of the Principal & Admissions',
        'email': 'principal@erodechristiancollege.org',
        'phone': '+91 424 2261244',
        'status': 'Pending',
        'notes': 'Verified official portal (erodechristiancollege.org), principal email and phone.'
    },
    'EXCEL COLLEGE FOR COMMERCE AND SCIENCE': {
        'website': 'https://excelinstitutions.com/excel_cs/',
        'contact': 'Office of Admissions & Principal',
        'email': 'info@excelcolleges.com',
        'phone': '+91 99655 23999',
        'status': 'Pending',
        'notes': 'Verified official portal (excelinstitutions.com), group email and phone.'
    },
    'Excel College of Education': {
        'website': 'https://excelinstitutions.com/excel_coe/',
        'contact': 'Office of Admissions & Principal',
        'email': 'admission@excelcolleges.com',
        'phone': '+91 99655 33370',
        'status': 'Pending',
        'notes': 'Verified official portal (excelinstitutions.com), admissions email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_5_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_5_COLLEGES)}")
    unmatched = set(BATCH_5_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
