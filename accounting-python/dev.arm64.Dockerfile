FROM rust:slim-bookworm

ENV HOME /home
ENV PATH $PATH:$HOME/.cargo/bin
ENV PATH $PATH:$HOME/.local/bin
ENV PATH $PATH:$HOME/.elan/bin
ENV PYTHON_MAJOR_VERSION 3.12.2
ENV PYTHON_MINOR_VERSION 3.12.2
ENV NODE_VERSION 20

WORKDIR /home

RUN apt update \
    && apt-get install -y software-properties-common \
    wget \
    curl \
    gnupg2 \
    git \
    libssl-dev \
    pkg-config \
    build-essential \
    gnutls-bin \
    && rustup update \
    && rustup component add rustfmt clippy rls rust-analysis rust-src rust-analyzer \
    && mkdir -p ~/.cargo/bin \
    && cargo install cargo-edit \
    && wget https://www.python.org/ftp/python/${PYTHON_MAJOR_VERSION}/Python-${PYTHON_MINOR_VERSION}.tgz \
    && tar -xf Python-${PYTHON_MINOR_VERSION}.tgz \
    && rm -rf /var/lib/apt/lists/*

# build python
WORKDIR /home/Python-${PYTHON_MINOR_VERSION}
RUN apt update && apt install -y zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    # for scipy install
    # gfortran libopenblas-dev liblapack-dev \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make install \
    && curl -sL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt install -y nodejs \
    && pip3 install python-lsp-server pyright \
        ipython jupyterlab \
    && ln -sf /usr/local/bin/python3 /usr/local/bin/python \
    && ln -sf /usr/local/bin/pip3 /usr/local/bin/pip \
    && rm -rf /home/Python-${PYTHON_VERSION} \
    && rm /home/Python-${PYTHON_MINOR_VERSION}.tgz

# build lean
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | bash -s -- -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]
