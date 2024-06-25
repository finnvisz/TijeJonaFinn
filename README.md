# TijeJonaFinn

Het is na lezen van de README duidelijk hoe de resultaten te reproduceren zijn, via een interface (command line), argumenten die meegegeven kunnen worden voor de verschillende functionaliteiten/algoritmen, of bijvoorbeeld een duidelijke uitleg welke file te runnen om welk resultaat te krijgen.

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

Om deze case beter te begrijpen zijn er twee "kaarten" waar een oplossing voor gevonden kan worden. Een kleine kaart (Holland), en een grote kaart (Nationaal). We raden aan om te beginnen met de kleine kaart, waar de oplossingsruimte kleiner is en je sneller resultaten ziet. Als je goed plan van aanpak hebt kun je door naar de grote kaart om je plan te toetsen.


# Vereisten

Deze codebase is geschreven in Python 3.10.12. Om aan de slag te gaan moeten eerst twee commando's worden gerunt. Ga in je terminal naar de rootmap van ons project, en volg de volgende instructies:

1. In requirements.txt staan alle benodigde packages om de code succesvol te runnen. Ook 'istalleer'je onze repository. Deze zijn gemakkelijk te installeren via pip met de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

# Aan de slag! 
## Experimentatie
Als je een idee wilt krijgen van hoe de voorbeeldruimte van dit probleem eruit ziet,
daarvoor kun je ons experimentgerichte algoritme gebruiken. Run het volgende:

```
python3 main1.py
```

We vergelijken een eenvoudig random algoritme, een eenvoudig greedy algoritme en een random algoritme + heuristiek om te zien hoeveel verschil een heuristiek kan maken. Een plot zou moeten openen in een pop-up, maar wordt ook opgeslagen als pdf naar 
```
parent/code/experiments/plots
```

## Autorun Hillclimber
Dit duurt ietjes langer, maar het is het waard! Run het volgende:
```
python3 main2.py
```
Nu run je het autorun_hillclimber programma met de projectnaam 'my_first_project'. # Laten we beginnen met 10 runs en de kleinere kaart: "Holland"
Zo zie je (relatief) snel de resultaten en krijg je gevoel voor het programma.

Nu je een autorun hillclimber project hebt, krijg je een samenvatting van je logfile met behulp van een plot. Ook worden de eindscores van je hillclimber geplot. Deze worden opgeslagen in je project directory. Als je hierheen gaat vind je een directory genaamd 'solutions'. Dit bevat de oplossing van elke run als een csv bestand. Neem eens een kijkje en zie hoe jouw beste oplossing eruit ziet!


## Manim
Run het volgende:
```
python3 main3.py
```

# Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/parent/code**: bevat alle code van dit project
  - **/parent/code/algorithms**: bevat de code voor algoritmes
  - **/parent/code/classes**: bevat de benodigde classes voor deze case. Dit is de "bodemlaag" van onze code, dus wellicht minder interessant voor een gebruiker.
  - **/parent/code/experiments** bevat code om te experimenteren en de verdeling van de oplossingsruimte beter te leren kennen
  - **/parent/code/visualisation**: bevat de manim code voor het visualiseren van een oplossing
  - **/parent/code/tests** bevat een aantal tests voor de code in ons project. Ik zou hier niet te lang blijven rondhangen, dat hebben wij ook niet gedaan.
- **/parent/data**: bevat de verschillende databestanden. Er zijn twee "kaarten": "Holland" en "Nationaal", met elk eigen stations.
- **/parent/docs**: bevat een schematische weergave van ons project, voor wat extra overzicht.

## Algoritmes
Wij hebben eigenlijk twee algoritmes geschreven, maar in beide zijn er veel argumenten te variëren of aan/uit te zetten.
### Random-Greedy
TODO

### Hillclimber
Om het Hillclimber-algoritme te gebruiken, volg je deze stappen:

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


## Experiments

## Visualisatie

# Auteurs
- Jona Aalten
- Finn Dokter
- Tije Schut
