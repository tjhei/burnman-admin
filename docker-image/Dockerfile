FROM dealii/ubuntu16

MAINTAINER timo.heister@gmail.com

USER root
RUN apt-get update && apt-get -yq install \
  numdiff \
  wget \
  zile \
  git \
  python \
  python-scipy \
  python-numpy \
  python-matplotlib \
  texlive-latex-base \
  texlive-fonts-recommended \
  texlive-latex-recommended \
  texlive-latex-extra \
  python3-numpy python3-scipy python3-matplotlib \
  ipython3 ipython3-notebook python3-pygments

RUN apt-get update && apt-get -yq install \
  python-sympy python3-sympy

USER $USER

# build the font cache once (removes warnings):
RUN echo "import matplotlib.pyplot as plt" | python3 2>/dev/null || true
RUN echo "import matplotlib.pyplot as plt" | python 2>/dev/null || true
