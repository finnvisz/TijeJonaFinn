# RailNL

Een dienstregeling voor treinverkeer bestaat eigenlijk uit vier planningsonderdelen:

1. De lijnvoering: Wat zijn de trajecten waarover de treinen gedurende de dag heen en weer rijden?
2. De dienstregeling: hoe laat vertrekken de treinen van de stations over de trajecten?
3. Het materieelrooster: welk treinstel en welke wagons zijn op welk moment op welke plaats?
4. Het personeelsrooster: zijn alle treinen bemand door tenminste één bestuurder en twee conducteurs?

Deze case gaat over het eerste deel, het maken van de lijnvoering. Meer specifiek: over de lijnvoering van intercitytreinen. Dat betekent dat je binnen een gegeven tijdsframe een aantal trajecten uitzet. Een traject is een route van sporen en stations waarover treinen heen en weer rijden. Een traject mag niet langer zijn dan het opgegeven tijdsframe.

Voorbeeld: Het traject [Castricum , Zaandam , Hoorn , Alkmaar] is een traject met een duur van 59 minuten, en zou dus binnen het tijdseframe van een uur passen.

RailNL heeft recentelijk een doelfunctie opgesteld voor de kwaliteit van de lijnvoering. Als 100% van van de verbindingen bereden wordt, levert dat 10000 punten op je lijnvoering op, anders krijg je een een gedeelte daarvan. Maar hoe minder trajecten voor dezelfde service, hoe goedkoper. En in hoe minder tijd er in al die trajecten samen verbruikt wordt, hoe beter. Dus die factoren worden ook meegewogen in de doelfunctie:

```
K = p*10000 - (T*100 + Min)
```

Om deze case beter te begrijpen zijn er twee "kaarten" waar een oplossing voor gevonden kan worden. Een kleine kaart (Holland), en een grote kaart (Nationaal). We raden aan om te beginnen met de kleine kaart, waar de oplossingsruimte kleiner is en je sneller resultaten ziet. Als je een goed plan van aanpak hebt kun je door naar de grote kaart om je plan te toetsen.


# Vereisten

Deze codebase is geschreven in Python 3.10.12. Om aan de slag te gaan moeten eerst twee commando's worden gerunt. Ga in je terminal naar de rootmap van ons project, en volg de volgende instructies:

1. In requirements.txt staan alle benodigde packages om de code succesvol te runnen. Ook 'installeer' je onze repository met een editable install. Dit gaat allemaal via pip met de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

# Aan de slag
## Experimentatie
Als je een idee wilt krijgen van hoe de oplossingsruimte van dit probleem eruit ziet,
kun je daarvoor ons experimentgerichte algoritme gebruiken: `Random_Greedy`. We hebben een voorbeeldje klaargezet. Run het volgende:

```
python3 parent/main1.py
```

We vergelijken een eenvoudig random algoritme, een eenvoudig greedy algoritme en een random algoritme + heuristiek om te zien hoeveel verschil een heuristiek kan maken. Een plot zou moeten openen in een pop-up, maar wordt ook opgeslagen als pdf naar 
```
parent/code/experiments/plots/Heuristics matter: Random vs Greedy algorithm.pdf
```
Het interpreteren van de resultaten laten we aan de lezer, maar het moge duidelijk zijn dat wij heuristieken belangrijk vinden bij het oplossen van dit probleem.

## Autorun Hillclimber
> Dit duurt ietjes langer, maar het is het waard!

Om de beste oplossing te vinden voor ons probleem, hebben we een iteratief algoritme geïmplementeerd: de Hillclimber. Daarover later meer. We hebben met schade en schande geleerd welke instellingen optimale resultaten genereren, en vervolgens wilden we even achterover gaan zitten. Daarvoor is `autorun_hillclimber`. Deze functie runt het hillclimber algoritme met optimale instellingen automatisch N keer, en slaat de resultaten op in een door de gebruiker gekozen projectmap.

Run het volgende:
```
python3 parent/main2.py mijn_eerste_project
```
Nu run je het autorun_hillclimber programma met de projectnaam 'mijn_eerste_project'. Laten we beginnen met 10 runs en de kleinere kaart: "Holland". Elke run draait maar 600 iteraties (normaal doen we tot wel 600.000). Zo zie je snel de resultaten en krijg je gevoel voor het programma.

Als autorun_hillclimber klaar is, krijg je een samenvatting van je logfile met behulp van een plot. Ook worden de eindscores van je hillclimber geplot. Deze worden opgeslagen in je project directory:
```
parent/code/autorun_hillclimber/mijn_eerste_project/
```

Ook vind je hier een submap genaamd 'solutions'. Dit bevat de oplossing geproduceerd door elke run als een csv bestand. Neem eens een kijkje bij je project en zie hoe jouw beste oplossing eruit ziet!


## Manim
Alle visualisaties zijn gemaakt met de Mathematical Animation library Manim. 
Er zijn drie verschillende visualisaties voor zowel Holland als Nationaal. 
Er is een basale kaartvisualisatie, een video die een route visualiseert op de 
betreffende kaart, en ten slotte een afbeelding van de volledige route op de kaart.

### Requirements
Vanaf hier kan men de weg alleen vervolgen na het succesvol installeren van Manim.
Als het goed is heeft de lezer vanuit het requirements.txt bestand via bijvoorbeeld
pip Manim succesvol weten te installeren. Echter, er zijn bijkomende dependencies, die
per besturingssysteem verschillen. Deze moeten hier nog worden geinstalleerd. 
Please bear with us, de volgende link leidt je door de installatie van de dependencies 
heen. 

```
https://docs.manim.community/en/stable/installation.html#
```

De visualisaties lezen vanuit het bestand visualisation_settings.csv. Dit 
bestand bevat één regel tekst in de vorm: kaart,relatief_pad. De kaart is
Holland of Nationaal, en het relatieve pad wordt gegeven vanaf de code folder 
naar een csv output file van de vorm zoals vereist in de opdrachtomschrijving. 

Na het creeëren van een output file door het runnen van een experiment, moet je 
het script set_manim_settings.py aanroepen om visualisation_settings.csv te
overschrijven met de juiste settings. Bijvoorbeeld als volgt:

```
python3 set_manim_settings.py kaart relative_path_to_file/file.csv
```

Daarna kun je direct één van de drie visualisaties aanroepen op de door jou
ingestelde kaart en lijnvoering. Het makkelijkste is om de VSCode manim sideview
extension te downloaden. Alternatief kun je het ook gemakkelijk vanaf de 
commandline runnen als volgt. 

```
manim -pql script_to_animate.py class_to_animate
```

Run bijvoorbeeld het volgende script waarin we de route met de hoogst gevonden
score uit het voorgaande experiment visualiseren.

```
python3 parent/main3.py
```

Alle media die op deze manier wordt gegenereerd kan zolang niet overschreven, 
worden teruggevonden in de parent/code/visualisation/media folder.

# Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/parent/code**: bevat alle code van dit project
  - **/parent/code/algorithms**: bevat de code voor algoritmes
  - **/parent/code/autorun_hillclimber**: bevat autorun_hillclimber projecten + de autorun_hillclimber module zelf.
  - **/parent/code/classes**: bevat de benodigde classes voor deze case. Dit is de "bodemlaag" van onze code, dus wellicht minder interessant voor een gebruiker.
  - **/parent/code/experiments** bevat code om te experimenteren en de verdeling van de oplossingsruimte beter te leren kennen.
      - **plots** is de standaardmap voor plots van experimenten, wordt gebruikt door de `plot_scores` functie
      - **results** is de standaardmap voor resulaten van experimenten
  - **/parent/code/helpers** bevat allerlei overige hulpfuncties
  - **/parent/code/tests** bevat een aantal tests voor de code in ons project. Ik zou hier niet te lang blijven rondhangen, dat hebben wij ook niet gedaan.
  - **/parent/code/visualisation**: bevat de manim code voor het visualiseren van een oplossing
    - **media** is de output map voor manim visualisaties
  
- **/parent/data**: bevat de verschillende databestanden. Er zijn twee "kaarten": "Holland" en "Nationaal", met elk eigen stations.
- **/parent/docs**: bevat een schematische weergave van ons project, voor wat extra overzicht.

# Extra uitleg per onderdeel

## Algoritmes
Wij hebben eigenlijk twee algoritmes geschreven, maar in beide zijn er veel argumenten te variëren of aan/uit te zetten.
### Random_Greedy
Het Random_Greedy algoritme is onze experimenten-toolbox. Afhankelijk van de opties die je kiest is hij random, greedy, anderszijds deterministisch of iets ertussenin. Je kunt verschillende varianten van het algoritme runnen door de parameters van de run-method aan te passen.

Het runnen van Random_Greedy gaat in twee stappen:

1. Initialiseer het algoritme 

### Hillclimber
Om het Hillclimber-algoritme zelf met de hand te runnen, volg je deze stappen:

1. Zorg er eerst voor dat je een lijst routes hebt. Je kan deze óf zelf met de hand maken, óf het Random-Greedy algoritme eerst uitvoeren en daar de output van nemen (run):
```
start_routes = Random_Greedy(maprange).run(
                            starting_stations="fully_random",
                            final_number_of_routes = 20,
                            route_time_limit = 180)
```

2. Initialiseer het Algoritme: Initialiseer het Hillclimber-object met een set startposities en de gewenste kaart ("Holland" of "Nationaal"). In dit geval Nationaal:

```
hillclimber = Hillclimber(start_position=start_routes, maprange="Nationaal")
```
3. Voer het Hillclimber-algoritme uit voor een gespecificeerd aantal iteraties:
```
optimized_routes = hillclimber.run(iterations=1000)
```
4. Sla de resultaten op in een CSV-bestand. Gebruik hiervoor de functie write_solution_to_csv en geef als eerste argument de routes, dus in dit geval optimized_routes, en als tweede argument de filename van je CSV-bestand (mag je zelf kiezen):
```
write_solution_to_csv(optimized_routes, "optimized_routes.csv")
```

Er zijn parameters voor de hillclimber die je kan veranderen in de run-methode:
1. simulated-annealing: De run-methode heeft een optie voor simulated annealing, waarmee het algoritme soms slechtere scores accepteert om lokale optima te vermijden. Deze staat standaard uit.
2. improve_routes: Als de parameter improve_routes aan staat, verwijdert hij elke iteratie overbodige verbindingen binnen een route. Deze staat standaard aan.
3. only_original: De parameter original_connections_only zorgt ervoor dat een route nooit dezelfde verbinding meer dan één keer gebruikt. Deze staat standaard uit.

Voor meer details, raadpleeg de documentatie en het commentaar binnen de klasse-definitie.

## Autorun voor Hillclimber

### In het kort
Deze functie is bewust zo simpel mogelijk gehouden. Het idee is dat Hillclimber al perfect is afgesteld, dus de instellingen van het algoritme zelf zijn allemaal niet toegankelijk voor de gebruiker van autorun_hillclimber. In de basis werkt het zo:

De gebruiker kiest een aantal runs, projectnaam en map. Vervolgens maakt autorun_hillclimber een projectmap in `parent/code/autorun_hillclimber`, waar alle gegenereerde oplossingen worden opgeslagen. De functie runt het Hillclimber algoritme zo vaak als opgegeven en bewaart zoveel mogelijk data voor latere analyse. Jij kan even wat anders gaan doen.

### Argumenten
Er zijn 4 argumenten:

- `n_runs`: Het aantal keer dat Hillclimber moet worden gerunt.
- `project_name`: Projectnaam om gegenereerde data in op te slaan.
- `maprange`: Kaart om het algoritme op te runnen ("Holland" of "Nationaal"). Default is "Holland"
- `allow_overwrite`: Standaard is het niet toegestaan om een projectnaam te kiezen die al in gebruik is, om het overschrijven / mixen van resultaten te voorkomen. Als je `allow_overwrite` op `True` zet is het kiezen van een bestaande projectnaam wel toegestaan, en worden nieuwe resultaten toegevoegd aan dit bestaande project.

### Over de data

Er worden 3 dingen bijgehouden:

- In **solutions** wordt elke gegenereerd oplossing opgeslagen met een duidelijke naam.
- Er wordt een logbestand bijgehouden, waar elke kolom een run is en elke rij een iteratie binnen die run. 
- Eindscores worden ook in een apart csv-bestand opgeslagen. 

Het logbestand en de eindscores kunnen worden geplot met speciale functies (`logplot_autorun_hillclimber`, `plot_endscores_autorun_hillclimber`). Deze functies worden in meer detail beschreven in **Helpers -> plots**, verderop in deze README. Oplossingen kunnen worden gevisualiseerd met manim.

 ### Extra: zelf sleutelen aan het algoritme
 Wil je wel sleutelen aan de versie van Hillclimber die gebruikt wordt door autorun_hillclimber? Ga dan naar `parent/code/autorun_hillclimber/autorun_hillclimber.py`. Helemaal bovenaan staat de subfunctie `run_hillclimber`. Hier initialiseert het Random_Greedy algoritme een startstaat met onze parameters, die wordt doorgegeven aan Hillclimber. Vervolgens wordt Hillclimber zelf gerunt met door ons ingestelde parameters. Als je wil sleutelen onder de motorkap kan dat in deze subfunctie.

## Experiments
In de map experiments zitten drie python bestanden. 

### Experiment
Dit is een klasse. Gegeven een algoritme en de kaart ("Holland" of "Nationaal) kan je een algoritme een aantal keer runnen. Elke run berekent het de score van de lijnvoering. Daarna berekent het meteen de gemiddelde score en geeft het een lijst met alle scores aan je terug.

### Starting bins
Ook dit is een klasse. De Sort_Starting klasse is ontworpen om een verzameling stations te sorteren op basis van hun connectiviteit. Deze klasse maakt gebruik van combinaties van stations en verdeelt deze in bins (bakken) afhankelijk van hun connectiviteitsgraad. Hiermee probeerden we verschillende startstations te vergelijken voor Random_Greedy, maar hier is uiteindelijk geen concrete heuristiek uitgekomen.

## Helpers
Deze map bevat een verzameling functies voor het verwerken, opslaan, lezen en visualiseren van zowel scores als oplossingen gegenereerd door verschillende algoritmen. Hier volgt een korte uitleg van de belangrijkste modules:

### csv_helpers
1. `write_scores_to_csv`:
Schrijft een numpy array met scores naar een CSV-bestand.

2. `read_scores_from_csv`:
Leest scores van een CSV-bestand en retourneert deze als een numpy array.

3. `append_scores_to_csv`:
Voegt een numpy array met scores toe aan een bestaand CSV-bestand als een nieuwe kolom.

4. `append_single_score_to_csv`:
Voegt een enkele score toe aan een bestaand CSV-bestand als een nieuwe rij.

5. `write_solution_to_csv`:
Schrijft een lijst van Route-objecten naar een CSV-bestand.

6. `read_solution_from_csv`:
Leest een oplossing voor het RailNL-probleem van een CSV-bestand en geeft een lijst van Route-objecten.

### statistics
1. `calculate_p_value`:
Berekent de p-waarde om te bepalen of het verschil tussen twee sets scores significant is.

### plots
1. `plot_scores`:
Maakt een histogram van de scores van 1 tot 4 samples.

2. `logplot_autorun_hillclimber`:
Maakt een plot om een autorun_hillclimber logbestand samen te vatten.

### score
1. `calculate_score`:
Berekent de score gegeven een lijst routes en en de kaartnaam. ("Holland" of "Nationaal")

### statistics
1. `calculate_p_value`:
Berekent de p-waarde om te bepalen of het verschil tussen twee sets scores significant is.

### tot_con_used
Maakt, gegeven een lijst routes, een set met daarin alle connecties die gebruikt zijn. Hierin komen alle connecties maximaal één keer voor. Dus bijvoorbeeld als Alkmaar-Den Helder al in de set zit, komt Den Helder-Alkmaar er niet meer bij.

## Visualisatie

### visualisation_settings
Dit is een miniscuul csv bestand wat enkel een kaart: Holland of Nationaal,
en een pad vanaf de code folder naar een output csv bestand bevat. Dit 
output csv bestand bevat een lijnvoering geformat zoals door de opdracht
op de proglab website gespecifiëerd. 

### set_manin_settings
Dit is een klein script om de visualisation_settings vanaf de command line
te kunnen aanpassen na het runnen van een experiment.

### map_visualisation

Map visualisation is een manim Scene klasse en creëert een video preview 
van de kaart gespecifiëerd in visualisation_settings.

### route_visualisation
Route visualisation is een manim Scene klasse en creëert een video visualisatie
van een kaart met lijnvoering gespecifiëerd in visualisation_settings

### route_visualisation_image
Route visualisation image is ook een manim Scene klasse maar creëert een
afbeelding van een kaart met lijnvoering gespecifiëerd in visualisation_settings.

# Auteurs
- Jona Aalten
- Finn Dokter
- Tije Schut
