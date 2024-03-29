# Specs file to building RPM of Linux to DJGPP cross-compiler
# Tested on CentOS-6.8, Fedora 25. One may need
# to modify this file for other RPM based Linux distribution

%define gcc_version 10.3.0

%define gcc_source_name 10.3.0
%define rpm_version 10.3.0

%define gmp_version 6.2.0
%define mpfr_version 4.0.2
%define mpc_version 1.1.0
%define autoconf_version 2.69
%define automake_version 1.15.1
%define target i586-pc-msdosdjgpp
%define gcc_src_ext xz

%define include_ada 0
%define include_fortran 0
%define include_objc 0
%define enable_lto 1
%define do_native_bootstrap 1
%define create_djgpp_source_zip 1

%define __os_install_post %{nil}
%define _missing_build_ids_terminate_build 0
%define debug_package %{nil}

%if %include_ada
%define support_ada 1
%endif

%if %include_fortran
%define support_fortran 1
%endif

%if %include_objc
%define support_objc 1
%endif

%if %enable_lto
%define support_lto 1
%endif

%define languages c,c++%{?support_fortran:,f95}%{?support_objc:,objc,obj-c++}%{?support_ada:,ada}

Name: djcross-gcc
Summary:  GCC cross-compiler for target i586-pc-msdosdjgpp
Version: %{rpm_version}
Release: 1ap

License: GPL
Group: Development/Tools
URL: http://www.iki.fi/andris.pavenis/djgpp/gcc/
Source0: http://ap1.pp.fi/djgpp/gcc/%{gcc_version}/src/djcross-gcc-%{rpm_version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/gcc/gcc-%{gcc_version}/gcc-%{gcc_source_name}.tar.%{gcc_src_ext}
Source2: ftp://ftp.gmplib.org/pub/gmp-%{gmp_version}/gmp-%{gmp_version}.tar.bz2
Source3: http://mpfr.loria.fr/mpfr-%{mpfr_version}/mpfr-%{mpfr_version}.tar.bz2
Source4: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
Source5: ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{autoconf_version}.tar.gz
Source6: ftp://ftp.gnu.org/gnu/automake/automake-%{automake_version}.tar.gz

Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildArch: i686 x86_64
Requires: djcrx djcross-binutils >= 2.30
BuildRequires: gcc-c++ >= 4.4 djcrx >= 2.05 djcross-binutils >= 2.30
BuildRequires: zlib-devel glibc-devel texinfo-tex
BuildRequires:  flex

%define shortver %(echo %{rpm_version} | sed -e 's:\\.::2g' -e 's:_:-:g')
%define shortver2 %(echo %{rpm_version} | sed -e 's:\\.::g' -e 's:_:-:g')

%package c++
Summary: GCC cross-compiler for i586-pc-msdosdjgpp (C++)
Requires: djcross-gcc = %{version}
Group: Development/Tools

%if %include_fortran
%package gfortran
Summary: GCC cross-compiler for i586-pc-msdosdjgpp (GNU Fortran)
Requires: djcross-gcc = %{version}
Group: Development/Tools
%endif

%if %include_objc
%package objc
Summary: GCC cross-compiler for i586-pc-msdosdjgpp (Objective C and Objective C++)
Requires: djcross-gcc = %{version}
Group: Development/Tools
%endif

%if %include_ada
%package gnat
Summary: GCC cross-compiler for i586-pc-msdosdjgpp (GNU Ada)
Requires: djcross-gcc = %{version}
Group: Development/Tools
%endif

%package info
Summary: GCC cross-compiler for i586-pc-msdosdjgpp (Info files)
Group: Development/Tools

%package tools
Summary: Tools for Linux to DJGPP cross-compiler
Group: Development/Tools

%if %{create_djgpp_source_zip}
%package djdocs
Summary: DJGPP documentation archives for GCC
Group: Development/Tools
%endif

%description
Support of the following programing languages is included:
    C
    C++
    Fortran
    Objective C
    Objective C++
    Ada

%description c++
C++ Cross-compiler for target i586-pc-msdosdjgpp. Includes both
C++ compiler and C++ standard library.

%if %include_fortran
%description gfortran
GNU Fortran compiler for target i586-pc-msdosdjgpp
%endif

%if %include_objc
%description objc
GNU Objective C and Objective C++ compilers for target i586-pc-msdosdjgpp
%endif

%if %include_ada
%description gnat
GNU Ada compiler for target i586-pc-msdosdjgpp
%endif

%description info
Info files for Linux to DJGPP cross-compiler. These files are
in a separate package to avGNU Objective C and Objective C++ compilers for target i586-pc-msdosdjgpp

%description tools
Tools for Linux to DJGPP cross-compiler.

At this time there is only fixinc.
You don not need to install it unless You know why You need it...

%if %{create_djgpp_source_zip}
%description djdocs
DJGPP documentation archives for GCC

This RPM is built only to generate and pack PDF, PS and HTML
documentation archives for DJGPP. It is not intended to
be used in Linux system
%endif

#############################################################################
%if %do_native_bootstrap
%define native_cc_spec CC=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin/gcc
%define native_cxx_spec CXX=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin/g++
%else
%define native_cc_spec CC=gcc
%define native_cxx_spec CXX=g++
%endif

%prep

echo Build cross-compiler for DJGPP: languages are %{languages}

rm -rf $RPM_BUILD_DIR/%{name}-%{version}
%setup -q -n djcross-gcc-%{version}
ln -s $RPM_SOURCE_DIR/gcc-%{gcc_source_name}.tar.%{gcc_src_ext} $RPM_BUILD_DIR/%{name}-%{version}/
cd $RPM_BUILD_DIR/%{name}-%{version} || exit 1

tar xzf $RPM_SOURCE_DIR/autoconf-%{autoconf_version}.tar.gz || exit 1
cd $RPM_BUILD_DIR/%{name}-%{version}/autoconf-%{autoconf_version}
./configure --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst
make all install

cd $RPM_BUILD_DIR/%{name}-%{version} || exit 1
tar xzf $RPM_SOURCE_DIR/automake-%{automake_version}.tar.gz || exit 1
cd $RPM_BUILD_DIR/%{name}-%{version}/automake-%{automake_version}
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" ./configure --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" make all install

cd $RPM_BUILD_DIR/%{name}-%{version} || exit 1
tar xjf $RPM_SOURCE_DIR/gmp-%{gmp_version}.tar.bz2 || exit 1
tar xjf $RPM_SOURCE_DIR/mpfr-%{mpfr_version}.tar.bz2 || exit 1
tar xzf $RPM_SOURCE_DIR/mpc-%{mpc_version}.tar.gz || exit 1

# Create source archive for native DJGPP compiler
%if %{create_djgpp_source_zip}
cd $RPM_BUILD_DIR/%{name}-%{version}
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" \
    sh unpack-gcc.sh gcc-%{gcc_source_name}.tar.%{gcc_src_ext} || exit 1
%else
cd $RPM_BUILD_DIR/%{name}-%{version}
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" \
    sh unpack-gcc.sh --no-djgpp-source gcc-%{gcc_source_name}.tar.%{gcc_src_ext} || exit 1
%endif

for fn in gnu/gcc-%{shortver}/COPYING* gnu/gcc-%{shortver}/NEWS gnu/gcc-%{shortver}/README \
   gnu/gcc-%{shortver}/readme.DJGPP ; \
do \
      test -e $fn && cp -fv $fn ./; \
done

%build
# Build requires this directory to be present or to be creatable to work
#mkdir -p /usr/lib/gcc/i586-pc-msdosdjgpp/%{version} || exit 1
#

cd $RPM_BUILD_DIR/%{name}-%{version}/gmp-%{gmp_version}
./configure --build=${RPM_ARCH}-${RPM_OS} \
            --enable-fat \
            --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --enable-static --disable-shared
make %{_smp_mflags} all
make %{_smp_mflags} check
make install

cd $RPM_BUILD_DIR/%{name}-%{version}/mpfr-%{mpfr_version}
./configure --build=${RPM_ARCH}-${RPM_OS} \
            --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --with-gmp=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --enable-static --disable-shared
make %{_smp_mflags} all
make %{_smp_mflags} check
make install

cd $RPM_BUILD_DIR/%{name}-%{version}/mpc-%{mpc_version}
./configure --build=${RPM_ARCH}-${RPM_OS} \
            --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --with-gmp=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --with-mpfr=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
            --enable-static --disable-shared
make %{_smp_mflags} all
make %{_smp_mflags} check
make install

cd $RPM_BUILD_DIR/%{name}-%{version}

%if %do_native_bootstrap

# Bootstrap native compiler for building cross-compiler
# Native C compiler is being built always. Ada compiler
# is only built when building Ada cross-compiler is required.
# (This step is intended to ensure that the cross-compiler
# is built with the same GCC version). 
mkdir tmpbuild
cd tmpbuild

../gnu/gcc-%{shortver}/configure \
    --prefix=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
    --with-gmp=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
    --with-mpfr=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
    --with-mpc=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
    --enable-languages=c$(echo %{languages} | grep -q ada && echo ",ada") \
    --enable-__cxa_atexit \
    --disable-multilib \
    --disable-plugin \
    --disable-libsanitizer

make %{_smp_mflags} bootstrap
make install

cd ..

%endif

#

mkdir djcross
cd djcross

%native_cc_spec \
%native_cxx_spec \
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" \
../gnu/gcc-%{shortver}/configure --build=%{_build} \
                                 --host=%{_host} \
			         --target=%{target} \
			         --program-prefix=%{target}- \
			         --prefix=%{_prefix} \
			         --exec-prefix=%{_exec_prefix} \
			         --bindir=%{_bindir} \
			         --sbindir=%{_sbindir} \
			         --sysconfdir=%{_sysconfdir} \
			         --datadir=%{_datadir} \
			         --includedir=%{_includedir} \
			         --libdir=%{_libdir} \
			         --libexecdir=%{_libexecdir} \
			         --localstatedir=%{_localstatedir} \
			         --sharedstatedir=%{_sharedstatedir} \
			         --mandir=%{_mandir} \
			         --infodir=%{_infodir} \
			         --disable-nls \
                                 --disable-plugin \
			         --disable-lto \
				 --enable-libquadmath-support \
%if %enable_lto
                                 --enable-lto \
%endif
                                 --enable-libstdcxx-filesystem-ts \
                                 --with-gmp=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
                                 --with-mpfr=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
                                 --with-mpc=$RPM_BUILD_DIR/%{name}-%{version}/tmpinst \
			         --enable-version-specific-runtime-libs \
			         --enable-languages=%{languages} || exit 1

make %{_smp_mflags} PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" || exit 1

cd ..

# Build DJGPP documentation packages for GCC
%if %{create_djgpp_source_zip}
( cd gnu/install.gcc && perl mkdocs.pl )
for file in gnu/gcc-%{shortver}/COPYING* gnu/gcc-%{shortver}/NEWS gnu/gcc-%{shortver}/README gnu/gcc-%{shortver}/readme.DJGPP; do \
   test -f $file && cp -fv $file ./
done
%endif

%install
rm -fr %{buildroot}

export STRIP=/bin/true
cd $RPM_BUILD_DIR/%{name}-%{version}/djcross
# makeinstall
PATH="$RPM_BUILD_DIR/%{name}-%{version}/tmpinst/bin:$PATH" make install DESTDIR=%{buildroot} datadir=%{buildroot}/usr/share
( cd %{buildroot}%{_bindir} && for file in *; do case $file in *gccbug) ;; *) strip $file ;; esac; done )
( cd %{buildroot}%{_bindir} && if [ -f gprmake ] ; then mv -fv gprmake i586-pc-msdosdjgpp-gprmake; fi )
( cd %{buildroot}%{_bindir} && if [ -f vxaddr2line ] ; then mv -fv vxaddr2line i586-pc-msdosdjgpp-vxaddr2line; fi )
rm -f %{buildroot}/%{_libdir}/libiberty.a
rm -fr %{buildroot}%{_mandir}/man7/*
rm -fr %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}/usr/share/gcc-%{gcc_version}/python
rm -f %{buildroot}/usr/%{target}/lib/libiberty.a

for file in $(find %{buildroot}%{_mandir} -type f) ; do gzip -v9 $file; done

for file in cc1 cc1obj cc1objplus cc1plus collect2 f951 gnat1 install_tools/fixincl lto-wrapper ; do
    if [ -f %{buildroot}%{_libexecdir}/gcc/%{target}/%{gcc_version}/$file ] ; then
        strip %{buildroot}%{_libexecdir}/gcc/%{target}/%{gcc_version}/$file
    else
        echo "WARNING: File $file not found"
    fi
done

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{target}-cpp
%{_bindir}/%{target}-gcc*
%{_bindir}/%{target}-gcov*
%{_bindir}/%{target}-lto-dump
%{_libdir}/gcc/%{target}/%{gcc_version}/include-fixed/*
%{_libdir}/gcc/%{target}/%{gcc_version}/libgcc.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libgcov.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libquadmath.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libquadmath.la
%{_libdir}/gcc/%{target}/%{gcc_version}/libssp.*
%{_libdir}/gcc/%{target}/%{gcc_version}/libssp_nonshared.*
%{_libdir}/gcc/%{target}/%{gcc_version}/include/ssp/*.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/*intrin*.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/cet.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/cpuid.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/cross-stdarg.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/float.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/gcov.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/iso646.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/mm3dnow.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/mm_malloc.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdarg.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdatomic.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdbool.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stddef.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdfix.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/tgmath.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/unwind.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/varargs.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdint.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdalign.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdnoreturn.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/stdint-gcc.h
%{_libdir}/gcc/%{target}/%{gcc_version}/include/quadmath*.h
%{_libexecdir}/gcc/%{target}/%{gcc_version}/cc1
%{_libexecdir}/gcc/%{target}/%{gcc_version}/collect2
%{_libexecdir}/gcc/%{target}/%{gcc_version}/lto1
%{_libexecdir}/gcc/%{target}/%{gcc_version}/lto-wrapper
%{_mandir}/man1/%{target}-cpp.1.gz
%{_mandir}/man1/%{target}-gcc.1.gz
%{_mandir}/man1/%{target}-gcov.1.gz
%{_mandir}/man1/%{target}-gcov-dump.1.gz
%{_mandir}/man1/%{target}-gcov-tool.1.gz
%{_mandir}/man1/%{target}-lto-dump.1.gz
%doc COPYING* README readme.DJGPP

%files c++
%defattr(-,root,root)
%{_bindir}/%{target}-c++
%{_bindir}/%{target}-g++
%{_libdir}/gcc/%{target}/%{gcc_version}/include/c++/*
%{_libdir}/gcc/%{target}/%{gcc_version}/libstdc++.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libstdc++.la
%{_libdir}/gcc/%{target}/%{gcc_version}/libsupc++.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libsupc++.la
%{_libdir}/gcc/%{target}/%{gcc_version}/libstdc++fs.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libstdc++fs.la
%{_libdir}/gcc/%{target}/%{gcc_version}/libstdc++.a-gdb.py
%{_libexecdir}/gcc/%{target}/%{gcc_version}/cc1plus
%{_mandir}/man1/%{target}-g++.1.gz

%if %include_fortran
%files gfortran
%defattr(-,root,root)
%{_bindir}/%{target}-gfortran
%{_libdir}/gcc/%{target}/%{gcc_version}/libgfortran.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libgfortran.la
%{_libdir}/gcc/%{target}/%{gcc_version}/libgfortran.spec
%{_libdir}/gcc/%{target}/%{gcc_version}/libcaf_single.*
%{_libdir}/gcc/%{target}/%{gcc_version}/finclude
%{_libdir}/gcc/%{target}/%{gcc_version}/include/ISO_Fortran_binding.h
%{_libexecdir}/gcc/%{target}/%{gcc_version}/f951
%{_mandir}/man1/%{target}-gfortran.1.gz
%endif

%if %include_objc
%files objc
%defattr(-,root,root)
%{_libdir}/gcc/%{target}/%{gcc_version}/libobjc.a
%{_libdir}/gcc/%{target}/%{gcc_version}/libobjc.la
%{_libdir}/gcc/%{target}/%{gcc_version}/include/objc/*
%{_libexecdir}/gcc/%{target}/%{gcc_version}/cc1obj
%{_libexecdir}/gcc/%{target}/%{gcc_version}/cc1objplus
%endif

%if %include_ada
%files gnat
%defattr(-,root,root)
%{_bindir}/%{target}-gnat*
%{_libdir}/gcc/%{target}/%{gcc_version}/adainclude/*
%{_libdir}/gcc/%{target}/%{gcc_version}/adalib/*
%{_libdir}/gcc/%{target}/%{gcc_version}/ada_target_properties
%{_libexecdir}/gcc/%{target}/%{gcc_version}/gnat1
%endif

%files info
%defattr(-,root,root)
%{_infodir}/*

%files tools
%defattr(-,root,root)
%{_libdir}/gcc/%{target}/%{gcc_version}/install-tools
%{_libexecdir}/gcc/%{target}/%{gcc_version}/install-tools

%if %{create_djgpp_source_zip}
%files djdocs
%defattr(-,root,root)
%doc gnu/install.gcc/gcc*d.zip
%doc gnu/install.gcc/gfor*d.zip
%doc gnu/install.gcc/ada*d.zip
%endif

%changelog
* Sat Apr 10 2021 Andris Pavēnis <andris.pavenis@iki.fi>
- Update to GCC-10.3.0

* Fri Jul 24 2020 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-10.2.0

* Thu May  7 2020 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-10.1.0

* Fri May  1 2020 Andris Pavenis <andris.pavenis@iki.fi>
- Branch for upcoming gcc-10

* Tue May 15 2018 Andris Pavenis <andris.pavenis@iki.fi>
- Fix value of macros __DATE__ and __TIME__ for DJGPP host.

* Sat May  5 2018 Andris Pavenis <andris.pavenis@iki.fi>
- Update requirements for building and using cross-compiler RPMs

* Wed May  2 2018 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-8.1.0.

* Sat Feb 17 2018 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPFR-4.0.1

* Sun Jan 21 2018 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPFR-4.0.0 and MPC-1.1.0

* Sun Oct 15 2017 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPFR-3.1.6

* Tue May  2 2017 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-7.1.0
- Use GMP-6.1.2, MPFR-3.1.5

* Wed Jun 22 2016 Andris Pavenis <andris.pavenis@iki.fi>
- Use GMP-6.1.1

* Wed Apr 27 2016 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-6.1.0

* Fri Apr 15 2016 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-6-branch

* Wed Mar 09 2016 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPFR-3.1.4
- Do not remove tests for Linux build

* Sun Nov 08 2015 Andris Pavenis <andris.pavenis@iki.fi>
- Use GMP-6.1.0

* Wed Apr 22 2015 Andris Pavenis <andris.pavenis@iki.fi>
- Update to gcc-5.1.0

* Tue Apr 14 2015 Andris Pavenis <andris.pavenis@iki.fi>
- Change to gcc-5-branch (and derived DJGPP related branches)

* Sat Feb 28 2015 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPC-1.0.3

* Mon Feb 02 2015 Andris Pavenis <andris.pavenis@iki.fi>
- Use MPC-1.0.2 (already done time ago for gcc-4.8.X and 4.9.X)
- Note that part of gcc-4.8 and gcc-4.9 related changelog entries
  went to different branches and are not present here

* Wed Jul 16 2014 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.9.1

* Tue Apr 22 2014 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.9.0
- Use GMP-6.0.0

* Fri Apr 11 2014 Andris Pavenis <andris.pavenis@iki.fi>
- Update for upcomming gcc-4.9.0 (after SVN branching)

* Thu Nov 21 2013 Andris Pavenis <andris.pavenis@iki.fi>
- Package also stdatomic.h

* Fri Nov  1 2013 Andris Pavenis <andris.pavenis@iki.fi>
- Fix debugging info for DJGPP (backtrace command in GDB did not work properly)
- Fix list of executables for stripping debug info

* Sat Oct  5 2013 Andris Pavenis <andris.pavenis@iki.fi>
- Fix typo in SPEC file
- build also fortran, objc, objc++ compilers conditionally

* Thu Apr  4 2013 Andris Pavenis <andris.pavenis@iki.fi>
- Update for GCC trunk

* Sun Jul 22 2012 Andris Pavenis <andris.pavenis@iki.fi>
- Add support from building from GCC snapshots

* Sun Jun 17 2012 Andris Pavenis <andris.pavenis@iki.fi> 4.7.2-2ap
- Try to fix native build of Ada compiler
- Separate patches required for cross-compiler from ones needed
  for native compiler only

* Thu Jun 14 2012 Andris Pavenis <andris.pavenis@iki.fi> 4.7.1-1ap
- Update to GCC-4.7.1
- Use GMP-5.0.5

* Sat Mar 24 2012 Andris Pavenis <andris.pavenis@iki.fi> 4.7.0-1ap
- Update to GCC-4.7.0

* Fri Mar  2 2012 Andris Pavenis <andris.pavenis@iki.fi> 4.6.3-1ap
- Update to GCC-4.6.3
- Use GMP-5.0.4

* Tue Jun 28 2011 Andris Pavenis <andris.pavenis@iki.fi> 4.6.1-1ap
- Update to GCC-4.6.1
- Use GMP-5.0.2

* Fri May 27 2011 Andris Pavenis <andris.pavenis@iki.fi> 4.6.0-3ap
- Some small updates (additional and modified patches
  for generating gcc460s.zip)

* Sat May 21 2011 Andris Pavenis <andris.pavenis@iki.fi> 4.6.0-2ap
- Updates to build also libquadmath

* Tue May  3 2011 Andris Pavenis <andris.pavenis@iki.fi> 4.6.0-1ap
- Update to gcc-4.6.0

* Mon Jan  3 2011 Andris Pavenis <andris.pavenis@iki.fi> 4.5.2-1ap
- Conditionally include/exclude Ada
- Fix typo in patching libgfortran/Makefile.am

* Wed Dec 22 2010 Andris Pavenis <andris.pavenis@iki.fi> 4.5.2-1ap
- Update to GCC-4.5.2
- Disable Ada as it does not build (related source patches remain)

* Sun Jun 20 2010 Andris Pavenis <andris.pavenis@iki.fi> 4.4.4-2ap
- Some small changes related to generating sources for native build

* Mon Jun 14 2010 Andris Pavenis <andris.pavenis@iki.fi> 4.4.4-1ap
- Update to GCC-4.4.4

* Sat Jan 23 2010 Andris Pavenis <andris.pavenis@iki.fi> 4.4.3-1ap
- Update to GCC-4.4.3

* Fri Oct 16 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.2-1ap
- Update to GCC-4.4.2

* Fri Jul 24 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.1-1ap
- Update to GCC-4.4.1

* Fri Jun 19 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.0-5ap
- Do not override LINK_COMMAND_SPEC, modify gcc.c to add POST_LINK_SPEC
  for adding extra linking steps instead. Modify config/i386/djgpp.h
  accordingly
- Use %{build} instead of %{host} for detecting DJGPP in libfortran
  subdirectory (rename libgfortranbegin.a for native DJGPP compiler
  only).

* Tue Jun 16 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.0-4ap
- Fix Ada support.

* Fri May 22 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.0-2ap
- Split in several RPM packages
- Update to use gmp-4.3.1 and mpfr-2.4.1

* Fri May  1 2009 Andris Pavenis <andris.pavenis@iki.fi> 4.4.0-1ap
- Update for gcc-4.4.0.

* Tue Dec 30 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Leave Ada out as it does not build without sockets support

* Sat Dec 27 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Modified for GCC-4.4 development snapshots (used 20081205 snapshot)
- Included also autoconf-2.59 and automake-1.9.6 to avoid using
  newer versions.

* Sat Aug 30 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-4.3.2 (RPM version 4.3.2-7ap)

- I wanted to include also sources of GMP and MPFR to avoid dependency
  on their shared libraries. Unfortunatelly it did not work. So I left
  related stuff commented out from spec file.

* Sat Jun  7 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-4.3.1 (RPM version 4.3.1-6ap)

* Wed Apr 30 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Some small additional patches (does not affect functionality)

* Sat Apr  5 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Some small additional patches

* Sat Mar 15 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-4.3.0 (RPM version 4.3.0-3ap)

* Sun Feb 24 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-4.3-20080221
- use 'make install DESTDIR=...' instead of '%makeinstall'.

* Mon Feb  4 2008 Andris Pavenis <andris.pavenis@iki.fi>
- Use gcc-4.3-20080201
- Disable building libssp
- Fix libstdc++-v3 configuration for DJGPP (add os/djgpp/error_constants.h)

* Sat Nov 24 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Updates for using gcc-4.3.0 development snapshots

* Mon Oct 15 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Small updates (4.2.2-12ap) to scripts and readme.DJGPP
  in gcc422s2.zip

* Tue Oct  9 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.2.2 (4.2.2-11ap)

* Wed Sep  5 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Add BuildArch for x86_64.

* Wed Jul 25 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.2.1 (4.2.1-9).

* Mon Jul 23 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Small updates not really influencing functionality
  (4.2.0-8).

* Thu Jun 07 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Small updates not really influencing functionality
  (4.2.0-7).

* Mon May 28 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Include patch for fixing warnings about requested
  alignemnt exceeding one supported in object file
  from DJ Delorie <dj@delorie.com> 

* Wed May 23 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.2.0 (4.2.0-5)

* Sun Mar 25 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Test for cross-compiler installation directory at very
  begin, as it is nuisance to see build failing after an
  hour for this reason
- Merge changes from Gordon Schumacher with my updates to
  later GCC versions.

* Tue Mar 13 2007 Gordon Schumacher <whiplash@pobox.com>
- Updated to use RPM's prefix macros

* Thu Mar  8 2007 Andris Pavenis <andris.pavenis@iki.fi>
- Update to GCC-4.1.2 (4.1.2-1)
 
* Tue May 30 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Fixed libstdc++ name for cross-compiler (4.1.1-2)

* Sun May 28 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Updated to GCC-4.1.1 (4.1.1-1)

* Fri Apr  7 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Patched libssp directory to fix problem with generated
  gcc410s.zip. Cross-compiler itself does not change.

* Sun Mar  5 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Bootstrap at first native compiler to be used for building 
  cross-compiler as one need to build cross-compiler with the
  same version of GCC (use of GCC-4.0.2 causes failure in 
  building Ada tools). Updates to DJGPP related patchset.

* Wed Mar  1 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Updated for GCC-4.1.0

* Sun Feb 19 2006 Andris Pavenis <andris.pavenis@iki.fi>
- Added modification of readme.DJGPP according the version of GCC and DJGPP, as
  otherwise it is rather easy to forget to edit it manually when needed

* Tue Nov 15 2005 Andris Pavenis <pavenis@latnet.lv>
- Initial version of rpm spec file for DJGPP cross-compiler
