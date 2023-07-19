from geschäftslogik import einzelteilliste
from datenzugriffsobjekt import Session
from source.Entity import entities

e1 = entities.Einzelteil(einzelteil_id="1")
e2 = entities.Einzelteil(einzelteil_id="2")
e3 = entities.Einzelteil(einzelteil_id="3")
l1 = entities.Legoset(set_id="1",name="hi")
l2 = entities.Legoset(set_id="2",name="bye")
with Session() as session:
    with session.begin():
        session.add(e1)
        session.add(e2)
        session.add(e3)
        session.add(l1)
        session.add(l2)
        session.add(entities.EinzelzeilLegoset(anzahl=2,einzelteile=entities.Einzelteil(einzelteil_id="4"),set=entities.Legoset(set_id="3",name="peter")))
        session.commit()
    session.close()

for i in einzelteilliste():
    print(i)

