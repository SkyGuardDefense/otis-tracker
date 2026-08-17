#!/usr/bin/env python3
import csv,json,re,ssl
from datetime import datetime,timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1];CONFIG=json.loads((ROOT/'config'/'sources.json').read_text());NOW=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
class Links(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.href=None;self.text=[]
 def handle_starttag(self,t,a):
  if t=='a':self.href=dict(a).get('href');self.text=[]
 def handle_data(self,d):
  if self.href is not None:self.text.append(d)
 def handle_endtag(self,t):
  if t=='a' and self.href:self.links.append((self.href,' '.join(' '.join(self.text).split())));self.href=None;self.text=[]
def fetch(u):
 with urlopen(Request(u,headers={'User-Agent':'OTIS-Opportunity-Tracker/1.0 (+https://github.com/SkyGuardDefense/otis-tracker)'}),timeout=25,context=ssl.create_default_context()) as r:return r.status,r.geturl(),r.read(1500000).decode('utf-8',errors='replace')
def main():
 keys=[k.lower() for k in CONFIG['keywords']];report={'scannedAt':NOW,'sources':[]};candidates=[]
 for source in CONFIG['sources']:
  result={'name':source['name'],'channel':source['channel'],'url':source['url'],'checkedAt':NOW}
  try:
   status,final,html=fetch(source['url']);title=re.search(r'<title[^>]*>(.*?)</title>',html,re.I|re.S);result.update({'status':status,'finalUrl':final,'title':re.sub(r'\s+',' ',unescape(title.group(1))).strip() if title else ''});p=Links();p.feed(html);seen=set()
   for href,text in p.links:
    url=urljoin(final,href);matches=sorted({k for k in keys if k in f'{text} {url}'.lower()})
    if matches and url not in seen and url.startswith(('http://','https://')):seen.add(url);candidates.append({'source':source['name'],'channel':source['channel'],'sourceUrl':source['url'],'candidateUrl':url,'anchorText':text[:500],'keywordMatches':matches,'checkedAt':NOW,'reviewStatus':'Needs validation'})
   result['candidateCount']=sum(c['source']==source['name'] for c in candidates)
  except Exception as e:result['error']=f'{type(e).__name__}: {e}'
  report['sources'].append(result)
 reports=ROOT/'reports';reports.mkdir(exist_ok=True);(reports/'latest-scan.json').write_text(json.dumps(report,indent=2)+'\n');(reports/'candidates.json').write_text(json.dumps(candidates,indent=2)+'\n')
 records=json.loads((ROOT/'data'/'opportunities.json').read_text());fields=['id','opportunity','sponsor','channel','sourceUrl','datePosted','deadline','awardType','otisMatch','fitScore','urgency','status','nextAction','lastChecked']
 with (ROOT/'data'/'opportunities.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader()
  for r in records:
   row={f:r.get(f,'') for f in fields};row['otisMatch']=' | '.join(row['otisMatch']) if isinstance(row['otisMatch'],list) else row['otisMatch'];w.writerow(row)
 print(json.dumps({'scannedAt':NOW,'sources':len(report['sources']),'candidates':len(candidates)}))
if __name__=='__main__':main()
