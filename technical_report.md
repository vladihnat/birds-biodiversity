# Birds Biodiversity Technical report
LEIVA Martin (n°etu), PEÑA CASTAÑO Javier (n°etu), HERRERA NATIVI Vladimir (22205706)

It is to be seen if the final technical report will be written as an .md or a pdf

---
NOTE : 30/10/2025

### Next steps to take in consideration 

**Overview.md**\
first steps motivations :
- Check schema consistency with df.info() and df.head().
- Validate effort assumptions – confirm each transect has 10 points, look for sites with fewer than - 10 completed visits, and note detection modality distributions.
- Create orientation summaries – species richness by site, observer workload, yearly totals,   detection modality shares.

**Assignment.pdf**\
Goal :  To quantify how biodiversity indicatiors have evolved over time. With statistical uncertainity assessments, highlighting species-specific stories. 

Big points to treat : 
- Dataset Familiarisation and Descriptive Analysis : data structure, descriptive statistics 
- Multi-Year Indicator Trends : Select indicators, for each compute annual estimates, quantify and interpret temporal trends (maybe linear models)
- Species-Level Evolution  : choose subset of birds, for each specie analyse how its recorded presence have changed (CI), potential reasons ? 

---
## Initial approach, data discovery 
First problems encountered : Intial reading and separation of the raw data. 

| Sheet name | Problem in raw data |
|------------|---------------------|
| `ESPECES`  | The raw data sheet jumped the two first columns in the excel sheet, it had no headers and one single NaN on the last column |
| `GPS-MILIEU` | The raw data sheet jumped the two first columns, it had no prescence of NaNs. The headers were wrongly placed due to a double leveled header for geographical coordinates and last 3 columns didn't had headers.   |
| `NOM FRANÇAIS` | The original sheet had 26 columns but the last one was "hidden" (first values started a couple thounsand rows in). Headers were missplaced due to a triple and double leveled headers from columns 13 to 25 |

In order to correct this problems we proposed a 2 step solution, first we dropped the redundant columuns (in ESPECES ans GPS-MILIEU) and then we redefined the headers of the 3 sheets as listed next : 

| Sheet name | New headers |
|------------|---------------------|
| `ESPECES`  | "ESPECIES_NAME", "LATIN_NAME", "NATURE" |
| `GPS-MILIEU` |   "TRANSECT_NAME", "COORDINATE_X", "COORDINATE_Y", "HABITAT_TYPE","TRANSECT_ID", "POINT_ID",  |
| `NOM FRANÇAIS` | (Col 13 to 26) : "AL25", "VL25", "AL50", "VL50", "AL100", "VL100", "AG100", "VG100", "VOL", "TOT_A", "TOT_V_sV", "TOT_AV_sV", "TOT_AV_V", "COMPANIED", |

In the case of `NOM FRANÇAIS` only headers from columns 13 to 25 were changed following a patern that we stablished : \
For columns 13 to 20 (distances de contact) we stablished a 3 part code, the first letter (A or V) is for Auditif or Visuel, the second letter (L or G) is for "<" or ">" and finally the number corresponds to the distance in meters.\
For columns 22 to 25 (totaux) a simalar approach was used, the first section has one or two letters (A, V or AV) for "Auditif", "Visuel" or "A+V", the second sections has two different entries (sV or V) for "sans Vol" or "avec Vol"

**This new sheets were saved in "data/cleaned"**


---