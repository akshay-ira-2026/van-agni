import json, math, os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
W,H=1280,720; FPS=10; PAUSE=0.45
BG=(10,22,16); PANEL=(17,36,26); LINE=(44,84,62); INK=(238,244,238); SUB=(168,197,178)
GOLD=(255,201,64); RED=(255,77,58); ORG=(255,140,0); GRN=(64,199,120); WHT=(255,255,255)
F='/usr/share/fonts/truetype/'
def ft(p,s): return ImageFont.truetype(F+p,s)
BLACK=lambda s: ft('lato/Lato-Black.ttf',s); BOLD=lambda s: ft('noto/NotoSans-Bold.ttf',s)
REG=lambda s: ft('lato/Lato-Regular.ttf',s); MONO=lambda s: ft('dejavu/DejaVuSansMono.ttf',s)
DEVB=lambda s: ft('noto/NotoSansDevanagari-Bold.ttf',s); DEV=lambda s: ft('noto/NotoSansDevanagari-Regular.ttf',s)
os.makedirs('frames',exist_ok=True)
state_hit=[]
T=json.load(open('vo/timings.json'))
SEG=[]; t=0.0
for o in T:
    SEG.append((o['id'],t,t+o['dur'])); t+=o['dur']+PAUSE
TOTAL=t-PAUSE; print('total',round(TOTAL,1))
uk=json.load(open('uk.json')); geom=uk['geometry']
rings=[]
if geom['type']=='Polygon': rings=[geom['coordinates'][0]]
else: rings=[p[0] for p in geom['coordinates']]
rep=json.load(open('/tmp/va4/docs/replay_2024-04-22.json')); live=json.load(open('/tmp/va4/docs/live.json'))
cellsR=rep['cells']; cellsL=live['cells']; top10=[c['cell'] for c in rep['top10']]
actual=set(rep['actual_fire_cells_next7']); RBY={int(c['cell']):c for c in cellsR}
v=pd.read_csv('/tmp/va4/data/firms_viirs_snpp_uttarakhand_2019_2025.csv.gz')
v['d']=pd.to_datetime(v.acq_date)
wk=v[(v.d>='2024-04-22')&(v.d<'2024-04-29')][['longitude','latitude','d']].sort_values('d')
wk['day']=(wk.d-pd.Timestamp('2024-04-22')).dt.days
season=v.groupby(v.d.dt.month).size().reindex(range(1,13)).fillna(0)
def risk(p):
    p=max(0,min(1,p))
    def L(a,b,k): return tuple(int(a[i]+(b[i]-a[i])*k) for i in range(3))
    if p<0.5: return L((33,110,63),(255,214,64),p*2)
    return L((255,214,64),(211,31,24),(p-0.5)*2)
def wrap(d,txt,font,mw):
    out=[]; cur=''
    for w in txt.split():
        s=(cur+' '+w).strip()
        if d.textlength(s,font=font)<=mw: cur=s
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def text(d,xy,txt,font,fill=INK,anchor='la',lh=1.25,mw=None):
    x,y=xy
    lines=wrap(d,txt,font,mw) if mw else [txt]
    for ln in lines:
        d.text((x,y),ln,font=font,fill=fill,anchor=anchor); y+=font.size*lh
    return y
def header(d,kick,title):
    d.text((48,30),kick,font=BOLD(19),fill=GOLD)
    d.text((48,56),title,font=BLACK(40),fill=INK)
def base(kick,title):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im,'RGBA'); header(d,kick,title); return im,d
def progress(d,now):
    d.rectangle([0,H-6,W,H],fill=(24,48,36)); d.rectangle([0,H-6,W*now/TOTAL,H],fill=GOLD)
def mapbox(d,box,cells,show=None,pts=None,outl=None,ring=None,alpha=235):
    x0,y0,x1,y1=box; LON=(77.2,81.1); LAT=(28.5,31.8)
    X=lambda lo: x0+(lo-LON[0])/(LON[1]-LON[0])*(x1-x0)
    Y=lambda la: y1-(la-LAT[0])/(LAT[1]-LAT[0])*(y1-y0)
    d.rounded_rectangle(box,radius=18,fill=(13,30,21),outline=LINE,width=2)
    for c in cells:
        if show is not None and int(c['cell']) not in show: continue
        cx,cy=X(c['lon']),Y(c['lat']); dx=(X(c['lon']+0.125)-cx); dy=(Y(c['lat']+0.125)-cy)
        col=risk(c['p']); d.rectangle([cx-dx,cy+dy,cx+dx,cy-dy],fill=col+(alpha,))
    for r in rings: d.line([(X(a),Y(b)) for a,b in r],fill=(190,235,205),width=2)
    if pts is not None and len(pts):
        for lo,la in zip(pts.longitude,pts.latitude):
            x,y=X(lo),Y(la); d.ellipse([x-2.6,y-2.6,x+2.6,y+2.6],fill=(255,120,40,230))
    if outl:
        for cid in outl:
            c=RBY.get(int(cid));
            if not c: continue
            cx,cy=X(c['lon']),Y(c['lat']); dx=(X(c['lon']+0.125)-cx); dy=(Y(c['lat']+0.125)-cy)
            d.rectangle([cx-dx,cy+dy,cx+dx,cy-dy],outline=GOLD+(255,),width=4)
    if ring:
        for (lo,la,lab) in ring:
            x,y=X(lo),Y(la); d.ellipse([x-13,y-13,x+13,y+13],outline=WHT,width=3); d.text((x+18,y-11),lab,font=BOLD(17),fill=WHT)
    for lo,la,nm in [(78.27,30.32,'Dehradun'),(79.46,29.38,'Nainital'),(80.22,29.58,'Pithoragarh')]:
        x,y=X(lo),Y(la); d.ellipse([x-3,y-3,x+3,y+3],fill=WHT); d.text((x+7,y-9),nm,font=BOLD(15),fill=(210,230,215))
def chip(d,x,y,big,small,col=GOLD,w=340):
    d.rounded_rectangle([x,y,x+w,y+104],radius=16,fill=PANEL,outline=LINE,width=2)
    d.text((x+22,y+10),big,font=BLACK(44),fill=col); d.text((x+22,y+64),small,font=BOLD(17),fill=SUB)
def bars(d,x,y,items,maxv,w=760,bh=34,gap=16):
    for lab,val,txt,col in items:
        d.text((x,y),lab,font=BOLD(20),fill=INK)
        d.rounded_rectangle([x,y+26,x+w,y+26+bh],radius=8,fill=(26,52,38))
        d.rounded_rectangle([x,y+26,x+max(14,w*val/maxv),y+26+bh],radius=8,fill=col)
        d.text((x+w+18,y+30),txt,font=BLACK(28),fill=col); y+=26+bh+gap
    return y
def scene(sid,k,now):
    if sid=='s01':
        im,d=base('UTTARAKHAND · APRIL 2024','3,000+ satellite fire detections in one week')
        day=min(6.99,k*7); pts=wk[wk.day<=day]
        mapbox(d,[48,150,820,665],cellsR,pts=pts)
        chip(d,856,150,'%s'%format(int((wk.day<=day).sum()),','),'detections so far',ORG,376)
        chip(d,856,274,'Day %d of 7'%(int(day)+1),'22–28 April 2024',INK,376)
        text(d,(856,410),'NASA VIIRS (Visible Infrared Imaging Radiometer Suite), 375 m. Every orange dot is a real detection.',BOLD(19),SUB,mw=370)
        return im
    if sid=='s02':
        im,d=base('THE PROBLEM','Every spring, the hills burn first')
        x0,y0=90,560; bw=78; mx=season.max()
        MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for i,m in enumerate(range(1,13)):
            h=330*season[m]/mx*min(1,k*1.6); x=x0+i*(bw+12)
            col=RED if m in (4,5) else (ORG if m in (2,3,6) else (70,130,95))
            d.rounded_rectangle([x,y0-h,x+bw,y0],radius=7,fill=col)
            d.text((x+bw/2,y0+12),MON[i],font=BOLD(17),fill=SUB,anchor='ma')
            if m==4: d.text((x+bw/2,y0-h-34),'36,849',font=BLACK(24),fill=RED,anchor='ma')
        text(d,(90,150),'Forest staff usually learn about a fire after the smoke is seen. By then, the patrol is already late.',BOLD(24),INK,mw=1050)
        d.text((90,610),'VIIRS detections in Uttarakhand, 2019–2025, by month',font=BOLD(17),fill=SUB)
        return im
    if sid=='s03':
        im,d=base('GREENMIND · TRACK 08','')
        mapbox(d,[560,120,1240,660],cellsR)
        d.text((48,190),'VAN AGNI',font=BLACK(104),fill=GOLD)
        text(d,(52,310),'Forest fire risk, seven days ahead.',BLACK(34),INK,mw=470)
        text(d,(52,420),'So the patrol gets there first.',BOLD(24),GRN,mw=460)
        d.text((52,610),'Team: Akshay Wagh + Ira (AI teammate, declared)',font=BOLD(16),fill=SUB)
        return im
    if sid=='s04':
        im,d=base('LIVE EVERY MORNING','113 cells, rescored at 06:00')
        mapbox(d,[48,150,790,665],cellsL)
        x=828; y=150
        for b,s in [('06:00','daily free GitHub job'),('NASA + weather','VIIRS 375 m fire feed, 7 days'),('113 cells','each about 27 km wide'),('7 days','the forecast window')]:
            chip(d,x,y,b if len(b)<8 else b,s,GOLD if b=='06:00' else INK,404); y+=118
        d.text((48,678),'akshay-ira-2026.github.io/van-agni',font=BOLD(18),fill=GRN)
        return im
    if sid in ('s05','s06'):
        im,d=base('THE HONEST TEST · REPLAY','22 April 2024: predict, then watch')
        if sid=='s05': day=min(6.99,max(0,(k-0.35)/0.65)*7); pts=wk[wk.day<=day]; outl=top10; lab='top 10 patrol list (gold outline)'
        else: day=6.99; pts=wk; outl=top10; lab='gold = the 10 cells we named'
        mapbox(d,[48,150,820,665],cellsR,pts=pts,outl=outl)
        d.text((856,160),'DAY %d / 7'%(int(day)+1),font=BLACK(40),fill=GOLD)
        hit=0
        if len(pts):
            for cid in top10:
                c=RBY[cid]
                if ((abs(pts.longitude-c['lon'])<0.125)&(abs(pts.latitude-c['lat'])<0.125)).any(): hit+=1
        state_hit.append(hit)
        chip(d,856,230,'%d / 10'%hit,'named cells that burned',GRN if hit==10 else GOLD,376)
        text(d,(856,360),lab,BOLD(19),SUB,mw=370)
        if sid=='s06':
            s=1+0.25*math.sin(min(1,k)*3.14)
            d.rounded_rectangle([856,430,1232,560],radius=18,fill=(24,64,40),outline=GRN,width=3)
            d.text((1044,452),'10 / 10',font=BLACK(int(58*s)),fill=GRN,anchor='ma')
            d.text((1044,522),'all ten burned',font=BOLD(19),fill=INK,anchor='ma')
        return im
    if sid in ('s07','s08','s09'):
        im,d=base('WHAT THE OFFICER GETS','One alert, with its reasons')
        d.rounded_rectangle([70,150,520,660],radius=34,fill=(8,14,11),outline=(120,150,130),width=3)
        d.rounded_rectangle([92,196,498,560],radius=16,fill=(22,48,34))
        d.text((295,166),'09:41',font=BOLD(16),fill=SUB,anchor='ma')
        d.text((114,212),'VAN AGNI · VERY HIGH (95%)',font=BOLD(19),fill=RED)
        y=text(d,(114,244),'Fire risk near 29.12N 79.88E, next 7 days.',BOLD(19),INK,mw=360)
        y=text(d,(114,y+8),'Why: no rain for 49 days; humidity 24%; 44 fire points nearby this week.',REG(18),SUB,mw=360)
        y=text(d,(114,y+10),'वन अग्नि: अगले 7 दिन अति उच्च आग जोखिम (95%). कारण: 49 दिन से बारिश नहीं; कम नमी 24%.',DEV(18),INK,mw=360)
        d.text((114,508),'Advisory only: verify with beat staff.',font=BOLD(15),fill=GOLD)
        x=570
        if sid=='s07':
            rows=[('49 days','without rain',RED),('24%','low humidity',ORG),('44','fire points nearby this week',GOLD),('10 of 113','cells on the daily patrol list',GRN)]
            y=150
            for b,s,c in rows: chip(d,x,y,b,s,c,640); y+=118
        elif sid=='s08':
            y=text(d,(x,190),'वन अग्नि',DEVB(64),GOLD)
            y=text(d,(x,y+16),'अगले सात दिन, अति उच्च आग जोखिम।',DEVB(34),INK,mw=640)
            y=text(d,(x,y+18),'केवल सलाह: बीट स्टाफ से पुष्टि करें।',DEV(26),GRN,mw=640)
            text(d,(x,560),'The same alert, in the language of the beat.',BOLD(20),SUB,mw=620)
        else:
            text(d,(x,200),'Advice, not an order.',BLACK(46),GOLD,mw=620)
            text(d,(x,300),'Van Agni ranks the risk and shows its reasons. The beat officer verifies on the ground and decides. No automatic action is ever taken.',BOLD(24),INK,mw=630)
        return im
    if sid=='s10':
        im,d=base('HELD-OUT 2025 · A YEAR IT NEVER SAW','Does it actually work?')
        chip(d,48,150,'0.914','AUC (Area Under the Curve), 2025',GOLD,360)
        chip(d,432,150,'0.296','PR-AUC (precision–recall)',INK,360)
        chip(d,816,150,'+89%','more fires reached, same 10 patrols',GRN,416)
        g=min(1,k*1.4)
        bars(d,48,320,[('Van Agni top 10',38.6*g,'38.6%',GRN),('Watching past hotspots',20.4*g,'20.4%',(150,160,150))],40,w=820,bh=44,gap=26)
        text(d,(48,600),'Share of cells that actually burned, caught by a daily list of only 10 cells out of 113.',BOLD(20),SUB,mw=1100)
        return im
    if sid=='s11':
        im,d=base('INSIDE THE MODEL','What drives the risk?')
        g=min(1,k*1.3)
        items=[('Fire radiative power, past 7 days',100,'1st',RED),('VIIRS detections, past 7 days',32,'2nd',ORG),('VIIRS detections, past 3 days',24,'3rd',ORG),("Cell's own fire history",23,'4th',GOLD),('Season (day of year)',13,'5th',GRN),('Rain, past 90 days',13,'6th',GRN)]
        bars(d,48,160,[(a,b*g,c,col) for a,b,c,col in items],100,w=700,bh=26,gap=12)
        text(d,(48,640),'LightGBM feature gain, model v2. Satellite signal first, then history, season and rain.',BOLD(18),SUB,mw=1150)
        return im
    if sid=='s12':
        im,d=base('GREEN AI (ARTIFICIAL INTELLIGENCE)','Small on purpose')
        chip(d,48,160,'4.6 s','to train, on a laptop CPU',GRN,376)
        chip(d,452,160,'0.00023','kWh (kilowatt hours) per training run',GRN,376)
        chip(d,856,160,'0.16 g','CO2e to train (CodeCarbon)',GRN,376)
        chip(d,48,300,'0.000062 g','CO2e per 1,000 cell scores',GOLD,580)
        chip(d,652,300,'No LLM','no large language model at runtime',GOLD,580)
        text(d,(48,470),'Measured, not estimated: CodeCarbon logs ship with the code, and the Impact Data Sheet shows every conversion.',BOLD(24),INK,mw=1150)
        text(d,(48,580),'A year of daily maps costs less carbon than boiling a cup of water.',BOLD(22),GRN,mw=1150)
        return im
    if sid=='s13':
        im,d=base('OPEN AND REPRODUCIBLE','Check every number yourself')
        d.rounded_rectangle([48,150,1232,560],radius=16,fill=(7,14,10),outline=LINE,width=2)
        lines=[('$ git clone github.com/akshay-ira-2026/van-agni',SUB),('$ ./reproduce.sh',INK),('  src/features.py   rain 7/30/90 d, dry streak, VIIRS, FRP',SUB),('  src/train.py      LightGBM, train 2019-23 · val 2024 · test 2025',SUB),('  src/predict.py    live + replay modes',SUB),('  tests/            5 passed',GRN),('  outputs/metrics.json   AUC 0.914 · top-10 38.6%',GOLD),('  outputs/codecarbon_*.csv   0.00023 kWh',GOLD)]
        y=178
        for ln,c in lines: d.text((76,y),ln,font=MONO(21),fill=c); y+=44
        text(d,(48,585),'One script rebuilds the data, retrains the model and regenerates the maps in this video.',BOLD(21),SUB,mw=1150)
        return im
    if sid=='s14':
        im,d=base('DEPLOY AND NEXT','Four ways in, one pilot')
        cards=[('Free cloud','GitHub Actions + Pages, live today',GRN),('Docker','one container, offline capable',INK),('On premise','a range office machine',INK),('SMS edge','text alerts where there is no internet',GOLD)]
        x=48
        for b,s,c in cards:
            d.rounded_rectangle([x,170,x+276,360],radius=16,fill=PANEL,outline=LINE,width=2)
            text(d,(x+20,192),b,BLACK(28),c,mw=236); text(d,(x+20,262),s,BOLD(17),SUB,mw=236); x+=300
        d.rounded_rectangle([48,410,1232,560],radius=16,fill=(24,64,40),outline=GRN,width=2)
        d.text((76,434),'PILOT · FEB–JUN 2027',font=BLACK(34),fill=GRN)
        text(d,(76,486),'Nainital or Almora division: daily top-10 list to range officers, scored against what actually burns.',BOLD(21),INK,mw=1100)
        return im
    im,d=base('VAN AGNI','')
    mapbox(d,[560,120,1240,660],cellsR,outl=top10)
    d.text((48,200),'VAN AGNI',font=BLACK(100),fill=GOLD)
    text(d,(52,320),'See the fire before it starts.',BLACK(36),INK,mw=470)
    text(d,(52,440),'Live map\nakshay-ira-2026.github.io/van-agni\n\nCode\ngithub.com/akshay-ira-2026/van-agni',BOLD(19),GRN,mw=480)
    return im

WORDS={o['id']:o for o in T}
def caption(im,sid,now):
    o=WORDS.get(sid); st=[a for s_,a,b in SEG if s_==sid][0]
    if not o or not o['words']: return
    rel=now-st; ws=o['words']
    if rel>o['dur']+0.2: return
    idx=0
    for i,w in enumerate(ws):
        if w[0]<=rel: idx=i
    g=idx//7; grp=ws[g*7:g*7+7]
    d=ImageDraw.Draw(im,'RGBA'); f=DEVB(27) if o['lang']=='hi' else BOLD(27)
    parts=[w[2] for w in grp]; sp=d.textlength(' ',font=f)
    tw=sum(d.textlength(p,font=f) for p in parts)+sp*(len(parts)-1)
    x=(W-tw)/2; y=H-62
    d.rounded_rectangle([x-20,y-10,x+tw+20,y+44],radius=12,fill=(0,0,0,175))
    for j,p in enumerate(parts):
        col=GOLD if g*7+j==idx else WHT
        d.text((x,y),p,font=f,fill=col); x+=d.textlength(p,font=f)+sp

nf=int(TOTAL*FPS)
for i in range(nf):
    now=i/FPS; sid=None; k=1.0
    for s,a,b in SEG:
        if a<=now<b: sid=s; k=(now-a)/(b-a); break
        if now>=b: sid=s; k=1.0
    im=scene(sid,k,now); caption(im,sid,now); d=ImageDraw.Draw(im); progress(d,now)
    im.save('frames/%05d.png'%i)
    if i%300==0: print(i, sid)
print('frames',nf,'max_hit',max(state_hit) if state_hit else None)
