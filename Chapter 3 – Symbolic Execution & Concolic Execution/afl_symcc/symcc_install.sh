BASE=$PWD

sudo apt-get install -y cargo \
	clang-11 \
	cmake \
	g++ \
	git \
	libz3-dev \
	llvm-11-dev \
	llvm-11-tools \
	ninja-build \
	python3-pip \
	zlib1g-dev

pip3 install lit

cd ${BASE}
git clone https://github.com/Z3Prover/z3
cd z3
python scripts/mk_make.py
cd build
make
sudo make install


cd ${BASE}
git clone -b v2.56b https://github.com/google/AFL.git afl
cd afl && make


cd ${BASE}
git clone https://github.com/eurecom-s3/symcc symcc_source
cd symcc_source
git submodule init
git submodule update


cd ${BASE}
rm -rf ./symcc_build_simple
mkdir symcc_build_simple
cd symcc_build_simple
cmake -G Ninja \
	-DQSYM_BACKEND=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DZ3_TRUST_SYSTEM_VERSION=on \
	../symcc_source \
     && ninja check

cd ${BASE}
rm -rf ./symcc_build_qsym
mkdir symcc_build_qsym
cd symcc_build_qsym
cmake -G Ninja \
	-DQSYM_BACKEND=OFF \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DZ3_TRUST_SYSTEM_VERSION=on \
        ../symcc_source \
    && ninja check \
    && cargo install  --path ../symcc_source/util/symcc_fuzzing_helper


cd ${BASE}
git clone -b llvmorg-10.0.1 --depth 1 https://github.com/llvm/llvm-project.git
rm -rf ./libcxx_symcc_install
rm -rf ./libcxx_symcc_build
mkdir libcxx_symcc_install
mkdir libcxx_symcc_build
cd libcxx_symcc_build

export SYMCC_REGULAR_LIBCXX=yes SYMCC_NO_SYMBOLIC_INPUT=yes \
	&& cmake -G Ninja ../llvm-project/llvm \
	-DLLVM_ENABLE_PROJECTS="libcxx;libcxxabi" \
	-DLLVM_TARGET_TO_BUILD="X86" \
	-DLLVM_DISTRIBUTION_COMPONENTS="cxx;cxxabi;cxx-headers" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=${BASE}/libcxx_symcc_install \
	-DCMAKE_C_COMPILER=${BASE}/symcc_build_simple/symcc \
	-DCMAKE_CXX_COMPILER=${BASE}/symcc_build_simple/sym++ \
   && ninja distribution \
   && ninja install-distribution
