## Manifest

- `CB8-DOA-SAMPL-Answer-Sheet-20201014.docx`: Data provided by the Isaacs group (docx). Updated/corrected on Oct. 20, from earlier values posted in September.
- `CB8-DOA-SAMPL-Answer-Sheet-20201014.pdf`: Data provided by the Isaacs group (pdf). Updated/corrected on Oct. 20, from earlier values posted in September. 
- `Final-Data-Table-031621-SAMPL8.docx` : Data provided by the Gibb group (docx). 
- `experimental_measurements.csv`: Summary table of experimental data in `.csv` format. Currently only includes CB8 data.
- `experimental_measurements.json`: Summary table of experimental data in JSON format. Currently only includes CB8 data.
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi, and [the SAMPL7 `generate_tables.py`](https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by David Mobley.
- `PDFTable`: Contains experimental data in `.tex` and `.pdf` format. Currently only includes CB8 data.
Experimental conditions/details are available in the above provided files, the [Isaacs' CB8 README](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/CB8/README.md), and in [CB8 literature](https://chemrxiv.org/articles/preprint/In_Vitro_and_In_Vivo_Sequestration_of_Phencyclidine_by_Me4Cucurbit_8_uril/12994004) as of 9/25/20

## Notes on error propagation

Currently, for Isaacs' CB8 system, we are utilizing uncertainties provided by Lyle Isaacs, which provide ITC-based uncertainties, along with additional error propagation to handle uncertainties in titrant concentrations, as was done for SAMPL6 and SAMPL7.
