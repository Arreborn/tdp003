# Tester för datalagret

Detta repository innehåller tester för datalagret.

Lägg filerna `data_test.py`, `data.json` och `data.py` i samma katalog. `data.py` är den fil som innehåller era implementerade funktioner för API:t.

Kör testerna med följande kommando:
```sh
$ python3 data_test.py
```

Om någon känner att något test är för restriktivt bör diskussion ske i första
hand i ett issue, och i andra hand över discord.

## Om `SPEC.md`

`SPEC.md` innehåller en specifikation på hur datalagret ska se ut, mycket
lik den från [kurssidan](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/data-module.html#get_techniques).
Dock är den lite mer restriktiv, och innehåller detaljer och krav som inte
finns i kursspecen. Detta är för att ha ett mer utförligt underlag för att skriva
tester. Notera att alla datalager måste klara alla gemensamma tester, och då
dessa ska vara baserade på `SPEC.md` måste datalagret även upfylla den specen.

Det är tänkt att alla ska samarbeta med `SPEC.md` och förändra den så att den blir så
precis som möjligt, med rimliga krav.

## Att ändra `SPEC.md`

Att hejvilt ändra `SPEC.md` påverkar *alla* i hela klassen. Icke-triviala ändringar bör göras först
efter diskussion med andra i klassen, antingen över issues eller via Discord. Föredra dock issues.

## Att lägga till tester

Tilläg av nya tester och förbättring av befintliga tester är mycket uppskattat.
Tester ska kolla att `SPEC.md` följs; ifall du vill lägga till ett testfall som
inte stöds av `SPEC.md`, se till att `SPEC.md` också ändras. Som sagt ovan så 
bör alla icke-triviala ändringar av `SPEC.md` ske först efter diskussion.

I slutet av `SPEC.md` finns det en lista på alla tester, där det står kort om vad
testerna testar efter, och varför, samt vem som skapat testet. Ändra gärna där när
tillägg eller ändringar av tester görs.

## Automatisk testkoll via Gitlab CI

Gitlab har en funktion där tester automatiskt kan utföras när man pushar kod upp 
till repositoryt.

Här finns instruktioner om hur man kan fixa det själv.

Notera att detta kräver att man har ett gitlab-repo som ligger på `gitlab.liu.se`.
Instruktionerna är även anpassade till att en pythonfil innehåller hela datalagerimplementationen.

Först måste man lägga till `tdp003-gemensam-installationsmanual-2022` som en
submodul i git. Detta kommer att göra att man har en
`tdp003-gemensam-installationsmanual-2022`-mapp i sit repo, som kommer vara länkat
till detta repo.
Mer om submoduler i git finns att läsa om bl.a. [här](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

Det kan finnas sätt där man inte behöver lägga till submodulen, men det är inget
som jag har koll på.

För att skapa submodulen:
```bash
$ git submodule add ../../pohna45/tdp003-gemensam-installationsmanual-2022
```

Lägg sedan in texten nedan i en fil `.gitlab-ci.yml`, och ersätt `<data_layer>`
med sökvägen till den pythonfil som ni implementerat datalagret i.

```yaml
variables:
  GIT_SUBMODULE_STRATEGY: recursive     # needed to initite submodules

image: python

stages:     # Job stages; might be unnecessary
  - test

before_script:
  - python --version        # For debugging

test-job:
  stage: test
  before_script:
    - git submodule update --recursive --remote
  script:
    - cp <data_layer.py> tdp003-gemensam-installationsmanual-2022/databastester/data.py
    - cd tdp003-gemensam-installationsmanual-2022/databastester/ && python data_test.py
```

Committa både submodulen och `.gitlab-ci.yml` och pusha upp dem till ert repo.

Jag tror inget mer ska behövas för att få igång CI.
Nu borde varje commit som pushas härefter få en symbol som visar om
testerna klarats eller ej.

Notera att om testerna modifieras kommer de nya testerna användas till
nästa gång som kod pushas; redan pushad kod kommer inte testas på nytt.
