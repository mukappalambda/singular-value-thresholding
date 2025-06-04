# Singular Value Thresholding

This repo provides a Python implementation for the Singular Value Thresholding (SVT) algorithm, and illustrate one of its application: image inpainting.

The images I use are downloaded from [Pexels](https://www.pexels.com/), which is a website that provides a variety of free images.

The main reference is the following:

- Jian-Feng Cai, Emmanuel J. Candes, Zuowei Shen, [A Singular Value Thresholding Algorithm for Matrix Completion](https://arxiv.org/abs/0810.3286)

---

## Installing SVT

**Install from GitHub using `pip`**

```bash
pip install git+https://github.com/mukappalambda/singular-value-thresholding.git@main
```

**Install in a virtual environment from source using `poetry`**

> Note that poetry v2 is required in this case.

Create the virtual environment (assuming that the [poetry](https://github.com/python-poetry/poetry) library is installed):

```bash
poetry install ## Install the package
$(poetry env activate) ## Enter into the virtual environment
svt-cli --help ## Check that svt-cli has been installed
deactivate ## Exit the virtual environment
```

## Uninstalling SVT

```bash
pip uninstall -y svt
```

---

Run the code:

```console
$ svt-cli --help

 Usage: svt-cli [OPTIONS] /path/to/image

 Examples:
 $ svt-cli ./input.png
 $ svt-cli ./input.png --pct 0.2
 $ svt-cli ./input.png --it 150

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    fname      /path/to/image  input image path [default: None] [required]                                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --random-state              INTEGER RANGE [x>=0]       random state [default: None]                                                                                                                          │
│ --width                     INTEGER RANGE [x>=0]       resize width; smaller width for faster convergence. [default: 500]                                                                                    │
│ --pct                       FLOAT RANGE [0.0<=x<=1.0]  mask percentage; higher percentage for faster convergence [default: 0.1]                                                                              │
│ --it                        INTEGER RANGE [x>=0]       maximum iterations [default: 100]                                                                                                                     │
│ --install-completion                                   Install completion for the current shell.                                                                                                             │
│ --show-completion                                      Show completion for the current shell, to copy it or customize the installation.                                                                      │
│ --help                                                 Show this message and exit.                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Results:

![Original image](landscape.jpg?raw=true "Original image")

![Impaired image](assets/impaired.png?raw=true "Impaired image")

![Recovered image](assets/recovered.png?raw=true "Recovered image")
