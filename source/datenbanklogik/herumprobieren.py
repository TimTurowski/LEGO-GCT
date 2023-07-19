from geschäftslogik import einzelteilliste, legosetpreise
from datenzugriffsobjekt import Session
from source.Entity import entities
"""
e1 = entities.Einzelteil(einzelteil_id="1")
e2 = entities.Einzelteil(einzelteil_id="2")
e3 = entities.Einzelteil(einzelteil_id="3")
l1 = entities.Legoset(set_id="1",name="hi")"""
l2 = entities.Legoset(set_id="2",name="bye")
"""with Session() as session:
    with session.begin():
        session.add(e1)
        session.add(e2)
        session.add(e3)
        session.add(l1)
        session.add(l2)
        session.add(entities.EinzelzeilLegoset(anzahl=2,einzelteile=entities.Einzelteil(einzelteil_id="4"),set=entities.Legoset(set_id="3",name="peter")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id,preis=3.12,url="www.tim.de",anbieter=entities.Anbieter(url="www.peter.de",name="peter")))
        session.add(entities.SetMarktpreis(preis=12.23, url="www.humbuck.com/4", set=entities.Legoset(set_id="4",name="hallo"),
                                           anbieter=entities.Anbieter(url="www.lego.de", name="lego")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id, preis=15.32, url="www.peter.com/2",
                                           anbieter=entities.Anbieter(url="www.peter.com", name="peter")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id, preis=10.99, url="www.alfred.de/2",
                                           anbieter=entities.Anbieter(url="www.alfred.de", name="alfred")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id,anbieter_url="www.lego.de", preis=14.99, url="www.lego.de/2"))
        session.commit()
    session.close()"""
    
"""for i in einzelteilliste():
    print(i)"""
for i in legosetpreise(l2):
    print(i)