# Report-PDF-Creation
This python projects uses PyMuPDF to create generic report templates, with widgets that are easily fillable and modifiable.

## To publish a new pip version
1. Increment version in setup.py
2. `python setup.py bdist_wheel`
3. `twine upload dist/*`
