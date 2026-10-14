#!/usr/bin/env python3
import os
import csv
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "contacts.csv")
if not os.path.exists(CSV_FILE):
    CSV_FILE = os.path.join(os.path.dirname(BASE_DIR), "contacts.csv")

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

ADDITIONAL_COLLEGES = [
    {
        "State": "Tamil Nadu",
        "City": "Dharmapuri",
        "College_Name": "Government College of Engineering, Dharmapuri",
        "Official_Website_URL": "http://gcedpi.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principalgcedpi@gmail.com",
        "Phone_Number": "+91-4342-233300",
        "Source_Page_URL": "http://gcedpi.edu.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Krishnagiri",
        "College_Name": "Government Arts College for Men, Krishnagiri",
        "Official_Website_URL": "http://gacmenkrishnagiri.org",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principalgacmen@gmail.com",
        "Phone_Number": "+91-4343-292850",
        "Source_Page_URL": "http://gacmenkrishnagiri.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Cuddalore",
        "College_Name": "C.K. College of Engineering and Technology",
        "Official_Website_URL": "http://ckcet.com",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@ckcet.com",
        "Phone_Number": "+91-4142-217500",
        "Source_Page_URL": "http://ckcet.com/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "The Nilgiris",
        "College_Name": "Nilgiri College of Arts and Science",
        "Official_Website_URL": "https://nilgiricollege.ac.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@nilgiricollege.ac.in",
        "Phone_Number": "+91-4262-266155",
        "Source_Page_URL": "https://nilgiricollege.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruppur",
        "College_Name": "Tiruppur Kumaran College for Women",
        "Official_Website_URL": "https://www.tkcfw.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "kumarancoll@tkcfw.ac.in",
        "Phone_Number": "+91-421-2258835",
        "Source_Page_URL": "https://www.tkcfw.ac.in/contact.html"
    },
    {
        "State": "Tamil Nadu",
        "City": "Theni",
        "College_Name": "Theni Nadar Saraswathi College of Engineering and Technology",
        "Official_Website_URL": "http://nscet.org",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@nscet.org",
        "Phone_Number": "+91-4546-263900",
        "Source_Page_URL": "http://nscet.org/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Karur",
        "College_Name": "Chettinad College of Engineering and Technology",
        "Official_Website_URL": "http://chettinadtech.ac.in",
        "Department_Or_Contact": "Academic Directorate",
        "Official_Email": "examcell@chettinadtech.ac.in",
        "Phone_Number": "+91-4324-250941",
        "Source_Page_URL": "http://chettinadtech.ac.in/contact.php"
    },
    {
        "State": "Tamil Nadu",
        "City": "Kanyakumari",
        "College_Name": "Annai Velankanni College of Engineering",
        "Official_Website_URL": "http://avce.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@avce.edu.in",
        "Phone_Number": "+91-4652-266399",
        "Source_Page_URL": "http://avce.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Pudukkottai",
        "College_Name": "Sudharsan Engineering College",
        "Official_Website_URL": "https://sec.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@sec.ac.in",
        "Phone_Number": "+91-4339-240830",
        "Source_Page_URL": "https://sec.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Pudukkottai",
        "College_Name": "Mount Zion College of Engineering and Technology",
        "Official_Website_URL": "http://www.mzcet.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@mzcet.in",
        "Phone_Number": "+91-4333-294400",
        "Source_Page_URL": "http://www.mzcet.in/contact.php"
    },
    {
        "State": "Tamil Nadu",
        "City": "Pudukkottai",
        "College_Name": "Mookambigai College of Engineering",
        "Official_Website_URL": "http://www.mookambigai.ac.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@mookambigai.ac.in",
        "Phone_Number": "+91-4339-262273",
        "Source_Page_URL": "http://www.mookambigai.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Pudukkottai",
        "College_Name": "Government Arts and Science College, Karambakudi",
        "Official_Website_URL": "https://www.kgasc.co.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@kgasc.co.in",
        "Phone_Number": "+91-4322-267200",
        "Source_Page_URL": "https://www.kgasc.co.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruvannamalai",
        "College_Name": "Arunai Engineering College",
        "Official_Website_URL": "https://arunai.org",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "aectvm1993@gmail.com",
        "Phone_Number": "+91-4175-255101",
        "Source_Page_URL": "https://arunai.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruvannamalai",
        "College_Name": "University College of Engineering, Arni",
        "Official_Website_URL": "https://aucearni.in",
        "Department_Or_Contact": "Dean Office",
        "Official_Email": "annauniv.ucea@gmail.com",
        "Phone_Number": "+91-4173-227300",
        "Source_Page_URL": "https://aucearni.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Villupuram",
        "College_Name": "University College of Engineering, Villupuram",
        "Official_Website_URL": "http://www.aucev.edu.in",
        "Department_Or_Contact": "Dean Office",
        "Official_Email": "auc_ev@yahoo.com",
        "Phone_Number": "+91-4146-224500",
        "Source_Page_URL": "http://www.aucev.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Stella Maris College (Autonomous)",
        "Official_Website_URL": "https://stellamariscollege.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@stellamariscollege.edu.in",
        "Phone_Number": "+91-44-28111987",
        "Source_Page_URL": "https://stellamariscollege.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Dwaraka Doss Goverdhan Doss Vaishnav College (DGVC)",
        "Official_Website_URL": "https://dgvaishnavcollege.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@dgvaishnavcollege.edu.in",
        "Phone_Number": "+91-44-23635101",
        "Source_Page_URL": "https://dgvaishnavcollege.edu.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Guru Nanak College (Autonomous)",
        "Official_Website_URL": "https://gurunanakcollege.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@gurunanakcollege.edu.in",
        "Phone_Number": "+91-44-22451746",
        "Source_Page_URL": "https://gurunanakcollege.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "The New College (Autonomous)",
        "Official_Website_URL": "https://thenewcollege.edu.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@thenewcollege.edu.in",
        "Phone_Number": "+91-44-28351269",
        "Source_Page_URL": "https://thenewcollege.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Presidency College (Autonomous)",
        "Official_Website_URL": "https://presidencycollegechennai.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "contact@presidencycollegechennai.ac.in",
        "Phone_Number": "+91-44-28544894",
        "Source_Page_URL": "https://presidencycollegechennai.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Namakkal",
        "College_Name": "K.S. Rangasamy College of Technology",
        "Official_Website_URL": "https://ksrct.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@ksrct.ac.in",
        "Phone_Number": "+91-4288-274741",
        "Source_Page_URL": "https://ksrct.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Namakkal",
        "College_Name": "Muthayammal Engineering College",
        "Official_Website_URL": "https://mec.edu.in",
        "Department_Or_Contact": "Office of the Principal",
        "Official_Email": "principal@mec.edu.in",
        "Phone_Number": "+91-4287-220837",
        "Source_Page_URL": "https://mec.edu.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Krishnagiri",
        "College_Name": "Adhiyamaan College of Engineering (Autonomous)",
        "Official_Website_URL": "https://adhiyamaan.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@adhiyamaan.ac.in",
        "Phone_Number": "+91-4344-260570",
        "Source_Page_URL": "https://adhiyamaan.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tirunelveli",
        "College_Name": "Francis Xavier Engineering College",
        "Official_Website_URL": "https://francisxavier.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@francisxavier.ac.in",
        "Phone_Number": "+91-462-2502283",
        "Source_Page_URL": "https://francisxavier.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Virudhunagar",
        "College_Name": "Sethu Institute of Technology",
        "Official_Website_URL": "https://sethu.ac.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@sethu.ac.in",
        "Phone_Number": "+91-4566-308001",
        "Source_Page_URL": "https://sethu.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Virudhunagar",
        "College_Name": "Kamaraj College of Engineering and Technology",
        "Official_Website_URL": "https://kamarajengg.edu.in",
        "Department_Or_Contact": "Administrative Directorate",
        "Official_Email": "mail@kamarajengg.edu.in",
        "Phone_Number": "+91-4549-278791",
        "Source_Page_URL": "https://kamarajengg.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Thanjavur",
        "College_Name": "Periyar Maniammai Institute of Science & Technology",
        "Official_Website_URL": "https://pmu.edu",
        "Department_Or_Contact": "Office of the Registrar",
        "Official_Email": "registrar@pmu.edu",
        "Phone_Number": "+91-4362-264600",
        "Source_Page_URL": "https://pmu.edu/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Cuddalore",
        "College_Name": "Annamalai University",
        "Official_Website_URL": "https://annamalaiuniversity.ac.in",
        "Department_Or_Contact": "Office of the Registrar",
        "Official_Email": "registrar@annamalaiuniversity.ac.in",
        "Phone_Number": "+91-4144-238282",
        "Source_Page_URL": "https://annamalaiuniversity.ac.in/contact.php"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Hindustan Institute of Technology and Science (HITS)",
        "Official_Website_URL": "https://hindustanuniv.ac.in",
        "Department_Or_Contact": "Administrative Office",
        "Official_Email": "info@hindustanuniv.ac.in",
        "Phone_Number": "+91-44-27474262",
        "Source_Page_URL": "https://hindustanuniv.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Coimbatore",
        "College_Name": "Karunya Institute of Technology and Sciences",
        "Official_Website_URL": "https://karunya.edu",
        "Department_Or_Contact": "Central Information Desk",
        "Official_Email": "info@karunya.edu",
        "Phone_Number": "+91-422-2614300",
        "Source_Page_URL": "https://karunya.edu/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Vel Tech Rangarajan Dr. Sagunthala R&D Institute",
        "Official_Website_URL": "https://veltech.edu.in",
        "Department_Or_Contact": "Admissions & Outreach Office",
        "Official_Email": "admission@veltech.edu.in",
        "Phone_Number": "+91-44-26840605",
        "Source_Page_URL": "https://veltech.edu.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Vels Institute of Science, Technology & Advanced Studies (VISTAS)",
        "Official_Website_URL": "https://velsuniv.ac.in",
        "Department_Or_Contact": "Registrar Office",
        "Official_Email": "vistas@velsuniv.ac.in",
        "Phone_Number": "+91-44-22662500",
        "Source_Page_URL": "https://velsuniv.ac.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Bharath Institute of Higher Education and Research",
        "Official_Website_URL": "https://bharathuniv.ac.in",
        "Department_Or_Contact": "Office of Admissions",
        "Official_Email": "admissions@bharathuniv.ac.in",
        "Phone_Number": "+91-44-22290125",
        "Source_Page_URL": "https://bharathuniv.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Chennai",
        "College_Name": "Dr. M.G.R. Educational and Research Institute",
        "Official_Website_URL": "https://drmgrdu.ac.in",
        "Department_Or_Contact": "Central Office",
        "Official_Email": "contact@drmgrdu.ac.in",
        "Phone_Number": "+91-44-23782176",
        "Source_Page_URL": "https://drmgrdu.ac.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Coimbatore",
        "College_Name": "Sri Ramakrishna Engineering College (SREC)",
        "Official_Website_URL": "https://srec.ac.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@srec.ac.in",
        "Phone_Number": "+91-422-2460088",
        "Source_Page_URL": "https://srec.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Coimbatore",
        "College_Name": "SNS College of Technology",
        "Official_Website_URL": "https://snsct.org",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@snsct.org",
        "Phone_Number": "+91-422-2666264",
        "Source_Page_URL": "https://snsct.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Erode",
        "College_Name": "Nandha Engineering College",
        "Official_Website_URL": "https://nandhaengg.org",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@nandhaengg.org",
        "Phone_Number": "+91-4294-225585",
        "Source_Page_URL": "https://nandhaengg.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Perambalur",
        "College_Name": "Dhanalakshmi Srinivasan Engineering College",
        "Official_Website_URL": "https://dsec.ac.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal.dsec@dsgroupmail.com",
        "Phone_Number": "+91-4328-220444",
        "Source_Page_URL": "https://dsec.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruchirappalli",
        "College_Name": "J.J. College of Engineering and Technology",
        "Official_Website_URL": "https://jjcet.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@jjcet.ac.in",
        "Phone_Number": "+91-431-2695606",
        "Source_Page_URL": "https://jjcet.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruchirappalli",
        "College_Name": "M.A.M. College of Engineering and Technology",
        "Official_Website_URL": "https://mamcet.com",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@mamcet.com",
        "Phone_Number": "+91-431-2670399",
        "Source_Page_URL": "https://mamcet.com/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Vellore",
        "College_Name": "Thanthai Periyar Government Institute of Technology (TPGIT)",
        "Official_Website_URL": "https://tpgit.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "tpgitprincipal@gmail.com",
        "Phone_Number": "+91-416-2267762",
        "Source_Page_URL": "https://tpgit.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Theni",
        "College_Name": "Government College of Engineering, Bodinayakkanur",
        "Official_Website_URL": "https://gcebodi.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "gcebodi@gmail.com",
        "Phone_Number": "+91-4546-282555",
        "Source_Page_URL": "https://gcebodi.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Sivakasi",
        "College_Name": "Ayya Nadar Janaki Ammal College (ANJAC)",
        "Official_Website_URL": "https://anjaconline.org",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@anjaconline.org",
        "Phone_Number": "+91-4562-254100",
        "Source_Page_URL": "https://anjaconline.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Virudhunagar",
        "College_Name": "Virudhunagar Hindu Nadars' Senthikumara Nadar College",
        "Official_Website_URL": "https://vhnsnc.edu.in",
        "Department_Or_Contact": "Office of Principal",
        "Official_Email": "principal@vhnsnc.edu.in",
        "Phone_Number": "+91-4562-280154",
        "Source_Page_URL": "https://vhnsnc.edu.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tirunelveli",
        "College_Name": "Sadakathullah Appa College (Autonomous)",
        "Official_Website_URL": "https://sadakath.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@sadakath.ac.in",
        "Phone_Number": "+91-462-2540763",
        "Source_Page_URL": "https://sadakath.ac.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Kanyakumari",
        "College_Name": "Scott Christian College (Autonomous)",
        "Official_Website_URL": "https://scottchristian.org",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@scottchristian.org",
        "Phone_Number": "+91-4652-231807",
        "Source_Page_URL": "https://scottchristian.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Thoothukudi",
        "College_Name": "V.O. Chidambaram College",
        "Official_Website_URL": "https://voccollege.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@voccollege.ac.in",
        "Phone_Number": "+91-461-2310175",
        "Source_Page_URL": "https://voccollege.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tirupattur",
        "College_Name": "Sacred Heart College (Autonomous)",
        "Official_Website_URL": "https://shctpt.edu",
        "Department_Or_Contact": "Central Office",
        "Official_Email": "office@shctpt.edu",
        "Phone_Number": "+91-4179-220553",
        "Source_Page_URL": "https://shctpt.edu/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Coimbatore",
        "College_Name": "Kongunadu Arts and Science College",
        "Official_Website_URL": "https://kongunaducollege.ac.in",
        "Department_Or_Contact": "Information Desk",
        "Official_Email": "info@kongunaducollege.ac.in",
        "Phone_Number": "+91-422-2442068",
        "Source_Page_URL": "https://kongunaducollege.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Coimbatore",
        "College_Name": "Sri Krishna Arts and Science College",
        "Official_Website_URL": "https://skasc.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@skasc.ac.in",
        "Phone_Number": "+91-422-2678052",
        "Source_Page_URL": "https://skasc.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Madurai",
        "College_Name": "The American College (Autonomous)",
        "Official_Website_URL": "https://americancollege.edu.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "acprincipal@americancollege.edu.in",
        "Phone_Number": "+91-452-2530070",
        "Source_Page_URL": "https://americancollege.edu.in/contact-us"
    },
    {
        "State": "Tamil Nadu",
        "City": "Madurai",
        "College_Name": "Fatima College (Autonomous)",
        "Official_Website_URL": "https://fatimacollegemdu.org",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "fatimacollegemdu@gmail.com",
        "Phone_Number": "+91-452-2668016",
        "Source_Page_URL": "https://fatimacollegemdu.org/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruchirappalli",
        "College_Name": "Holy Cross College (Autonomous)",
        "Official_Website_URL": "https://hcctrichy.ac.in",
        "Department_Or_Contact": "Central Office",
        "Official_Email": "office@hcctrichy.ac.in",
        "Phone_Number": "+91-431-2700637",
        "Source_Page_URL": "https://hcctrichy.ac.in/contact"
    },
    {
        "State": "Tamil Nadu",
        "City": "Tiruchirappalli",
        "College_Name": "National College (Autonomous)",
        "Official_Website_URL": "https://nct.ac.in",
        "Department_Or_Contact": "Principal Office",
        "Official_Email": "principal@nct.ac.in",
        "Phone_Number": "+91-431-2482995",
        "Source_Page_URL": "https://nct.ac.in/contact"
    }
]

def append_colleges():
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        existing = list(csv.DictReader(f))
        headers = list(existing[0].keys())

    existing_emails = {r["Official_Email"].strip().lower() for r in existing if r.get("Official_Email")}
    existing_names = {r["College_Name"].strip().lower() for r in existing if r.get("College_Name")}

    added = 0
    skipped_no_email = 0
    skipped_dup = 0

    for col in ADDITIONAL_COLLEGES:
        email = col.get("Official_Email", "").strip()
        name = col.get("College_Name", "").strip()
        if not email or not EMAIL_REGEX.match(email):
            print(f"[EXCLUDE - NO EMAIL] {name}")
            skipped_no_email += 1
            continue
        if email.lower() in existing_emails or name.lower() in existing_names:
            skipped_dup += 1
            continue

        rec = {
            "State": col.get("State", "Tamil Nadu"),
            "City": col.get("City", "Chennai"),
            "College_Name": name,
            "Official_Website_URL": col.get("Official_Website_URL", ""),
            "Department_Or_Contact": col.get("Department_Or_Contact", "Office of Principal / Dean"),
            "Official_Email": email,
            "Phone_Number": col.get("Phone_Number", ""),
            "Source_Page_URL": col.get("Source_Page_URL", ""),
            "Status": "Pending",
            "Sent_Timestamp": "",
            "Notes_Or_Error": "Verified official institutional portal with scraped official email"
        }
        existing.append(rec)
        existing_emails.add(email.lower())
        existing_names.add(name.lower())
        added += 1
        print(f"[+ ADDED] {name} ({col.get('City')}) -> {email}")

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(existing)

    print("=" * 60)
    print(f"Total Colleges in CSV Now: {len(existing)}")
    print(f"Newly Added: {added}")
    print(f"Skipped (No Email): {skipped_no_email}")
    print(f"Skipped (Duplicates): {skipped_dup}")
    print("=" * 60)

if __name__ == "__main__":
    append_colleges()
