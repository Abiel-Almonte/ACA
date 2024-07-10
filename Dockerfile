FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

RUN apt-get update && \
    apt-get -y install sudo vim

ARG USER=aca
ARG UID=1001
ARG GID=1002
ARG PSWD

ENV USER=${USER}

RUN groupadd -g ${GID} -o ${USER}
RUN useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${USER} && \
    echo ${USER}:${PSWD} | chpasswd && \
    adduser ${USER} sudo
USER ${USER}

WORKDIR /home/${USER}/workspace

COPY --chown=${UID}:${GID} ./server /home/${USER}/app/
COPY --chown=${UID}:${GID} ./client /home/${USER}/app/

RUN echo ${PSWD} | sudo -S apt install -y python3 python-is-python3 pip git && \
    pip install torch torchvision torchaudio && \
    pip install datasets transformers sentence-transformers pymilvus vllm langchain

#docker build --build-arg PSWD=<yourPassword>  --network=host -t app-image ./deploy
#docker compose up -d