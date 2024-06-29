# Use an Ubuntu base image
FROM ubuntu:22.04

# Set the default shell to bash
ENV SHELL /bin/bash

# Set shell as bash
SHELL ["/bin/bash", "-c"]

# Install necessary packages and tools
RUN apt-get update && apt-get install -y

RUN apt-get install curl git unzip nano make locales zip -y 

# Run arch specificexpectations for specific arch (x86_64, arm64, aarch64)
COPY ./arch_spec_install_script.sh /scripts/

RUN chmod +x /scripts/arch_spec_install_script.sh

RUN /scripts/arch_spec_install_script.sh

COPY ./python_env.sh /scripts/

RUN chmod +x /scripts/python_env.sh 

# installing oh my bash - https://github.com/ohmybash/oh-my-bash
RUN curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh | bash

# customize the bash shell ans set vscode theme
RUN sed -i 's/^OSH_THEME=.*/OSH_THEME="vscode"/' ~/.bashrc

# locale generation is important to make bash 
# work properly with newlines and such
RUN locale-gen en_US.UTF-8

# installing language specific tools like nvm, node, python, go, cargo, rust 

# install tfenv to manage terraform version
RUN git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv

RUN echo 'export PATH=$PATH:$HOME/.tfenv/bin' >> ~/.bashrc

RUN echo 'alias tf="terraform"' >> ~/.bashrc

# install latest terraform version
RUN $HOME/.tfenv/bin/tfenv install latest

RUN $HOME/.tfenv/bin/tfenv use latest

# installing google cloud sdk: https://cloud.google.com/sdk/docs/install-sdk
RUN apt-get install apt-transport-https ca-certificates gnupg -y

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
 && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \ 
 && apt-get update -y \ 
 && apt-get upgrade -y \
 && apt-get install google-cloud-sdk -y \
 # python env set up
 && apt-get install -y python3.10 \
 # install python3-pip
 && apt-get install -y python3-pip \
 # install venv 
 && apt-get install -y python3.10-venv