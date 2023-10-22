#!/bin/bash

jupyter nbconvert Slides.ipynb --to slides --post serve \
  --SlidesExporter.reveal_theme=solarized \
  --SlidesExporter.reveal_scroll=True \
  --SlidesExporter.reveal_transition=none \
  --SlidesExporter.exclude_input_prompt=True \
  --SlidesExporter.exclude_output_prompt=True \
  --TagRemovePreprocessor.remove_input_tags='{"hide"}'
  
# or beige, blood, league, moon, night, serif, simple, sky, solarized, white 