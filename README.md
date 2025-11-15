## ArcGIS Story Map

View the ArcGIS project here:

[Open the ArcGIS Story Map](https://arcg.is/0y8XrL)

Click the link above to open the story map in your browser.


**Climate Vulnerability Index for Iloilo City (Barangay Level)**

**A data-driven pipeline to calculate a granular Climate Vulnerability Index (CVI) for every barangay in Iloilo City, identifying communities most vulnerable to climate and socioeconomic pressures.**

**Project by: Team Bernoulli** **For: PJDSC 2025**

**The Problem: A Complex Picture of Risk**

Iloilo City faces multiple, overlapping risks. These dangers are not spread evenly across the city:

- Some barangays face high **climate exposure** (floods, heat).
- Others have dense **populations** living in vulnerable areas.
- Others lack access to critical **infrastructure** like health centers and shelters.

For city planners, disaster management offices (DRRMOs), and local government units (LGUs), this creates a critical challenge: **With limited resources, where do we act first?**

Without a clear, unified metric, resource allocation is difficult to justify and efforts can be reactive rather than proactive.

**Our Solution: A Barangay-Level Prioritization Tool**

We developed the **Climate Vulnerability Index (CVI)**, a composite index that synthesizes these complex factors into a single, actionable score for all 180 barangays in Iloilo City.

This index clusters every barangay into one of three categories:

- **LOW RISK**
- **MEDIUM RISK**
- **HIGH RISK**

The result is a clear, data-driven prioritization map that answers the question: "Which communities are most vulnerable and need our help first?"

**The Six Pillars of the Climate Vulnerability Index**

The CVI is a weighted average of six key risk dimensions. Each factor is normalized into a "risk contribution" score, where a higher value means higher risk.

| **Weight** | **Component** | **Description** |
| --- | --- | --- |
| **30%** | **Climate Exposure** | Direct physical risk from climate hazards. |
| **20%** | **Population Pressure** | Risk from high population counts and density. |
| **20%** | **Infrastructure** | Risk from poor access to health, education, and safety facilities. |
| **15%** | **Economic Wealth** | Risk from low economic resilience (inverted Relative Wealth Index). |
| **10%** | **Environment (NDVI)** | Risk from a lack of protective green spaces (inverted vegetation). |
| **5%** | **Coastal Proximity** | Risk associated with being near the coast. |

**Data Sources**

The analysis is built on datasets provided by **Project CCHAIN**, which were extracted from a central SQLite database (stand_datasets.db).

Key data tables included:

- CLIMATE_EXPOSURE_INDEX
- POP_STANDARDIZED (Latest population counts)
- HEALTH_STANDARDIZED (% population reached)
- AMENITY_STANDARDIZED (Distance to facilities)
- RWI_STANDARDIZED (Relative Wealth Index)
- CLIMATE_STANDARDIZED (Average NDVI)
- BRGY_STANDARDIZED (Distance to coast)

**Real-World Applications**

This index is a decision-support tool for:

- **Strategic Planning (LGU):** Guide long-term land-use planning and justify climate adaptation budgets.
- **Disaster Preparedness (DRRMO):** Prioritize "High Risk" barangays for pre-disaster preparations, such as pre-positioning relief goods, rescue boats, and mobile health clinics.
- **Targeted NGO & Community Action:** Help NGOs and community groups focus their efforts (e.g., resilience workshops, mangrove planting) where they are needed most.

**Future Directions**

This Iloilo pilot serves as a powerful blueprint. The next steps are to:

- **Go Deeper (Better Data):** Integrate hyper-granular data, such as Project NOAH flood maps, building footprints, and precise locations of informal settlements.
- **Go Smarter (Better Model):** Create an interactive "what-if" scenario tool or web application where planners can adjust the weights of the index based on their specific policy priorities.
- **Go Wider (Better Scope):** Use this successful pilot as a template to scale the Urban Risk Index to other vulnerable Philippine cities.

**Team Bernoulli**

- Kent Ryan Baluyot
- John Gabriel Cruz
- Jeb Jovero

- Dominic Lumibao
