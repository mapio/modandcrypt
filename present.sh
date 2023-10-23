#!/bin/bash

while true; do
  jupyter nbconvert Slides.ipynb --to slides --post serve \
    --ServePostProcessor.open_in_browser=False \
    --SlidesExporter.reveal_theme=serif \
    --SlidesExporter.reveal_scroll=True \
    --SlidesExporter.reveal_transition=none \
    --SlidesExporter.exclude_input_prompt=True \
    --SlidesExporter.exclude_output_prompt=True \
    --TagRemovePreprocessor.remove_input_tags='{"hide"}'
done

# or beige, blood, league, moon, night, serif, simple, sky, solarized, white 

