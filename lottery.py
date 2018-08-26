'''
store football lottery information

chen77fan@163.com

'''
import re
from bs4 import BeautifulSoup as BS
import sys
import csv
import requests

url = "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini&issue={date}"

def get_rank(text):
    pattern = re.compile('\d+')
    rank = pattern.findall(text)[0]
    return rank

class lottery(object):
    def __init__(self,tr,buyid):
        self.matchtype = tr['m']
        self.week = tr['d']
        wh4 = tr.find('td',class_='wh-4 t-r')
        self.team1 = wh4.find('a').get_text()
        self.team1_rank = get_rank(wh4.find('em').get_text())
        wh6 = tr.find('td',class_='wh-6 t-l')
        self.team2 = wh6.find('a').get_text()
        self.team2_rank = get_rank(wh6.find('em').get_text())
        wh8 = tr.find('td',class_='wh-8 b-l')
        self.rq=wh8.find('em',class_='rq ').get_text()
        if(len(tr.find('em',class_='rq jia ')>0)):
            self.rq2=tr.find('em',class_='rq jia ').get_text()
        else:
            self.rq2=tr.find('em',class_='rq jian').get_text()
        self.odds = tr.find('input',class_='spArr')['value'].replace('|',' ').split(' ')
        self.profit = str(float(self.odds[buyid])*(-1))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f1 = open('mylo.csv','ab+')
    mylowriter = csv.writer(f1)

    date = sys.argv[1]
    index = str(int(sys.argv[2])-1)
    buyid = int(sys.argv[3])-1

    print "fetch: ",url.format(date=date)
    reponse = requests.get(url.format(date=date))
    bs= BS(reponse.text)
    tr = bs.find('tr',i=index)
    assert tr!=None,"not find %s lottery"%index
    mylo = lottery(tr,buyid)
    print "%s\t%s vs %s\t%s\t%s vs %s\t(%s,%s)\t%s\t%s"%(mylo.matchtype,mylo.team1,mylo.team2,mylo.week,mylo.team1_rank,mylo.team2_rank,mylo.rq,mylo.rq2,('|').join(mylo.odds),mylo.profit)
    #mylowriter.writerow([mylo.matchtype,mylo.team1+"vs"+mylo.team2,mylo.team1_rank+"vs"+mylo.team2_rank,mylo.week,('|').join(mylo.odds),mylo.profit])
