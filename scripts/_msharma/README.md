# Census tract-level predictive model for tax lien sales in NYC

This exercise attempts to answer the original DataDive question #4: "For New York City properties eligible for a tax lien sale, which location information, demographic variables, socioeconomic variables, or trends in home values are predictive of a lien being put on a property?"

Theroetically, this question cannot be answered at the property level given the data at hand, because we only have information on "events" (i.e., properties that were put up for sale).
However, it is possible to roll up tax lien foreclosures to the census tract level and build a model on the tax lien foreclosure rate. That's exactly what this exercise attempted to do.
