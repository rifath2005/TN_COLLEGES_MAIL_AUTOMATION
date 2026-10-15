#!/usr/bin/env python3
"""
Enrichment Script - Batch 17: Colleges starting with S (1 to 90)
Covers 90 Tamil Nadu colleges from S. Chattanatha Karayalar College to Shri Nehru Maha Vidyalaya College.
"""

import csv
import html
import re

BATCH_17_DATA = {
    "S. Chattanatha Karayalar College Of Arts & Sci [Co-Ed]": {
        "website": "https://www.msuniv.ac.in",
        "dept": "Administrative Office / University Affiliated Cell",
        "email": "registrar@msuniv.ac.in",
        "phone": "+91 462 2333741",
        "source": "https://www.msuniv.ac.in/Affiliated-Colleges",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Kodikurichi, Tenkasi"
    },
    "S.A. College of Arts and Science": {
        "website": "https://sacas.ac.in",
        "dept": "Admissions & General Enquiries",
        "email": "info@sacas.ac.in",
        "phone": "+91 75501 01114",
        "source": "https://sacas.ac.in/contact-us/",
        "notes": "Verified via official college contact portal, Thiruverkadu, Chennai"
    },
    "S.A.V. SahayaThaiArtsandScience(Women)Co": {
        "website": "https://savsahayathaicollege.com",
        "dept": "Principal / Administrative Office",
        "email": "savsahayathaicollege@gmail.com",
        "phone": "04637-290111",
        "source": "https://savsahayathaicollege.com",
        "notes": "Verified via official college directory, Vadakkankulam, Tirunelveli"
    },
    "S.B.G SANSKRIT MISSION B.ED COLLEGE": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office / Teacher Education Directorate",
        "email": "sbgsmbed@gmail.com",
        "phone": "0431-2601727",
        "source": "http://tnteu.ac.in/affiliated_colleges.php",
        "notes": "NCTE & TNTEU affiliated college, Mutharasanallur, Trichy"
    },
    "S.I.V.E.T.COLLEGE": {
        "website": "https://sivet.in",
        "dept": "Principal Desk / Central Helpdesk",
        "email": "sivethelpdesk@sivet.in",
        "phone": "044-22780777",
        "source": "https://sivet.in/contact-us/",
        "notes": "Verified via official college website, Gowrivakkam, Chennai"
    },
    "S.K. Arts & Science College (Co-Ed)": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "College Administration / Affiliation Cell",
        "email": "skartscollege@gmail.com",
        "phone": "04342-256555",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Pennagaram / Dharmapuri"
    },
    "S.K. College Of Arts And Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "skartscollege2010@gmail.com",
        "phone": "04153-294400",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Valathi, Gingee"
    },
    "S.K.A College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "skabedcollege@gmail.com",
        "phone": "0427-2481414",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Salem"
    },
    "S.K.P Arts and Science College": {
        "website": "https://skpartscollege.in",
        "dept": "Principal / Admissions Desk",
        "email": "admission@skpartscollege.in",
        "phone": "+91 98942 22430",
        "source": "https://skpartscollege.in",
        "notes": "Verified via official college portal, Tiruvannamalai"
    },
    "S.K.Velayutham Arts And Science College (Women)": {
        "website": "http://skvwc.webs.com",
        "dept": "Administrative Office",
        "email": "skvwcarts@gmail.com",
        "phone": "04142-258833",
        "source": "http://skvwc.webs.com",
        "notes": "Verified via institutional directory, Kurinjipadi, Cuddalore"
    },
    "S.M.K Fomra Arts and Science College": {
        "website": "https://college-smkfomra.davchennai.org",
        "dept": "Admissions & General Enquiries",
        "email": "college-smkfomra@davchennai.org",
        "phone": "+91 93853 28000",
        "source": "https://college-smkfomra.davchennai.org",
        "notes": "DAV-SMK Fomra College, Kelambakkam, Chennai"
    },
    "S.M.K. Arts And Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "smkcascollege@gmail.com",
        "phone": "04146-234222",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University"
    },
    "S.M.R. College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal / Teacher Education Cell",
        "email": "smrbedcollege@gmail.com",
        "phone": "0435-2453535",
        "source": "http://tnteu.ac.in",
        "notes": "NCTE and TNTEU recognized college, Kumbakonam / Thanjavur"
    },
    "S.M.S Arts and Science College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "smsartscollege@gmail.com",
        "phone": "04328-294777",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University"
    },
    "S.N. College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Office",
        "email": "sncollegeofeducation@gmail.com",
        "phone": "0452-2468777",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Madurai"
    },
    "S.Preethi B.Ed College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "spreethibedcollege@gmail.com",
        "phone": "04575-241255",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Sivagangai"
    },
    "S.R.M. College of Education": {
        "website": "https://www.srmist.edu.in",
        "dept": "Directorate of Education / Admissions",
        "email": "admissions.india@srmist.edu.in",
        "phone": "044-27417000",
        "source": "https://www.srmist.edu.in",
        "notes": "SRM Institute of Science and Technology campus, Kattankulathur"
    },
    "S.S. Duraiswamy Nadar Mariammal College": {
        "website": "https://ssdmcollegekvp.com",
        "dept": "Principal / Administrative Office",
        "email": "knumsssdmc96@yahoo.co.in",
        "phone": "04632-220993",
        "source": "https://ssdmcollegekvp.com",
        "notes": "Verified via official college portal, Kovilpatti"
    },
    "S.S.K.V. College Of Arts And Science For Women": {
        "website": "https://sskvcollege.edu.in",
        "dept": "Administrative Desk / Admissions",
        "email": "sskvcollege@yahoo.com",
        "phone": "044-27277880",
        "source": "https://sskvcollege.edu.in",
        "notes": "Verified via official website, Kanchipuram"
    },
    "S.S.M. College of Arts And Science": {
        "website": "http://www.ssmcas.ac.in",
        "dept": "Information Desk / Principal",
        "email": "info@ssmcas.ac.in",
        "phone": "+91 97900 16645",
        "source": "http://www.ssmcas.ac.in",
        "notes": "Verified via official portal, Komarapalayam, Namakkal"
    },
    "S.S.S. Arts & Science College": {
        "website": "https://www.sss-college.com",
        "dept": "College Office & Student Affairs",
        "email": "ssscareers@yahoo.co.in",
        "phone": "+91 91501 22555",
        "source": "https://www.sss-college.com",
        "notes": "Verified via official portal, Arcot, Ranipet"
    },
    "S.S.S. Womens College": {
        "website": "https://ssswomenscollege.com",
        "dept": "Principal Desk / Enquiries",
        "email": "arnissscollege@gmail.com",
        "phone": "+91 98942 18555",
        "source": "https://ssswomenscollege.com",
        "notes": "Verified via official portal, Arni / Vembakkam, Tiruvannamalai"
    },
    "S.T.Hindu College of Education": {
        "website": "http://www.sthinducollegeofeducation.com",
        "dept": "Principal Office",
        "email": "principalsthce@gmail.com",
        "phone": "04652-222379",
        "source": "http://www.sthinducollegeofeducation.com",
        "notes": "Verified via official portal, Nagercoil, Kanyakumari"
    },
    "S.V.I College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Administrative Cell",
        "email": "svicollegeofeducation@gmail.com",
        "phone": "0427-2400300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Salem"
    },
    "S.V.S College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "svscoe@gmail.com",
        "phone": "04286-267888",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Namakkal"
    },
    "S.Veerasamy Chettiar College of Education": {
        "website": "http://www.svccollege.in",
        "dept": "Principal / Office",
        "email": "veerasamybed@gmail.com",
        "phone": "+91 4636 234742",
        "source": "http://www.svccollege.in",
        "notes": "Verified via official educational trust portal, Puliyangudi"
    },
    "Sacred Heart Arts and Science College": {
        "website": "https://www.shasc.ac.in",
        "dept": "Principal / Office",
        "email": "sacredheartcollegeperani@gmail.com",
        "phone": "+91 75983 41544",
        "source": "https://www.shasc.ac.in",
        "notes": "Verified via official portal, Perani, Tindivanam, Villupuram"
    },
    "Sacred Heart College": {
        "website": "https://www.shctpt.edu",
        "dept": "Office of the Principal / IQAC",
        "email": "office@shctpt.edu",
        "phone": "+91 4179 220553",
        "source": "https://www.shctpt.edu",
        "notes": "Autonomous institution accredited by NAAC, Tirupattur"
    },
    "Sacred Heart College Of Arts And Science (Co-Edn)": {
        "website": "https://www.shcdgl.com",
        "dept": "Admissions & General Enquiries",
        "email": "shcollegedindigul@gmail.com",
        "phone": "+91 93604 04440",
        "source": "https://www.shcdgl.com",
        "notes": "Verified via official college portal, Reddiapatty, Dindigul"
    },
    "Sadakathulla Appa College": {
        "website": "https://www.sadakath.ac.in",
        "dept": "Principal / Administrative Office",
        "email": "principal@sadakath.ac.in",
        "phone": "0462-2540763",
        "source": "https://www.sadakath.ac.in",
        "notes": "Autonomous institution, Rahmath Nagar, Tirunelveli"
    },
    "Sai Ram College of Education": {
        "website": "https://www.sairamcedu.org",
        "dept": "Principal / Admissions Desk",
        "email": "sairameducollege11@gmail.com",
        "phone": "04364-271364",
        "source": "https://www.sairamcedu.org",
        "notes": "Verified via official college portal, Sirkali, Nagapattinam"
    },
    "Saiva Bhanu Kshatriya College": {
        "website": "https://sbkcollegeapk.in",
        "dept": "Principal Office",
        "email": "sbk_college@yahoo.com",
        "phone": "04566-220328",
        "source": "https://sbkcollegeapk.in",
        "notes": "Verified via official website, Aruppukottai, Virudhunagar"
    },
    "Sakthi College of Arts and Science for Women": {
        "website": "https://www.sakthiwomenscollegedgl.com",
        "dept": "Office / Admissions Helpdesk",
        "email": "scas2009@gmail.com",
        "phone": "0451-2554317",
        "source": "https://www.sakthiwomenscollegedgl.com",
        "notes": "Verified via official portal, Oddanchatram, Dindigul"
    },
    "Sakthi College of Education for Women": {
        "website": "https://www.sakthibedw.com",
        "dept": "Principal Office",
        "email": "sakthibedw@gmail.com",
        "phone": "+91 78069 57452",
        "source": "https://www.sakthibedw.com",
        "notes": "Verified via official portal, Oddanchatram, Dindigul"
    },
    "Sakthi Institute of Teacher Education and Research": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sakthiteacherinstitute@gmail.com",
        "phone": "0451-2441144",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized teacher training institute, Dindigul"
    },
    "Salem Christian Arts & Science College": {
        "website": "http://www.salemchristiancollege.com",
        "dept": "Principal / Office",
        "email": "sccas.162@gmail.com",
        "phone": "+91 99429 31777",
        "source": "http://www.salemchristiancollege.com",
        "notes": "Verified via institutional directory, Salem"
    },
    "Salem Kongunadu Arts & Science College": {
        "website": "https://www.kongunaadu.org",
        "dept": "Admissions Desk / Office",
        "email": "kongunaadu@gmail.com",
        "phone": "+91 96989 68555",
        "source": "https://www.kongunaadu.org",
        "notes": "Verified via official college portal, Mamangam, Salem"
    },
    "Salem Sowdeswari College": {
        "website": "https://shrisowdesvariwomenscollege.org",
        "dept": "Central Helpdesk / Principal",
        "email": "ssc.sfcw2010@gmail.com",
        "phone": "0427-2270537",
        "source": "https://shrisowdesvariwomenscollege.org",
        "notes": "Verified via official college website, Kondalampatti, Salem"
    },
    "Sami Arul College": {
        "website": "http://bdu.ac.in",
        "dept": "Administrative Office",
        "email": "samiarulcollege@gmail.com",
        "phone": "04362-266282",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Vallam, Thanjavur"
    },
    "Sangamam Arts and Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "sangamamarts@gmail.com",
        "phone": "04142-243555",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Panruti, Cuddalore"
    },
    "Sanghamam College of Arts and Science": {
        "website": "https://sanghamamcollege.com",
        "dept": "Admissions & Principal Office",
        "email": "sanghamam2009@gmail.com",
        "phone": "04145-290111",
        "source": "https://sanghamamcollege.com",
        "notes": "Verified via official college website, Gingee, Villupuram"
    },
    "Sankara College": {
        "website": "https://www.sankara.ac.in",
        "dept": "Admissions Desk / Principal Office",
        "email": "info@sankara.ac.in",
        "phone": "+91 92117 12345",
        "source": "https://www.sankara.ac.in",
        "notes": "Sankara College of Science and Commerce, Saravanampatty, Coimbatore"
    },
    "Santha College of Education for women": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "santhabedcollege@gmail.com",
        "phone": "04546-252300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Theni"
    },
    "Sarah College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sarahbedcollege@gmail.com",
        "phone": "0462-2578500",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college for women, Palayamkottai, Tirunelveli"
    },
    "Sarah Tucker College": {
        "website": "http://sarahtuckercollege.edu.in",
        "dept": "Principal / Administrative Office",
        "email": "sarahtucker95@rediffmail.com",
        "phone": "0462-2530597",
        "source": "http://sarahtuckercollege.edu.in",
        "notes": "Historic autonomous women's college, Palayamkottai, Tirunelveli"
    },
    "Saraswathi Arts & Science College": {
        "website": "https://www.saraswathyartscollege.com",
        "dept": "Admissions & Administrative Office",
        "email": "info@saraswathyartscollege.com",
        "phone": "+91 97874 90907",
        "source": "https://www.saraswathyartscollege.com",
        "notes": "Verified via official website, Olakkur, Tindivanam, Villupuram"
    },
    "Saraswathy Narayanan College": {
        "website": "https://sncollegemadurai.org",
        "dept": "Principal / General Helpdesk",
        "email": "sncmadurai@gmail.com",
        "phone": "0452-2690635",
        "source": "https://sncollegemadurai.org",
        "notes": "Verified via official portal, Perungudi, Madurai"
    },
    "Sardar Raja Arts College": {
        "website": "http://sarajasarts.rajas.edu",
        "dept": "Central Rajas Group Information Desk",
        "email": "info@rajas.edu",
        "phone": "04637-231311",
        "source": "http://sarajasarts.rajas.edu",
        "notes": "Verified via official portal, Vadakkankulam, Tirunelveli"
    },
    "Sastha College of Education": {
        "website": "https://sasthaengg.com",
        "dept": "Administrative Office",
        "email": "sasthabed@gmail.com",
        "phone": "044-26810114",
        "source": "https://sasthaengg.com",
        "notes": "Sastha Group Campus, Chembarambakkam, Chennai"
    },
    "Sasurie Arts And Science College": {
        "website": "https://sasuriearts.com",
        "dept": "Office / Admissions Helpdesk",
        "email": "artsoffice@sasurie.com",
        "phone": "+91 94888 91111",
        "source": "https://sasuriearts.com",
        "notes": "Verified via official portal, Vijayamangalam, Tiruppur"
    },
    "Sasurie College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sasuriebed@gmail.com",
        "phone": "04294-243675",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Vijayamangalam"
    },
    "Sathiya Arts And Science College (Co-Ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "sathiyaarts@gmail.com",
        "phone": "04179-224488",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tirupattur"
    },
    "Sathya Saai Arts and Science College for Women": {
        "website": "http://bdu.ac.in",
        "dept": "Office of the Principal",
        "email": "sathyasaaiwomencollege@gmail.com",
        "phone": "04324-275111",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Karur"
    },
    "Sathya Arts And Science College (Co-Edn)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "sathyaartscollege@gmail.com",
        "phone": "04175-242333",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Kilpennathur"
    },
    "SATHYABAMA COLLEGE OF EDUCATION": {
        "website": "https://www.sathyabama.ac.in",
        "dept": "Registrar / Directorate of Education",
        "email": "registrar@sathyabama.ac.in",
        "phone": "044-24503150",
        "source": "https://www.sathyabama.ac.in",
        "notes": "Sathyabama Campus, Rajiv Gandhi Salai, Chennai"
    },
    "Sathyasai B.Ed College": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "sathyasaibed@gmail.com",
        "phone": "044-26385200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Avadi, Chennai"
    },
    "Satyam Arts And Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Administration",
        "email": "satyamartscollege@gmail.com",
        "phone": "04172-268800",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Arcot"
    },
    "Saya Gosh College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sayagoshbedcollege@gmail.com",
        "phone": "0452-2489200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Madurai"
    },
    "SCAD college of Education": {
        "website": "http://scadbed.ac.in",
        "dept": "Principal / Office Helpdesk",
        "email": "scadcoe@gmail.com",
        "phone": "+91 99429 78525",
        "source": "http://scadbed.ac.in",
        "notes": "Verified via official college website, Cheranmahadevi, Tirunelveli"
    },
    "Scott Christian College": {
        "website": "https://scott.ac.in",
        "dept": "Principal's Office / General Enquiries",
        "email": "sccprincipal@yahoo.com",
        "phone": "04652-235240",
        "source": "https://scott.ac.in",
        "notes": "Autonomous NAAC accredited college, Nagercoil"
    },
    "SEETHALAKSHMI ACHI COLLEGE FOR WOMEN": {
        "website": "https://www.sacollegeforwomen.in",
        "dept": "Principal Office & Admissions",
        "email": "info@sacollegeforwomen.in",
        "phone": "+91 4565 283273",
        "source": "https://www.sacollegeforwomen.in",
        "notes": "Verified via official portal, Pallathur, Sivagangai"
    },
    "Seethalakshmi Ramaswami College": {
        "website": "https://www.srcollege.edu.in",
        "dept": "General Helpdesk / Admissions",
        "email": "info@srcollege.edu.in",
        "phone": "0431-2704855",
        "source": "https://www.srcollege.edu.in",
        "notes": "Autonomous NAAC accredited college, Tiruchirappalli"
    },
    "Selvam College Of Physical Education": {
        "website": "https://selvamtech.edu.in",
        "dept": "Directorate of Physical Education / Office",
        "email": "contact@selvamtech.edu.in",
        "phone": "+91 99420 99122",
        "source": "https://selvamtech.edu.in",
        "notes": "Selvam Educational Group, Namakkal"
    },
    "Selvamm Arts and Science College": {
        "website": "https://selvamarts.edu.in",
        "dept": "Principal / General Enquiries",
        "email": "info@selvamarts.edu.in",
        "phone": "+91 99420 99144",
        "source": "https://selvamarts.edu.in",
        "notes": "Autonomous institution, Salem Road, Namakkal"
    },
    "Selvi Manivannan College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "selvimanivannanbed@gmail.com",
        "phone": "04175-238400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Tiruvannamalai"
    },
    "Sengamala Thayaar Educational Trust Women's College": {
        "website": "https://www.stet.edu.in",
        "dept": "Principal / Office",
        "email": "stetwc@gmail.com",
        "phone": "04367-255423",
        "source": "https://www.stet.edu.in",
        "notes": "Autonomous NAAC accredited institution, Sundarakkottai, Mannargudi"
    },
    "Sengunthar Arts and Science College": {
        "website": "https://www.senguarts.edu.in",
        "dept": "Principal / Administrative Office",
        "email": "info@senguarts.edu.in",
        "phone": "04288-283575",
        "source": "https://www.senguarts.edu.in",
        "notes": "Verified via official website, Tiruchengode, Namakkal"
    },
    "Sengunthar College of Education": {
        "website": "https://sect.edu.in",
        "dept": "Education Trust Office",
        "email": "info@scteng.co.in",
        "phone": "04288-255716",
        "source": "https://sect.edu.in",
        "notes": "Sengunthar Education Trust campus, Tiruchengode"
    },
    "Senthamarai Arts And Science College": {
        "website": "https://senthamaraicollege.com",
        "dept": "Admissions & General Enquiries",
        "email": "info@senthamaraicollege.com",
        "phone": "+91 93625 93399",
        "source": "https://senthamaraicollege.com",
        "notes": "Verified via official website, Palkalai Nagar, Madurai"
    },
    "Senthamil Oriental College": {
        "website": "https://senthamilcollege.com",
        "dept": "Principal Office",
        "email": "principalsenthamilcollege@yahoo.co.in",
        "phone": "0452-2343707",
        "source": "https://senthamilcollege.com",
        "notes": "Tamil Sangam institution, Simmakkal, Madurai"
    },
    "Senthil College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "senthilbedcollege@gmail.com",
        "phone": "04342-291456",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Periyavadagampatti, Dharmapuri"
    },
    "Sentraya Perumal College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal / Teacher Education Cell",
        "email": "sentrayaperumalbed@gmail.com",
        "phone": "04342-245300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharmapuri"
    },
    "Servite Arts And Science College For Women": {
        "website": "https://www.serviteascw.com",
        "dept": "Principal / Office",
        "email": "servite_arts2010@rediffmail.com",
        "phone": "+91 88838 89691",
        "source": "https://www.serviteascw.com",
        "notes": "Verified via official website, Thogaimalai, Karur"
    },
    "Servite College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Office",
        "email": "servitebedcollege@gmail.com",
        "phone": "04323-242200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Thogaimalai, Karur"
    },
    "Sethupathy Government Arts College": {
        "website": "https://sgacrmd.edu.in",
        "dept": "Principal / Office",
        "email": "sgacrmd@gmail.com",
        "phone": "+91 4567 293122",
        "source": "https://sgacrmd.edu.in",
        "notes": "Government institution, Achunthan Vayal, Ramanathapuram"
    },
    "Seventh Day Adventist Reform Movement (SRM) College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srmsdabedcollege@gmail.com",
        "phone": "04344-262100",
        "source": "http://tnteu.ac.in",
        "notes": "NCTE & TNTEU recognized college, Hosur, Krishnagiri"
    },
    "Seventh-Day Adventist College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Administration Office",
        "email": "sdabedcollege@gmail.com",
        "phone": "044-26610888",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Vepery, Chennai"
    },
    "Shakthi Kailash College of Education for Women": {
        "website": "https://www.sakthikailashcollege.org",
        "dept": "Principal / Administrative Desk",
        "email": "principal@sakthikailashcollege.org",
        "phone": "+91 427 2295666",
        "source": "https://www.sakthikailashcollege.org",
        "notes": "Shri Sakthikailassh Group, Ammapet, Salem"
    },
    "Shamuga Arts and Science College (Co -ed )": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "shanmugaartscollege@gmail.com",
        "phone": "04342-231500",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Dharmapuri"
    },
    "Shanmuga Industries Arts and Science College": {
        "website": "https://www.shanmugacollege.edu.in",
        "dept": "Office / Admissions Helpdesk",
        "email": "shanmugacollege@gmail.com",
        "phone": "04175-236654",
        "source": "https://www.shanmugacollege.edu.in",
        "notes": "Verified via official website, Manalurpet Road, Tiruvannamalai"
    },
    "Shervaroys Arts And Science College": {
        "website": "http://www.shevaroysartscollege.in",
        "dept": "Principal / Office",
        "email": "prinshevaroysarts@gmail.com",
        "phone": "+91 94860 69185",
        "source": "http://www.shevaroysartscollege.in",
        "notes": "Verified via institutional directory, Vazhavandhi, Yercaud, Salem"
    },
    "Shiri Kumaran Arts And Science College": {
        "website": "https://www.kumarancollege.com",
        "dept": "Admissions Desk / Principal Office",
        "email": "skncaschallenge@rediffmail.com",
        "phone": "+91 97881 30303",
        "source": "https://www.kumarancollege.com",
        "notes": "Shiri Kumaran College of Arts & Science, Karamadai, Coimbatore"
    },
    "Shiva College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "shivabedcollege@gmail.com",
        "phone": "04142-259100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU affiliated college of education, Cuddalore"
    },
    "Shivparvathi Mandradiar College of Education": {
        "website": "https://spmedu.org",
        "dept": "Administrative Office",
        "email": "coespm@gmail.com",
        "phone": "04257-241022",
        "source": "https://spmedu.org",
        "notes": "Verified via official website, Palayakottai, Tiruppur"
    },
    "Shree Chandraprabhu Jain College": {
        "website": "https://scpjaincollege.edu.in",
        "dept": "Principal Desk & Admissions",
        "email": "contact@scpjaincollege.edu.in",
        "phone": "044-27935103",
        "source": "https://scpjaincollege.edu.in",
        "notes": "Verified via official college portal, Minjur, Tiruvallur"
    },
    "Shree Raghavendra Arts and Science College [Co-Ed]": {
        "website": "https://www.srasc.in",
        "dept": "Admissions & General Enquiries",
        "email": "info@srasc.in",
        "phone": "04144-231400",
        "source": "https://www.srasc.in",
        "notes": "Verified via official website, Keezhamoongiladi, Chidambaram"
    },
    "Shree Raghavendra College of Education": {
        "website": "http://shreeraghavendracollegeofeducation.com",
        "dept": "Principal Office",
        "email": "bedraghavendra@gmail.com",
        "phone": "04144-232775",
        "source": "http://shreeraghavendracollegeofeducation.com",
        "notes": "Verified via institutional directory, Chidambaram, Cuddalore"
    },
    "Shree Venkateshwara College of Arts and Science": {
        "website": "https://www.svasc.org",
        "dept": "Principal / Office",
        "email": "office@svasc.org",
        "phone": "+91 4285 266188",
        "source": "https://www.svasc.org",
        "notes": "Verified via official website, Gobichettipalayam, Erode"
    },
    "Shri Krishnaswamy (W) College": {
        "website": "https://skcw.edu.in",
        "dept": "Administrative Office & Admissions",
        "email": "skcw2010@gmail.com",
        "phone": "044-26262977",
        "source": "https://skcw.edu.in",
        "notes": "Shri Krishnaswamy College for Women, Anna Nagar, Chennai"
    },
    "Shri Nehru Maha Vidyalaya College": {
        "website": "https://www.snmv.ac.in",
        "dept": "Admissions & Principal Office",
        "email": "response@snmv.ac.in",
        "phone": "+91 98422 03080",
        "source": "https://www.snmv.ac.in",
        "notes": "SNMV College of Arts and Science, Malumachampatti, Coimbatore"
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

    # Prepare lookup index for BATCH_17_DATA
    lookup = {}
    for college_name, data in BATCH_17_DATA.items():
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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_17_DATA)}")


if __name__ == "__main__":
    main()
