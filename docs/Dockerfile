ARG ARCH
ARG MAJOR
ARG BASE_TAG=${MAJOR}-${ARCH}
ARG BASE_IMAGE
ARG REPO_NAME

FROM ${BASE_IMAGE}:${BASE_TAG}

ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"

RUN apt-get update; apt-get install -y git

RUN python -m pip install sphinx==1.7.0 sphinx-rtd-theme sphinx-autobuild mock

RUN cd "/" \
  && git clone https://github.com/AleksandarPetrov/napoleon \
  && git checkout 0dc3f28a309ad602be5f44a9049785a1026451b3 \
  && cd /napoleon \
  && python setup.py install -f

CMD "/ros_entrypoint.sh"
