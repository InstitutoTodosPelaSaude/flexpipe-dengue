# flexpipe-dengue
Nextstrain pipeline for genomic epidemiology of dengue virus (serotypes 1-4). This tool derives from [flexpipe](https://github.com/InstitutoTodosPelaSaude/flexpipe/), a nextstrain pipeline developed to be flexibly adapted to any pathogen of interest (here adapted for dengue virus).

This repository contains the essential files to create a dengue virus [nextstrain build](https://nextstrain.org/). By using this pipeline users can to perform genomic epidemiology analyses and visualize phylogeographic results to track dengue virus spread using genomic data and their associated metadata.

![alt text](https://github.com/InstitutoTodosPelaSaude/flexpipe-dengue/blob/main/overview.png)
Nextstrain panel with results overview

## Getting started

In order to run this pipeline for your dengue project, see instructions available on the original [flexpipe repository](https://github.com/InstitutoTodosPelaSaude/flexpipe/), which provides essential information needed to navigate in Unix CLI, to install a nextstrain environment with conda/mamba, and a tutorial with detailed instructions on how to generate a Nextstrain build, which involves preparing, aligning, and visualizing genomic data.

### Adjustments for dengue virus runs

The currently provided Snakefile is set up with parameters related to Dengue virus serotype 2, such as 5' unstranslated regions to be masked (`mask_5prime` and `mask_3prime`), evolutionary rate (`clock_rate` and `clock_std_dev`), and root method:

```
rule parameters:
	params:
		mask_5prime = 96,
		mask_3prime = 451,
		bootstrap = 1,
		model = "GTR",
		root = "least-squares",
		clock_rate = 0.00078,
		clock_std_dev = 0.00004,
```

Below are the parameters for each dengue virus serotype, which need to be adjusted within the `rule parameters`:

| serotype | mask_5prime | mask_3prime | clock_rate | clock_stddev |
|:--------:|:-----------:|:-----------:|:----------:|:------------:|
|  DenV1   |      94     |     462     |  0.00060    |   0.00004    |
|  DenV2   |      96     |     451     |  0.00078   |   0.00004    |
|  DenV3   |      94     |     440     |  0.00068   |   0.00004    |
|  DenV4   |     101     |     384     |  0.00066   |   0.00004    |


## Author

* **Anderson Brito, Instituto Todos pela Saúde (ITpS)** - [Website](https://www.itps.org.br/membros) - anderson.brito@itps.org.br

## License

This project is licensed under the MIT License.
