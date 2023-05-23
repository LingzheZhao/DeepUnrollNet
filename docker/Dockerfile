FROM nvcr.io/nvidia/pytorch:22.12-py3

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai LANG=C.UTF-8 LC_ALL=C.UTF-8 PIP_NO_CACHE_DIR=1 TORCH_CUDA_ARCH_LIST="8.6 8.9" MAX_JOBS=32

RUN sed -i  "s/archive.ubuntu.com/mirrors.ustc.edu.cn/g" /etc/apt/sources.list &&\
    sed -i  "s/security.ubuntu.com/mirrors.ustc.edu.cn/g" /etc/apt/sources.list &&\
    rm -f /etc/apt/sources.list.d/* &&\
    # Fix /opt/hpcx/ompi/lib/libmpi.so.40: undefined symbol: opal_hwloc201_hwloc_get_type_depth
    rm -rf /opt/hpcx/ &&\
    apt-get update && apt-get upgrade -y &&\
    apt-get install -y --no-install-recommends \
        autoconf automake autotools-dev build-essential ca-certificates \
        make cmake yasm pkg-config gdb gcovr binutils-dev libiberty-dev \
        ninja-build ccache doxygen graphviz plantuml \
        libatlas-base-dev libboost-all-dev libcereal-dev \
        libceres-dev libcgal-dev \
        libcxsparse3 libsuitesparse-dev libeigen3-dev liblapack-dev liblapacke-dev \
        metis libmetis-dev libopenblas-base libopenblas-dev libopenmpi-dev openmpi-bin \
        libgtk2.0-dev libglew-dev libglu1-mesa-dev mesa-utils \
        freeglut3-dev libassimp-dev libglfw3-dev libqt5opengl5-dev \
        libxrandr-dev libxxf86vm-dev \
        libgflags-dev libgoogle-glog-dev libgtest-dev \
        libopencv-dev libopenexr-dev libjpeg-dev libpng-dev libtiff-dev libtiff5-dev \
        libavcodec-dev libavformat-dev libavutil-dev libavdevice-dev \
        libpcap-dev libpostproc-dev libpq-dev libswscale-dev ffmpeg \
        libtbb2 libtbb-dev libxine2-dev zlib1g-dev \
        libkrb5-dev libssl-dev libtool \
        libyaml-dev libyaml-cpp-dev libicu-dev \
        ## Tools
        git curl wget unzip nano net-tools sudo htop iotop \
        cloc daemontools krb5-user nfs-common rsync \
        openssh-server openssh-client unattended-upgrades \
        software-properties-common &&\
    rm /etc/ssh/ssh_host_ecdsa_key &&\
    rm /etc/ssh/ssh_host_ed25519_key &&\
    rm /etc/ssh/ssh_host_rsa_key &&\
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config_bak &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Install Conda and Determined AI stuff
WORKDIR /tmp
ENV PYTHONUNBUFFERED=1 PYTHONFAULTHANDLER=1 PYTHONHASHSEED=0
ENV JUPYTER_CONFIG_DIR=/run/determined/jupyter/config
ENV JUPYTER_DATA_DIR=/run/determined/jupyter/data
ENV JUPYTER_RUNTIME_DIR=/run/determined/jupyter/runtime
RUN git clone https://github.com/LingzheZhao/determinedai-container-scripts &&\
    cd determinedai-container-scripts &&\
    git checkout v0.1 &&\
    pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple &&\
    pip install determined && pip uninstall -y determined &&\
    pip install -r notebook-requirements.txt &&\
    pip install -r additional-requirements.txt &&\
    ./add_det_nobody_user.sh &&\
    ./install_libnss_determined.sh &&\
    rm -rf /tmp/*

COPY requirements.txt /tmp
RUN cd /tmp &&\
    pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple &&\
    pip install -U pip &&\
    pip install -r requirements.txt

RUN cd /tmp &&\
    git clone https://github.com/LingzheZhao/DeepUnrollNet &&\
    cd DeepUnrollNet &&\
    cd ./package_correlation &&\
    python setup.py install &&\
    cd ../package_forward_warp &&\
    python setup.py install &&\
    cd ../package_core &&\
    python setup.py install &&\
    rm -rf /tmp/*
