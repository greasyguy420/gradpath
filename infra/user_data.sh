#!/bin/bash
# installs and starts the gradpath container

set -euxo pipefail

dnf update -y
dnf install -y git docker
systemctl start docker
systemctl enable docker

rm -rf /opt/gradpath
git clone "${repo_url}" /opt/gradpath
cd /opt/gradpath
git checkout "${repo_branch}"

docker build -t gradpath .
docker stop gradpath || true
docker rm gradpath || true
docker run -d --name gradpath -p 8501:8501 gradpath
