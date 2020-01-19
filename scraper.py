import requests
import bs4
from bs4 import BeautifulSoup
import json



print("input season and year in format \"<season> <year>\"")
semester = input()
semester = semester.split(" ")

month = ''
if semester[0] == 'fall':
    month = '08'
elif semester[0] == 'summer':
    month = '05'
elif semester[0] == 'winter':
    month = '12'
elif semester[0] == 'spring':
    month = '01'
else:
    print("bad input")

semester = semester[1] + month

# list of extracted majors to query
majors = ["AASP", "AAST", "AGNR", "AMSC", "AMST", "ANSC", "ANTH", "AOSC", "ARAB",
          "ARCH", "AREC", "ARHU", "ARMY", "ARSC", "ARTH", "ARTT", "ASTR", "BCHM", "BEES",
          "BIOE", "BIOL", "BIOM", "BIPH", "BISI", "BMGT", "BSCI", "BSCV", "BSGC", "BSOS",
          "BSST", "BUAC", "BUDT", "BUFN", "BULM", "BUMK", "BUMO", "BUSI", "BUSM", "BUSO",
          "CBMG", "CCJS", "CHBE", "CHEM", "CHIN", "CHPH", "CLAS", "CLFS", "CMLT", "CMSC",
          "COMM", "CPBE", "CPET", "CPGH", "CPJT", "CPMS", "CPPL", "CPSA", "CPSD", "CPSF",
          "CPSG", "CPSN", "CPSP", "CPSS", "DANC", "EALL", "ECON", "EDCP", "EDHD", "EDHI",
          "EDMS", "EDSP", "EDUC", "ENAE", "ENCE", "ENCH", "ENCO", "ENEE", "ENES", "ENFP",
          "ENGL", "ENMA", "ENME", "ENPM", "ENRE", "ENSE", "ENSP", "ENST", "ENTM", "ENTS",
          "EPIB", "FGSM", "FILM", "FIRE", "FMSC", "FREN", "GEMS", "GEOG", "GEOL", "GERM",
          "GREK", "GVPT", "HACS", "HDCC", "HEBR", "HEIP", "HESI", "HESP", "HHUM", "HISP",
          "HIST", "HLMN", "HLSA", "HLSC", "HLTH", "HONR", "IDEA", "IMMR", "INAG", "INFM",
          "INST", "ISRL", "ITAL", "JAPN", "JOUR", "JWST", "KNES", "KORA", "LARC", "LASC",
          "LATN", "LBSC", "LGBT", "LING", "MATH", "MEES", "MIEH", "MITH", "MLAW", "MLSC",
          "MOCB", "MUED", "MUSC", "MUSP", "NACS", "NAVY", "NFSC", "NIAS", "PEER", "PERS",
          "PHIL", "PHSC", "PHYS", "PLCY", "PLSC", "PORT", "PSYC", "RDEV", "RELS", "RUSS",
          "SLAA", "SLLC", "SOCY", "SPAN", "SPHL", "STAT", "SURV", "TDPS", "THET", "TLPL",
          "TLTC", "TOXI", "UMEI", "UNIV", "URSP", "USLT", "VMSC", "WMST"]

abrvhash ={'AJC': '429 - A. James Clark Hall', 'AVW': '115 - A.V. Williams Building',
           'SSU': '163 - Adele H. Stamp Student Union Buildings', 'ANS': '142 - Animal Science/Agricultural Engineering Building',
           'ANA': '060 - Anne Arundel Hall', 'ARC': '145 - Architecture Building', 'ASY': '146 - Art-Sociology Building',
           'EDU': '143 - Benjamin Building', 'BPS': '144 - Biology-Psychology Building', 'BRB': '413 - Biosciences Research Building',
           'CCC': '097 - Cambridge Community Center', 'CEN': '098 - Centreville Hall (Residence Hall)',
           'CHE': '090 - Chemical and Nuclear Engineering Building', 'CHM': '091 - Chemistry Building',
           'PAC': '386 - Clarice Smith Performing Arts Center', 'COL': '162 - Cole Student Activities Building',
           'CSI': '406 - Computer Science Instructional Center',
           'CBD': '122 - Cumberland Hall (Residence Hall)', 'DOR': '064 - Dorchester Hall (Residence Hall)',
           'ESJ': '226 - Edward St. John Learning and Teaching Center', 'ELK': '254 - Elkton Hall (Residence Hall)',
           'ELL': '256 - Ellicott Hall (Residence Hall)', 'EGL': '089 - Engineering Laboratory Building',
           'ERC': '068 - Eppley Campus Recreation Center', 'KEY': '048 - Francis Scott Key Hall',
           'GEO': '237 - Geology Building', 'GLF': '166 - Golf Course Clubhouse', 'HJP': '073 - H.J. Patterson Hall',
           'HAG': '258 - Hagerstown Hall (Residence Hall)', 'HBK': '147 - Hornbake Library',
           'ITV': '045 - Instructional Television Facility', 'JMP': '083 - J.M. Patterson Building',
           'KEB': '225 - Jeong H. Kim Engineering Building', 'JMZ': '034 - Jimenez Hall',
           'JUL': '227 - Jull Hall', 'KNI': '417 - Knight Hall', 'LPA': '259 - LaPlata Hall (Residence Hall)',
           'LEF': '038 - LeFrak Hall', 'MMH': '046 - Marie Mount Hall', 'EGR': '088 - Martin Hall',
           'MTH': '084 - Mathematics Building', 'MCB': '231 - Microbiology Building',
           'NCC': '232 - Nyumburu Cultural Center', 'PHY': '082 - Physics Building',
           'PLS': '036 - Plant Science Building', 'QAN': '061 - Queen Annes Hall',
           'ARM': '078 - Reckord Armory', 'SPH': '255 - School of Public Health',
           'SHM': '037 - Shoemaker Building', 'SKN': '044 - Skinner Building',
           'SOM': '063 - Somerset Hall (Residence Hall)', 'SQH': '233 - Susquehanna Hall',
           'SYM': '076 - Symons Hall', 'TLF': '043 - Taliaferro Hall',
           'TWS': '141 - Tawes Fine Arts Building', 'TYD': '042 - Tydings Hall',
           'VMH': '039 - Van Munching Hall', 'WDS': '047 - Woods Hall',
           'SCC' : '997 - South Campus Commons 1', 'ATL' : '224 - Atlantic Building (ATL)',
           'IRB' : '432 - Brendan Iribe Center (IRB)', 'PFR' : '425 - Prince Frederick Hall',
           'PFH': '425 - Prince Frederick Hall',
           'ERC' : '068 - Eppley Recreation Center (CRC)', 'PSC' : '805 - Patapsco Building'}

# split day array into list
def daysplit(days):
    schedule = []
    i = 0
    while i < len(days):
        if days[i] == 'T' or days[i] == 'S':
            schedule.append(days[i:i + 2])
            i += 2
        else:
            schedule.append(days[i:i+1])
            i += 1
    return schedule

# recursive search functions to find correct container
def searchsections2(div):
    for tags in div.contents:
        if type(tags) is not bs4.element.NavigableString:
            if 'class' in tags.attrs and tags.attrs['class'][0] == 'sections-container':
                return tags.contents[1]


def searchsections(div):
    for tags in div.contents:
        if type(tags) is not bs4.element.NavigableString:
            if 'class' in tags.attrs and tags.attrs['class'][0] == 'toggle-sections-link-container':
                return searchsections2(tags.contents[1].contents[1].contents[1])

# retrieve all tags from a contents list
def gettags(div):
    l = []
    for content in div:
        if type(content) is bs4.element.Tag:
            l.append(content)
    return l
# record classes that failed
bad = []

# ignore ambigious class descriptions 
ignore = ['BLD3', 'TBA', 'BLD2', 'ONLINE','Class time/details on ELMS','Contact department or instructor for details.']
noloc = []
classes = []
# sending get request for every major
for m in majors:
    print("\n\nscraping " + m)

    URL = "https://app.testudo.umd.edu/soc/search?courseId=" + m + "&sectionId=&termId="+semester+"&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=UGRAD&instructor=&facetoface=true&_facetoface=on&blended=true&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=*&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
    # test for bad urls only....
    #URL = "https://app.testudo.umd.edu/soc/search?courseId="+ m + "&sectionId=&termId=201908&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=UGRAD&instructor=&facetoface=true&_facetoface=on&blended=true&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=*&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

    # request the page and parse using beautiful soup with html5lib parser
    r = requests.get(url=URL)
    soup = BeautifulSoup(r.content.decode('utf-8'), features="html5lib")

    # make list of all objects nested in "class":"course"
    courses = soup.find_all('div', {"class": "course"})

    for course in courses:

        title = course.contents[1].attrs['value']
        if title == 'EDSP400':
            print('hi')
        try:
            sections = searchsections(course.contents[3].contents[3])

            # traverse down to class-days-container
            if sections != None:
                sections = gettags(sections.contents)
                for child in sections:
                    childcontents = gettags(child)
                    sectionId = childcontents[0].attrs['value']
                    for section in childcontents:
                        if 'class' in section.attrs and section.attrs['class'][0] == 'class-days-container':
                            meetings = gettags(section)

                            # handle delivery-blended to face to face schedules
                            for meeting in meetings:
                                if child.attrs['class'][1] == 'delivery-blended':
                                    try:
                                        time = section.contents[3].contents[1].text.strip()
                                        location = section.contents[3].contents[3].text.strip()
                                    except IndexError:
                                        time = section.contents[1].contents[1].text.strip()
                                        location = section.contents[1].contents[3].text.strip()
                                else:
                                    try:
                                        time = section.contents[1].contents[1].text.strip()
                                        location = section.contents[1].contents[3].text.strip()
                                    except IndexError:
                                        time = section.contents[3].contents[1].text.strip()
                                        location = section.contents[3].contents[3].text.strip()

                                # string results and record 
                                # these were some ambigious building names 
                                l = location.split('\n')
                                bdg = l[0]
                                if bdg == "PFR":
                                    building = "PFH"
                                if bdg == "ERC":
                                    buiding = "CRC"
                                if time in ignore or bdg in ignore:
                                    continue

                                if bdg not in abrvhash and bdg not in noloc:
                                    print(bdg)
                                    noloc.append(bdg)
                                    continue

                                bdg = abrvhash[bdg]
                                sched = time.split('\n')
                                days = daysplit(sched[0])
                                t = sched[1].strip().split(' - ')
                                start = t[0]
                                end = t[1]
                                s = [days,start,end,bdg,sectionId,title]
                                print(s)
                                classes.append(s)
                # print results co nsole (my editor outputs to file) skips duplicates

            else: # could not find needed content container
                print("ERROR: location look for " + title)

        except IndexError: # could not find needed content container
            print("ERROR: index look for " + title)
            bad.append(title)

week = {'M': {}, 'Tu': {}, 'W': {}, 'Th': {}, 'F': {}, 'Sa': {}, 'Su': {}}

# put classes into hashmap
for c in classes:

        title = c[5]
        days = c[0]
        building = c[3]
        start = c[1]
        end = c[2]
        room = c[4] # this is actually the section


        for d in days:
            dayschedule = week[d]
            if start not in dayschedule:
                dayschedule[start] = {}
            if end not in dayschedule[start]:
                dayschedule[start][end] = {}
            if building not in dayschedule[start][end]:
                dayschedule[start][end][building] = {}
            if room not in dayschedule[start][end][building]:
                dayschedule[start][end][building][room] = ''

            dayschedule[start][end][building][room] = title


        classinfo = [start,end, building, room, title]
        classinfo = [x.strip() for x in classinfo]
        classinfo.insert(0,days)



with open('data/classlistJson', 'w') as outfile:
    json.dump(week, outfile)
