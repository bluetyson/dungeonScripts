import requests, os, io
from bs4 import BeautifulSoup
from shutil import move

gameList = []    
gameList2 = []    

def getUrl():
    return 'http://www.drivethrurpg.com/browse.php?filters=0_0_600_45285_0'

def getBackupFile():
    return 'backupSuperhero.txt'

def getCurrentFile():
    return 'titleListSuperhero.txt'

def getHtmlResponse(url):
   return requests.get(url).text

def makeSoup(url):
    return BeautifulSoup(getHtmlResponse(url), 'html.parser')

def Backup():
	if os.path.isfile(getCurrentFile()):
		move(getCurrentFile(), getBackupFile())

def processData(url, count):
    soup = makeSoup(url)
    #with open(getCurrentFile(), 'a', encoding="utf-8") as f:
    with io.open(getCurrentFile(), "a", encoding="utf-8-sig") as f:
        [f.write(x['title']+'\n') for x in soup.find('table', class_='productListing').find_all('a', title=True)[3:]]
        [ gameList.append(x['title'])  for x in soup.find('table', class_='productListing').find_all('a', title=True)[3:]]
    getNextPage(soup, count)
      
def getData(fileName):
    with io.open( fileName, 'r' ) as inputFile:
        return [line.rstrip('\n').encode('utf-8') for line in inputFile]

def compareData():
	diff = set(getData(getCurrentFile())) - set(getData(getBackupFile()))
	if len(diff) > 0:
		print(set(getData(getCurrentFile())) - set(getData(getBackupFile())))
	else:
		print("No new books.")

def getNextPage(soup, count):
	nextPage = soup.find('a', title=' Next Page ')
	if nextPage is not None:
		processData(nextPage['href'], count+1)
	else:
		compareData()

Backup()        
processData(getUrl(), 1)

for game in gameList:
    # GAME :  book
    #make more clever if want to get the stuff that has no parenthetical system references
    #but mostly for D&D purposes
    if '(' in str(game):
        myList = game.split('(')
        gameFamily = myList[1]
        strFamily = str.replace(gameFamily,')','')
        myList[1] = strFamily
        gameList2.append([myList[1],myList[0]])

g = open("gamelistSuperhero.txt", "w")
gameList2.sort()
for game2 in gameList2:
    g.write(str(game2[0]) + " : " + str(game2[1]) + "\n" )

g.close()

