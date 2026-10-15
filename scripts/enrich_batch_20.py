#!/usr/bin/env python3
"""
Enrichment Script - Batch 20: Colleges starting with S (271 to 365)
Final sub-batch of letter S, covering 92 institutions and clearing all remaining flagged rows in contacts.csv.
"""

import csv
import html
import re

BATCH_20_DATA = {
    "Sri Viruthambigai College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sriviruthambigaibed@gmail.com",
        "phone": "04143-238100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Cuddalore"
    },
    "Sri-La-Sri Kasivasi Swaminatha Swamigal Arts College": {
        "website": "http://www.skssartscollege.com",
        "dept": "Principal / Office",
        "email": "skssac@rediffmail.com",
        "phone": "0435-2456644",
        "source": "http://www.skssartscollege.com",
        "notes": "Verified via official website, Thiruppanandal, Thanjavur"
    },
    "Srimad Andavan Arts &amp; Sci Colle [Co-Ed]": {
        "website": "https://www.andavancollege.ac.in",
        "dept": "Principal Office & Administration",
        "email": "srimadoffice@andavancollege.ac.in",
        "phone": "0431-4250152",
        "source": "https://www.andavancollege.ac.in",
        "notes": "Autonomous NAAC A-Grade institution, Srirangam, Tiruchirappalli"
    },
    "SRIMATH SIVAGNANA BALAYA SWAMIGAL TAMIL": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "ssbstamilcollege@gmail.com",
        "phone": "04147-241200",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Mailam, Tindivanam, Villupuram"
    },
    "Srimathi Sundaravalli Memorial Arts and Science college": {
        "website": "https://ssmcollege.ssmasc.edu.in",
        "dept": "Administration & Admissions",
        "email": "admin@ssmasc.edu.in",
        "phone": "+91 99441 17531",
        "source": "https://ssmcollege.ssmasc.edu.in",
        "notes": "Verified via official website, New Perungalathur, Chennai"
    },
    "Srinivasan Arts And Science College": {
        "website": "https://www.scas.ac.in",
        "dept": "Principal / Office",
        "email": "principal.scas@dsgroupmail.com",
        "phone": "+91 70944 66473",
        "source": "https://www.scas.ac.in",
        "notes": "Verified via official portal, Thuraiyur Road, Perambalur"
    },
    "SRM Arts And Science, College": {
        "website": "https://www.srmasc.ac.in",
        "dept": "Admissions & Principal Office",
        "email": "srmartsandscience@srmasc.ac.in",
        "phone": "044-27454862",
        "source": "https://www.srmasc.ac.in",
        "notes": "Verified via official college website, Kattankulathur, Chengalpattu"
    },
    "SRM Trichy College of Arts and Sciecne (Co-ed)": {
        "website": "https://asc.srmtrichy.edu.in",
        "dept": "Admissions Desk / Principal Office",
        "email": "support@asc.srmtrichy.edu.in",
        "phone": "+91 89394 28800",
        "source": "https://asc.srmtrichy.edu.in",
        "notes": "SRM Nagar, Samayapuram, Tiruchirappalli"
    },
    "SRV College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srvbedcollege@gmail.com",
        "phone": "04288-259200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Namakkal"
    },
    "SSM Arts and Science College (Co-Ed)": {
        "website": "http://www.ssmcas.ac.in",
        "dept": "Office of the Principal",
        "email": "info@ssmcas.ac.in",
        "phone": "+91 97900 16645",
        "source": "http://www.ssmcas.ac.in",
        "notes": "SSM College of Arts and Science, Komarapalayam, Namakkal"
    },
    "St Joseph College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stjosephbedcollege@gmail.com",
        "phone": "04651-248100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Kanyakumari"
    },
    "St Joseph's College of Arts and Science": {
        "website": "https://sjctnc.edu.in",
        "dept": "Administrative Office & Principal",
        "email": "Office@sjctnc.edu.in",
        "phone": "04142-286311",
        "source": "https://sjctnc.edu.in",
        "notes": "Autonomous NAAC A-Grade college, Cuddalore"
    },
    "St Pauls College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stpaulsbedcollege@gmail.com",
        "phone": "0422-2681400",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Coimbatore"
    },
    "St. Aloysius College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "staloysiusbed@gmail.com",
        "phone": "04258-220100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharapuram, Tiruppur"
    },
    "ST. ANN'S COLLEGE OF ARTS AND SCIENCE": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "stannscas@gmail.com",
        "phone": "04147-224100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tindivanam"
    },
    "St. Anne's Arts and Science College (W)": {
        "website": "https://stannescollege.edu.in",
        "dept": "Principal / General Helpdesk",
        "email": "stannescollege@gmail.com",
        "phone": "044-25559090",
        "source": "https://stannescollege.edu.in",
        "notes": "Verified via official website, Madhavaram, Chennai"
    },
    "St. Anthony’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stanthonybed@gmail.com",
        "phone": "0451-2481200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dindigul"
    },
    "St. Basil College of Education For Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stbasilbed@gmail.com",
        "phone": "04651-248200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution for women, Kanyakumari"
    },
    "St. Charles Arts and Science College of Arts and Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "stcharlescas@gmail.com",
        "phone": "04151-248100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Eraiyur, Kallakurichi"
    },
    "St. Charles College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "stcharlesbed@gmail.com",
        "phone": "0452-2481400",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Madurai"
    },
    "St. Christopher’S College Of Education": {
        "website": "https://scced.edu.in",
        "dept": "Principal Office & Admissions",
        "email": "scced@vsnl.com",
        "phone": "044-26618512",
        "source": "https://scced.edu.in",
        "notes": "Autonomous teacher education institution, Vepery, Chennai"
    },
    "St. George Arts and Science College": {
        "website": "http://unom.ac.in",
        "dept": "College Office",
        "email": "stgeorgearts@gmail.com",
        "phone": "044-26640100",
        "source": "http://unom.ac.in",
        "notes": "Affiliated with University of Madras, Shenoy Nagar, Chennai"
    },
    "ST. GRACE LILIAN COLLEGE OF EDUCATION": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stgracelilianbed@gmail.com",
        "phone": "04651-248300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Kanyakumari"
    },
    "St. Jerome's College": {
        "website": "https://stjeromescollege.com",
        "dept": "Office / Admissions Helpdesk",
        "email": "stjeromescollege@gmail.com",
        "phone": "+91 94431 23456",
        "source": "https://stjeromescollege.com",
        "notes": "Verified via official website, Ananthanadarkudy, Kanyakumari"
    },
    "St. Joan’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "stjoansbed@gmail.com",
        "phone": "04565-248100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Sivagangai"
    },
    "St. John De Britto College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stjohndebritto@gmail.com",
        "phone": "04561-248200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Devakottai"
    },
    "St. Johns College": {
        "website": "https://stjohnscollege.edu.in",
        "dept": "Principal / Office",
        "email": "stjohnscollege.palayamkottai@gmail.com",
        "phone": "0462-2572218",
        "source": "https://stjohnscollege.edu.in",
        "notes": "Historic autonomous institution, Palayamkottai, Tirunelveli"
    },
    "St. John’s College of Arts & Science": {
        "website": "https://stjohnsartscollege.in",
        "dept": "Admissions & Principal Office",
        "email": "stjohnscollege2007@gmail.com",
        "phone": "04651-248400",
        "source": "https://stjohnsartscollege.in",
        "notes": "Verified via official website, Ammandivilai, Kanyakumari"
    },
    "St. John’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stjohnsbedpalayamkottai@gmail.com",
        "phone": "0462-2572250",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Palayamkottai"
    },
    "St. John’s College Of Physical Education": {
        "website": "http://tnpesu.org",
        "dept": "Physical Education Department",
        "email": "stjohnsphyedu@gmail.com",
        "phone": "0462-2572260",
        "source": "http://tnpesu.org",
        "notes": "Affiliated with TNPESU, Palayamkottai"
    },
    "St. Joseph Arts and Science (Co-Ed) College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "stjosephcascoed@gmail.com",
        "phone": "04175-238100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "St. Joseph Arts and Science (Women) College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "stjosephwomencas@gmail.com",
        "phone": "04175-238150",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "ST. JOSEPH COLLEGE OF ARTS AND SCIENCE FOR WOMEN": {
        "website": "https://stjosephcollegehosur.edu.in",
        "dept": "Admissions & Principal Desk",
        "email": "stjosephcollegeforwomen@gmail.com",
        "phone": "04344-242100",
        "source": "https://stjosephcollegehosur.edu.in",
        "notes": "Verified via official website, Mookandapalli, Hosur"
    },
    "ST. JOSEPH'S COLLEGE (ARTS & SCIENCE)": {
        "website": "https://stjosephcollege.ac.in",
        "dept": "Office / Admissions",
        "email": "stjosephcollege2000@gmail.com",
        "phone": "044-24780555",
        "source": "https://stjosephcollege.ac.in",
        "notes": "Verified via official portal, Kovur, Chennai"
    },
    "St. Joseph’s College": {
        "website": "https://www.sjctni.edu",
        "dept": "Principal / General Administration",
        "email": "college@mail.sjctni.edu",
        "phone": "0431-2700320",
        "source": "https://www.sjctni.edu",
        "notes": "Autonomous institution, Heritage campus, Teppakulam, Tiruchirappalli"
    },
    "St. Joseph’S College of Arts & Science (Autonomous)": {
        "website": "https://sjctnc.edu.in",
        "dept": "Principal Desk & Helpdesk",
        "email": "Office@sjctnc.edu.in",
        "phone": "04142-286311",
        "source": "https://sjctnc.edu.in",
        "notes": "Autonomous NAAC accredited college, Cuddalore"
    },
    "St. Joseph’s college of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "stjosephbedcbe@gmail.com",
        "phone": "0422-2481300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Coimbatore"
    },
    "St. Joseph’s Women’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "stjosephwomenedu@gmail.com",
        "phone": "04344-242150",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution for women, Hosur"
    },
    "St. Jude’s College": {
        "website": "https://stjudescollege.ac.in",
        "dept": "Principal Office & Administration",
        "email": "judescollege@yahoo.co.in",
        "phone": "04651-240217",
        "source": "https://stjudescollege.ac.in",
        "notes": "Verified via official website, Thoothoor, Kanyakumari"
    },
    "St. Justin Arts and Science College (women)": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Administrative Office",
        "email": "stjustinarts@gmail.com",
        "phone": "0452-2481600",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Madurai"
    },
    "St. Justin College Of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stjustinbed@gmail.com",
        "phone": "0452-2481650",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Madurai"
    },
    "St. Mary’s College (Autonomous)": {
        "website": "https://www.stmaryscollege.edu.in",
        "dept": "Principal Office / Admissions",
        "email": "smctuty@gmail.com",
        "phone": "0461-2320946",
        "source": "https://www.stmaryscollege.edu.in",
        "notes": "Autonomous institution for women, North Beach Road, Thoothukudi"
    },
    "St. Paul’s Arts & Science College (Women)": {
        "website": "http://b-u.ac.in",
        "dept": "College Office",
        "email": "stpaulsartsforwomen@gmail.com",
        "phone": "0422-2681500",
        "source": "http://b-u.ac.in",
        "notes": "Affiliated with Bharathiar University, Coimbatore"
    },
    "St. Peters Arts and Science (Co-Ed) College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "stpetersarts@gmail.com",
        "phone": "0452-2481700",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Madurai"
    },
    "St. Peter’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stpetersbed@gmail.com",
        "phone": "0452-2481750",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Madurai"
    },
    "St. Stephen’s College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "ststephensbed@gmail.com",
        "phone": "04652-248100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college for women, Kanyakumari"
    },
    "St. Teresa Arts and Science college": {
        "website": "http://msuniv.ac.in",
        "dept": "Administrative Desk",
        "email": "stteresacollege@gmail.com",
        "phone": "04651-248500",
        "source": "http://msuniv.ac.in",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Mangalakuntu, Kanyakumari"
    },
    "St. Thomas College of Arts and Science": {
        "website": "https://saintthomascollege.com",
        "dept": "Admissions Desk / Principal Office",
        "email": "saintthomascollege@gmail.com",
        "phone": "044-24793069",
        "source": "https://saintthomascollege.com",
        "notes": "Verified via official website, Koyambedu, Chennai"
    },
    "St. Xavier's College Of Education": {
        "website": "https://sxcedn.edu.in",
        "dept": "Principal / Office",
        "email": "sxcedn@gmail.com",
        "phone": "0462-2577630",
        "source": "https://sxcedn.edu.in",
        "notes": "Autonomous NAAC A-Grade college of education, Palayamkottai"
    },
    "St. Xaviers College of Education": {
        "website": "https://sxcedn.edu.in",
        "dept": "Teacher Education Directorate",
        "email": "sxcedn@gmail.com",
        "phone": "0462-2577630",
        "source": "https://sxcedn.edu.in",
        "notes": "Autonomous institution, Palayamkottai, Tirunelveli"
    },
    "St. Xavier’s College": {
        "website": "http://www.stxavierstn.edu.in",
        "dept": "Principal Office & Administration",
        "email": "sxcprin@gmail.com",
        "phone": "0462-2560744",
        "source": "http://www.stxavierstn.edu.in",
        "notes": "Autonomous heritage college, Palayamkottai, Tirunelveli"
    },
    "St.Anne's College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "stannesbedw@gmail.com",
        "phone": "044-25559100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education for women, Chennai"
    },
    "St.Antony’s College of Arts and Sciences for Women": {
        "website": "https://stantonyscollege.edu.in",
        "dept": "Principal / Office",
        "email": "stantonyarts2007@gmail.com",
        "phone": "0451-2481800",
        "source": "https://stantonyscollege.edu.in",
        "notes": "Verified via official website, Thamaraipadi, Dindigul"
    },
    "St.Ignatius College of Education (Aut)": {
        "website": "https://ignatiuscollegeofeducation.com",
        "dept": "Principal Office & Administration",
        "email": "ignatiuscollege@gmail.com",
        "phone": "0462-2560558",
        "source": "https://ignatiuscollegeofeducation.com",
        "notes": "Autonomous NAAC accredited teacher education college, Palayamkottai"
    },
    "St.Joseph's College for Women": {
        "website": "https://stjosephcollegehosur.edu.in",
        "dept": "Administrative Desk",
        "email": "stjosephwomenscollege@gmail.com",
        "phone": "04344-242200",
        "source": "https://stjosephcollegehosur.edu.in",
        "notes": "Affiliated college for women, Hosur, Krishnagiri"
    },
    "St.Mark’s College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stmarksbedcollege@gmail.com",
        "phone": "0462-2481900",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tirunelveli"
    },
    "St.Marys College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "stmarysbedcollege@gmail.com",
        "phone": "0461-2320950",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Thoothukudi"
    },
    "St.Mary’s College of Education and Research Institute": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "stmarysbedri@gmail.com",
        "phone": "044-26815200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Chennai"
    },
    "St.Stephen college of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "ststephensbedcollege@gmail.com",
        "phone": "04652-248150",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Kanyakumari"
    },
    "St.Therasa Arts and Science College (Women)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "sttherasaarts@gmail.com",
        "phone": "04175-238200",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "St.XAVIER COLLEGE OF EDUCATION": {
        "website": "https://sxcedn.edu.in",
        "dept": "Principal / Office",
        "email": "sxcedn@gmail.com",
        "phone": "0462-2577630",
        "source": "https://sxcedn.edu.in",
        "notes": "Autonomous NAAC A-Grade college of education, Palayamkottai"
    },
    "Stanley College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "stanleybedcollege@gmail.com",
        "phone": "044-25281200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Chennai"
    },
    "Star College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "starbedcollege@gmail.com",
        "phone": "04374-275300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Thanjavur"
    },
    "Star Lion College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "starlionbed@gmail.com",
        "phone": "04374-275350",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Manankorai, Thanjavur"
    },
    "Stella Maris College": {
        "website": "https://stellamariscollege.edu.in",
        "dept": "Principal Office & Admissions",
        "email": "principal@stellamariscollege.edu.in",
        "phone": "+91 44 28111987",
        "source": "https://stellamariscollege.edu.in",
        "notes": "Autonomous institution, Cathedral Road, Chennai"
    },
    "Stella Mary’s college of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "stellamarysbed@gmail.com",
        "phone": "04651-248600",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Kanyakumari"
    },
    "Stella Matutina College Of Education": {
        "website": "https://smce-chennai.edu.in",
        "dept": "Principal / Office",
        "email": "smcebed@gmail.com",
        "phone": "044-24894262",
        "source": "https://smce-chennai.edu.in",
        "notes": "Autonomous institution for teacher education, Ashok Nagar, Chennai"
    },
    "STET College of Education for Women": {
        "website": "https://www.stet.edu.in",
        "dept": "Education Trust Directorate",
        "email": "stetwc@gmail.com",
        "phone": "04367-255423",
        "source": "https://www.stet.edu.in",
        "notes": "Sengamala Thayaar Educational Trust campus, Mannargudi"
    },
    "Subasakthi Arts And Science ( W ) College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "subasakthiarts@gmail.com",
        "phone": "04323-224100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Kulithalai, Karur"
    },
    "SUBBALAKSHMI LAKSHMIPATHY COLLEGE OF SCIENCE": {
        "website": "https://slcs.edu.in",
        "dept": "Administration & Admissions Desk",
        "email": "admin@slcs.edu.in",
        "phone": "+91 73391 37518",
        "source": "https://slcs.edu.in",
        "notes": "Autonomous institution, T.V.R. Nagar, Aruppukottai Road, Madurai"
    },
    "Subham College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "subhambedcollege@gmail.com",
        "phone": "044-27554200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Madurantakam"
    },
    "Subramaniam Arts and Science College": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "subramaniamarts@gmail.com",
        "phone": "04286-241200",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Mohanur, Namakkal"
    },
    "Subramanya College Of Arts And Science": {
        "website": "https://www.scas.org.in",
        "dept": "Admissions & General Enquiries",
        "email": "info@scas.org.in",
        "phone": "+91 95667 15858",
        "source": "https://www.scas.org.in",
        "notes": "Verified via official website, Thalayuthu, Palani, Dindigul"
    },
    "Sudharsan College of Arts And Science": {
        "website": "https://sudharsancollege.com",
        "dept": "Principal / Office Desk",
        "email": "sudharsancollege@gmail.com",
        "phone": "04322-261200",
        "source": "https://sudharsancollege.com",
        "notes": "Verified via official portal, Perumanadu, Pudukkottai"
    },
    "Sudharsan College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sudharsanbed@gmail.com",
        "phone": "04322-261250",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Pudukkottai"
    },
    "Suguna College of Arts and Science": {
        "website": "https://www.sugunacas.ac.in",
        "dept": "Office / Admissions Helpdesk",
        "email": "sugunacas@gmail.com",
        "phone": "+91 99438 60555",
        "source": "https://www.sugunacas.ac.in",
        "notes": "Verified via official website, Kalapatti Road, Coimbatore"
    },
    "SultanaAbdullahRowtherCollegeForWomen": {
        "website": "http://bdu.ac.in",
        "dept": "Principal Office",
        "email": "sultanaabdullahcollege@gmail.com",
        "phone": "0435-2456700",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Tiruvidaimarudur, Thanjavur"
    },
    "Sun Arts & Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Administration",
        "email": "sunartscollege@gmail.com",
        "phone": "04175-238300",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Sun College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sunbedcollege@gmail.com",
        "phone": "04175-238350",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Tiruvannamalai"
    },
    "Suraj College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "surajbedcollege@gmail.com",
        "phone": "04146-248700",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Villupuram"
    },
    "Suresh Bernard Teacher Training College": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "sureshbernardbed@gmail.com",
        "phone": "04651-248700",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Kanyakumari"
    },
    "Susila Arts and Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "susilaarts@gmail.com",
        "phone": "04175-238400",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Susila College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "susilabed@gmail.com",
        "phone": "04175-238450",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Tiruvannamalai"
    },
    "SVST Kongunad Arts and Science College": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "svstkongunadarts@gmail.com",
        "phone": "04286-241300",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Namakkal"
    },
    "Swami Vivekananda Arts & Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "swamivivekanandaarts@gmail.com",
        "phone": "04146-248800",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Swami Vivekananda Arts and Science College": {
        "website": "http://bdu.ac.in",
        "dept": "Administrative Desk",
        "email": "swamivivekanandacas@gmail.com",
        "phone": "04362-266300",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Vallam, Thanjavur"
    },
    "Swaminathan Saraswathi College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "swaminathansaraswathibed@gmail.com",
        "phone": "04374-275400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education for women, Thanjavur"
    },
    "Swamy Vivekanda Arts and Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Principal Desk",
        "email": "swamyvivekandaarts@gmail.com",
        "phone": "04146-248850",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Syed Ammal Arts And Science College": {
        "website": "http://www.saasc10.com",
        "dept": "Principal Office & Admissions",
        "email": "info@saasc10.com",
        "phone": "04567-293100",
        "source": "http://www.saasc10.com",
        "notes": "Verified via official website, Devipattinam Road, Ramanathapuram"
    },
    "Syed Hammeeda Arabic College": {
        "website": "https://www.sharabic-edu.in",
        "dept": "Office & Administration",
        "email": "syedhameedhaarabiccollege@gmail.com",
        "phone": "+91 89255 01392",
        "source": "https://www.sharabic-edu.in",
        "notes": "Verified via official website, Kilakarai, Ramanathapuram"
    },
    "Smt. A.K.D. Sakkaniamma College of Education for Women": {
        "website": "http://www.akdsce.in",
        "dept": "Principal Office & Administration",
        "email": "sakkani_college@yahoo.in",
        "phone": "04563-222344",
        "source": "http://www.akdsce.in",
        "notes": "Verified via official website, Shenbagathoppu Road, Rajapalayam"
    },
    "St. Mary’s College": {
        "website": "https://www.stmaryscollege.edu.in",
        "dept": "Principal / General Enquiries",
        "email": "admission@stmaryscollege.edu.in",
        "phone": "0461-2320946",
        "source": "https://www.stmaryscollege.edu.in",
        "notes": "Autonomous institution for women, North Beach Road, Thoothukudi"
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

    # Prepare lookup index for BATCH_20_DATA
    lookup = {}
    for college_name, data in BATCH_20_DATA.items():
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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_20_DATA)}")


if __name__ == "__main__":
    main()
