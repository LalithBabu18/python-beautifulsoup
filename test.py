import json
import pymongo
from bs4 import BeautifulSoup
client = pymongo.MongoClient("mongodb+srv://localhost")
db = client.test
col = db["resumes"]
documents = col.find({},no_cursor_timeout=True) # if limit not necessary then discard limit
print(type(documents))
new_col = db["resultResumes"]
for i in documents:
    dict = {}
    doc = i["Resume-Html"]
    soup = BeautifulSoup(''.join(doc),features="html.parser")
    dict['_id'] = i['_id']
    dict['createdTime'] = i['createdTime']
    dict['Title'] = i['Title']
    location = soup.find('p', attrs={'class' : 'locality'})
    if location is not None:
        loc = location.get_text()
        locspace = " ".join(loc.split())
        dict['Location'] = locspace
    else:
        dict['Location'] = ""
    education = soup.find('div',attrs={'class':'section-item education-content'})
    if education is not None:
        edu= education.get_text()
        eduspace = " ".join(edu.split())
        edurem = eduspace.replace('Education', '')
        dict['Education'] = edurem
    else:
        dict['Education'] = ""

    workexperience = soup.find('div', attrs={'class':'section-item workExperience-content'})
    if workexperience is not None:
        # print(workexperience.get_text())
        bza = []
        abcd = soup.findAll('div', attrs={'class': 'work-experience-section'})
        k = 0
        for j in range(len(abcd)):

            print('---------------------------------------------------')
            print(j)
            worka = abcd[j].find('p', attrs={'class': 'work_title'})
            if worka is not None:
                workaa = worka.get_text()
                workspa = " ".join(workaa.split())
            workb = abcd[j].find('div', attrs={'class': 'work_company'})
            if workb is not None:
                workba = workb.get_text()
                workspb = " ".join(workba.split())
            workc = abcd[j].find('p', attrs={'class': 'work_dates'})
            if workc is not None:
                workca = workc.get_text()
                workspc = " ".join(workca.split())
            workd = abcd[j].find('p', attrs={'class': 'work_description'})
            if workd is not None:
                workda = workd.get_text()
                workspd = " ".join(workda.split())
            vskp = workspa +   workspb   + workspc + workspd

            # vskp.append(wora)
            # vskp.append(worb)
            # vskp.append(worc)
            # vskp.append(word)

            bza.append(vskp)


            print('---------------------------------------------------')
        print(bza)

        dict['WorkExperience'] = bza
    else:
        dict['WorkExperience'] = ""
    currentcompany =  soup.find('div', attrs={'class':'work_company'})
    if currentcompany is not None:
        company= currentcompany.get_text()
        companyspace = " ".join(company.split())
        dict['CurrentCompany'] = companyspace
    else:
        dict['CurrentCompany'] = ""
    skills = soup.find('div', attrs={'class':'data_display'})
    if skills is not None:
        skill= skills.get_text()
        skillspace = " ".join(skill.split())
        skillarr = []
        skillarr.append(skillspace)
        dict['Skills'] = skillarr
    else:
        dict['Skills'] = ""
    introduction = soup.find('p', attrs={'class' : 'summary'})
    if introduction is not None:
        introduction = introduction.get_text()
        introductionspace = " ".join(introduction.split())
        dict['Introduction'] = introductionspace
    else:
        dict['Introduction'] = ""


    new_col.insert_one(dict)
