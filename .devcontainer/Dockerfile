FROM ghcr.io/shoppal-ai/llm-base:pytorch-2.0.1-py3.10-cuda-11.8.0-cudnn8-devel-22.04

RUN apt update && apt install -y zsh curl git sudo wget libsndfile1 ffmpeg

# # install python environment
# RUN apt install -y python3.8-dev python3-pip 
# RUN update-alternatives --install /usr/bin/pthon python /usr/bin/python3.10 1 
RUN apt install -y python3.10-venv

RUN  wget -qO /usr/local/bin/websocat https://github.com/vi/websocat/releases/latest/download/websocat.x86_64-unknown-linux-musl
RUN chmod a+x /usr/local/bin/websocat


ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN usermod -aG sudo $USERNAME
RUN echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $USERNAME

RUN cd ~ && wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh && sh install.sh

RUN python3 -m venv ~/venv
RUN echo "source ~/venv/bin/activate" >> ~/.zshrc

# Set Python path in the virtual environment.
RUN echo "export PYTHONPATH=\$PYTHONPATH:/workspace" >> ~/.zshrc
RUN /bin/zsh ~/.zshrc

# Setup HF_ENDPOINT and PYANNOTE_CACHE
ENV HF_ENDPOINT=https://hf-mirror.com
ENV PYANNOTE_CACHE=/data0/cache/pyannote/

ENV DEBIAN_FRONTEND=dialog

