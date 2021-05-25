#!/bin/bash

#jupyter nbconvert 1.1W--Lesson-1.1--Virtual-Machine-Docker-Setup.ipynb --output-dir='./gridappsd-docs/docs/source/installation/windows10' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --EmbedImagesPreprocessor.embed_images=True  --to rst
#jupyter nbconvert 1.2W--Lesson-1.2--Installing-GridAPPS-D.ipynb --output-dir='./gridappsd-docs/docs/source/installation/windows10' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to rst
#jupyter nbconvert 1.3W--Lesson-1.3--Running-GridAPPS-D.ipynb --output-dir='./gridappsd-docs/docs/source/installation/windows10' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to rst
#jupyter nbconvert 1.4W--Lesson-1.4--Installing-Python-Tutorials.ipynb --output-dir='./gridappsd-docs/docs/source/installation/windows10' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to rst

jupyter nbconvert 1.0W--Module-1--Windows-10-Installation-Complete.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 1.5--Lesson-1.5--Using-GridAPPS-D-Viz.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 1.6--Lesson 1.6--Docker Shortcuts.ipynb.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook

jupyter nbconvert 2.1--Lesson-2.1--Intro-to-GridAPPS-D.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 2.2--Lesson-2.2--GridAPPS-D-Architecture.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 2.3--Lesson-2.3--GridAPPS-D-Python-Library.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 2.4--Lesson-2.4--GridAPPS-D-Application-Structure.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 2.5--Lesson-2.5--GridAPPS-D-Service-Structure.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
jupyter nbconvert 2.6--Lesson-2.6--Common-Information-Model.ipynb --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook

#jupyter nbconvert  --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook
#jupyter nbconvert  --output-dir='./docs/source/' --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" --to notebook









