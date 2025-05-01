# Steel Column AI Dataset Generator

Genereert trainingsdata voor een AI-model dat voorspelt of stalen kolommen voldoen aan knikcontrole volgens Eurocode 3, zonder knikverkorters.

## Bestandsoverzicht
- `check_column_strength.py`: bevat de EC3-rekenregels.
- `generate_dataset.py`: maakt datasets met verschillende lengtes, profielen en belastingen.
- `data/profiles.csv`: bevat geometrie van HEA/HEB-profielen.

## Gebruik
```bash
python generate_dataset.py
```
