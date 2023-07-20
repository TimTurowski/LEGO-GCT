from datenzugriffsobjekt import Session
from source.Entity import entities
"""
e1 = entities.Einzelteil(einzelteil_id="1")
e2 = entities.Einzelteil(einzelteil_id="2")
e3 = entities.Einzelteil(einzelteil_id="3")"""
l1 = entities.Legoset(set_id="1",name="hi")
l2 = entities.Legoset(set_id="2",name="bye")
with Session() as session:
    with session.begin():
        """session.add(e1)
        session.add(e2)
        session.add(e3)
        session.add(l1)
        session.add(l2)
        session.add(entities.EinzelteilLegoset(anzahl=2,einzelteile=entities.Einzelteil(einzelteil_id="4"),set=entities.Legoset(set_id="3",name="peter")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id,preis=3.12,url="www.tim.de",anbieter=entities.Anbieter(url="www.peter.de",name="peter")))
        session.add(entities.SetMarktpreis(preis=12.23, url="www.humbuck.com/4", set=entities.Legoset(set_id="4",name="hallo"),
                                           anbieter=entities.Anbieter(url="www.lego.de", name="lego")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id, preis=15.32, url="www.peter.com/2",
                                           anbieter=entities.Anbieter(url="www.peter.com", name="peter")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id, preis=10.99, url="www.alfred.de/2",
                                           anbieter=entities.Anbieter(url="www.alfred.de", name="alfred")))
        session.add(entities.SetMarktpreis(set_id=l2.set_id,anbieter_url="www.lego.de", preis=14.99, url="www.lego.de/2"))
        session.add(entities.SetMarktpreis(set_id=l1.set_id,anbieter_url=["www.lego.de","www.peter.com","www.alfred.de"],preis=[12.5,13.5,11.5],url=["www.lego.de/1","www.peter.com/1","www.alfred.de/1"]))
        session.add(entities.EinzelteilLegoset(anzahl=3,einzelteile=entities.Einzelteil(einzelteil_id="1"),set=entities.Legoset(set_id="3",name="peter")))"""
        session.add(entities.EinzelteilMarktpreis(preis=5.99,url="hi",einzelteile=entities.Einzelteil(einzelteil_id="134"),anbieter=session.query(entities.Anbieter).filter(entities.Anbieter.url == "peter").first()))
        """session.add(entities.EinzelteilMarktpreis(preis=4.01,url="hey",einzelteile=entities.Einzelteil(einzelteil_id="125"),anbieter=entities.Anbieter(url="peter",name="peterius")))"""
        session.commit()
    session.close()
    
"""for i in einzelteilliste():
    print(i)"""
"""for i in legosetpreise(l1):
    print(i)"""
