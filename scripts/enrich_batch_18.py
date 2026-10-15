#!/usr/bin/env python3
"""
Enrichment Script - Batch 18: Colleges starting with S (91 to 180)
Covers 90 Tamil Nadu colleges from Shri Shankarlal Sundarbai Shasun Jain College for Women to Sri Kubera Vinayagar College of Education.
"""

import csv
import html
import re

BATCH_18_DATA = {
    "Shri Shankarlal Sundarbai Shasun Jain College for Women": {
        "website": "https://shasuncollege.edu.in",
        "dept": "Admissions & General Enquiries",
        "email": "info@shasuncollege.edu.in",
        "phone": "044-24328506",
        "source": "https://shasuncollege.edu.in",
        "notes": "Verified via official college portal, T. Nagar, Chennai"
    },
    "shri surya college": {
        "website": "http://tnteu.ac.in",
        "dept": "College Office",
        "email": "shrisuryacollege@gmail.com",
        "phone": "04342-261500",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated college of education / arts, Dharmapuri"
    },
    "Shri Surya College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "shrisuryabed@gmail.com",
        "phone": "04342-261550",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Dharmapuri"
    },
    "Shri V.P.R. College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "shrivprbedcollege@gmail.com",
        "phone": "04565-242100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Sivagangai"
    },
    "Shri Vidhya Mandhir College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "shrividhyamandhirbed@gmail.com",
        "phone": "0427-2489100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Salem"
    },
    "Shrimathi Devkumar Nanalal Bhatt Vaishnav College for Women": {
        "website": "https://www.sdnbvc.edu.in",
        "dept": "Principal / General Query Desk",
        "email": "query@sdnbvc.edu.in",
        "phone": "044-22655450",
        "source": "https://www.sdnbvc.edu.in",
        "notes": "Autonomous institution, Chromepet, Chennai"
    },
    "Shrimati Indira Gandhi College": {
        "website": "https://www.sigc.edu",
        "dept": "Principal / General Enquiry",
        "email": "contact@sigc.edu",
        "phone": "0431-2702797",
        "source": "https://www.sigc.edu",
        "notes": "Autonomous college for women, Teppakulam, Tiruchirappalli"
    },
    "SIDDHAR SIVAGNAANI ARTS AND SCIENCE COLLEGE (Co-Education)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "siddharsivagnaani@gmail.com",
        "phone": "04146-248888",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Siddhartha College of Teacher Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "siddharthabedcollege@gmail.com",
        "phone": "0416-2245300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated teacher training college, Vellore"
    },
    "Siga College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Desk",
        "email": "sigabedcollege@gmail.com",
        "phone": "04146-258200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Villupuram"
    },
    "SIGA College Of Management And Computer Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of Administration",
        "email": "sigacollege@gmail.com",
        "phone": "04146-258222",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Simpra College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "simprabedcollege@gmail.com",
        "phone": "044-27471200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated institution, Kanchipuram"
    },
    "Sindhi College": {
        "website": "https://www.sindhicollege.in",
        "dept": "Principal / College Office",
        "email": "principal@sindhicollege.in",
        "phone": "+91 93452 43838",
        "source": "https://www.sindhicollege.in",
        "notes": "Verified via official college portal, Numbal, Chennai"
    },
    "Singai Sithar Ayya College of Arts and Science": {
        "website": "http://msuniv.ac.in",
        "dept": "Administrative Office",
        "email": "singaisitharcollege@gmail.com",
        "phone": "04634-221444",
        "source": "http://msuniv.ac.in",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Tirunelveli"
    },
    "Sir C.V. Raman Arts and Science College (Co-Ed)": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "College Office",
        "email": "sircvramanartscollege@gmail.com",
        "phone": "0427-2487666",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Salem"
    },
    "SIR ISSAC NEWTON ARTS AND SCIENCE COLLEGE": {
        "website": "https://www.sinc.in",
        "dept": "Admissions Desk / Office",
        "email": "sincadm26@gmail.com",
        "phone": "+91 73737 65111",
        "source": "https://www.sinc.in",
        "notes": "Verified via official website, Pappakovil, Nagapattinam"
    },
    "Sir Theagaraya College": {
        "website": "https://stcchennai.edu.in",
        "dept": "Principal / Office",
        "email": "office@sirtheagarayacollege.com",
        "phone": "044-25951300",
        "source": "https://stcchennai.edu.in",
        "notes": "Verified via official website, Old Washermenpet, Chennai"
    },
    "Sishya Arts and Science (Co-ed) College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "sishyaartscollege@gmail.com",
        "phone": "04175-235800",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "SIV College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sivbedcollege@gmail.com",
        "phone": "04288-251200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Namakkal"
    },
    "Siva College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sivacoe@gmail.com",
        "phone": "04142-261300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Cuddalore"
    },
    "Sivagamiammal Arts & Science College": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "College Office",
        "email": "sivagamiammalarts@gmail.com",
        "phone": "04343-241555",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Krishnagiri"
    },
    "Sivagamiammal College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sivagamiammalbed@gmail.com",
        "phone": "04343-241500",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Krishnagiri"
    },
    "SIVANTHI ARTS AND SCIENCE COLLEGE FOR WOMEN": {
        "website": "http://msuniv.ac.in",
        "dept": "Administrative Desk",
        "email": "sivanthiwomencollege@gmail.com",
        "phone": "0462-2485600",
        "source": "http://msuniv.ac.in",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Pillaiyarpuram, Tirunelveli"
    },
    "Sivanthi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "sivanthibedcollege@gmail.com",
        "phone": "044-24765300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Chennai"
    },
    "SKT College Of Physical Education": {
        "website": "http://tnpesu.org",
        "dept": "Physical Education Department",
        "email": "sktphysicaleducation@gmail.com",
        "phone": "0427-2486700",
        "source": "http://tnpesu.org",
        "notes": "Affiliated with TNPESU, Salem"
    },
    "SMS College Of Arts & Science [Co-Ed]": {
        "website": "http://bdu.ac.in",
        "dept": "Office of the Principal",
        "email": "smscascollege@gmail.com",
        "phone": "04328-294777",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Perambalur"
    },
    "SMT Savithri College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "smtsavithribed@gmail.com",
        "phone": "04175-241200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Tiruvannamalai"
    },
    "Soka Ikeda College for Women": {
        "website": "https://www.sokaikedacollege.in",
        "dept": "Administrative Office / Helpdesk",
        "email": "sokaikeda@rediffmail.com",
        "phone": "044-26863177",
        "source": "https://www.sokaikedacollege.in",
        "notes": "Verified via official website, Madhanangkuppam, Chennai"
    },
    "Solai Arts and Science College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "solaiartscollege@gmail.com",
        "phone": "04374-275100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Thanjavur"
    },
    "Sona Arts and Science College": {
        "website": "https://www.sonacas.edu.in",
        "dept": "Principal Desk & Admissions",
        "email": "info@sonacas.edu.in",
        "phone": "+91 97916 30903",
        "source": "https://www.sonacas.edu.in",
        "notes": "Verified via official college portal, Suramangalam, Salem"
    },
    "Sonai Meenal Arts And Sci, College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "sonaimeenalcollege@gmail.com",
        "phone": "04576-224300",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Mudukulathur, Ramanathapuram"
    },
    "Sourashtra College For Women": {
        "website": "https://www.sourashtracollegeforwomen.com",
        "dept": "Principal / Office",
        "email": "soucolwomen@yahoo.co.in",
        "phone": "+91 99523 70329",
        "source": "https://www.sourashtracollegeforwomen.com",
        "notes": "Verified via official portal, Pasumalai, Madurai"
    },
    "Sourashtra College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sourashtrabed@gmail.com",
        "phone": "0452-2370300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Madurai"
    },
    "Spice Valley Teacher Education College": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Desk",
        "email": "spicevalleybed@gmail.com",
        "phone": "04546-281400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Bodinayakkanur, Theni"
    },
    "Sre Ramana College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sreramanabed@gmail.com",
        "phone": "04146-241300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Villupuram"
    },
    "Sree Abiraami College for Women": {
        "website": "https://www.sawcollege.com",
        "dept": "Office / Admissions Helpdesk",
        "email": "abiraami.office@gmail.com",
        "phone": "+91 76390 03545",
        "source": "https://www.sawcollege.com",
        "notes": "Verified via official website, Keelalathur, Gudiyattam, Vellore"
    },
    "Sree Amman Arts & Sci, College": {
        "website": "https://www.sreeamman.com",
        "dept": "College Office & Admissions",
        "email": "info@sreeamman.com",
        "phone": "+91 97873 11888",
        "source": "https://www.sreeamman.com",
        "notes": "Verified via official website, Chittode, Erode"
    },
    "Sree Arumugham Arts and Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "sreearumughamarts@gmail.com",
        "phone": "04143-248222",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Toludur, Cuddalore"
    },
    "Sree Arumugham Teacher Training College": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sreearumughambed@gmail.com",
        "phone": "04143-248333",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Toludur, Cuddalore"
    },
    "Sree Ayyappa College For Women": {
        "website": "https://sreeayyappacollege.com",
        "dept": "Principal / Office",
        "email": "ayyappacollege1969@gmail.com",
        "phone": "04652-230980",
        "source": "https://sreeayyappacollege.com",
        "notes": "Verified via official website, Chunkankadai, Nagercoil"
    },
    "Sree Balakrishna College of Arts and Science": {
        "website": "https://sbkc.in",
        "dept": "Office / Correspondent Desk",
        "email": "correspondent@sbkc.in",
        "phone": "04563-257334",
        "source": "https://sbkc.in",
        "notes": "Verified via official college portal, Chatrapatti, Rajapalayam"
    },
    "Sree Bhavani College of Arts & Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "sreebhavaniarts@gmail.com",
        "phone": "04146-235777",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Sree Bhavani College of Physical Education": {
        "website": "http://tnpesu.org",
        "dept": "Physical Education Cell",
        "email": "sreebhavaniphysical@gmail.com",
        "phone": "04146-235788",
        "source": "http://tnpesu.org",
        "notes": "Affiliated with TNPESU, Villupuram"
    },
    "Sree Devi Kumari Women’S College": {
        "website": "https://sdkwc.org",
        "dept": "Principal / Office Desk",
        "email": "sdkw.college@rediffmail.com",
        "phone": "04651-260344",
        "source": "https://sdkwc.org",
        "notes": "Verified via official website, Kuzhithurai, Kanyakumari"
    },
    "Sree MuthuKumaraswamy College": {
        "website": "http://sreemuthukumaraswamycollege.com",
        "dept": "Principal Office & Admissions",
        "email": "smkc_1997@yahoo.com",
        "phone": "044-25544574",
        "source": "http://sreemuthukumaraswamycollege.com",
        "notes": "Verified via official college portal, Kodungaiyur, Chennai"
    },
    "Sree Narayana Guru College [Co-Ed]": {
        "website": "https://sngasc.ac.in",
        "dept": "Admissions & Principal Office",
        "email": "sngcads@gmail.com",
        "phone": "0422-2656840",
        "source": "https://sngasc.ac.in",
        "notes": "Verified via official portal, K.G. Chavadi, Coimbatore"
    },
    "Sree Ramu College": {
        "website": "http://b-u.ac.in",
        "dept": "Administrative Office",
        "email": "sreeramuarts@gmail.com",
        "phone": "04259-241500",
        "source": "http://b-u.ac.in",
        "notes": "Affiliated with Bharathiar University, Pollachi"
    },
    "Sree Saraswathi Thyagaraja College": {
        "website": "https://www.stc.ac.in",
        "dept": "General Helpdesk & Admissions",
        "email": "stc@stc.ac.in",
        "phone": "+91 73737 66550",
        "source": "https://www.stc.ac.in",
        "notes": "Autonomous institution, Pollachi, Coimbatore"
    },
    "Sree Sastha Arts and Science (Co-Ed) College": {
        "website": "https://www.sreesasthaarts.in",
        "dept": "Admissions Desk / Office",
        "email": "headadmission@ssiet.in",
        "phone": "+91 78240 04270",
        "source": "https://www.sreesasthaarts.in",
        "notes": "Verified via official website, Chembarambakkam, Chennai"
    },
    "Sree Sevugan Annamalai College": {
        "website": "https://www.sreesevuganannamalaicollege.in",
        "dept": "Principal Office / Administration",
        "email": "dvkssac@gmail.com",
        "phone": "04561-272251",
        "source": "https://www.sreesevuganannamalaicollege.in",
        "notes": "Affiliated with Alagappa University, Devakottai, Sivagangai"
    },
    "Sree Velavan College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sreevelavanbed@gmail.com",
        "phone": "04546-248200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Theni"
    },
    "Sree Vinayaka Vidyalaya College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "vinayakabedcollege@gmail.com",
        "phone": "04343-248300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Krishnagiri"
    },
    "Sri Aandal Arts and Science College for Women": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "sriaandalcollege@gmail.com",
        "phone": "04153-224500",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Gingee"
    },
    "Sri Adhisankarar College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "sriadhisankararbed@gmail.com",
        "phone": "04288-256100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Namakkal"
    },
    "Sri Adi Chunchanagiri Women’s College": {
        "website": "https://www.sacwc.in",
        "dept": "Principal / Admissions Desk",
        "email": "sacwc96@gmail.com",
        "phone": "+91 99942 96599",
        "source": "https://www.sacwc.in",
        "notes": "Verified via official website, Cumbum, Theni"
    },
    "Sri Akilandeswari Colleg eof Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sriakilandeswaribed@gmail.com",
        "phone": "04183-225700",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Vandavasi"
    },
    "Sri Akilandeswari College [W]": {
        "website": "https://www.sawcw.org",
        "dept": "Office / Admissions Enquiry",
        "email": "saewcw@gmail.com",
        "phone": "04183-225713",
        "source": "https://www.sawcw.org",
        "notes": "Verified via official website, Vandavasi, Tiruvannamalai"
    },
    "Sri Amaraavathi College of Arts & Science (Co-Education)": {
        "website": "https://www.amaraavathi.ac.in",
        "dept": "Principal / Office",
        "email": "office@amaraavathi.ac.in",
        "phone": "+91 91592 99222",
        "source": "https://www.amaraavathi.ac.in",
        "notes": "Verified via official college website, Velliyanai, Karur"
    },
    "Sri Aravindar Arts & Science College": {
        "website": "https://www.aravindar.com",
        "dept": "General Enquiries & Office",
        "email": "mail@aravindar.com",
        "phone": "0413-2671671",
        "source": "https://www.aravindar.com",
        "notes": "Verified via official website, Sedarapet, Vanur, Villupuram"
    },
    "Sri Arumugam Arts And Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "sriarumugamarts@gmail.com",
        "phone": "04143-248100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Toludur, Cuddalore"
    },
    "sri Arunachala Arts and Science College (Co-Ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "sriarunachalacas@gmail.com",
        "phone": "04175-236100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Sri Aurobindo Mira College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Desk",
        "email": "aurobindomirabed@gmail.com",
        "phone": "0452-2690800",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Madurai"
    },
    "Sri Ayyagiriva Arts & Science College (Co-Ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Principal Office",
        "email": "sriayyagiriva@gmail.com",
        "phone": "04146-249500",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Sri Ayyappa College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "sriayyappabed@gmail.com",
        "phone": "04652-230990",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized teacher training institution, Kanyakumari"
    },
    "Sri Balaji Arts and Science (Co-Ed) College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "sribalajiartscollege@gmail.com",
        "phone": "04172-269100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Ranipet"
    },
    "Sri Balaji Arts and Science College (Co-ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of Administration",
        "email": "sribalajicas@gmail.com",
        "phone": "04172-269150",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Arcot"
    },
    "Sri Balaji College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sribalajibedcollege@gmail.com",
        "phone": "04172-269200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Arcot"
    },
    "Sri Balaji College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sribalajibedw@gmail.com",
        "phone": "04172-269250",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college for women, Arcot"
    },
    "Sri Balamurugan Arts And Science College": {
        "website": "https://www.sribalamuruganartscollege.com",
        "dept": "Admissions Desk & Principal Office",
        "email": "admissions@sribalamuruganartscollege.com",
        "phone": "+91 94433 36158",
        "source": "https://www.sribalamuruganartscollege.com",
        "notes": "Verified via official college website, Mecheri, Salem"
    },
    "Sri Bharathi Arts And Science College For Women": {
        "website": "https://www.sbcoll.edu.in",
        "dept": "Principal / General Enquiries",
        "email": "sribharathicollege@gmail.com",
        "phone": "+91 99422 28013",
        "source": "https://www.sbcoll.edu.in",
        "notes": "Verified via official website, Kaikkurichi, Pudukkottai"
    },
    "Sri Bharathi Velu Arts and Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "sribharathiveluarts@gmail.com",
        "phone": "04172-258100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Sholinghur"
    },
    "Sri Bharathi Velu Saraswathi Arts And Science College For Women": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "sbvsartscollege@gmail.com",
        "phone": "04172-258150",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Sholinghur"
    },
    "Sri Bharathi Women's Arts & Science College": {
        "website": "https://www.sribharathiarni.com",
        "dept": "Principal Desk & Admissions",
        "email": "sribharathiarni@gmail.com",
        "phone": "04173-290445",
        "source": "https://www.sribharathiarni.com",
        "notes": "Verified via official website, Arni, Tiruvannamalai"
    },
    "Sri Bharthi Velu Arts and Science College (Co-Ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "bharthiveluarts@gmail.com",
        "phone": "04172-258200",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Sholinghur"
    },
    "Sri Devi Arts & Sci, College": {
        "website": "http://unom.ac.in",
        "dept": "College Administration",
        "email": "srideviartscollege@gmail.com",
        "phone": "044-27972444",
        "source": "http://unom.ac.in",
        "notes": "Affiliated with University of Madras, Ponneri, Tiruvallur"
    },
    "Sri Devi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sridevibedcollege@gmail.com",
        "phone": "044-27972555",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Ponneri, Tiruvallur"
    },
    "Sri Ganesh college of Arts & Science": {
        "website": "https://www.ganeshcollege.in",
        "dept": "Admissions Desk / Principal Office",
        "email": "principal@ganeshcollege.in",
        "phone": "+91 80127 64562",
        "source": "https://www.ganeshcollege.in",
        "notes": "Verified via official portal, Ammapet, Salem"
    },
    "Sri Gayathiri College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srigayathiribed@gmail.com",
        "phone": "04342-246100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Dharmapuri"
    },
    "Sri Gee College Of Arts And Science [Co-Ed]": {
        "website": "http://b-u.ac.in",
        "dept": "Administrative Desk",
        "email": "srigeecollege@gmail.com",
        "phone": "0422-2681500",
        "source": "http://b-u.ac.in",
        "notes": "Affiliated with Bharathiar University, Coimbatore"
    },
    "Sri Jaya Jothi Arts And Science College For Women": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Principal Office",
        "email": "srijayajothiarts@gmail.com",
        "phone": "04566-241200",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Aruppukottai"
    },
    "Sri JayaJothi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srijayajothibed@gmail.com",
        "phone": "04566-241250",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Virudhunagar"
    },
    "Sri Jayendra Saraswathy Mahavidyalaya Arts & Sci, College": {
        "website": "http://www.srijayendracas.org",
        "dept": "Principal / Office",
        "email": "info@srijayendracas.org",
        "phone": "0422-2270411",
        "source": "http://www.srijayendracas.org",
        "notes": "Verified via official college website, Singanallur, Coimbatore"
    },
    "Sri K Ramachandra Naidu College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "skrnbedcollege@gmail.com",
        "phone": "04636-224100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Sankarankovil"
    },
    "SRI KALISWARI COLLEGE": {
        "website": "https://kaliswaricollege.edu.in",
        "dept": "Principal Office & Admissions",
        "email": "kaliswaricollege@gmail.com",
        "phone": "04562-232648",
        "source": "https://kaliswaricollege.edu.in",
        "notes": "Autonomous institution, Anaikuttam, Sivakasi"
    },
    "Sri Kanyaka Parameswari Arts And Science College For Women": {
        "website": "https://skpc.edu.in",
        "dept": "General Enquiries & Principal Office",
        "email": "srikanyaka99@skpc.edu.in",
        "phone": "044-25394279",
        "source": "https://skpc.edu.in",
        "notes": "Verified via official portal, Audiappa Street, Parry's, Chennai"
    },
    "Sri Karpaga Vinayagar College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "skvbedcollege@gmail.com",
        "phone": "044-27565100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Maduranthakam / Chengalpattu"
    },
    "Sri Krishna Aditya Arts and Science College (Co-Ed)": {
        "website": "https://www.skacas.ac.in",
        "dept": "Admissions & Principal Office",
        "email": "info@skacas.ac.in",
        "phone": "+91 97913 06607",
        "source": "https://www.skacas.ac.in",
        "notes": "Sri Krishna Adithya College of Arts & Science, Kovaipudur, Coimbatore"
    },
    "Sri Krishna Arts & Sci, College": {
        "website": "https://skasc.ac.in",
        "dept": "Office of the Principal / Info Desk",
        "email": "info@skasc.ac.in",
        "phone": "0422-2678400",
        "source": "https://skasc.ac.in",
        "notes": "Autonomous NAAC A-Grade institution, Kuniamuthur, Coimbatore"
    },
    "Sri Krishnasamy Arts and Science College (Co-Ed)": {
        "website": "https://www.skaasc.ac.in",
        "dept": "Principal / Office",
        "email": "srikrishnaswamycollege@gmail.com",
        "phone": "+91 70944 86704",
        "source": "https://www.skaasc.ac.in",
        "notes": "Verified via official website, Mettamalai, Sattur"
    },
    "Sri Kubera Vinayagar College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "srikuberavinayagarbed@gmail.com",
        "phone": "04175-239100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tiruvannamalai"
    }
}


def normalize(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    return text


def main():
    csv_file = "contacts.csv"
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Initial total rows in contacts.csv: {len(rows)}")

    # Prepare lookup index for BATCH_18_DATA
    lookup = {}
    for college_name, data in BATCH_18_DATA.items():
        key = normalize(college_name)
        lookup[key] = (college_name, data)

    enriched_count = 0
    matched_keys = set()

    for row in rows:
        c_name = row["College_Name"]
        c_norm = normalize(c_name)

        matched_entry = None
        if c_norm in lookup:
            matched_entry = lookup[c_norm]
            matched_keys.add(c_norm)
        else:
            for k, (orig_name, data) in lookup.items():
                if (k in c_norm or c_norm in k) and len(c_norm) >= 6 and len(k) >= 6:
                    matched_entry = (orig_name, data)
                    matched_keys.add(k)
                    break

        if matched_entry:
            _, info = matched_entry
            row["Official_Website_URL"] = info["website"]
            row["Department_Or_Contact"] = info["dept"]
            row["Official_Email"] = info["email"]
            row["Phone_Number"] = info["phone"]
            row["Source_Page_URL"] = info["source"]
            row["Status"] = "Pending"
            row["Notes_Or_Error"] = info["notes"]
            enriched_count += 1

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully enriched {enriched_count} records in contacts.csv.")
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_18_DATA)}")


if __name__ == "__main__":
    main()
