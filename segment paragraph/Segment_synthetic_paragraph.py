import os
import re
import xml.etree.ElementTree as ET


# 判断标题是否符合要求
def estTitle(title):
    titles = ["catalyst preparation", "materials preparation", "catalyst synthesis", "materials synthesis",
              "experimental procedure", "synthesis procedure", "synthesis conditions", "preparation conditions"]
    for tit in titles:
        t = title.strip().lower()
        if tit == t:
            return True
    patterns = ["preparation\\s\\w+\\scatalys", "preparation\\s\\w+\\smaterial",
                "synthesis\\s\\w+\\scatalyst", "synthesis\\s\\w+\\smaterial"]
    '''
     patterns_1 = ["(?=.*\\bcatalyst\\b)(?=.*\\bpreparation\\b).+", "(?=.*\\bmaterials\\b)(?=.*\\bpreparation\\b).+",
                  "(?=.*\\bcatalyst\\b)(?=.*\\bsynthesis\\b).+", "(?=.*\\bmaterials\\b)(?=.*\\bsynthesis\\b).+",
                  "(?=.*\\bexperimental\\b)(?=.*\\bprocedure\\b).+", "(?=.*\\bsynthesis\\b)(?=.*\\bprocedure\\b).+",
                  "(?=.*\\bsynthesis\\b)(?=.*\\bconditions\\b).+", "(?=.*\\bpreparation\\b)(?=.*\\bconditions\\b).+"]
    
    '''
   
    #for pattern in patterns + patterns_1:
    for pattern in patterns:
        match = re.search(pattern, title.strip().lower())
        if match:
            return True
    return False


def writeTxt(fileName, txt):
    with open(".//result//{}.txt".format(fileName.replace(".xml", "")), "w", encoding="utf-8") as file:
        file.write(txt)


def getAllxml():
    nameList = os.listdir(".//xml//")
    nameList = filter(lambda x: x.split(".")[-1] == "xml", nameList)
    return nameList


def getTxt(fileName):
    tree = ET.parse('.//xml//{}'.format(fileName))
    root = tree.getroot()

    rules = [['.//{http://www.elsevier.com/xml/xocs/dtd}item-toc-entry',
              '{http://www.elsevier.com/xml/xocs/dtd}item-toc-section-title'],
             ['.//{http://www.elsevier.com/xml/common/dtd}section',
              '{http://www.elsevier.com/xml/common/dtd}section-title']]

    text = []
    for rule in rules:
        elements = root.findall(rule[0])
        for elem in elements:
            title = elem.find(rule[1])
            if title is not None and type(title.text) == str:
                # 判断标题是否符合要求
                if estTitle(title.text):
                    for ele in elem.itertext():
                        lines = ele.splitlines()
                        stripped_lines = [line.strip() for line in lines]
                        result = "\n".join(stripped_lines)
                        text.append(result)
    if len(text) != 0:
        text = filter(lambda x: type(x) == str, text)
        writeTxt(fileName, "".join(text))


if __name__ == '__main__':
    for filename in getAllxml():
        getTxt(filename)
        print('finish')
