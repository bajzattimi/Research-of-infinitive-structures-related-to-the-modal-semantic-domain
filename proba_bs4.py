from bs4 import BeautifulSoup
import lxml
import requests

file = open("akar_fni_384.xml", "r", encoding="utf8")
contents = file.read()
soup = BeautifulSoup(contents, "lxml")
lines = soup.find_all("line")
for i in lines:
    ref = list(soup.find("ref"))
    sor = list(soup.left_context) + list(soup.kwic) + list(soup.right_context)
    osszefuz = " ".join(sor)
    teljes = osszefuz.split()
    print(teljes)
    print(ref)


corpus = list(soup.find("corpus"))
hits = list(soup.find("hits"))
query = list(soup.find("query"))



