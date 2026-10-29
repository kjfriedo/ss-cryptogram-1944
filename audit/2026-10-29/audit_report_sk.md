# SS kryptogram 1944/45: nezávislý audit

Dátum: 29. 10. 2026. Audit issue https://github.com/kjfriedo/ss-cryptogram-1944/issues/1
a stavu repozitára na commite `1eac5795a712322331e76ba1b82f71291cf1ea48`.
Issue pri načítaní nemalo komentáre. Tento audit nebol publikovaný do issue.

## Verdikt

Sekvencia má veľmi silnú väzbu na geometriu klávesnice QWERTZ. Najúspornejšie pracovné
vysvetlenie je tvorba textu pohybmi po klávesnici, s opakovanými smerovými ťahmi.
Formulácia „je definitívne dokázané, že nejde o šifru“ však presahuje dostupné dôkazy.
Nie je určené, či dokument slúžil ako výplň, cvičenie, klamný text, chybne generovaný kľúč
alebo nosič dodatočnej informácie. Štatistika neurčuje pôvod, datovanie ani úmysel autora.

## 1. Pevné zistenia

Reprodukoval som pôvodný program a napísal samostatný výpočet. Rozšírené permutačné
testy používajú numpy/scipy, seed 20261029 a 100 000 realizácií na hlavný náhodný model.
Úplné číselné výsledky sú v `audit_results.json`; výpočet v `independent_audit.py`.

| Štatistika | Pozorovanie | Referenčný model |
|---|---:|---:|
| Počet písmen | 575 | 574 po sebe idúcich dvojíc |
| Pôvodná susednosť, vrátane rovnakej klávesy | 300/574 = 52,26 % | presný priemer premiešania 17,00 % |
| Susednosť iba rôznych klávesov | 278/574 = 48,43 % | priemer simulácie 12,11 % |
| Iba vodorovné susedné rôzne klávesy | 214/574 = 37,28 % | 8,97 % |
| Rôzne klávesy, vzdialenosť ≤ 1,3 | 369/574 = 64,29 % | 21,62 % |
| Susednosť vnútri fyzických riadkov | 294/541 = 54,34 % | pri premiešaní každého riadka 100,81/541 = 18,63 % |
| QWERTY, pôvodná definícia | 246/574 = 42,86 % | 16,54 % |
| Index koincidencie | 0,0488896 | rovnomerné nezávislé A–Z: 1/26 ≈ 0,03846 |

V každom z uvedených permutačných testov susednosti bolo 0 prekročení zo 100 000.
Monte Carlo hodnota s korekciou +1 je 1/100001; pri nulovom počte prekročení je
jednostranná 95 % horná hranica skutočnej pravdepodobnosti približne 3×10⁻⁵.
To nie je numerický dôkaz extrémnej gaussovskej pravdepodobnosti odvodený zo z≈23.

Silný signál nezmizol pri zachovaní frekvencií každého riadka. Nedá sa teda vysvetliť
iba tým, že rôzne riadky používajú odlišné oblasti klávesnice. Navyše pri náhodnom
priradení všetkých 26 označení písmen ku klávesom, so zachovaním celej bigramovej
štruktúry, bolo opäť 0/100000 skóre aspoň takých vysokých ako skutočné QWERTZ.
Tento test podporuje špecifickú väzbu označení písmen na klávesnicu; nie je to test
všetkých možných substitučných kľúčov zvolených zámerne podľa klávesnice.

QWERTZ sedí lepšie ako QWERTY, ale aj QWERTY má silný signál, pretože väčšina rozloženia
je spoločná. Geometria podporuje rodinu rozložení, sama neidentifikuje národnosť pisára
ani konkrétny model stroja.

## 2. Čo je metodicky správne a čo treba opraviť

### Náhodný model a význam p-hodnoty

Permutácia rovnakých písmen je dobrý prvý test: zachováva presné monogramové frekvencie,
a teda neopiera výsledok o nesprávny predpoklad rovnomerného výskytu A–Z. Jej nulová
hypotéza však znie „poradie je výmenné pri daných počtoch písmen“, nie „text je šifra“.
Odmietnutie tejto hypotézy odhaľuje závislosti. Samo nerozhoduje medzi jazykom,
šifrou so zachovanou štruktúrou, klávesnicovými ťahmi a zámernou konštrukciou.

Pôvodných 2000 permutácií umožňuje rozlíšiť p najnižšie približne 0,0005.
z≈22 je opis vzdialenosti od stredu náhodného modelu, nie overený normálny chvost.
Pri testoch odvodených z rovnakých bigramov nemožno násobiť p-hodnoty, akoby išlo
o nezávislé dôkazy. Výber testov po pozretí textu tiež treba uviesť; veľkosť efektu
ostáva presvedčivá, presná nekorigovaná p-hodnota však nie je univerzálna miera istoty.

### „Susedná klávesa“

Kód používa idealizované rady s posunmi 0 / 0,25 / 0,75 a euklidovskú vzdialenosť ≤1,1.
Započítava aj opakovaný úder do tej istej klávesy: 22 z 300 úspechov. Niektoré prirodzené
diagonály pri tejto hranici vynecháva. Definícia nie je neutrálna historická norma
pre všetky písacie stroje. Rozšírené výpočty vyššie ukazujú, že výsledok nestojí
na opakovaných klávesoch ani na jedinej úzkej hranici vzdialenosti.

### Frekvencie nie sú rovnomerné

„Flat frequencies / IC close to random“ je zavádzajúce. Chí-kvadrát proti rovnomernému
A–Z je 180,63 pri 25 stupňoch voľnosti, nominálne p≈1,55×10⁻²⁵ v nezávislom rovnomernom
modeli. Pre reálne závislý text nie je toto p univerzálny test, ale jasne ukazuje,
že uniformita nie je vhodný opis. IC premiešaného textu musí zostať presne rovnaké;
nie je to ďalší dôkaz náhodnosti. Jediný autorsky zostavený nemecký kontrolný text
nie je reprezentatívny jazykový korpus ani dobový historický kontrolný materiál.

### Periodicita

Samostatne som kalibroval maximum štandardizovaného stĺpcového IC cez periódy 2–17
na 10000 permutáciách. Pre čítanie po blokoch vyšlo p_MC≈0,222; pri prekladaní riadkov
troch blokov p_MC≈0,101. Nenašiel sa presvedčivý nadbytok stĺpcových koincidencií
v týchto poradiach a periódach. Perióda 1 je základný IC, nie samostatný periodický signál.

Toto je negatívny výsledok jedného typu detektora. Nevylučuje všetky Vigenèrove varianty,
dlhšie kľúče, autokľúč, priebežný kľúč, reset kľúča na riadkoch alebo predchádzajúcu
transpozíciu. Pri perióde 17 má jeden stĺpec iba približne 34 znakov; sila testu závisí
od jazyka, kľúča, normalizácie a správneho poradia čítania. Nebol vykonaný nezávislý
korpusový test sily pre každú takúto alternatívu. Permutačný model navyše nezachováva
lokálne závislosti textu, preto jeho p-hodnoty nepredstavujú úplný test klávesnicového modelu.

### Model keyboard mashing nie je úspešne validovaný

Publikovaný náhodný pohyb s 68 % lokálnych krokov dáva v priemere asi 73 % susednosti
namiesto pozorovaných 52 %, asi 127 vzorov ABA namiesto 31 a inú bigramovú informáciu.
Zhoda IC a priemernej vzdialenosti nestačí. Model má tiež ručne volené obmedzenie
množiny cieľových klávesov a resetov; nejde o nezávislý historický model pisára.
Nesúlad nevyvracia mechanické ťahy: skôr naznačuje pohyb so smerovou zotrvačnosťou,
nie rovnomernú voľbu ľubovoľného suseda. Taký model však treba najprv overiť.

Pri ApEn je orientácia testu problematická: program testuje −ApEn, hoci pozorovaný
odhad 0,849 je vyšší než premiešaných 0,663. Krátke, riedko obsadené 2-/3-gramové
odhady majú silný výberový efekt; výsledok nie je možné používať ako ďalší dôkaz
nízkej entropie. Ani test rúk sám nedokazuje skutočnú techniku písania oboma rukami.

## 3. Hranice riadkov: reálny efekt, podmienená interpretácia

Na fotografii je záverečné `eet hgfmuzzaa` jeden fyzický riadok. Súbor ho rozdeľuje
na dva. Preto je po oprave 6/33 susedných prechodov cez hranice, nie 6/34.
Vnútri je 294/541. Zmena nemení základný obraz.

Pri nulovom modeli ľubovoľnej spoločnej fázy zalomenia celého zachovaného reťazca
majú iba 3 z 575 posunov tak málo susedných prechodov na hraniciach: podiel 0,00522.
Po vynechaní záverečnej samostatnej skupiny je to 10/563≈0,0178. Ide o podmienené
fázové testy s predpokladom stacionárneho toku a zvoleného poradia čítania.
Podporujú väzbu vzoru na riadkovú štruktúru, nie univerzálny dôkaz proti šifre.

Druhý kontrolný model zachová každému riadku jeho cyklické poradie a nezávisle
posúva začiatok riadka. Potom rozdiel vnútri/medzi riadkami vychádza bežne:
p_MC≈0,467. Tento model už predpokladá oddelené riadkové jednotky; preto sa ním
nedá rozhodnúť, či sú riadky pôvodné samostatné jednotky. Ukazuje však, že presné
začiatky a konce nie sú mimoriadne oproti náhodnému rozrezaniu tých istých cyklov.
Hranice teda nepodávajú samostatný dôkaz, že každý riadok zodpovedá jednému pohybu ruky.

## 4. Neisté glyfy

Prezrel som publikovanú fotografiu aj zväčšené výrezy. Na miestach i/f nevidno
jednoznačný dôkaz, ktorý by oprávňoval uzavrieť všetky tri čítania. Rozlíšenie podľa
háčika alebo bodky je citlivé na farbu, opotrebovanie a kvalitu kópie. Vo finálnej
skupine uprednostňujem m; zostáva to čítanie fotografie, nie originálu.

Vyskúšaných bolo všetkých 16 kombinácií troch i/f a jedného m/n, nie iba dvojica
„všetko prvé“ a „všetko druhé“. Výsledok: 300–302/574 = 52,26–52,61 % susednosti;
IC 0,048890–0,049271. Tieto štyri neistoty základný záver neovplyvňujú.
Jedna zmena znaku môže ovplyvniť najviac dva susedné páry. Na odstránenie približne
202 nadbytočných párov oproti referencii by aj pri ideálnom znižovaní bolo potrebné
zmeniť vyše sto pozícií; presná referencia sa pri takých zmenách tiež mení.
Tento hrubý odhad nie je dôkaz správnosti celého prepisu.

Čítanie sa nesmie vyberať podľa toho, ktoré dá vyššie klávesnicové skóre.
Nezávislý slepý prepis a fotografia originálu majú vyššiu dôkaznú hodnotu.

## 5. Šifrové a transpozičné alternatívy

| Hypotéza | Čo vysvetľuje a čo jej chýba |
|---|---|
| Čistá transpozícia bežnej nemčiny | Zachová presné frekvencie aj IC. Nemôže sama sploštiť monogramy. Náhodná transpozícia by lokálnu klávesnicovú geometriu spravidla narušila. Bez konkrétneho kľúča, ktorý dá jazyk a vysvetlí geometriu, je slabá. Špeciálna krátka predloha alebo zámerná konštrukcia nie sú logicky vylúčené. |
| Pevná monoalfabetická substitúcia, posun klávesov | Zachová IC a celý multiset frekvencií. Osobitne zvolený substitučný kľúč môže umiestniť časté dvojice na blízke klávesy, preto tvrdenie „žiadna substitúcia to nemôže vyprodukovať“ nie je platné. Pre tento dokument nemáme konkrétny taký kľúč a súvislý text. |
| Bežná polyalfabetická/strojová šifra | Môže znížiť IC; bez klávesnicovej konštrukcie nemá prirodzený dôvod zachovať také silné QWERTZ ťahy. Dáta ju robia málo presvedčivou, nie matematicky nemožnou. |
| Homofónna alebo smerová klávesnicová šifra, riadkový reset | Môže v princípe spájať nízke IC s geometriou. Chýba doložený dobový postup a kompaktný kľúč. Voľné dodatočné priraďovanie významov by bolo preučenie. |
| Klávesnicou generovaný kľúčový materiál | Realistická funkčná alternatíva: aj zlé kľúčové listy môžu vzniknúť mechanickým písaním. Vysvetľuje geometriu bez toho, aby dokument musel byť bezúčelný. Vyžaduje archívny kontext a súvisiaci materiál. Nie je to dôkaz kvalitného OTP. |
| Steganografia v smeroch, odskokoch či výberoch znakov | Logicky možná, ale bez vopred určeného extrakčného pravidla prakticky nefalsifikovateľná. Zatiaľ nie konkurenčné riešenie. |

Numerickú časť som použil iba ako kontextový podklad z repozitára a blogu, nie ako
nový nezávisle vykonaný numerický audit. Nemožno tvrdiť, že každý nomenklátor alebo
aditívny systém musí mať rovnomerné jednotlivé číslice. Neprítomnosť nuly oslabuje
model nezávislých rovnomerných desatinných číslic, nie všetky číselné kódy.
Zhoda nezvyčajných dĺžok 17/17/19/17 je dôvod na vopred určený test párovania,
nie na ľubovoľné skúšanie ASCII posunov. Úplné systematické rozlúštenie alebo
vylúčenie párovania písmen a číslic nie je výsledkom tohto auditu.

## 6. Testy s najväčším vplyvom na záver

1. **Originál a archívne okolie.** Získať celý list, rub, signatúru, sprievodné záznamy
   a vysvetlenie hlavičiek. Rozlíšenie správy, kľúčového listu a cvičného materiálu
   by zmenilo interpretáciu viac než ďalší všeobecný test náhodnosti.
2. **Slepý prepis a nezávislý kontrolný materiál.** Dvaja čitatelia bez informácie o
   klávesnicovej hypotéze; neistoty zmraziť pred ďalšou analýzou. Pridať viac skutočných
   nemeckých textov, známych šifier a ľudských klávesnicových ťahov rovnakej dĺžky.
3. **Predikcia odloženého bloku.** Na bloku 1 odhadnúť malý smerový model s resetom
   a bez resetu; parametre zmraziť; na blokoch 2–3 porovnať logaritmickú vierohodnosť,
   dĺžky smerových ťahov, ABA a reziduálnu štruktúru. Pozor na viditeľný rozdiel
   monogramov a skóre medzi blokmi. Dobrý výsledok by posilnil mechanický pôvod;
   organizované rezíduum by otvorilo šifrovú alternatívu.
4. **Obmedzený test prípadného kľúčového párovania.** Najprv určiť z archívneho rozloženia
   prípustné zarovnania a malý súbor historicky zmysluplných operácií. Vyžadovať jeden
   kľúč a súvislý jazyk vo viacerých riadkoch plus úspech na odložených pozíciách.
   Netestovať stovky voľných transformácií a následne nevyberať najlepšie útržky.

## Odporúčaná formulácia záveru issue

„Text vykazuje veľmi silné, voči prepisovým neistotám odolné závislosti zodpovedajúce
rozloženiu QWERTZ. Klávesnicou vytvorená sekvencia je momentálne najúspornejšie
vysvetlenie. Testy však neurčujú účel dokumentu a nevylučujú všetky šifrové alebo
kľúčové funkcie; najmä absencia periodického IC nie je všeobecným vylúčením šifier.“

## Zdroje a reprodukcia

- Issue: https://github.com/kjfriedo/ss-cryptogram-1944/issues/1
- Zdrojový program: https://github.com/kjfriedo/ss-cryptogram-1944/blob/1eac5795a712322331e76ba1b82f71291cf1ea48/analysis/randomness_tests.py
- Prepis: https://github.com/kjfriedo/ss-cryptogram-1944/blob/1eac5795a712322331e76ba1b82f71291cf1ea48/data/transcription.md
- Publikácia a fotografia: https://klausschmeh.net/who-can-decipher-this-message-from-world-war-ii/
- Obraz: https://klausschmeh.net/wp-content/uploads/2026/10/SS-Cryptogram.jpg

Rozbaľte balík, nainštalujte numpy a scipy, spustite `python3 independent_audit.py`.
Overený beh: Python 3, numpy 2.3.5, scipy 1.17.0. Pôvodný program v `analysis/`
potrebuje iba štandardnú knižnicu. Výsledky sú podmienené publikovaným prepisom;
nevznikol nový úplný diplomatický prepis ani historické overenie proveniencie.
