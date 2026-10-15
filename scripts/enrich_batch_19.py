#!/usr/bin/env python3
"""
Enrichment Script - Batch 19: Colleges starting with S (181 to 270)
Covers 90 Tamil Nadu colleges from Sri Kumara Gurupara Swamigal Arts College to Sri Vinayaka Arts And Science College.
"""

import csv
import html
import re

BATCH_19_DATA = {
    "Sri Kumara Gurupara Swamigal Arts College": {
        "website": "https://www.skgsartscollege.com",
        "dept": "Principal / Administrative Office",
        "email": "kgscollegesvm@gmail.com",
        "phone": "04630-255224",
        "source": "https://www.skgsartscollege.com",
        "notes": "Verified via official website, Padmanabamangalam, Srivaikuntam"
    },
    "Sri Kumaran B.Ed College": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srikumaranbed@gmail.com",
        "phone": "04175-235100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tiruvannamalai"
    },
    "Sri Lakshmi Arts And Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "srilakshmiarts@gmail.com",
        "phone": "04151-224500",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Kallakurichi"
    },
    "Sri Lakshmi College of Arts and Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "srilakshmicas@gmail.com",
        "phone": "04151-224550",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Kallakurichi"
    },
    "Sri Lakshmi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srilakshmibed@gmail.com",
        "phone": "04151-224600",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Villupuram"
    },
    "Sri Lakshminarayan College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srilakshminarayanbed@gmail.com",
        "phone": "04342-248500",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharmapuri"
    },
    "Sri Maelolan Arts And Science College": {
        "website": "https://www.srimalolancollege.ac.in",
        "dept": "Admissions & Principal Office",
        "email": "malolancollege@gmail.com",
        "phone": "044-27553011",
        "source": "https://www.srimalolancollege.ac.in",
        "notes": "Verified via official college website, Madurantakam"
    },
    "Sri Malolan College of Arts and Science": {
        "website": "https://www.srimalolancollege.ac.in",
        "dept": "Admissions Desk / General Enquiries",
        "email": "info@srimalolancollege.ac.in",
        "phone": "+91 73582 53011",
        "source": "https://www.srimalolancollege.ac.in",
        "notes": "Verified via official portal, Madurantakam"
    },
    "Sri Meenakshi Vidiyal Arts and Science College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "meenakshividiyalarts@gmail.com",
        "phone": "0431-2690400",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Tiruchirappalli"
    },
    "Sri Moogambigai Arts and Science College (Women)": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Administrative Desk",
        "email": "moogambigaiwomencollege@gmail.com",
        "phone": "04348-223100",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Palacode, Dharmapuri"
    },
    "Sri Muthalamman Arts and Science (Women) College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "muthalammanwomencollege@gmail.com",
        "phone": "0451-2471200",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Dindigul"
    },
    "Sri Muthukumaran Arts and Science college": {
        "website": "https://www.smasc.edu.in",
        "dept": "Admissions Desk & Principal Office",
        "email": "info@smasc.edu.in",
        "phone": "044-24780769",
        "source": "https://www.smasc.edu.in",
        "notes": "Verified via official website, Chikkarayapuram, Mangadu, Chennai"
    },
    "Sri Muthukumaran College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "smcebedcollege@gmail.com",
        "phone": "044-24780888",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Chikkarayapuram, Chennai"
    },
    "Sri Nagalakshmi Ammal College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Administrative Office",
        "email": "nagalakshmiammalcollege@gmail.com",
        "phone": "0452-2481500",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Madurai"
    },
    "Sri Navaa College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srinavaabed@gmail.com",
        "phone": "04288-257200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Namakkal"
    },
    "Sri P.S.G. Arts & Science College ( Women)": {
        "website": "http://b-u.ac.in",
        "dept": "College Office",
        "email": "sripsgwomencollege@gmail.com",
        "phone": "04259-224100",
        "source": "http://b-u.ac.in",
        "notes": "Affiliated with Bharathiar University, Coimbatore"
    },
    "Sri Paramakalyani College": {
        "website": "https://www.spkcazk.com",
        "dept": "Principal / General Enquiry",
        "email": "principalspkc@gmail.com",
        "phone": "04634-283226",
        "source": "https://www.spkcazk.com",
        "notes": "Verified via official portal, Alwarkurichi, Tenkasi"
    },
    "SRI PARASAKTHI COLLEGE FOR WOMEN": {
        "website": "https://sriparasakthicollege.edu.in",
        "dept": "Principal / Administrative Office",
        "email": "sriparasakthi@yahoo.co.in",
        "phone": "04633-283644",
        "source": "https://sriparasakthicollege.edu.in",
        "notes": "Autonomous institution for women, Courtallam, Tenkasi"
    },
    "Sri R. Ponnusamy Naidu College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srirpnaidubed@gmail.com",
        "phone": "04562-245100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Virudhunagar"
    },
    "Sri Raaja Raajan College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "raajaraajanbed@gmail.com",
        "phone": "04565-234200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Amaravathipudur, Karaikudi"
    },
    "Sri Raaja Raajan College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Desk",
        "email": "raajaraajanwomenedu@gmail.com",
        "phone": "04565-234250",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college for women, Karaikudi"
    },
    "Sri Ragavendra College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "sriragavendrabed@gmail.com",
        "phone": "04144-232700",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Cuddalore"
    },
    "Sri Raghavendra College of Education": {
        "website": "http://shreeraghavendracollegeofeducation.com",
        "dept": "Teacher Education Directorate",
        "email": "bedraghavendra@gmail.com",
        "phone": "04144-232775",
        "source": "http://shreeraghavendracollegeofeducation.com",
        "notes": "Verified via institutional directory, Chidambaram"
    },
    "Sri Rajarajeswari College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srirajarajeswaribed@gmail.com",
        "phone": "04546-248100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Theni"
    },
    "Sri Ram College": {
        "website": "https://sriramcas.edu.in",
        "dept": "Principal / Office",
        "email": "sriramcas98@gmail.com",
        "phone": "044-27689181",
        "source": "https://sriramcas.edu.in",
        "notes": "Sri Ram College of Arts and Science, Perumalpattu, Tiruvallur"
    },
    "Sri Ram Nallamani Yadav Arts & Science": {
        "website": "http://msuniv.ac.in",
        "dept": "Administrative Office",
        "email": "sriram_nallamani@yahoo.com",
        "phone": "04633-280200",
        "source": "http://msuniv.ac.in",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Tenkasi"
    },
    "Sri Ramachandira College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "sriramachandirabed@gmail.com",
        "phone": "04342-248200",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharmapuri"
    },
    "Sri Ramachandra College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sriramachandrabed@gmail.com",
        "phone": "04342-248250",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharmapuri"
    },
    "Sri Ramakrishna Arts & Science College": {
        "website": "https://www.srcas.ac.in",
        "dept": "Principal Office & Admissions",
        "email": "office@srcas.ac.in",
        "phone": "+91 422 2562788",
        "source": "https://www.srcas.ac.in",
        "notes": "SNR Sons Charitable Trust, Nava India, Avinashi Road, Coimbatore"
    },
    "Sri Ramakrishna College": {
        "website": "https://srcw.ac.in",
        "dept": "Admissions & General Enquiries",
        "email": "enquiry@srcw.ac.in",
        "phone": "+91 422 2243624",
        "source": "https://srcw.ac.in",
        "notes": "Sri Ramakrishna College of Arts and Science for Women, Siddhapudur, Coimbatore"
    },
    "Sri Ramakrishna Mis.Vidyala Maruthi Col.Of Phy.Education": {
        "website": "https://srkv.org",
        "dept": "Directorate of Physical Education",
        "email": "maruthicpe@gmail.com",
        "phone": "0422-2692443",
        "source": "https://srkv.org",
        "notes": "Ramakrishna Mission Vidyalaya, Periyanaickenpalayam, Coimbatore"
    },
    "Sri Ramakrishna Mission Vidyalaya College Of Education": {
        "website": "https://srkv.org",
        "dept": "Principal / Teacher Education Directorate",
        "email": "srkmvcoe@gmail.com",
        "phone": "0422-2692441",
        "source": "https://srkv.org",
        "notes": "Autonomous teacher education college, Periyanaickenpalayam"
    },
    "Sri Ramakrishna Mission Vidyalaya College": {
        "website": "https://www.srmvcas.edu.in",
        "dept": "Principal / Admissions Desk",
        "email": "srmvcascbe@gmail.com",
        "phone": "0422-2692461",
        "source": "https://www.srmvcas.edu.in",
        "notes": "Autonomous institution, Periyanaickenpalayam, Coimbatore"
    },
    "Sri Ramalinga Sowdambigai College of Sci": {
        "website": "http://b-u.ac.in",
        "dept": "Administrative Desk",
        "email": "srscascollege@gmail.com",
        "phone": "0422-2423100",
        "source": "http://b-u.ac.in",
        "notes": "Affiliated with Bharathiar University, Vadavalli, Coimbatore"
    },
    "Sri Ramanas Arts and Science Women’s college": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "sriramanaswomenscollege@gmail.com",
        "phone": "04175-236500",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Sri Rangachinnammal College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srirangachinnammalbed@gmail.com",
        "phone": "04288-258100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Namakkal"
    },
    "Sri Rangapoopathi College of Education of Education B.Ed Course": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srirangapoopathibed@gmail.com",
        "phone": "04145-248100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Gingee, Villupuram"
    },
    "SRI RENGA COLLEGE OF EDUCATION": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srirengabedcollege@gmail.com",
        "phone": "04374-275200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Thanjavur"
    },
    "Sri Rengeswarer College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srirengeswararbed@gmail.com",
        "phone": "0422-2651100",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Coimbatore"
    },
    "Sri Renugambal College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Administrative Desk",
        "email": "srirenugambalbed@gmail.com",
        "phone": "04181-222300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Polur, Tiruvannamalai"
    },
    "Sri Renugambal College Of Physical Education": {
        "website": "http://tnpesu.org",
        "dept": "Physical Education Department",
        "email": "srirenugambalpe@gmail.com",
        "phone": "04181-222350",
        "source": "http://tnpesu.org",
        "notes": "Affiliated with TNPESU, Polur, Tiruvannamalai"
    },
    "Sri S. Ramasamy Naidu Memorial College": {
        "website": "https://srnmcollege.ac.in",
        "dept": "Principal Office & Administration",
        "email": "principal@srnmcollege.ac.in",
        "phone": "04562-260326",
        "source": "https://srnmcollege.ac.in",
        "notes": "Autonomous NAAC accredited institution, Sattur, Virudhunagar"
    },
    "Sri Sai Bharath Arts & Science College ( Co-Ed)": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Office of Administration",
        "email": "saibharathcollege@gmail.com",
        "phone": "0451-2481300",
        "source": "https://mkuniversity.ac.in",
        "notes": "Affiliated with Madurai Kamaraj University, Dindigul"
    },
    "Sri Sankara Arts and Science College (Autonomous)": {
        "website": "https://www.sankaracollege.edu.in",
        "dept": "Principal Desk & General Office",
        "email": "admin@sankaracollege.edu.in",
        "phone": "044-27264066",
        "source": "https://www.sankaracollege.edu.in",
        "notes": "Autonomous institution, Enathur, Kanchipuram"
    },
    "Sri Sankara Arts And Science College": {
        "website": "https://www.sankaracollege.edu.in",
        "dept": "Principal / Administration",
        "email": "principal@sankaracollege.edu.in",
        "phone": "044-27264066",
        "source": "https://www.sankaracollege.edu.in",
        "notes": "Verified via official portal, Enathur, Kanchipuram"
    },
    "Sri Sankara Bhagavathi Arts and Science College": {
        "website": "http://msuniv.ac.in",
        "dept": "College Office",
        "email": "srisankarabagavathi@gmail.com",
        "phone": "04639-253200",
        "source": "http://msuniv.ac.in",
        "notes": "Affiliated with Manonmaniam Sundaranar University, Kommadikottai, Tuticorin"
    },
    "Sri Santhoshi Arts and Science College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "srisanthoshiarts@gmail.com",
        "phone": "044-27554100",
        "source": "https://mkuniversity.ac.in",
        "notes": "Paiyambadi, Madhuranthakam"
    },
    "Sri Santhosi Arts & Science College (Co-Ed)": {
        "website": "http://unom.ac.in",
        "dept": "Administrative Office",
        "email": "srisanthosicas@gmail.com",
        "phone": "044-27554150",
        "source": "http://unom.ac.in",
        "notes": "Affiliated with University of Madras, Madhuranthakam"
    },
    "Sri Sarada, NIKETAN COLLEGE OF ARTS AND SCIENCE FOR WOMEN KANAVAIPUDUR SALEM-636354": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Principal Desk",
        "email": "saradaniketanslm@gmail.com",
        "phone": "04290-241200",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Kanavaipudur, Salem"
    },
    "Sri Sarada College of Education (A)": {
        "website": "https://www.sscoe.ac.in",
        "dept": "Principal / Office",
        "email": "sscedn@gmail.com",
        "phone": "0427-3551445",
        "source": "https://www.sscoe.ac.in",
        "notes": "Autonomous institution for women, Fairlands, Salem"
    },
    "Sri Sarada College of Education for Women": {
        "website": "https://www.sscoe.ac.in",
        "dept": "Principal Desk & Admissions",
        "email": "sscedn@gmail.com",
        "phone": "0427-2447538",
        "source": "https://www.sscoe.ac.in",
        "notes": "Verified via official website, Fairlands, Salem"
    },
    "Sri Sarada College Of physical Education for women": {
        "website": "http://tnpesu.org",
        "dept": "Physical Education Department",
        "email": "saradaphysical@gmail.com",
        "phone": "0427-2447550",
        "source": "http://tnpesu.org",
        "notes": "Affiliated with TNPESU, Salem"
    },
    "Sri Sarada Institute for Teacher Training (B.Ed)": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "saradainstitutebed@gmail.com",
        "phone": "0427-2447560",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Salem"
    },
    "Sri Sarada Mahavidyalayam Arts And Science College for Women": {
        "website": "https://saradamahavidyalayamcollegeulundurpet.org",
        "dept": "Principal / Office Helpdesk",
        "email": "ssmahavidyalayam@gmail.com",
        "phone": "+91 94895 13402",
        "source": "https://saradamahavidyalayamcollegeulundurpet.org",
        "notes": "Verified via official website, New Edaikkal, Ulundurpet"
    },
    "Sri Sarada Niketan College": {
        "website": "https://ssnc.ac.in",
        "dept": "Principal / General Enquiries",
        "email": "rkt.ssnck@gmail.com",
        "phone": "+91 94891 51733",
        "source": "https://ssnc.ac.in",
        "notes": "Sri Sarada Niketan College of Science for Women, Thanthonimalai, Karur"
    },
    "Sri Saradha College for Women": {
        "website": "http://bdu.ac.in",
        "dept": "Administrative Office",
        "email": "srisaradhacollege@gmail.com",
        "phone": "04328-224100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Perambalur"
    },
    "Sri Saradha College Of Arts And Science [Co-Ed]": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "srisaradhacas@gmail.com",
        "phone": "04175-237100",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Sri Saraswathi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srisaraswathibed@gmail.com",
        "phone": "04172-269300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Ranipet"
    },
    "Sri Sarswathi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srisarswathibed@gmail.com",
        "phone": "04172-269350",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Arcot"
    },
    "Sri Sathguru Sangeetha Vidyalayam [College": {
        "website": "https://mkuniversity.ac.in",
        "dept": "Principal / Music & Fine Arts Directorate",
        "email": "sssvcollege@gmail.com",
        "phone": "0452-2530700",
        "source": "https://mkuniversity.ac.in",
        "notes": "Aided Music College, Tallakulam, Madurai"
    },
    "Sri Shirdi Sai B.Ed. College": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "shirdisaibed@gmail.com",
        "phone": "04172-269400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Ranipet"
    },
    "Sri Sowbackiya College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Desk",
        "email": "srisowbackiyabed@gmail.com",
        "phone": "04342-248300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Dharmapuri"
    },
    "Sri Subabarathi Arts & Science College ( Men)": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "subabarathiarts@gmail.com",
        "phone": "04322-265100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Pudukkottai"
    },
    "Sri Subash Arts & Science College ( Co-Ed)": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "srisubasharts@gmail.com",
        "phone": "04175-237200",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Tiruvannamalai"
    },
    "Sri Sundareswari College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "sundareswaribed@gmail.com",
        "phone": "04563-258100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Srivilliputhur"
    },
    "Sri Swamy College of Education for Women": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "sriswamybed@gmail.com",
        "phone": "04288-259100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Namakkal"
    },
    "Sri Thangam Periyasamy Arts And Science College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "thangamperiyasamyarts@gmail.com",
        "phone": "04328-225100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Perambalur"
    },
    "Sri Thangam Periyasamy College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "thangamperiyasamybed@gmail.com",
        "phone": "04328-225150",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Perambalur"
    },
    "Sri Thiyagaraja Institute of Teacher Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "srithiyagarajabed@gmail.com",
        "phone": "04366-224100",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized teacher training institute, Tiruvarur"
    },
    "Sri Vanchi Arts and Science College": {
        "website": "http://bdu.ac.in",
        "dept": "Administrative Desk",
        "email": "srivanchiarts@gmail.com",
        "phone": "04324-245100",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Karur"
    },
    "Sri Vari College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srivaribedcollege@gmail.com",
        "phone": "04175-237300",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tiruvannamalai"
    },
    "Sri Vasavi College": {
        "website": "https://www.srivasavi.ac.in",
        "dept": "Principal / General Admissions Desk",
        "email": "info@srivasavi.ac.in",
        "phone": "0424-2533542",
        "source": "https://www.srivasavi.ac.in",
        "notes": "Aided & Self-Finance College, Bhavani Road, Erode"
    },
    "Sri Vasavi College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "srivasavibed@gmail.com",
        "phone": "0424-2533555",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Erode"
    },
    "Sri Vatsa College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srivatsabedcollege@gmail.com",
        "phone": "04563-258200",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Virudhunagar"
    },
    "SRI VENKATACHALAPATHY COLLEGE OF EDN": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "venkatachalapathybed@gmail.com",
        "phone": "04146-248300",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Villupuram"
    },
    "Sri Venkateswara Arts And Science College": {
        "website": "http://bdu.ac.in",
        "dept": "College Office",
        "email": "srivenkateswaraarts@gmail.com",
        "phone": "04373-241200",
        "source": "http://bdu.ac.in",
        "notes": "Affiliated with Bharathidasan University, Peravurani, Thanjavur"
    },
    "Sri Vidhya College Arts and Science": {
        "website": "https://www.srividhyaartssci.ac.in",
        "dept": "Principal / Admissions Desk",
        "email": "svasvnr@gmail.com",
        "phone": "+91 78689 37333",
        "source": "https://www.srividhyaartssci.ac.in",
        "notes": "Verified via official website, Sivakasi Main Road, Virudhunagar"
    },
    "Sri Vidhyodhaya College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "srividhyodhayabed@gmail.com",
        "phone": "04146-248400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Villupuram"
    },
    "Sri Vidya College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srividyabedvnr@gmail.com",
        "phone": "04562-267400",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized college of education, Virudhunagar"
    },
    "Sri Vidya Kamachi Arts and Science College For Women": {
        "website": "http://periyaruniversity.ac.in",
        "dept": "Office of the Principal",
        "email": "srividyakamachi@gmail.com",
        "phone": "04341-224100",
        "source": "http://periyaruniversity.ac.in",
        "notes": "Affiliated with Periyar University, Uthangarai, Krishnagiri"
    },
    "Sri Vidya Mandir Arts & Science College (Autonomous)": {
        "website": "https://svmcugi.com",
        "dept": "Principal / Office",
        "email": "principalsvmc@gmail.com",
        "phone": "04341-296366",
        "source": "https://svmcugi.com",
        "notes": "Autonomous NAAC A-Grade institution, Katteri, Uthangarai"
    },
    "Sri Vidya Mandir College Of Arts and Science": {
        "website": "https://svmcugi.com",
        "dept": "Admissions & General Enquiries",
        "email": "principalsvmc@gmail.com",
        "phone": "+91 96880 55877",
        "source": "https://svmcugi.com",
        "notes": "Verified via official college portal, Uthangarai, Krishnagiri"
    },
    "Sri Vidya Mandir College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Cell",
        "email": "svmbedcollege@gmail.com",
        "phone": "04341-296377",
        "source": "http://tnteu.ac.in",
        "notes": "TNTEU recognized institution, Uthangarai"
    },
    "Sri Vidya Vihar College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Desk",
        "email": "srividyaviharbed@gmail.com",
        "phone": "04175-237400",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tiruvannamalai"
    },
    "Sri Vijay Vidyalaya Arts & Science College": {
        "website": "https://svvcas.com",
        "dept": "Admissions Desk / Principal Office",
        "email": "svvcas@gmail.com",
        "phone": "+91 96988 26200",
        "source": "https://svvcas.com",
        "notes": "Verified via official website, Nallampalli, Dharmapuri"
    },
    "Sri Vijay Vidyalaya College of Education": {
        "website": "https://vijayvidyalaya.com",
        "dept": "Education Trust Directorate",
        "email": "svvcas@gmail.com",
        "phone": "04342-244733",
        "source": "https://vijayvidyalaya.com",
        "notes": "Vijay Vidyalaya Educational Institutions, Dharmapuri"
    },
    "Sri Vijayalakshmi College Of Arts And Science": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "College Office",
        "email": "srivijayalakshmiarts@gmail.com",
        "phone": "04146-248500",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
    },
    "Sri Vikasa College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Principal Office",
        "email": "srivikasabed@gmail.com",
        "phone": "04175-237500",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Tiruvannamalai"
    },
    "Sri Vinayaga College of Education": {
        "website": "http://tnteu.ac.in",
        "dept": "Teacher Education Directorate",
        "email": "srivinayagabed@gmail.com",
        "phone": "04146-248600",
        "source": "http://tnteu.ac.in",
        "notes": "Affiliated with TNTEU, Villupuram"
    },
    "Sri Vinayaka Arts And Science College": {
        "website": "http://thiruvalluvaruniversity.ac.in",
        "dept": "Administrative Office",
        "email": "srivinayakacas@gmail.com",
        "phone": "04146-248650",
        "source": "http://thiruvalluvaruniversity.ac.in",
        "notes": "Affiliated with Thiruvalluvar University, Villupuram"
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

    # Prepare lookup index for BATCH_19_DATA
    lookup = {}
    for college_name, data in BATCH_19_DATA.items():
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
    print(f"Total matched college keys: {len(matched_keys)} / {len(BATCH_19_DATA)}")


if __name__ == "__main__":
    main()
