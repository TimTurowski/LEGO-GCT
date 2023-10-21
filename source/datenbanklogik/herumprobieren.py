from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.Entity import entities
from sqlalchemy.orm import joinedload
dao = Datenzugriffsobjekt()
"""e1 = entities.Einzelteil(einzelteil_id="1")
e2 = entities.Einzelteil(einzelteil_id="2")
e3 = entities.Einzelteil(einzelteil_id="3")
l1 = entities.Legoset(set_id="1",name="hi")
l2 = entities.Legoset(set_id="2",name="bye")""""""
with dao.Session() as session:
    with session.begin():
        session.add(e1)
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
        session.add(entities.EinzelteilLegoset(anzahl=3,einzelteile=entities.Einzelteil(einzelteil_id="1"),set=entities.Legoset(set_id="3",name="peter")))
        session.add(entities.EinzelteilMarktpreis(preis=5.99,url="hi",einzelteile=entities.Einzelteil(einzelteil_id="134"),anbieter=session.query(entities.Anbieter).filter(entities.Anbieter.url == "peter").first()))
        session.add(entities.EinzelteilMarktpreis(preis=4.01,url="hey",einzelteile=entities.Einzelteil(einzelteil_id="125"),anbieter=entities.Anbieter(url="peter",name="peterius")))
        session.add(entities.EinzelteilMarktpreis(preis=0.99,url="www.a.de/1",einzelteile=entities.Einzelteil(einzelteil_id="1"),anbieter=entities.Anbieter(url="www.a.de",name="a")))
        session.add(entities.EinzelteilMarktpreis(anbieter_url="www.a.de",preis=1.99,url="www.a.de/2",einzelteile=entities.Einzelteil(einzelteil_id="2")))
        session.add(entities.EinzelteilMarktpreis(einzelteil_id="1",preis=2.99,url="www.b.de/1",anbieter=entities.Anbieter(url="www.b.de",name="b")))
        session.add(entities.EinzelteilMarktpreis(einzelteil_id="2",anbieter_url="www.b.de",preis=3.99,url="www.b.de/2"))
        session.add(entities.Anbieter(url="www.c.de",name="c"))
        session.add(entities.Einzelteil(einzelteil_id="3"))
        session.add(entities.EinzelteilMarktpreis(anbieter_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick",preis=4.99,url="www.c.de/3",einzelteile=entities.Einzelteil(einzelteil_id="5")))
        e1 = session.query(entities.Einzelteil).options(joinedload(entities.Einzelteil.anbieter_marktpreise)).filter(entities.EinzelteilMarktpreis.anbieter_url == "https://www.lego.com/de-de/pick-and-build/pick-a-brick").all()
        a = session.query(entities.Legoset).filter(entities.Legoset.set_id == "21058").all()
        session.commit()
    session.close()
dao.loesche_sets(a)"""
print(len(dao.einzelteile_zu_legoset('31203')))
for i in dao.einzelteile_zu_legoset('31203'):
    print(i)
"""for i in einzelteilliste():
    print(i)"""
"""for i in legosetpreise(l1):
    print(i)"""
"""for i in e1:
    print(i)"""
