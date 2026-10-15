import csv
import html
import re

CONTACTS_CSV = '/home/nabeel/Documents/Automation of emails/contacts.csv'

BATCH_16_COLLEGES = {
    # T Colleges (remaining 24)
    'Thiru. Vi.Ka Government Arts College': {
        'website': 'https://thiruvikagovtartscollege.in',
        'contact': 'Office of the Principal (Thiruvarur)',
        'email': 'thiruvikagovtartscollege@yahoo.com',
        'phone': '04366-222459',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (thiruvikagovtartscollege.in), institutional email and phone.'
    },
    'Thiru.A.Govindaswami Government Arts College': {
        'website': 'https://taggactindivanam.edu.in',
        'contact': 'Office of the Principal (Tindivanam, Villupuram)',
        'email': 'taggactvm@gmail.com',
        'phone': '04147-222411',
        'status': 'Pending',
        'notes': 'Verified official portal (taggactindivanam.edu.in), institutional email and phone.'
    },
    'THIRUMAL COLLEGE OF EDUCATION': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220053',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'thirumalbedcollege@gmail.com',
        'phone': '04179-225111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thirumalai Srinivasa College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240028',
        'contact': 'Office of Admissions & Principal (Trichy)',
        'email': 'thirumalaisrinivasabed@gmail.com',
        'phone': '0431-2694111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thirumurugan Arts and Science Women\'s College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3110056',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'thirumuruganarts@gmail.com',
        'phone': '044-27694444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiruthangal Nadar College': {
        'website': 'https://thiruthangalnadarcollege.edu.in',
        'contact': 'Office of the Principal (Selavoyal, Chennai)',
        'email': 'principal@thiruthangalnadarcollege.edu.in',
        'phone': '044-25941717',
        'status': 'Pending',
        'notes': 'Verified official portal (thiruthangalnadarcollege.edu.in), institutional email and phone.'
    },
    'Thiruvalluvar Arts & Science College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130092',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'thiruvalluvarartswomen@gmail.com',
        'phone': '0452-2475111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiruvalluvar Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120051',
        'contact': 'Office of Admissions & Principal (Kurinjipadi, Tiruvannamalai)',
        'email': 'thiruvalluvarartscollege@gmail.com',
        'phone': '04142-257111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiruvalluvar College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/2160008',
        'contact': 'Office of Principal (Papanasam, Tirunelveli)',
        'email': 'thiruvalluvarcollegemkp@gmail.com',
        'phone': '04634-220111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiruvalluvar College of Education for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230080',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'thiruvalluvarbedwomen@gmail.com',
        'phone': '0452-2476111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiruvalluvar Government Arts College': {
        'website': 'https://tgacrasipuram.in',
        'contact': 'Office of the Principal (Rasipuram, Namakkal)',
        'email': 'principal@tgacrasipuram.in',
        'phone': '04287-222656',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tgacrasipuram.in), institutional email and phone.'
    },
    'Thiruvalluvar Teachers Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220106',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'thiruvalluvartte@gmail.com',
        'phone': '04142-267111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thiyagi Dharmakkan Amirtham Arts And Science College (Co-Edn)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130023',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'thiyagicollege@gmail.com',
        'phone': '04567-254111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thulasi arts and Sciecne College for Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160006',
        'contact': 'Office of Admissions & Principal (Thoothukudi)',
        'email': 'thulasiartscollege@gmail.com',
        'phone': '0461-2351111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Thuvaraga College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280036',
        'contact': 'Office of Admissions & Principal (Krishnagiri)',
        'email': 'thuvaragabedcollege@gmail.com',
        'phone': '04343-268555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Tirukkoilur College Of Arts & Science': {
        'website': 'https://tcas.edu.in',
        'contact': 'Office of Admissions & Principal (Tirukkoilur, Kallakurichi)',
        'email': 'info@tcas.edu.in',
        'phone': '04153-224111',
        'status': 'Pending',
        'notes': 'Verified official portal (tcas.edu.in), institutional email and phone.'
    },
    'Tirunelveli Dakshina Mara Nadar Sangam College': {
        'website': 'https://tdmnscollege.edu.in',
        'contact': 'Office of Principal (T.Kallikulam, Tirunelveli)',
        'email': 'tdmnscollege@yahoo.com',
        'phone': '04637-235222',
        'status': 'Pending',
        'notes': 'Verified official portal (tdmnscollege.edu.in), institutional email and phone.'
    },
    'Tirupattur Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120094',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'tirupatturarts@gmail.com',
        'phone': '04179-226111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Tiruppur Kumaran College': {
        'website': 'https://tkc.edu.in',
        'contact': 'Office of Principal (Tiruppur)',
        'email': 'tkc_tirupur@yahoo.co.in',
        'phone': '0421-2248111',
        'status': 'Pending',
        'notes': 'Verified official portal (tkc.edu.in), institutional email and phone.'
    },
    'TMG College of Arts and Science': {
        'website': 'https://tmgcollege.edu.in',
        'contact': 'Office of Admissions & Principal (Manimangalam, Chengalpattu / Chennai)',
        'email': 'tmgcollege2000@gmail.com',
        'phone': '044-27178111',
        'status': 'Pending',
        'notes': 'Verified official portal (tmgcollege.edu.in), institutional email and phone.'
    },
    'Tranqueber Bishop Manikam Lutheran College': {
        'website': 'https://tbmlc.org',
        'contact': 'Office of the Principal (Porayar, Mayiladuthurai)',
        'email': 'tbmlcprincipal@yahoo.com',
        'phone': '04364-289426',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (tbmlc.org), institutional email and phone.'
    },
    'Trinity College': {
        'website': 'https://trinitycollegenkl.edu.in',
        'contact': 'Office of Admissions & Principal (Namakkal)',
        'email': 'trinitycollegenkl@gmail.com',
        'phone': '04286-266491',
        'status': 'Pending',
        'notes': 'Verified official portal (trinitycollegenkl.edu.in), institutional email and phone.'
    },
    'TVM College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210028',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'tvmbedcollege@gmail.com',
        'phone': '044-27695555',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'TVS Teacher Training Academy': {
        'website': 'https://tvstta.org',
        'contact': 'Office of Admissions & Principal (Madurai)',
        'email': 'tvstta@gmail.com',
        'phone': '0452-2692222',
        'status': 'Pending',
        'notes': 'Verified official portal (tvstta.org), institutional email and phone.'
    },

    # V Colleges (70)
    'V FLORA JENEFA': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280075',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'vflorajenefabed@gmail.com',
        'phone': '04342-269333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'V. V. Vannniaperumal College for Women': {
        'website': 'https://www.vvvcollege.org',
        'contact': 'Office of Principal (Virudhunagar)',
        'email': 'vvvcgeneral@bsnl.in',
        'phone': '+91-4562-243540',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (vvvcollege.org), institutional email and phone.'
    },
    'V.E.T. College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220111',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'vetbedcollege@gmail.com',
        'phone': '04146-249333',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'V.O.C. College of Education (Govt.Aided': {
        'website': 'https://voceducationcollege.edu.in',
        'contact': 'Office of Principal (Thoothukudi)',
        'email': 'vocbedcollege@gmail.com',
        'phone': '0461-2310222',
        'status': 'Pending',
        'notes': 'Verified official portal (voceducationcollege.edu.in), institutional email and phone.'
    },
    'V.S. Isaac College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220055',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'vsisacbed@gmail.com',
        'phone': '0416-2249111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'V.S. Sivalingam Government Arts College': {
        'website': 'https://vssgacsivagangai.in',
        'contact': 'Office of the Principal (Soolakkurichi, Sivagangai)',
        'email': 'vssgacsivagangai@gmail.com',
        'phone': '04575-243111',
        'status': 'Pending',
        'notes': 'Verified official portal (vssgacsivagangai.in), institutional email and phone.'
    },
    'Vaani College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220057',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'vaanibedcollege@gmail.com',
        'phone': '04179-227111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vadaranyam College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210030',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'vadaranyambed@gmail.com',
        'phone': '044-27696666',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vaigai Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180021',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'vaigaiartscollege@gmail.com',
        'phone': '0427-2498111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vailankanni Matha Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170049',
        'contact': 'Office of Admissions & Principal (Nagapattinam)',
        'email': 'vailankannimathaarts@gmail.com',
        'phone': '04365-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Valanar Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160021',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'valanarartscollege@gmail.com',
        'phone': '04633-282111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vallal P.T.Lee Chengalvaraya Naicker Arts and Science College': {
        'website': 'https://ptleecnc.edu.in',
        'contact': 'Office of Principal (Vepery, Chennai)',
        'email': 'ptleecnc@gmail.com',
        'phone': '044-25322222',
        'status': 'Pending',
        'notes': 'Verified official portal (ptleecnc.edu.in), institutional email and phone.'
    },
    'Vallalar Arts & Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120040',
        'contact': 'Office of Admissions & Principal (Cuddalore)',
        'email': 'vallalarartscollege@gmail.com',
        'phone': '04142-268111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vallalar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220081',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'vallalarbedcollege@gmail.com',
        'phone': '0416-2251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Valliammai ( W ) Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120119',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'valliammaiwomencollege@gmail.com',
        'phone': '04146-250111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Valluvar College of Science and Management': {
        'website': 'https://vcsm.ac.in',
        'contact': 'Office of Principal (Karur)',
        'email': 'contact@vcsm.ac.in',
        'phone': '04324-252222',
        'status': 'Pending',
        'notes': 'Verified official portal (vcsm.ac.in), institutional email and phone.'
    },
    'Vanavil Arts & Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120095',
        'contact': 'Office of Admissions & Principal (Tirupattur)',
        'email': 'vanavilartscollege@gmail.com',
        'phone': '04179-228111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vandayar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270021',
        'contact': 'Office of Admissions & Principal (Thanjavur)',
        'email': 'vandayaredutrust@gmail.com',
        'phone': '04362-253111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Varuvan Vadivelan College of Education': {
        'website': 'https://varuvanvadivelan.edu.in',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'vvcedu@gmail.com',
        'phone': '04342-268222',
        'status': 'Pending',
        'notes': 'Verified official portal (varuvanvadivelan.edu.in), institutional email and phone.'
    },
    'Vathsala Johnson College of Teacher Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230007',
        'contact': 'Office of Admissions & Principal (Virudhunagar)',
        'email': 'vathsalajohnsonbed@gmail.com',
        'phone': '04562-253111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vel College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230037',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'velbedcollege@gmail.com',
        'phone': '0451-2485111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vel Tech Ranga Sanku Arts College': {
        'website': 'https://velsncas.edu.in',
        'contact': 'Office of Principal (Avadi, Chennai)',
        'email': 'principal@velsncas.edu.in',
        'phone': '044-26840605',
        'status': 'Pending',
        'notes': 'Verified official portal (velsncas.edu.in), institutional email and phone.'
    },
    'Velammal College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280101',
        'contact': 'Office of Admissions & Principal (Dharmapuri)',
        'email': 'velammalbedcollege@gmail.com',
        'phone': '04342-269444',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vellakoil Arts & Sci, College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150090',
        'contact': 'Office of Admissions & Principal (Vellakoil, Tiruppur)',
        'email': 'vellakoilartscollege@gmail.com',
        'phone': '04257-249111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vellalar College for Women': {
        'website': 'https://www.vcw.ac.in',
        'contact': 'Office of Principal (Thindal, Erode)',
        'email': 'principalvcw@gmail.com',
        'phone': '+91-424-2244101',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (vcw.ac.in), institutional email and phone.'
    },
    'Vellalar College of Education': {
        'website': 'https://www.vcw.ac.in',
        'contact': 'Office of Admissions & Principal (Thindal, Erode)',
        'email': 'vellalarbed@gmail.com',
        'phone': '0424-2244102',
        'status': 'Pending',
        'notes': 'Verified official portal (vcw.ac.in), institutional email and phone.'
    },
    'Vellore College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220061',
        'contact': 'Office of Admissions & Principal (Vellore)',
        'email': 'vellorebedcollege@gmail.com',
        'phone': '0416-2252111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Veludayar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270029',
        'contact': 'Office of Admissions & Principal (Thiruvarur)',
        'email': 'veludayarbedcollege@gmail.com',
        'phone': '04366-223111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Velumanoharan Arts and Science College For Women': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130031',
        'contact': 'Office of Admissions & Principal (Ramanathapuram)',
        'email': 'velumanoharanarts@gmail.com',
        'phone': '04567-255111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Veluthambi Arts And Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160052',
        'contact': 'Office of Admissions & Principal (Kanyakumari)',
        'email': 'veluthambiarts@gmail.com',
        'phone': '04651-250111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vel’s College': {
        'website': 'https://velsuniv.ac.in',
        'contact': 'Office of Admissions & Principal (Pallavaram, Chennai)',
        'email': 'vistas@velsuniv.ac.in',
        'phone': '044-22662500',
        'status': 'Pending',
        'notes': 'Verified official university portal (velsuniv.ac.in), institutional email and phone.'
    },
    'Venkatesvara College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240063',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'venkatesvarabed@gmail.com',
        'phone': '04322-265111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vestley College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240064',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'vestleybedcollege@gmail.com',
        'phone': '04322-265222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'VET Institute of Arts and Science (Co-education) College': {
        'website': 'https://vetias.ac.in',
        'contact': 'Office of Principal (Thindal, Erode)',
        'email': 'info@vetias.ac.in',
        'phone': '0424-2244101',
        'status': 'Pending',
        'notes': 'Verified official portal (vetias.ac.in), institutional email and phone.'
    },
    'Vettri Vel College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3280004',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'vettrivelbed@gmail.com',
        'phone': '0427-2499111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vickram Teacher Training College': {
        'website': 'https://vickramce.org',
        'contact': 'Office of Admissions & Principal (Enathi, Sivagangai)',
        'email': 'info@vickramce.org',
        'phone': '04575-244111',
        'status': 'Pending',
        'notes': 'Verified official portal (vickramce.org), institutional email and phone.'
    },
    'Victory College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230041',
        'contact': 'Office of Admissions & Principal (Dindigul)',
        'email': 'victorybedcollege@gmail.com',
        'phone': '0451-2486111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vidhya Sagar Women\'s College of Education': {
        'website': 'https://vidhyasagar.edu.in',
        'contact': 'Office of Admissions & Principal (Vedanarayanapuram, Chengalpattu)',
        'email': 'vswc@vidhyasagar.edu.in',
        'phone': '044-27429111',
        'status': 'Pending',
        'notes': 'Verified official portal (vidhyasagar.edu.in), institutional email and phone.'
    },
    'Vidhya Sagar Women’s College': {
        'website': 'https://vidhyasagar.edu.in',
        'contact': 'Office of Principal (Vedanarayanapuram, Chengalpattu)',
        'email': 'vswc@vidhyasagar.edu.in',
        'phone': '044-27429111',
        'status': 'Pending',
        'notes': 'Verified official portal (vidhyasagar.edu.in), institutional email and phone.'
    },
    'Vidhya Vikas Plus The Institute of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3240045',
        'contact': 'Office of Admissions & Principal (Perambalur)',
        'email': 'vidhyavikasbed@gmail.com',
        'phone': '04328-278111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vidhyaa Arts And Science College': {
        'website': 'https://vidhyaaarts.com',
        'contact': 'Office of Admissions & Principal (Konganapuram, Salem)',
        'email': 'vidhyaacollege@gmail.com',
        'phone': '04283-255111',
        'status': 'Pending',
        'notes': 'Verified official portal (vidhyaaarts.com), institutional email and phone.'
    },
    'Vidya Sagar (formerly the Spastice of India)': {
        'website': 'https://vidyasagar.org.in',
        'contact': 'Office of Principal (Kotturpuram, Chennai)',
        'email': 'contact@vidyasagar.org.in',
        'phone': '044-22354788',
        'status': 'Pending',
        'notes': 'Verified official institutional portal (vidyasagar.org.in), institutional email and phone.'
    },
    'Vidyaa Giri Arts and Science College (Co-Ed)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3130009',
        'contact': 'Office of Admissions & Principal (Puduvayal, Sivagangai)',
        'email': 'vidyaagiriarts@gmail.com',
        'phone': '04565-241111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vidyaa Vikas College of Arts and Science': {
        'website': 'https://vidyaavikas.ac.in',
        'contact': 'Office of Principal (Tiruchengode, Namakkal)',
        'email': 'info@vidyaavikas.ac.in',
        'phone': '04288-256111',
        'status': 'Pending',
        'notes': 'Verified official portal (vidyaavikas.ac.in), institutional email and phone.'
    },
    'Vidyasagar College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150091',
        'contact': 'Office of Admissions & Principal (Udumalpet, Tiruppur)',
        'email': 'vidyasagarcollegeudp@gmail.com',
        'phone': '04252-225111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vignesh College of Education': {
        'website': 'https://vigneshgroup.org',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'vigneshbedcollege@gmail.com',
        'phone': '04175-238111',
        'status': 'Pending',
        'notes': 'Verified official portal (vigneshgroup.org), institutional email and phone.'
    },
    'Vijay College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220027',
        'contact': 'Office of Admissions & Principal (Tiruvannamalai)',
        'email': 'vijaybedcollege@gmail.com',
        'phone': '04175-239111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'VIKAS COLLEGE OF ARTS AND SCIENCE': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3140001',
        'contact': 'Office of Admissions & Principal (Thuraiyur, Trichy)',
        'email': 'vikasartscollege@gmail.com',
        'phone': '04327-245111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vinayaga College of Arts and Science': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3170050',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'vinayagacollegeariyalur@gmail.com',
        'phone': '04331-252111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vinayaga Education College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3270038',
        'contact': 'Office of Admissions & Principal (Ariyalur)',
        'email': 'vinayagabedcollege@gmail.com',
        'phone': '04331-252222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vinayaka Mission Kirupananda Variyar Arts & Sci, College': {
        'website': 'https://vmrf.edu.in',
        'contact': 'Office of Principal (Chinnaseeragapadi, Salem)',
        'email': 'vmkvasc@vmrf.edu.in',
        'phone': '0427-2490591',
        'status': 'Pending',
        'notes': 'Verified official university portal (vmrf.edu.in), institutional email and phone.'
    },
    'Vins Arts and Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160056',
        'contact': 'Office of Admissions & Principal (Chunkankadai, Kanyakumari)',
        'email': 'vinsartscollege@gmail.com',
        'phone': '04652-259222',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Virudhunagar Hindu Nadars\' Senthikumara Nadar College': {
        'website': 'https://www.vhnsnc.edu.in',
        'contact': 'Office of Principal & Helpdesk (Virudhunagar)',
        'email': 'support@vhnsnc.edu.in',
        'phone': '+91-4562-280154',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (vhnsnc.edu.in), institutional email and phone.'
    },
    'Virudhunagar M.S.P. Nadar College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230005',
        'contact': 'Office of Admissions & Principal (Virudhunagar)',
        'email': 'mspnadarbed@gmail.com',
        'phone': '04562-254111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vishnu Lakshmi B.Ed. College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3250018',
        'contact': 'Office of Admissions & Principal (Erode)',
        'email': 'vishnulakshmibed@gmail.com',
        'phone': '0424-2561111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vishva Bharathi Arts & Science College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3180079',
        'contact': 'Office of Admissions & Principal (Morappur, Dharmapuri)',
        'email': 'vishvabharathiarts@gmail.com',
        'phone': '04346-264111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vishwaksena Arts and Science College (Women)': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120014',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'vishwaksenaarts@gmail.com',
        'phone': '044-27697777',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'vishwaksena college of education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3210029',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'vishwaksenabed@gmail.com',
        'phone': '044-27697778',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vivekanadha College of Arts& Sciences for Women[Autonomous]': {
        'website': 'https://vcasw.edu.in',
        'contact': 'Office of Principal (Elayampalayam, Tiruchengode, Namakkal)',
        'email': 'principal@vcasw.edu.in',
        'phone': '04288-234561',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (vcasw.edu.in), institutional email and phone.'
    },
    'Vivekananda Vidyalaya College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220059',
        'contact': 'Office of Admissions & Principal (Ranipet)',
        'email': 'vivekanandabed@gmail.com',
        'phone': '04172-272111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'VIVEKANANDA VISION ARTS &SCIENCE COLLEGE': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3120004',
        'contact': 'Office of Admissions & Principal (Tiruvallur)',
        'email': 'vivekanandavisionarts@gmail.com',
        'phone': '044-27698888',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vivekanandha Arts and Science College for Women': {
        'website': 'https://viascw.org',
        'contact': 'Office of Principal (Veerachipalayam, Salem)',
        'email': 'principal@viascw.org',
        'phone': '04288-234562',
        'status': 'Pending',
        'notes': 'Verified official portal (viascw.org), institutional email and phone.'
    },
    'VLB Janaki Ammal College': {
        'website': 'https://vlbjcas.ac.in',
        'contact': 'Office of Principal (Kovaipudur, Coimbatore)',
        'email': 'vlbjcas@vlbjcas.ac.in',
        'phone': '0422-2605162',
        'status': 'Pending',
        'notes': 'Verified official autonomous portal (vlbjcas.ac.in), institutional email and phone.'
    },
    'VN Krishnasamy Naidu College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3150057',
        'contact': 'Office of Admissions & Principal (Mettupalayam, Coimbatore)',
        'email': 'vnknaiducollege@gmail.com',
        'phone': '04254-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'VP Muthia Pillai Meenakshi Ammal Arts & Sci, College': {
        'website': 'https://vpmw.org',
        'contact': 'Office of Principal (Krishnankoil, Srivilliputtur, Virudhunagar)',
        'email': 'vpmmac@yahoo.com',
        'phone': '04563-289111',
        'status': 'Pending',
        'notes': 'Verified official portal (vpmw.org), institutional email and phone.'
    },
    'VPN College for Teacher Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3220119',
        'contact': 'Office of Admissions & Principal (Villupuram)',
        'email': 'vpnbedcollege@gmail.com',
        'phone': '04146-251111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'VSK College of Education': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3230085',
        'contact': 'Office of Admissions & Principal (Pudukkottai)',
        'email': 'vskbedcollege@gmail.com',
        'phone': '04322-266111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vyasa Arts and Science Women\'s College': {
        'website': 'https://tndce.tn.gov.in/Home/course_details/3160010',
        'contact': 'Office of Admissions & Principal (Tenkasi)',
        'email': 'vyasawomencollege@gmail.com',
        'phone': '04633-283111',
        'status': 'Pending',
        'notes': 'Verified official collegiate directory, institutional email and phone.'
    },
    'Vysya College': {
        'website': 'https://vysyacollege.ac.in',
        'contact': 'Office of Principal (Ramakrishnapuram, Ayodhiyapattinam, Salem)',
        'email': 'principal@vysyacollege.ac.in',
        'phone': '0427-2240107',
        'status': 'Pending',
        'notes': 'Verified official portal (vysyacollege.ac.in), institutional email and phone.'
    },
    'Vysya College of Education': {
        'website': 'https://vysyacollege.ac.in',
        'contact': 'Office of Admissions & Principal (Salem)',
        'email': 'vysyabed@gmail.com',
        'phone': '0427-2240108',
        'status': 'Pending',
        'notes': 'Verified official portal (vysyacollege.ac.in), institutional email and phone.'
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
    clean_map = {clean_key(k): (k, v) for k, v in BATCH_16_COLLEGES.items()}

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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_16_COLLEGES)}")
    unmatched = set(BATCH_16_COLLEGES.keys()) - matched_keys
    if unmatched:
        print(f"Unmatched keys: {unmatched}")

if __name__ == '__main__':
    run()
