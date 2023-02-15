FROM fedora:37
RUN dnf install -y mock rpmdevtools
RUN dnf install -y zlib-devel texinfo-tex flex automake gcc gcc-c++
RUN useradd -m build
COPY bld /
COPY rpms /
RUN rpm -ivh /djcrx-2.05-5.x86_64.rpm /djcross-binutils-2.34-1ap.x86_64.rpm
USER build
