NFL Quarterback Passing Yard Projections:

This repository contains Python code for a statistical analysis project focused on evaluating NFL quarterbacks' likelihood of hitting the over on their projected passing yards line for a given week. The project leverages data from Pro Football Reference to determine the odds that a quarterback will exceed their line based on past performance against similar defenses. Additionally, Bayesian analysis is applied to adjust the projection based on the quarterback's recent game history.

Features:

This project performs two main tasks

Calculate Odds of Hitting the Over:

For each quarterback, the model calculates the likelihood they will exceed their projected passing yards line for the week.
The calculation is based on the quarterback's past performance against defenses that are statistically similar to their opponent's defense.

Bayesian Adjustment for Recent History:

If the calculated odds are significantly different from 50%, Bayesian analysis is used to determine whether the quarterback’s recent performance justifies this line.
The Bayesian model compares the quarterback to other QBs who could be expected to produce similar numbers against a defense of comparable strength.

Data: 

All data is sourced from Pro Football Reference, focusing on quarterback performance stats and defensive rankings for teams.
Cleaning and Preparation: Data is cleaned and formatted to build a dataframe suitable for statistical analysis.

Acknowledgments:

Special thanks to Pro Football Reference for providing the data for this project.
