'''
store football lottery information

chen77fan@163.com

'''
import re
from bs4 import BeautifulSoup as BS
import sys
import csv
import requests
import datetime
import time

url = "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini&issue={date}"

def get_rank(text):
    pattern = re.compile('\d+')
    result=pattern.findall(text)
    if(len(result)>0):
        rank=result[0]
    else:
        rank="None"
    return rank

def create_assist_date(datestart = None,dateend = None):
    if datestart is None:
        datestart = '2013-01-01'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    datestart=datetime.datetime.strptime(datestart,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(dateend,'%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart<dateend:
        datestart+=datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    print date_list
    return date_list

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
        if(wh8.find('em',class_='rq ')!=None):
            self.rq=wh8.find('em',class_='rq ').get_text()
        else:
            self.rq=wh8.find('em',class_='rq dg').get_text()
        if(tr.find('em',class_='rq jia dg')!=None):
            self.rq2=tr.find('em',class_='rq jia dg').get_text()
        elif(tr.find('em',class_='rq jian dg')!=None):
            self.rq2=tr.find('em',class_='rq jian dg').get_text()
        elif(tr.find('em',class_='rq jia ')!=None):
            self.rq2=tr.find('em',class_='rq jia ').get_text()
        else:
            self.rq2=tr.find('em',class_='rq jian ').get_text()
        self.odds = tr.find('input',class_='spArr')['value'].replace('|',' ').split(' ')
        #self.profit = str(float(self.odds[buyid])*(-1))


def getOneDayData(date):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f1 = open('mylo.csv','ab+')
    mylowriter = csv.writer(f1)

    #print "fetch: ",url.format(date=date)
    reponse = requests.get(url.format(date=date))
    bs= BS(reponse.text)
    trs = bs.find_all('tr',attrs={"class":"endBet"})
    assert trs!=None,"not find any lottery"
    for tr in trs:
        mylo = lottery(tr,0)
        #print "%s\t%s vs %s\t%s\t%s vs %s\t(%s,%s)\t%s"%(mylo.matchtype,mylo.team1,mylo.team2,mylo.week,mylo.team1_rank,mylo.team2_rank,mylo.rq,mylo.rq2,('|').join(mylo.odds))
        mylowriter.writerow([mylo.matchtype,mylo.team1+"vs"+mylo.team2,mylo.team1_rank+"vs"+mylo.team2_rank,mylo.week,date,mylo.rq+"|"+mylo.rq2,('|').join(mylo.odds)])
if __name__ == '__main__':
    fdate=open('lastdate.txt','r+')
    date=fdate.readlines()[0]
    #getOneDayData(date)
    datelist=create_assist_date(date)
    for d in datelist:
        getOneDayData(d)
        print "finish %s "%d
        fdate.seek(0)
        fdate.write(d)
        time.sleep(1)
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    f1 = open('mylo.csv','ab+')
#    mylowriter = csv.writer(f1)
#
#    date = sys.argv[1]
#    index = str(int(sys.argv[2])-1)
#    buyid = int(sys.argv[3])-1
#
#    print "fetch: ",url.format(date=date)
#    reponse = requests.get(url.format(date=date))
#    bs= BS(reponse.text)
#    tr = bs.find('tr',i=index)
#    assert tr!=None,"not find %s lottery"%index
#    mylo = lottery(tr,buyid)
#    print "%s\t%s vs %s\t%s\t%s vs %s\t(%s,%s)\t%s\t%s"%(mylo.matchtype,mylo.team1,mylo.team2,mylo.week,mylo.team1_rank,mylo.team2_rank,mylo.rq,mylo.rq2,('|').join(mylo.odds),mylo.profit)
#    #mylowriter.writerow([mylo.matchtype,mylo.team1+"vs"+mylo.team2,mylo.team1_rank+"vs"+mylo.team2_rank,mylo.week,('|').join(mylo.odds),mylo.profit])
