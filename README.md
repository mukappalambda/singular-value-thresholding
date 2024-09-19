# Singular Value Thresholding

This repo provides a Python implementation for Singular Value Thresholding (SVT) algorithm, and illustrate one of its application: image inpainting.

The image I use is downloaded from [Pexels](https://www.pexels.com/), which is a website that provides a variety of free images.

The main reference is the following:

- Jian-Feng Cai, Emmanuel J. Candes, Zuowei Shen, [A Singular Value Thresholding Algorithm for Matrix Completion](https://arxiv.org/abs/0810.3286)

---

## Install SVT

**Method 1**

```bash
pip install git+https://github.com/mukappalambda/singular-value-thresholding.git@main
```

**Method 2**

Create the virtual environment (assuming that the [poetry](https://github.com/python-poetry/poetry) library is installed):

```bash
poetry install
poetry shell
```

## Uninstall SVT

```bash
pip uninstall -y svt
```

---

Run the code:

```bash
python main.py
```

Results:

![Original image](landscape.jpg?raw=true 'Original image')

![Impaired image](output_folder/impaired.png?raw=true 'Impaired image')

![Recovered image](output_folder/recovered.png?raw=true 'Recovered image')
