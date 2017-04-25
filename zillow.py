# from BeautifulSoup import BeautifulSoup
# import urllib2
#
# url = "http://www.zillow.com/chandler-az-85225/fsbo/"
#
# content = urllib2.urlopen(url).read()
#
# soup = BeautifulSoup(content)
#
#
# print soup.title
#
# print soup.title.string
#
# print soup.article.a

from BeautifulSoup import BeautifulSoup
import urllib2


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "https://mcassessor.maricopa.gov/mcs.php?q=310%20N%20Eucalyptus%20Pl"
response = opener.open(url)
page = response.read()

soup = BeautifulSoup(page)

rows = soup.findAll('tr')
row1 = rows[1]
apn = row1.td.text
apn_strip = apn.replace('-', '')
urlapn = "https://mcassessor.maricopa.gov/mcs.php?q="+apn_strip
responseapn = opener.open(urlapn)
pageapn = responseapn.read()
soupapn = BeautifulSoup(pageapn)

print soupapn.findAll('table')