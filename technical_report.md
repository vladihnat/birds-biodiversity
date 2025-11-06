# Birds Biodiversity Technical report
LEIVA Martin (22205863), PEÑA CASTAÑO Javier (22203616), HERRERA NATIVI Vladimir (22205706)

---

## 1. Dataset Familiarisation and Descriptive Analysis 

- **Cleaning** : Talk about all the incoherences, initial problems and how we treat them in utils.py 
- **Familarisation** : Quick glance at all the initial statistical analysis (one for each of the 3 intial tabs) and give first key insights

Here we can explain the dropped columns and the new headers names, ...

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
For columns 22 to 25 (totaux) a simalar approach was used, the first section has one or two letters (A, V or AV) for "Auditif", "Visuel" or "A+V", the second sections has two different entries (sV or V) for "sans Vol" or "avec Vol".
For this study, we defined the total number of birds per record using `TOT_AV_sV`(auditory + visual counts of non-flying birds). We excluded `TOT_AV_V` (= `TOT_AV_sV` + `vol`), because we found the meaning of `vol` unclear: many rows had non-NaN values in it despite showing no detected birds in the `distances de contact` fields, which we found inconsistent.

**This new sheets were saved in "data/cleaned"**

## Descriptive Analysis

After cleaning the data, we got the following shapes for each of the 3 sheets:
1. `Especes`: (87, 4)
2. `GPS`: (650, 6)
3. `Nom Français`: (114496, 26)

### Especies 

Out of the 87 species, we found 86 unique species (french and latin names), with the only duplicated one being the `Astrid ondulé` (french) or `Estrilda astrild` (latin). 

Then, we created two dataFrames where we grouped each species by family along with the corresponding number of species. Birds of the same family were defined as having the same first word of `ESPECIES_NAME` and `LATIN_NAME`. This resulted in the following dataframes:

1. `ESPECIES_FAMILY` with 53 families
2. `LATIN_FAMILY` with 71 families

For `french families`, more than half the families have a unique species, while the rest is distributed between $2$, $3$ and $4$ species.  
For `latin families`, almost $60$ families have $1$ unique species, while the rest is distributed in-between $2$ to $4$. 

Finally, we found $9$ different natures of bird, with `migrateur` being the more present (24 species) , and `Migrateur rare` (1 species) being the least one.

### GPS-MILIEU 

In this dataFrame, there are $7$ distincts types of habitat:

1. `Forêt sèche`: $19$ unique transects
2. `Agricole`: $14$ unique transects
3. `Forêt humid`: $13$ unique transects
4. `Périurbain`: $12$ unique transects
5. `Mangrove`: $3$ unique transects
6. `Plage`: $3$ unique transects
7. `Urbain`: $2$ unique transects

### Nom_Français

In this data, the number of observations rise from 2014 to 2016, dip slightly in 2017 and then mantain a rather stable plateau until 2025.

As well, it can be seen that the most present observer is `CONDE Beatriz`, with 41345 observations in 12 years, far ahead of the second place, `BAUAUD Anthony` with 8719 observations in 10 years.

The top 10 most observed transects are:

1. `Morne Babet`: 2878 transects
2. `Habitation Petite Rivière`: 2821 transects
3. `Moulin à Vent`: 2792 transects
4. `Là-Haut`: 2383 transects
5. `Hotêl des Plaisirs`: 2366 transects
6. `Autre Bord`: 2334 transects
7. `Borelie`: 2287 transects
8. `Fond Rousseau`: 2253 transects
9. `Jeannot`: 2222 transects
10. `O'Mullane`: 2203 transects

The top 10 most observed species over the years are: `Sucrier à ventre jaune`, `Elénie siffleuse`, `Sporophile rougegorge`, `Tourterelle à queue carrée`, `Quiscale merle`, `Tyran gris`, `Saltator gros-bec`, `Sporophile cici`, `Viréo à moustaches` and `Merle à lunettes`.

The top 10 most observed families over the years are: `Sporophile`, `Sucrier`, `Tourterelle`, `Elénie`, `Quiscale`, `Tyran`, `Saltator`, `Viréo`, `Merle`, `Moqueur`.


___


## 2. Multi-Year Indicator Trends

### Density Study - Summary of Computations

The density indicator measures the relative abundance of birds observed per transect and year.

  
First of all, from the cleaned observation dataset (`nom_francais_clean`), we aggregated total bird counts by `(year, transect)` using column `TOT_V_sV`.

Secondly each transect’s annual count was normalized by the maximum count observed across all years:

$$ 
\text{density\_norm}_{i,t} = \frac{\text{count}_{i,t}}{\max(\text{count}_{\text{all years}})}
$$
Densities are thus scaled to the range [0, 1].

After that, we used a bootstrap resampling method to estimate uncertainty:

1. For each year, resample transects with replacement \( B \) times (e.g. \( B = 1000 \)).
2. Compute the mean normalized density for each resample.
3. Obtain 95% confidence intervals from the empirical quantiles of the bootstrap distribution.

$$ 
\text{CI}_{95\%} = [\hat{\theta}^*_{2.5\%}, \hat{\theta}^*_{97.5\%}]
$$

For a better understanding of the computed results, we did some plots:
- Annual mean normalized density computed and plotted over time.  
- Per-year density distribution visualized by transect (color-coded).  
- Temporal evolution of normalized densities visualized across transects.  
- Bootstrap mean and confidence intervals plotted for density trends.
  
#### Interpretation

The density analysis provides a standardized way to compare bird abundance across years by accounting for variation in sampling effort. The first density plots reveal clear differences in abundance between transects all over the years, reflecting variations in the environment and how well each habitat supports species. When examining annual mean densities, we observe temporal fluctuations that suggest movements in overall bird activity from year to year.

The bootstrap procedure adds statistical rigor by quantifying uncertainty around the estimated yearly densities. The confidence intervals show how stable these density estimates are over time. Smaller intervals indicate consistent sampling responses across transects, while wider intervals suggest a bigger variability in bird presence.

Since 2018, the transect **Fort de France Centre Ville** consistently emerges as the most densely sampled and bird-rich zone, showing the highest normalized densities in the period 2018–2025. This pattern likely reflects a combination of favorable urban habitats, consistent observer effort, and possibly higher detectability of certain species in this area. 

Taken together, the density plots and bootstrap confidence intervals analysis provide complementary evidence that allows us to evaluate not only the magnitude of density changes but also their reliability and ecological relevance. This integrated approach helps distinguish true shifts in bird community activity such as the consistently high urban density observed at **Fort de France Centre Ville** from random sampling fluctuation.

---

### Species Diversity Study


We choose the species diversty as an informative indicator because it ummarizes not only **how** many species are present (richness) but also **how they are distributed** across individuals (evenness). Consequently, computing the evolution of the diversity through time is informative because:

- it portraits changes in community/population structure

- it’s less sensitive than raw abundance to observers effort spikes limited to a few common species

Thus, we decided to use 3 indices to capture different facets of diversity, the indeces used are ***Shannon, Simpson and Richness***, let's define them :

For the following measures we consider $p_i$ to be : 

$p_i = \frac{abundannce_i}{total}$ per year, computed from ```TOT_AV_sV```

- **Richness** (number of species observed) :\
pure count, easy to interpret, but doesn’t weight by abundance (rare and common species contribute equally).

- **Shannon** :\
$H' = -\sum_i p_i ln(p_i)$, where $p_i$ is the proportion of the entire community made up of species *i*. The higher the value of H, the higher the diversity of species in a particular community. The lower the value of H, the lower the diversity. A value of H = 0 indicates a community that only has one species.

- **Simpson** :\
$1-D$, where $D = \sum_i p_i^2$
The Simpson's Diversity Index is a measure of diversity which takes into account the number of species present, as well as the relative abundance of each species. As species richness and evenness increase, so diversity increases. It emphasizes dominance/evenness; less influenced by rare species than Shannon.\
A community dominated by one or two species is considered to be less diverse than one in which several different species have a similar abundance.


Using all three avoids over-reliance on a single definition and lets us diagnose whether changes are driven by **appearance of more species** (richness) or by **more even communities** (Shannon/Simpson).



Finally for each indicator we fitted a linear model in the following way : 
$\text{Indicator}_t = \beta_0 + \beta_1 \cdot \text{year}_t + \epsilon_t$

This gives a simple, interpretable slope ($\beta$) = *average annual change* in the indicator over 2014–2025. With 12 annual points, a linear model is a defensible first-order summary. We report the slope, its p-value, and R². Thus the linear slope shows a clear effect size (e.g., per decade change).

#### Interpretation 
Shannon shows a small, near-significant positive trend. Over a decade this is $\approx +0.062$ units, consistent with slightly more even communities and/or modest richness gains. Given the p-value just above 0.05, we describe this indicator as **weak evidence** of increase; bootstrap CIs in the plots provide complementary uncertainty.

For the Simpson's the slope is positive $\beta_1 \approx +0.0009 $ and and the p-value significant ($\approx 0.001$), it indicates increasing evenness (less dominance). 

Contrarily, the Richness indicator gave us a slope $\approx 0$ per year and a p-value = 1.0, thus we conclude that there is no linear trend in the number of species detected per year, combined with the near-increase in Shannon, this suggests community balance (evenness) changed slightly rather than the sheer count of species.

---

### Detectability Study (auditory V.S. visual)

#### Introduction

For this sampling indicator, we wanted to see how many of the detections were visual/auditory per year, for the top five of most visited transects (for more reliable data).

To analyse if this indicator was informative, we first plotted some initial histograms, where we observed that for some transects there seemed to be an increase in the ratio of auditory observations. In order to confirm this trend, we decided to further research this topic.

To count the needed values for this, we used the cleaned observation dataset `nom_francais_clean`. 

#### Computations

Total auditory/visual bird counts were aggregated by `(year, transect)` adding the data from column `TOT_AV_sV`, while the individual auditory and visual totals were extracted from the columns `TOT_A` and `TOT_V_sV` respetively.  

To calculate the percentage of observed audio shares, we did:
$$
\widehat{p}_{y,t}=\frac{A_{y,t}}{AV_{y,t}},\qquad \text{Auditory (in \%)}=100\times \widehat{p}_{y,t}
$$
where $A_{y,t}=\text{auditory detections}$, $V_{y, t} = \text{visual detections}$ and $AV_{y,t} = A_{y,t} + V_{y,t}$ for each year $y$ at transect $t$.

To trace the confidence intervals for the observed shares, we used the Wilson method, because classic "Wald" Confidence Intervalls perform poorly with small $n$ or extreme $p$ (bounds can leave [0, 1]). 
Instead, Wilson score intervals have better coverage and stay in [0, 1], which matters because if we increase the number of transects, the $\text{year} \times \text{transect}$ might have modest totals.

The formula used for $95\%$ CI is:
Let $z = 1.96$, $\widehat{p} = \frac{A_{y,t}}{AV_{y,t}}$. 

$$
\text{CI}_{\text{Wilson}} = \frac{\widehat{p} + \frac{z^2}{2n} \pm z\sqrt{\frac{\widehat{p}(1 - \widehat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}
$$

In the code, this is calculated by the imported function `statsmodels.stats.proportion.proportion_confint(method="wilson")`, then we multiply it by 100 to get the percentage.

Then, to interpret the slope and temporal trend, we used a **Binomial Generalized Linear Model**. This model is useful for this study, because the share of auditory detections is a proportion (each value comes from a count of auditory detections out of a total number of detections), so it follows a binomial distribution. Also, a GLM with a binomial family and a logit link models how the probability of an auditory detection changes with time (year), while taking into account that the years with more detections provide more reliable estimates. 

$$
\text{logit}(\text{Pr}[\text{auditory}|y,t]) = \beta_0 + \beta_1 (y - \widehat{y})
$$

With:
1. $\beta_0$: intercept
2. $\beta_1$: slope on year
3. $(y-\hat y)$: centered year

To calculate the p_value $p$ of each transect, we are going to do the following computations:

$$
z = \frac{\hat \beta_1}{\text{SE}(\hat \beta_1)d},\qquad p=2(1 - \phi(|z|))
$$

Where $\phi(\cdot)$ is the standard normal CDF.

#### Conclusion

After tracing these figures, with their corresponding CIs, p_values and slopes, we can see that for: 
1. Morne Babet:  $p = 1.32 \times 10^{-6} \implies$ p_value much smaller than $0.05$. The trend is highly significant and there is a strong and steady increase in the proportion of auditory detections over time.
2. Habitation Petit Rivière: $p = 1.8 \times 10^{-9} \implies$ similar interpretation as in Morne Babet.
3. Moulin à Vent: $p = 0.000369 \implies$ p_value is smaller than $0.05$. The trend is signicant and although there is more variability across the years, the fitted line still shows a positive slope.
4. Là-Haut: $p = 0.723 \implies$ p_value is much bigger than $0.05$. The trend is not significant and the percentage of auditory observations remains roughly constant over time.
5. Hôtel des Plaisirs: $p = 0.259 \implies$ p_value is bigger than $0.05$. Although the slope is slightly positive, uncertainty is large, so we cannot conclude an increase in auditory share.

Overall, the results point to different conclusions depending of each one of the top five most visited transects:  `(Morne Babet, Habitation Petit Rivière, and Moulin à Vent)` have a proportion of auditory detections that rises significantly over time, whereas `(Là-Haut and Hôtel des Plaisirs)` have no statistically detectable trend. The significant cases show consistent positive slopes, supported by narrow CIs and GLM p_values much smaller than $0.05$, that indicates that the increase is unlikely to be due to chance. On the other hand, the two non-significant transects show a wider uncertainty and flat fitted lines, suggesting stability in the percentage of auditory observations. Taken together, these findings imply that changes in detectability are not uniform across space.

---

### Spatial Coverage Study (Not interesting)

#### Summary

Initially, we analysed the spatial coverage, in order to see if it was an informative sampling indicator. We used the cleaned observation dataset `nom_francais_clean` and grouped for each year, the following attributes:
1. The distinct transects that were surveyed
2. The total point-visits that were recorded (row count)

Afterwards, we defined a new column `combo`, which contains each unique combination of (transect, point, n° pass) in order to count how many of such combos were actually observed, and divide them by a theoretical maximum: number of transects that year $\times$ 10 points $\times$ 2 passes (given maximal passes). This yields the `combo_coverage` metric per year.

At the end, we have tree different figures:
1. `Transects sampled per year`: how many distinct transects were visited each year
2. `Point-pass coverage ratio per year`: the ratio of possible (point, pass) combos were actually observed, aggregated at the year level.
3. `Coverage heatmap`: for the top 15 transects, the counts of unique (point, pass) combos per year, showing which transects were thouroughly sampled and when.

#### Analysis

Let's analyse each of those figures:

1) **Transects sampled per year** : 
Early years show fewer transects visited (around 41 in 2014), then a ramp-up through 2018 (around 65) and a rather stable plateau afterward (mostly between 62–65). So spatial coverage by number of transects expanded fast and then stabilized.

2) **Point–pass coverage ratio per year** :
Although the line looks dramatic at first, the y-axis is very tight: from around 0.91 to 1.00. The only clear drop is between 2019 and 2020, and after that, the coverage rebounds to around 0.99 and remains high. These graph shows there is a near-complete coverage most years, with 2020 as the outlier.

3) **Coverage heatmap (unique point×pass combos by transect–year, top-15 transects)**:
 On the first few years, we can see some gaps (Borelie, Boucle du Vauclin) and then some isolated holes (Hôtel des Plaisirs around 2018–2019). Besides those, cells are almost always at the maximum (around 20 combos), which indicates a full pointxpass combo after 2016.

Overall, with the three figures, we can observe that there is a big increase in spatial coverage in the first years, followed by a stable coverage from 2018 onward. This sampling indicator looks strong and steady after the initial ramp-up, so besides the 2020 dip and a few early gaps, we decided that there wasn't much added value in further analyzing this indicator.

---

## 3. Species-Level Evolution

We focused on the top 5 most observed bird species to highlight the core contributors to overall abundance and to simplify interpretation.
These species account for a large proportion of total observations, ensuring that trends reflect meaningful ecological signals rather than noise from rare or sporadically detected species.

### Abundance Evolution Study 

We used mean abundance instead of total number counted per year because:

 - Sampling effort changes across years (number of transects visited, observers present, duration, weather conditions, etc.).
 - The total number of birds counted is therefore not directly comparable from year to year.

But the mean abundance standardizes for effort, making trends fair and comparable.

#### Trend Significance per Species

For all this species except "Quiscale merle" , the slope is > 0 , so species abundance is increasing over time, but the only significant values are for "Elénie siffleuse" and 	"Tourterelle à queue carrée". "Quiscale merle" has also a significant negative value, so could suppose that the abundance is decreasing over the time, but the p-value is quite high. This suggests a possible decline, but evidence is weak. By looking at p-value (< 0.05), we can say that trend is statistically significant for "Elénie siffleuse" and "Tourterelle à queue carrée".

#### Interpretation of Species-Specific Abundance Trends

The figures display the temporal evolution of abundance for the five most frequently recorded bird species in the dataset, using the standardized mean abundance (TOT_AV_sV) per year and associated confidenc intervals estimated via bootstrap resampling. For **Élenie siffleuse**, the annual mean abundance shows a generally increasing pattern over the study period, and the fitted linear trend is positive with confidence intervals that do not overlap heavily with zero, indicating a statistically supported rise in abundance. This rise is also support by a p-value below 0.05. A similar positive and statistically significant trend is observed for **Tourterelle à queue carrée**, where the slope, the p-value and the bootstrap confidence intervals suggest a sustained increase in occurrence intensity over time. 

In contrast, **Quiscale merle** shows a declining fitted trend line, but the year-to-year variability is relatively high (pvalue = 0.5) and the confidence intervals are broader, resulting in a non-significant trend. This suggests that maybe the species may be experiencing a reduction in recorded abundance, but further data or more controlled sampling would be needed to statistically confirm this decline. For **Sporophile rougegorge** and **Sucrier à ventre jaune**, the mean abundance values fluctuate from year to year without displaying a marked directional change. Their fitted trends are near-flat and associated confidence intervals are wide, indicating that these populations have remained relatively stable across the studied period.

Overall, these results highlight two species experiencing significant increases (**Élenie siffleuse** and **Tourterelle à queue carrée**), one species with a possible but unconfirmed decline (**Quiscale merle**), and two species showing stable abundance levels with no evidence of directional long-term change (**Sporophile rougegorge** and **Sucrier à ventre jaune**).

#### Limitations

The mean-abundance and bootstrap approach provides a robust, effort-standardized indicator of species presence over time. However, this method does not explicitly correct for variation in detection probability (observer effects, weather, time of day), and assumes independence between sampling events, which may not always hold. Additionally, mean abundance reflects relative observation rates rather than absolute population sizes, because mean abundance is how often the species are recorded, not how many individuals exist in the ecosystem. Therefore, while the approach reliably identifies broad directional changes, results should be interpreted as population indices rather than direct population estimates. 


### Ecological Interpretation of Observed Abundance Trends

The differing abundance trajectories among the five focal bird species suggest that shifts in land use, habitat structure, and species-specific ecological traits have influenced population dynamics over the study period.

The increasing trends observed for **Élenie siffleuse** and **Tourterelle à queue carrée** likely reflect their status as generalist species with flexible foraging strategies and broad habitat tolerance. Both can exploit semi-open and human-modified environments, such as gardens, secondary vegetation, or agricultural mosaics. As such landscapes have expanded or become more prevalent, these species may have gained additional foraging and nesting opportunities, resulting in sustained increases in their recorded abundance. 

In contrast, the decline suggested for **Quiscale merle**, though not statistically significant, may indicate greater ecological sensitivity. This species displays more territorial behavior and may rely on more specific foraging or social conditions. Declining abundance could arise from competition with expanding generalist species, altered food availability, or localized habitat degradation. 

For **Sporophile rougegorge** and **Sucrier à ventre jaune**, the absence of a consistent upward or downward trend indicates population stability. These species are also relatively common but appear to maintain stable ecological niches across habitats. Their feeding strategies (granivory for Sporophile rougegorge, nectarivory/insectivory for Sucrier à ventre jaune) allow them to utilize widely available and renewable resources, which may buffer their populations against environmental change.

Overall, the observed patterns align with a well-established ecological principle:

Species with greater ecological flexibility tend to persist or increase under landscape change,  species with smaller ecological requirements or territorial constraints may be more vulnerable to decline.

---

### Per-Transect Detection Rate Evolution Study 
In this section we are looking at **where** each **top-5** species is seen (by transect) and **how often** they’re detected.

For each species and transect, we computed detection rate per year:


$$ \text{DetectionRate}_t = \frac{\text{Number of visits where the species was detected​}}{\text{Total number of visits}} $$

We judge this as a good standardized indicator because it accounts for variable sampling effort across years (e.g. some years had more visits than others), reflecting both population presence and detectability.

However, it comes with important limitations:
1. Detection $\neq$ True Presence\
In fact, it might be possible for a bird to be present in a given transect but **not be detected** because of several reasons such as : 
    - *observer skills*
    - *possible background noise* (e.g. urban noise, winds) 
    - *climate conditions* (e.g. Time of day, weather, vegetation density)\
Thus we are cheking detectability and not population size.

2. Changes in Sampling Effort May Affect Trends\
Even though we normalize by the number of visits, the observer effort differences might affect:
    - Time spent per point
    - Observer rotation schedule
    - Seasonality of surveys per year\
If later years had more experienced observers, detection could rise **without actual population increase**.

3. Habitat Changes Influence Detectability\
Similarly to sampling effort, as the vegetation structure changes the detection might get affected, with phenomenoms like reforestation or urbanization, birds become either : 
    - harder to detect (dense vegetation)
    - easier to detect (open areas)
Thus the habitat shifts, that are no presented in the main data, can bias the results. 

4. Sample Size at Some Transects May Be Small\
On the other hand, when working with some incoherences from the raw data, such as the size difference in the number of visits per transect per year, the study might reveal wide confidence intervals or unstable trend coefficients

5. Non-linearity\
For the model fitting section, we decided to use a linear model to try and capture a possible trend, however as we use ecological time series we often find nonlinear changes.\
Thus, the linear slope must be interpreted as a first-order summary, not a full model of population dynamics.


On the other hand, this same study yielded several results for our logistic trend, we highlight the interpretations of slopes and p values, as they will give us a important hint on possible trends.
Thus we define to possible outcomes, a significant p-value (p < 0.05) and a "borderline" case (0.05 < p < 0.1).\
 We will interpret them for each of the 5 top species and give plausible explanations for the presented behavior :

 

1. **Quiscale merle** (Caribbean Grackle): 

We observe a significant decline at the transect ```Habitation Petite Rivière ``` (slope = -0.1644, p = 0.020) and a borderline case at the transect ```O'Mullane``` (p $\approx$ 0.074). In the case of ```Habitation Petite Rivière ``` given a significant p-value we can supposse that a "negative"  trend is detected, this can be explained by the fact that the Grackle is a generalist (i.e. that is able to thrive in a wide variety of environmental conditions and can make use of a variety of different resources) urban species that benefits from human activity, in consequence this decline could indicate a reduction of food waste and human provisioning and/or incresead vegetation cover. This pattern could suggest local reduction of anthropogenic resources, not necessarily a regional population collapse. The absence of strong trends in central urban zones (Fort-de-France Centre Ville) suggests that declines are localized, not island-wide.

2. **Sucrier à ventre jaune** (Bananaquit) : 

We observe a significant decline at the transect ```Pointe Lynch ``` (slope = 0.1390, p = 0.001) and a borderline increase at the transect ```Fond Rousseau``` (slope = 0.0901, p $\approx $ 0.083). Other transects show stable trends.\
The Bananaquit is a nectar-feeding generalist with strong adaptability to urban gardens, flowering shrubs, and secondary forest edges. Increases at these transects likely correspond to:
- Expansion of shrub habitats
- Stable or rising nectar resource availability

This pattern is logical given that this species benefits from mild urbanization and heterogeneous vegetation structure.

3. **Elénie siffleuse** : 

This species is the one with more trends detected, in fact we had the following p-values : 
- increase : 
    - ```Tunnel Didier 2``` (p = 0.008)
    - ```Pointe Lynch``` (p = 0.007)
    - ```Habitation Petite Rivière``` (p = 0.018)
    - ```Morne Babet``` (p = 0.041)
    - ```La Démarche``` (p < 0.001)
- decrease :
    - ```Galion``` (slope = -0.1401, p = 0.001)

The Elénie is an insectivorous flycatcher that favors forest edges, open understories, and regenerating woodland. It shows strong positive trends in several semi-natural transects, wich may be explained with possible recovering of secondary forest structures, whereas its decline at Galion suggests localized habitat degradation or reduced prey availability.

4. **Tourterelle à queue carrée** (Zenaida Dove) : 

We observe a significant increase at the transect ```Pointe Lynch ``` (slope = 0.1429, p = 0.001). The species is a granivore tolerant of open woodlands, agricultural edges, and peri-urban spaces. The increasing trend at ```Pointe Lynch ``` may reflect:
- Expansion of shrubs habitats
- Availability of seed-dominated ground vegetation

Thus, the Tourterelle à queue carrée appears generally stable across the region, with a localized increase linked to the shrub habitat expansion. 

5. **Sporophile rougegorge** (Grassquit) : 

We observe increasing trends at the transects ```Tunnel Didier 2 ``` (p = 0.045) and a borderline case at the transect ```Fond Rousseau``` (p = 0.003). The other transects have stable trends.\
The Sporophile rougegorge increases in areas with recent grass regeneration, consistent with its preference for open-seeded habitats.


Summary : 

The species-level trends reveal coherent ecological patterns linked to habitat structure, vegetation dynamics, and human land activities. Several species that rely vegetation, including the ```Sucrier à ventre jaune```, the ```Elénie siffleuse``` and the ```Tourterelle à queue carrée```, show increasing detection rates in transects where semi-natural or shrubby vegetation has likely expanded. This suggests that vegetation maturation may create a more favorable environment for nectarivores and insectivores. Thus, these increasing trends appear consistent with progressive regeneration or maintenance of semi-natural habitats rather than random variation.\
In contrast, the ```Quiscale merle```, a species strongly associated with open, anthropogenic food sources, exhibits localized declines in transects where vegetation may be closing or where urban provisioning (waste, crops, feeding) is reduced.\
Taken together, these patterns indicate that variation in **detection trends** across species is best explained by *habitat structure* and *disturbance history* rather than uniform directional change in bird communities. Vegetation dynamics, whether through natural reasons or human driven, appear to influence species trajectories. Generalist nectarivores and insectivores tend to benefit from increasing vegetation complexity, while open-ground foragers respond positively to habitat disturbance, and urban-adapted omnivores may decline where anthropogenic resource availability decreases. This highlights the importance of maintaining heterogeneous habitats to support bird diversity across the landscape.

---

## 4. Synthesis and Recommendations

### Main Insights and Converging Evidence

Across all indicators, the multi-year analysis reveals a coherent picture of a largely stable but subtly evolving bird community.
The **density study** shows moderate interannual variation in bird abundance but no systematic decline. Densities remain high in core urban transects such as **Fort de France Centre Ville**, where consistent sampling effort and habitat heterogeneity sustain strong bird activity.

The **diversity indices (Shannon, Simpson, and Richness)** collectively suggest a slight improvement in community evenness over the studied period, driven more by balanced species representation than by increases in the total number of species.

The **detectability study** highlights spatial heterogeneity in observation modes: auditory detections increased significantly in several transects (e.g., Morne Babet, Habitation Petite Rivière), pointing to evolving field conditions or observer expertise rather than ecological decline.

At the **species level**, trends differ by ecological strategy, generalist species such as *Élenie siffleuse* and *Tourterelle à queue carrée* are increasing, while the urban-associated **Quiscale merle** shows localized declines.
Together, these findings indicate that habitat structure and vegetation dynamics rather than uniform environmental change the observed differences in abundance and detection rates.

---

### Actionable Recommendations

* **Enhance habitat data collection**: Record vegetation structure, land-use type, and disturbance level per transect to better explain spatial and temporal variation in density and diversity.
* **Improve GPS coordinates**: Add altitude to the coordinates allowing a better study related to the species positions.
* **Maintain strong spatial coverage**: The current network provides good geographic representation; ensure consistent sampling effort and coverage continuity beyond 2025.
* **Add phenological or climatic covariates**: Including rainfall, temperature, and seasonality measures could clarify the ecological drivers behind yearly fluctuations.
* **Modify data collection**: Automatize data collection by installing cameras, mouvement and sound sensors, evenly distributed for a more uniform data. 

---

### Reflections and Limitations

* **Data quality and consistency**: Early years show lower coverage and possible underrepresentation of some transects; these differences should be accounted for in future analyses.
* **Methodological assumptions**: Normalization and linear modelling simplify complex dynamics; non-linear models may capture patterns more faithfully.
* **Sampling bias**: Despite normalization, changes in observer effort, weather, or habitat accessibility can influence observed counts.
* **Temporal scope**: The 2014–2025 window may be too short to capture multi-decadal trends; ongoing monitoring is essential for robust long-term inference.

---

In summary, the combined indicators shown a resilient yet dynamic bird community responding to subtle habitat and observational changes.


---

