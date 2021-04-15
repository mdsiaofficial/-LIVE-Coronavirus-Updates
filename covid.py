#this code uses data from Google's own COVID map at
#https://google.com/covid19-map/?hl=en

import subprocess
import sys
#use this install() function to pip-install modules
def install(package):
    subprocess.run([
        sys.executable, "-m", "pip", "-q", "install", package
    ])
install("bs4")


from urllib.request import urlopen
from bs4 import BeautifulSoup


m = str(urlopen("https://google.com/covid19-map/?hl=en").read())
page = BeautifulSoup(m,"html.parser")


lis = list(filter(lambda x:x.string!=None and "Updated" in x.string,page.find_all("div")))
print(lis[0].string)


def parse(entry):
    region = entry.find_all("span")[0].string
    stats = list(map(lambda x:x.string,entry.find_all("td")))
    stats = [stats[1]]+stats[3:]
    return [region.string]+stats


data = page.find_all("tbody")[0]
entr = data.find_all("tr")
full_list = list(map(parse,entr))

print("-"*49)
print("|    Location     |  Total  |Recovered|  Deaths |")
print("-"*49)
for i in full_list:
    print(("|{:<17}"+"|{:<9}"*3+"|").format(*i))
print("-"*49)
