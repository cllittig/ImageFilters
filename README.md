# Índice
================

- [Índice](#índice)
  - [Introdução](#introdução)
  - [Classes e Funções](#classes-e-funções)
    - [Classe Imagem](#classe-imagem)
    - [Função refaz\_apos](#função-refaz_apos)
  - [Testes](#testes)
  - [Kernels](#kernels)
    - [Convolution](#convolution)
    - [Kernel de Borda](#kernel-de-borda)
    - [Kernel de Blur](#kernel-de-blur)
  - [Dependências](#dependências)

## Introdução
==============

O código fornecido consiste em três arquivos: `main.py`, `model/Image.py` e `test.py`.

## Classes e Funções
=====================

### Classe Imagem

A classe `Imagem` é definida em `model/Image.py`. Ela tem métodos para manipulação de imagens.

### Função refaz_apos

A função `refaz_apos` é definida em `main.py`. Ela é chamada a cada 500 milissegundos para refazer a imagem.

## Testes
==========

Os testes são definidos em `test.py`. Eles testam as classes e funções.

## Kernels
=====================

Os kernels são usados para aplicar transformações em imagens. Eles são representados por uma matriz de valores que são aplicados a cada pixel da imagem.

### Convolution

A convolução é um tipo de transformação que é aplicada a uma imagem usando um kernel. Ela é definida pela seguinte fórmula:

`g(x, y) = ∑∑f(x+i, y+j) \* k(i, j)`

onde `g(x, y)` é o valor do pixel resultante, `f(x, y)` é o valor do pixel original, `k(i, j)` é o valor do kernel na posição `(i, j)` e `∑∑` é a soma sobre todos os pixels da imagem.

### Kernel de Borda

O kernel de borda é usado para detectar bordas em imagens. Ele é definido pela seguinte matriz:

`[-1 0 1]
 [-2 0 2]
 [-1 0 1]`

### Kernel de Blur

O kernel de blur é usado para aplicar um efeito de blur em imagens. Ele é definido pela seguinte matriz:

`[1/9 1/9 1/9]
 [1/9 1/9 1/9]
 [1/9 1/9 1/9]`

## Dependências
================

* Python 3.x
* Biblioteca `PIL` (Python Imaging Library)