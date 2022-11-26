TODO:

* Hitta ett bättre ord än felläge?
* Bättre på svenska eller engelska?

# Specifikation

Denna specifikation är den som alla tester ska följa.

Målet med att ha ännu en spec är så att man kan specifiera exakt hur testerna
ska fungera. [API-specen från kurssidan](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/) (här kallad *kursspecen*) specar inte
exakt hur datalagret ska hantera fellägen, d.v.s när saker går fel.

För att kunna skapa fler och mer robusta tester krävs en mer specifik specifikation,
vilket är vad som försöks ådstakommas här.

Notera att för att datalagret ska bli godkänt *måste* den följa kursspecen (samt [kravspecen](https://www.ida.liu.se/~TDP003/current/projekt/uppgift.sv.shtml)).
Använd därför inte den här specen som en ersättning för kursspecen, utan
istället som ett tillägg.

För att datalagret ska bli godkänt måste den även klara alla tester som finns
i det här git-repositoryt. Då dessa följer specen betyder det att denna spec
måste följas.

## Datatyper

### Projekt

Ett projekt representeras som en Python-`dict`.

| Fältnamn           | Datatyp | Beskrivning                                                                          |
| ------------------ | ------- | ------------------------------------------------------------------------------------ |
| `project_id`       | `int`   | Projekt-id. Måste vara unikt.                                                        |
| `project_name`     | `str`   | Projektnamn.                                                                         |
| `start_date`       | `str`   | Startdatum, representerat enligt [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). |
| `end_date`         | `str`   | Slutdatum, representerat enligt [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).  |
| `course_id`        | `str`   | Kurs-ID. Inget särskilt format specifierat.                                          |
| `course_name`      | `str`   | Kursnamn.                                                                            |
| `techniques_used`  | `[str]` | En lista över alla tekniker som använts i projektet.                                 |
| `description`      | `str`   | En kort beskrivning av projektet.                                                    |
| `long_description` | `str`   | En längre beskrivning av projektet.                                                  |
| `image`            | `str`   | En länk till en bild; antingen en extern URL, eller en sökväg till en fil på disk.   |
| `external_link`    | `str`   | En länk till en extern projektsida.                                                  |

## Endpoints

Lista över endpoints.

| Endpoint                                      |
| --------------------------------------------- |
| [`load`](#load)                               |
| [`get_project_count`](#get-project-count)     |
| [`get_project`](#get-project)                 |
| [`search`](#search)                           |
| [`get_techniques`](#get_techniques)           |
| [`get_technique_stats`](#get_technique_stats) |

Alla endpoints nedan följer samma struktur:
* Hur funktionen ser ut, med alla parametrar etc.
* En kort beskrivning av funktionen
* En lista på alla parametrar
* En beskrivning av vilket värde som ska returneras
* En lista på möjliga fellägen och deras åtgärder

Vissa fellägen kan datalagret strunta i, då ansvaret läggs på presentationslagret:

* Argument kan antas ha rätt datatyp.
* Alla endpoints förutom `load` kan anta att `db`-parametern innehåller en lista
  som returnerats från `load`.

Dessa finns inte listade under varje endpoint.


### Load

`load(filename)`

Läser in JSON-formatterad data från filen `filename` och returnerar en lista
på alla projekt.
Denna lista ska vara sorterad efter projekt-id.

Filen måste vara en giltig JSON-fil med en lista av ett eller flera [projekt](#projekt).

#### Parametrar

| Parameter  | Datatyp | Beskrivning                            |
| ---------- | ------- | -------------------------------------- |
| `filename` | `str`   | Sökvägen till den fil som ska läsas in |

#### Returvärde

`load` ska returnera en lista med alla projekt, inläst från filen `filename`.
Ifall något av [fellägena](#fellägen) uppstår, se beskrivningen under det felläget.

#### Fellägen

| Felläge                                                                  | Åtgärd                                                                                                   |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Filen `filename` finns inte                                              | Returnera `None`                                                                                         |
| Filen `filename` innehåller inte giltig JSON                             | Returnera `None`                                                                                         |
| Filen `filename` innehåller giltig JSON, men inte i det format som krävs | Returnera `None`                                                                                         |
| Fler än ett projekt har samma `project_id`                               | Bara det första projektet med det ID:t ska finnas med i den returnerade listan; alla andra ska ignoreras |

### Get Project Count

`get_project_count(db)`

Returnerar det antal projekt som finns i `db`.

#### Parametrar

| Parameter | Datatyp   | Beskrivning                                        |
| --------- | --------- | -------------------------------------------------- |
| `db`      | `[{...}]` | Den lista med projekt som returnerats från `load`. |

#### Returvärde

`get_project_count` ska returnera antalet projekt i `db` som en `int`.

#### Fellägen

Inga `get_project_count`-specifika fellägen specifieras.

### Get Project

`get_project(db, id)`

Returnerar det projekt i `db` som har ID:t `id`.
Returnerar `None` ifall inget sådant projekt finns.

#### Parametrar

| Parameter | Datatyp   | Beskrivning                                       |
| --------- | --------- | ------------------------------------------------- |
| `db`      | `[{...}]` | Den lista med projekt som returneras från `load`. |
| `id`      | `int`     | ID:t på projektet som ska hämtas.                 |

#### Returvärde

`get_project` ska returnera det projekt i `db` som har `id` som ID, ifall något sådant projekt hittas.

#### Fellägen

| Felläge                   | Åtgärd           |
| ------------------------- | ---------------- |
| Inget projekt har ID `id` | Returnera `None` |

### Search

`search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None)`

Söker efter projekt i `db` som uppfyller de kraven som specifieras i parametrarna.

#### Parametrar

| Parameter       | Datatyp              | Beskrivning                                                                                                                                                                                                                                                                                                                               |
| --------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `db`            | `[{...}]`            | Den lista med projekt som returneras från `load`.                                                                                                                                                                                                                                                                                         |
| `sort_by`       | `str`                | Det fält som den returnerade listan ska sorteras efter.                                                                                                                                                                                                                                                                                   |
| `sort_order`    | `str`                | `'asc'` eller `'desc'` för stigande respektive fallande sorteringsordning.                                                                                                                                                                                                                                                                |
| `techniques`    | `[str]` eller `None` | En lista på tekniker att filtrera efter. Alla resultat måste innehålla alla tekniker i `techniques` i sin `techniques_used`.                                                                                                                                                                                                              |
| `search`        | `str` eller `None`   | Strängen som ska sökas efter. `None` betyder att ingen sökning ska ske, utan bara eventuell filtrering enligt `techniques`. Sökningen ska vara *case-insensitive*.                                                                                                                                                                        |
| `search_fields` | `[str]` eller `None` | De fält vari `search` ska sökas efter. En tom lista betyder att inga resultat ska returneras, oavsett vad `search` är. Ett värde på `None` betyder att *alla* fält ska sökas i; inte bara de som defineras under [projekt](#projekt), utan även eventuella extra fält som kan finnas. Det räcker med att *ett* fält innehåller söktermen. |

#### Returvärde

`search` ska returnera en lista med resultat, filtrerat efter både `techniques` och `search` + `search_fields`.
Listan ska även vara sorterad enligt `sort_by` och `sort_order`.

#### Fellägen

| Felläge                                                                       | Åtgärd                                                                                        |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Fältet som specifieras i `sort_by` finns inte                                 | Lägg de projekt som inte innehåller `sort_by` sist; dessa ska vara sorterade efter projekt-ID |
| Fältet som specifieras i `sort_by` innehåller värden som inte går att jämföra | Raise:a ett `TypeError`                                                                       |
| `sort_order` är varken `asc` eller `desc`                                     | Raise:a ett `ValueError`                                                                      |

### Get Techniques

`get_techniques(db)`

Returnerar en lista med alla tekniker som finns med i `db`.
Denna lista ska vara lexikografiskt sorterad enligt svenska regler.

#### Parametrar

| Parameter | Datatyp   | Beskrivning                                       |
| --------- | --------- | ------------------------------------------------- |
| `db`      | `[{...}]` | Den lista med projekt som returneras från `load`. |

#### Returvärde

`get_techniques` ska returnera en lista med alla tekniker som finns med i `db`.
Listan ska vara lexikografiskt sorterad enligt svenska regler (t.ex. åäö sist).
Varje teknik ska endast finnas med *en* gång i listan.

#### Fellägen

Inga `get_techniques`-specifika fellägen specifieras.

### Get Technique Stats

`get_technique_stats(db)`

Returnerar information om vilka projekt som innehåller varje teknik.

#### Parametrar

| Parameter | Datatyp   | Beskrivning                                       |
| --------- | --------- | ------------------------------------------------- |
| `db`      | `[{...}]` | Den lista med projekt som returneras från `load`. |

#### Returvärde

`get_technique_stats` ska returnera en `dict`, där det finns en nyckel för varje
teknik i `db`, vars värde är en lista med `dict`s.

Dessa `dict`s ska se ut så här:

| Nyckel   | Värde                      |
| -------- | -------------------------- |
| `"id"`   | Projekt-ID:t som en `int`  |
| `"name"` | Projektnamnet som en `str` |

Exempel:

```JSON
{
    "python": [{"id": 42, "name": "TDP003"}, {"id": 17, "name": "TDP002"}],
    "c++": [{"id": 3, "name": "TDP005"}]
}
```

#### Fellägen

Inga `get_technique_stats`-specifika fellägen specifieras.

## Tester

Här beskrivs tester: vad de vill testa och varför.
Exakt hur testerna går till måste inte beskrivas.

| Test                                                                                                          |
| ------------------------------------------------------------------------------------------------------------- |
| [`test_load`](#test_load)                                                                                     |
| [`test_load_gives_sorted_data`](#test_load_gives_sorted_data)                                                 |
| [`test_load_ignores_duplicate_id`](#test_load_ignores_duplicate_id)                                           |
| [`test_reload`](#test_reload)                                                                                 |
| [`test_get_project_count`](#test_get_project_count)                                                           |
| [`test_get_project`](#test_get_project)                                                                       |
| [`test_search_all`](#test_search_all)                                                                         |
| [`test_search_filter`](#test_search_filter)                                                                   |
| [`test_search`](#test_search)                                                                                 |
| [`test_case_insensitive_search`](#test_case_insensitivite_search)                                             |
| [`test_search_places_non_existant_sort_by_fields_last`](#test_search_places_non_existant_sort_by_fields_last) |
| [`test_search_sort_order_is_valid`](#test_search_sort_order_is_valid)                                         |
| [`test_search_invalid_comparison`](#test_search_invalid_comparison)                                           |
| [`test_get_techniques`](#test_get_techniques)                                                                 |
| [`test_get_technique_stats`](#test_get_technique_stats)                                                       |

### `test_load`

Fanns från första början.

Ej modifierad.

### `test_load_gives_sorted_data`

Testar att listan som [`load`](#load) returnerar är sorterad efter projekt-ID.
Detta testar inte [`test_load`](#test_load).

Detta test implementerades för att upprätthålla [API-specen](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/)s krav på `load`.

Testförfattare: Viktor Norlin (vikno856)

### `test_load_ignores_duplicate_id`

Testar att [`load`](#load) ignorerar projekt med samma projekt-ID som redan finns;
d.v.s. att alla projekt med samma ID förutom det första ignoreras.

Detta test implementerades för att upprätthålla denna specs krav på [`load`](#load).

Testförfattare: Viktor Norlin (vikno856)

### `test_reload`

Testar att `load` faktiskt läser in filen varje gång den anropas.
Om den cachar data på ett naivt sätt kommer
datalagret ej att klara detta test.

Detta test implementerades för att upprätthålla krav 7 från [kravspecen](https://www.ida.liu.se/~TDP003/current/projekt/uppgift.sv.shtml).

Testförfattare: Einar Persson (einpe291)

### `test_get_project_count`

Testar att [`get_project_count`](#get-project-count) returnerar ett nummer som stämmer överens med antal projekt i projektlistan.

Detta test är för att upprätthålla [API-specens](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/)s krav på [`get_project_count`](#get-project-count).

### `test_get_project`

Testar att [`get_project`](#get-project) returnerar projektet med angivet ID från den angivna listan. Om projektet med angivet ID inte finns så returneras None.

Detta test är för att upprätthålla [API-specens](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/)s krav på [`get_project`](#get-project).

### `test_search_all`

Testar att ett anrop till `data.search(db)` returnerar alla projekt.
Antar att `test_search_places_non_existant_sort_by_fields_last` inte failar.

Detta test implementerades for att upprätthålla [API-specen](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/)s krav på `search`.

Testförfattare: Einar Persson (einpe291)

### `test_search_filter`

Testar att anrop till `data.search(db, techniques=[...])` returnerar alla projekt som innehåller
de tekniker som stoppats in.

Detta test implementerades för att upprätthålla [API-specen](https://www.ida.liu.se/~TDP003/current/portfolio-api_python3/)s krav på `search`.

Testförfattare: Einar Persson (einpe291)

### `test_search`

Fanns från första början.

Ej modifierad.

### `test_case_insensitive_search`

Testar så [`search`](#search) kan hantera strängar med både stora och små bokstäver.

Testförfattare: Filip Ingvarsson (filin764)

### `test_search_places_non_existant_sort_by_fields_last`

Testar att [`search`](#search) placerar de projekt som saknar det fält som specificeras i `sort_by` sist i listan den returnerar.

Om fler projekt saknar det fält som specificeras i `sort_by` sorteras de efter projekt-ID.

Detta test implementerades för att upprätthålla denna specs krav på [`search`](#search).

Testförfattare: Viktor Norlin (vikno856)

### `test_search_sort_order_is_valid`

Testar att [`search`](#search) raise:ar ett ValueError om parametern `sort_order` är en sträng men inte "desc" eller "asc"

Detta test implementerades för att upprätthålla denna specens krav på [`search`](#search)

Testförfattare: Viktor Norlin (vikno856)

### `test_search_invalid_comparison`

Testar att [`search`](#search) raise:ar ett TypeError om fältet specificerat i `sort_by` är icke jämförbart.

Detta test implementerades för att upprätthålla denna specens krav på [`search`](#search)

Testförfattare: Viktor Norlin (vikno856)

### `test_get_techniques`

Fanns från första början.

Ej modifierad.

### `test_get_technique_stats`

Fanns från första början.

Ej modifierad.
