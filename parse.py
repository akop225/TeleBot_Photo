import asyncio
import logging
from bs4 import BeautifulSoup
import requests
import pyppeteer as pyp
import websockets
import datetime
# from pyppeteer_stealth import stealth


async def scrap(page, dic):
    await page.click('#favorite',{'clickCount':2})
    group = await page.xpath('//div[@class="media-body"]//h5')
    logging.info(page.url)
    logging.info(await page.evaluate('el=>el.textContent', group[0]))
    for i in range(1, 7):
        path = f'//descendant::div[1]/descendant::div[@class="container"][{i}]'
        await page.waitForXPath(path)
        day = await page.xpath(path + "//descendant::th[@class='dayh']//descendant::h5")
        day = await page.evaluate("el => el.textContent", day[0])
        if dic.get(day, 0) == 0:
            dic[day] = {}
        path = path + "//descendant::*[@class='slot']"
        pars = await page.xpath(path)
        for y in range(1, len(pars) + 1):
            tds = await page.xpath(path + f'[{y}]' + '//td')
            if len(tds) < 2:
                continue
            par =await page.evaluate("el => el.textContent", tds[0])
            par = par.strip()
            ispar = await page.evaluate("el => el.textContent", tds[1])
            ispar = ispar.strip().split('\n')
            spis = [i.strip() for i in ispar]
            if len(spis) > 2:
                if dic[day].get(par, 0) == 0:
                    dic[day][par] = []
                aud = spis[4] + spis[5]
                if spis[3] == '- Комиссия':
                    aud = spis[5] + spis[6]
                if aud == '+ подгруппы':
                    el = await page.xpath(path + f'[{y}]' + "//*[@class='task']")
                    el=el[0]
                    await page.evaluate('el => el.click()',el)
                    await page.waitForXPath('//div[@id="upTimeslotInfo"]//div[@id="slotDetails"]//*[@data-subgroup]')
                    r = await page.xpath('//div[@id="upTimeslotInfo"]//div[@id="slotDetails"]//*[@data-subgroup]')
                    for j in range(1, len(r) + 1):
                        qw = await page.xpath(
                            f'//descendant::div[@id="upTimeslotInfo"]//descendant::div[@id="slotDetails"]//descendant::div[@data-subgroup][{j}]')
                        qw = await page.evaluate('tableCell04 => tableCell04.innerHTML', qw[0])
                        qw = qw.strip().split('\n')
                        spis1 = [i.strip() for i in qw]
                        aud = spis1[5] + spis1[6]
                        if 'Комиссия' in spis1[2]:
                            aud = spis1[6] + spis1[7]
                        if aud not in dic[day][par]:
                            dic[day][par].append(aud)
                    if y < len(pars):
                        l=[]
                        cnt1=0
                        while l==[]:
                            try:
                                await page.click('#upTimeslotInfo > div > div > div.modal-header > button[aria-label="Close"]')
                                l=await page.xpath('//div[@id="upTimeslotInfo"][@aria-hidden="true"]')
                                cnt1+=1
                                if cnt1>50:
                                    logging.info('cnt>2000')
                                    break
                            except:
                                break
                        await page.setViewport({'width': 1000, 'height': 2500})
                    elif i < 6:
                        l=[]
                        cnt1=0
                        while l == []:
                            try:
                                await page.click(
                                    '#upTimeslotInfo > div > div > div.modal-header > button[aria-label="Close"]')
                                l = await page.xpath('//div[@id="upTimeslotInfo"][@aria-hidden="true"]')
                                if cnt1>50:
                                    logging.info('cnt>2000')
                                    break
                            except:
                                break
                        await page.setViewport({'width': 1000, 'height': 2500})
                else:
                    if aud not in dic[day][par]:
                        dic[day][par].append(aud)
async def parse():
    a=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    logging.basicConfig(filename=f"ITC/ITC_serv/parse_logs/parse-{a}.log", level=logging.INFO)
    logging.info("works")
    dic1={}
    browser = await pyp.launcher.launch(ignoreHTTPSErrors=True,executablePath='/usr/bin/google-chrome', options={'args': ['--no-sandbox', "--disabled-setupid-sandbox"]})
    page = await browser.newPage()
    await stealth(page)
    await page.goto('https://rasp.rea.ru/')
    await page.setViewport({'width':1000,'height':2500})
    page.setDefaultNavigationTimeout(45000)
    await page.waitForSelector('#searchBarContainer > div.clearfix > div > a')
    element=await page.querySelector('#searchBarContainer > div.clearfix > div > a')
    #print(element)
    rect = await page.evaluate("""el => {
        const
    {x, y} = el.getBoundingClientRect();
    return {x, y};
    }""", element)
    print(rect)
    await page.mouse.click(rect['x'],rect['y'])
    #await page.click('#searchBarContainer > div.clearfix > div > a')
    # await page.evaluate(f"""() => {{
    #     document.getElementsByClassName('dropdown-toggle')[0].dispatchEvent(new MouseEvent('click', ));
    # }}""")
    # await page.click('#searchBarContainer > div.clearfix > div > a')
    # await page.click('#searchBarContainer > div.clearfix > div > a')
    # await page.evaluate('element => element.click()', element)
    await page.waitForSelector('a[id="expanderGroup"]')
    #element=await page.querySelector('a[id="expanderGroup"]')
    #print(element)
    # await page.evaluate(f"""() => {{
    #         document.getElementById('expanderGroup').dispatchEvent(new MouseEvent('click', ));
    #     }}""")
    await page.waitFor(1000)
    await page.click('a[id="expanderGroup"]')
    #await page.evaluate( 'element => element.click()', element)
    await page.waitForXPath('//select[@name="Faculty"]')
    logging.info(page.url)
    q=await page.evaluate("""optionSelector => {
            return Array.from(document.querySelector(optionSelector))
                .filter(o => o.value)
                .map(o => {
                    return {
                        value: o.value
                    };
                });        
        }""", 'select[name="Faculty"]')
    await page.setViewport({'width':1000,'height':2500})
    logging.info(page.url)
    q=await page.evaluate("""optionSelector => {
            return Array.from(document.querySelector(optionSelector))
                .filter(o => o.value)
                .map(o => {
                    return {
                        value: o.value
                    };
                });        
        }""", 'select[name="Faculty"]')
    await page.setViewport({'width':1000,'height':2500})
    for i in range(1,len(q)):
        print(q[i]['value'])
        await page.select('select[name="Faculty"]', q[i]['value'])
        await page.waitForXPath(f"""//select[@name="Faculty"]/option[@selected][@value='{q[i]['value']}']""")
        await page.waitForXPath('//select[@name="Course"]/option')
        await page.waitFor(600)
        await page.setViewport({'width':1000,'height':2500})
        y=await page.evaluate("""optionSelector => {
            return Array.from(document.querySelector(optionSelector))
                .filter(o => o.value)
                .map(o => {
                    return {
                        value: o.value
                    };
                });        
        }""", 'select[name="Course"]')
        for u in range(1,len(y)):
            logging.info(y[u]['value'])
            await page.select('select[name="Course"]', y[u]['value'])
            await page.waitForXPath(f"""//select[@name="Course"]/option[@selected][@value='{y[u]['value']}']""")
            await page.waitForXPath('//select[@name="Type"]/option')
            await page.waitFor(600)
            await page.setViewport({'width':1000,'height':2500})
            k=await page.evaluate("""optionSelector => {
            return Array.from(document.querySelector(optionSelector))
                .filter(o => o.value)
                .map(o => {
                    return {
                        value: o.value
                    };
                });        
        }""", 'select[name="Type"]')
            for z in range(1,len(k)):
                print(k[z]['value'])
                await page.select('select[name="Type"]', k[z]['value'])
                await page.waitForXPath(f"""//select[@name="Type"]/option[@selected][@value='{k[z]['value']}']""")
                await page.waitForXPath('//select[@name="Group"]/option')


                await page.waitFor(600)
                await page.setViewport({'width':1000,'height':2500})
                p=await page.evaluate("""optionSelector => {
                return Array.from(document.querySelector(optionSelector))
                    .filter(o => o.value)
                    .map(o => {
                        return {
                            value: o.value
                        };
                    });        
                     }""", 'select[name="Group"]')
                for x in range(1,len(p)):
                    print(p[x]['value'])
                    await asyncio.wait([page.select('select[name="Group"]', p[x]['value']),
                    page.waitForNavigation({'waitUntil':'networkidle0'})],return_when=asyncio.ALL_COMPLETED)
                    await page.waitFor(200)
                    await page.setViewport({'width':1000,'height':2500})
                    page.setDefaultNavigationTimeout(45000)
                    logging.info(page.url)
                    await scrap(page, dic1),
                    await page.waitForXPath('//span[@id="weekNumLabel"]')
                    a=await page.xpath('//span[@id="weekNumLabel"]')
                    a=await page.evaluate("a => a.textContent", a[0])
                    logging.info(a)
                    el=await page.xpath('//div[@id="rightButton"]/button')
                    await page.evaluate('b => b.click()',el[0])
                    await page.waitForXPath(f'//span[@id="weekNumLabel"][text()="{int(a)+1}"]')
                    await page.waitFor(200)
                    await page.setViewport({'width': 1000, 'height': 2500})
                    a=await page.xpath('//span[@id="weekNumLabel"]')
                    a=await page.evaluate("a => a.textContent", a[0])
                    await scrap(page, dic1)
                    await page.waitFor(100)
                    logging.info(a)
    dic2={}
    for i in dic1.keys():
        for y in dic1[i].keys():
            h='_'.join(i.split(', '))
            n='_'.join(y.split())
            dic2[''.join(h.split('.'))+'_'+'_'.join(n.split(':'))]=dic1[i][y].copy()
    lis=[]
    days=dic2.keys()
    dic3={}
    for i in dic2.keys():
        dic3[i]=[]
        for y in dic2[i]:
            if '*' in y:
                dic3[i].append(y[:-1])
            else:
                dic3[i].append(y)
    dic2=dic3.copy()
    for key in days:
        for aud in dic2[key]:
            if aud not in lis:
                if aud.split('-')[1] not in 'Вебинар!' and 'с/з' not in aud.split('-')[1]:
                    lis.append(aud)
    create='''CREATE TABLE weeks_auds
                   (aud text PRIMARY KEY,
                   corp text,
                   floor int,
                   aud_qlear text'''
    for day in days:
        create=create+','+day+' decimal(2,2)'
    create=create+');'
    many_auds=[]
    for i in lis:
        try:
            if len(i.split('-')[1])<=2 and '1' in i.split('-')[0]:
                k=0
            elif len(i.split('-')[1])<=2 and '3' in i.split('-')[0]:
                k=6
            else:
                k=int(i.split('-')[1][0])
        except:
            k=0
        aud=[i, i.split('-')[0], k,i.split('-')[1]]
        for key in days:
            if i in dic2[key]:
                aud.append(1.00)
            else:
                aud.append(0.00)
        aud=tuple(aud)
        many_auds.append(aud)
    insert="insert into weeks_auds values (?"
    for i in range(1,len(many_auds[0])):
        insert=insert+', ?'
    insert=insert+');'

    import sqlite3 as sql
    con = sql.connect('ITC/ITC_serv/chbsa.db')
    cur = con.cursor()
    try:
        cur.execute('drop table weeks_auds')
        con.commit()
    except:
        pass
    cur.execute(create)
    con.commit()
    cur.executemany(insert, many_auds)
    con.commit()
    con = sql.connect('ITC/ITC_serv/chbsa.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    try:
        cur.execute('select * from bron_auds;')
        one=cur.fetchone()
        keys=one.keys()
        create=keys[0]
        for i in keys[1:]:
            create+=', '+i
        cur.execute(f'create table last_bron_auds ({create})')
        con.commit()
        cur.execute('insert into last_bron_auds select * from bron_auds;')
        con.commit()
        cur.execute('drop table bron_auds;')
        con.commit()
    except:
        pass
    create='''CREATE TABLE bron_auds_first
                   (aud text PRIMARY KEY,
                   corp text,
                   floor int,
                   aud_qlear text'''
    create1='''CREATE TABLE bron_auds
                   (aud text PRIMARY KEY,
                   corp text,
                   floor int,
                   aud_qlear text'''
    for day in days:
        create=create+','+day+' decimal(2,2)'
        create1=create1+','+day+' decimal(2,2)'
    create=create+');'
    create1=create1+');'
    cur.execute(create)
    con.commit()
    cur.execute(create1)
    con.commit()
    many_auds=[]
    for i in lis:
        try:
            if len(i.split('-')[1])<=2 and '1' in i.split('-')[0]:
                k=0
            elif len(i.split('-')[1])<=2 and '3' in i.split('-')[0]:
                k=6
            else:
                k=int(i.split('-')[1][0])
        except:
            k=0
        aud=[i, i.split('-')[0], k,i.split('-')[1]]
        for key in days:
            aud.append(0)
        aud=tuple(aud)
        many_auds.append(aud)
    insert="insert into bron_auds_first values (?"
    for i in range(1,len(many_auds[0])):
        insert=insert+', ?'
    insert=insert+');'
    cur.executemany(insert, many_auds)
    con.commit()
    keys1=['aud', 'corp','floor', 'aud_qlear']+list(days)
    try:
        keys2=[]
        keys3=[]
        for i in days:
            if i in keys:
                keys2.append(i)
            else:
                keys3.append(i)
        j=''
        for i in keys3:
            j+=', '+i
        m=''
        for i in keys2:
            m+=f', coalesce({i}, 0.00)+coalesce({i}1,0.00) as {i}'
        q=''
        for i in keys:
            q+=', b.'+i+' as '+i+'1'
        cur.execute(f'''insert into bron_auds
             select distinct
             case when aud is null then aud1 else aud end as aud,
             case when corp is null then corp1 else corp end as corp,
             case when floor is null then floor1 else floor end as floor,
             case when aud_qlear is null then aud_qlear1 else aud_qlear end as aud_qlear
             {m}
             {j}
             from (SELECT a.* {q}
                            FROM   bron_auds_first as a 
                                   LEFT JOIN last_bron_auds b
                                      ON a.aud = b.aud
                            UNION
                            SELECT a.* {q}
                            FROM   last_bron_auds as b
                                   LEFT JOIN bron_auds_first as a
                                      ON a.aud = b.aud
                            WHERE  a.aud IS NULL)
             ''')
        con.commit()
        cur.execute('drop table bron_auds_first;')
        con.commit()
        cur.execute('drop table last_bron_auds;')
        con.commit()
    except:
        cur.execute('''insert into bron_auds
                    select * from bron_auds_first''')
        con.commit()
        cur.execute('drop table bron_auds_first;')
        con.commit()
    m=''
    for i in keys1[4:]:
            m+=f', coalesce({i}, 0)+coalesce({i}1,0) as {i}'
    q=''
    for i in keys1:
        q+=', b.'+i+' as '+i+'1'
    cur.execute('DROP view IF EXISTS weeks_with_bron;')
    con.commit()
    cur.execute(f'''create view weeks_with_bron as
             select distinct
             case when aud is null then aud1 else aud end as aud,
             case when corp is null then corp1 else corp end as corp,
             case when floor is null then floor1 else floor end as floor,
             case when aud_qlear is null then aud_qlear1 else aud_qlear end as aud_qlear
             {m}
             from (SELECT a.* {q}
                            FROM   bron_auds as a 
                                   LEFT JOIN weeks_auds b
                                      ON a.aud = b.aud
                            )
             ''')
    con.commit()

loop=asyncio.get_event_loop()
loop.run_until_complete(parse())