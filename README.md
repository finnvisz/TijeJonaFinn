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
score uit het voorgaande experiment mijn_eerste_project runnen.

```
python3 parent/main3.py
```

# Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/parent/code**: bevat alle code van dit project
  - **/parent/code/algorithms**: bevat de code voor algoritmes
  - **/parent/code/autorun_hillclimber**: bevat autorun_hillclimber projecten + de autorun_hillclimber module zelf.
  - **/parent/code/classes**: bevat de benodigde classes voor deze case. Dit is de "bodemlaag" van onze code, dus wellicht minder interessant voor een gebruiker.
  - **/parent/code/experiments** bevat code om te experimenteren en de verdeling van de oplossingsruimte beter te leren kennen.
      - **plots** is de standaardmap voor plots van experimenten, wordt gebruikt door de `plot_scores` functie
      - **results** is de standaardmap voor resulaten van experimenten
      - **solutions** is de standaardmap voor opgeslagen oplossingen 
  - **/parent/code/helpers** bevat allerlei overige hulpfuncties
  - **/parent/code/tests** bevat een aantal tests voor de code in ons project. Ik zou hier niet te lang blijven rondhangen, dat hebben wij ook niet gedaan.
  - **/parent/code/visualisation**: bevat de manim code voor het visualiseren van een oplossing
    - **media** is de output map voor manim visualisaties
  
- **/parent/data**: bevat de verschillende databestanden. Er zijn twee "kaarten": "Holland" en "Nationaal", met elk eigen stations.
- **/parent/docs**: bevat een schematische weergave van ons project, voor wat extra overzicht.

# Extra uitleg per onderdeel

## Algoritmes
Wij hebben twee algoritmes geschreven, in beide zijn er veel argumenten te variëren of aan/uit te zetten.

### Random_Greedy
Het Random_Greedy algoritme is onze experimenten-toolbox. Afhankelijk van de opties die je kiest is hij random, greedy, anderszijds deterministisch of iets ertussenin. Je kunt verschillende varianten van het algoritme runnen door de parameters van de run-method aan te passen.

Het runnen van Random_Greedy gaat als volgt:

1. Initialiseer het algoritme met de gewenste kaart (`maprange`; default is "Holland", anders "Nationaal"):
```
from parent.code.algorithms.random_greedy import Random_Greedy

random_greedy = Random_Greedy("Holland")
```

2. Run het algoritme met gewenste parameters (dit zijn er een hoop; voorbeeld is heuristiek die we als Hillclimber start state gebruiken voor Holland):
```
solution = random_greedy.run(starting_stations = "original_stations_only_hard", final_number_of_routes = 4)
```

3. Sla de gegenereerde oplossing op
```
from parent.code.helpers.csv_helpers import write_solution_to_csv

write_solution_to_csv(solution, filename = "Random_Greedy_solution_1.csv", map = "Holland")
```

4. De oplossing staat nu in `parent/code/experiments/solutions`. 

> De run method bevat nog veel meer opties, die uitgebreid beschreven staan in de docstring van de method. 

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


## Experiments
In de map experiments zitten twee classes. Ook staan hier submappen voor output van functies: **plots**, **results** en **solutions**. Het algemene idee is om verschillende instellingen voor het Random_Greedy algoritme met elkaar te vergelijken en bruikbare heuristieken te vinden.

### Experiment class
Deze class is gemaakt om experimenten te runnen met het Random_Greedy algoritme. Gegeven een algoritme en de kaart ("Holland" of "Nationaal) kan je een algoritme een aantal keer runnen. Elke run berekent het de score van de oplossing. Daarna geeft het een lijst met alle scores aan je terug, die je kunt opslaan naar **results** of meteen kunt plotten.

1. Initialiseer de Experiment class
```
from parent.code.experiments.experiment import Experiment

experiment = Experiment("Holland")
```
2. Run het Random_Greedy algoritme N keer met de opgegeven parameters (alles na argument 1 wordt doorgegeven als kwargs)
```
results = experiment.run_experiment(1000, next_connection_choice = "random", starting_stations = "original_stations_only_hard")
```
3. Sla je resultaten op naar CSV
  
  - a. Sla op naar CSV (doelmap: **experiments/results**)
```
from parent.code.helpers.csv_helpers import write_scores_to_csv

write_scores_to_csv(results, filename = "1000_mijn_eerste_experiment")
```
   - b. Plot resultaten meteen (doelmap: **experiments/plots**)
```
from parent.code.helpers.plots import plot_scores

plot_scores(results, title = "1000_mijn_eerste_experiment", save_to_pdf = True)
```

### Starting bins
Ook dit is een klasse. De Sort_Starting klasse is ontworpen om een verzameling stations te sorteren op basis van hun connectiviteit. Deze klasse maakt gebruik van combinaties van stations en verdeelt deze in bins (bakken) afhankelijk van hun connectiviteitsgraad. Hiermee probeerden we verschillende startstations te vergelijken voor Random_Greedy, maar hier is uiteindelijk geen concrete heuristiek uitgekomen.


## Autorun voor Hillclimber
TODO (Jona)

## Helpers
Deze map bevat een verzameling functies voor het verwerken, opslaan, lezen en visualiseren van zowel scores als oplossingen gegenereerd door verschillende algoritmen. Hier volgt een korte uitleg van de belangrijkste modules:

### autorun_hillclimber_helpers
TODO (Jona)

### csv_helpers
1. write_scores_to_csv
Schrijft een numpy array met scores naar een CSV-bestand.

2. read_scores_from_csv
Leest scores van een CSV-bestand en retourneert deze als een numpy array.

3. append_scores_to_csv
Voegt een numpy array met scores toe aan een bestaand CSV-bestand als een nieuwe kolom.

4. append_single_score_to_csv
Voegt een enkele score toe aan een bestaand CSV-bestand als een nieuwe rij.

5. write_solution_to_csv
Schrijft een lijst van Route-objecten naar een CSV-bestand.

6. read_solution_from_csv
Leest een oplossing voor het RailNL-probleem van een CSV-bestand en geeft een lijst van Route-objecten.


### plots
1. plot_scores
Maakt een histogram van de scores van 1 tot 4 samples.

2. logplot_autorun_hillclimber
Maakt een plot om een autorun_hillclimber logbestand samen te vatten.

### score
Berekent de score gegeven een lijst routes en en de kaartnaam. ("Holland" of "Nationaal")

### statistics
1. calculate_p_value
Berekent de p-waarde om te bepalen of het verschil tussen twee sets scores significant is.

### tot_con_used
Maakt, gegeven een lijst routes, een set met daarin alle connecties die gebruikt zijn. Hierin komen alle connecties maximaal één keer voor. Dus bijvoorbeeld als Alkmaar-Den Helder al in de set zit, komt Den Helder-Alkmaar er niet meer bij.

## Visualisatie

# Auteurs
- Jona Aalten
- Finn Dokter
- Tije Schut
