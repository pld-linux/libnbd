Summary:	NBD client library in userspace
Name:		libnbd
Version:	1.6.1
Release:	0.1
License:	LGPL v2+
URL:		https://github.com/libguestfs/libnbd
Source0:	http://libguestfs.org/download/libnbd/1.6-stable/%{name}-%{version}.tar.gz
# Source0-md5:	e90ca15020d9b8f3f72a0e4b9788146a
BuildRequires:	/usr/bin/pod2man
BuildRequires:	bash-completion
BuildRequires:	coreutils
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
BuildRequires:	jq
BuildRequires:	libfuse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ocamldoc
BuildRequires:	python3-devel
BuildRequires:	util-linux

# The Python module happens to be called lib*.so.  Don't scan it and
# have a bogus "Provides: libnbdmod.*".
%global __provides_exclude_from ^%{py3_sitedir}/lib.*\\.so

%description
NBD - Network Block Device - is a protocol for accessing Block Devices
(hard disks and disk-like things) over a Network.

This is the NBD client library in userspace, a simple library for
writing NBD clients.

The key features are:

 - Synchronous and asynchronous APIs, both for ease of use and for
   writing non-blocking, multithreaded clients.

 - High performance.

 - Minimal dependencies for the basic library.

 - Well-documented, stable API.

 - Bindings in several programming languages.

%package devel
Summary:	Development headers for %{name}
License:	LGPLv2+ and BSD
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development headers for %{name}.

%package -n ocaml-%{name}
Summary:	OCaml language bindings for %{name}
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-%{name}
This package contains OCaml language bindings for %{name}.

%package -n ocaml-%{name}-devel
Summary:	OCaml language development package for %{name}
Requires:	ocaml-%{name} = %{version}-%{release}

%description -n ocaml-%{name}-devel
This package contains OCaml language development package for %{name}.
Install this if you want to compile OCaml software which uses %{name}.

%package -n python3-%{name}
Summary:	Python 3 bindings for %{name}
Requires:	%{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
python3-%{name} contains Python 3 bindings for %{name}.

%package -n nbdfuse
Summary:	FUSE support for %{name}
License:	LGPLv2+ and BSD
Requires:	%{name} = %{version}-%{release}

%description -n nbdfuse
This package contains FUSE support for %{name}.

%package bash-completion
Summary:	Bash tab-completion for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description bash-completion
Install this package if you want intelligent bash tab-completion for
%{name}.

%prep
%setup -q

%build
%configure \
	PYTHON=%{__python3} \
	--disable-static \
	--with-tls-priority=@LIBNBD,SYSTEM \
	--enable-python \
	 --with-python-installdir=%{py3_sitedir} \
	--enable-ocaml \
	--enable-fuse \
	--disable-golang

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Delete libtool crap.
find $RPM_BUILD_ROOT -name '*.la' -delete

# Delete the golang man page since we're not distributing the bindings.
rm $RPM_BUILD_ROOT%{_mandir}/man3/libnbd-golang.3*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%doc COPYING.LIB
%attr(755,root,root) %{_bindir}/nbdcopy
%attr(755,root,root) %{_bindir}/nbdinfo
%{_libdir}/libnbd.so.*
%{_mandir}/man1/nbdcopy.1*
%{_mandir}/man1/nbdinfo.1*

%files devel
%defattr(644,root,root,755)
%doc TODO examples/*.c
%doc examples/LICENSE-FOR-EXAMPLES
%{_includedir}/libnbd.h
%{_libdir}/libnbd.so
%{_pkgconfigdir}/libnbd.pc
%{_mandir}/man3/libnbd.3*
%{_mandir}/man1/libnbd-release-notes-1.*.1*
%{_mandir}/man3/libnbd-security.3*
%{_mandir}/man3/nbd_*.3*

%files -n ocaml-%{name}
%defattr(644,root,root,755)
%{_libdir}/ocaml/nbd
%exclude %{_libdir}/ocaml/nbd/*.a
%exclude %{_libdir}/ocaml/nbd/*.cmxa
%exclude %{_libdir}/ocaml/nbd/*.cmx
%exclude %{_libdir}/ocaml/nbd/*.mli
%{_libdir}/ocaml/stublibs/dllmlnbd.so
%{_libdir}/ocaml/stublibs/dllmlnbd.so.owner

%files -n ocaml-%{name}-devel
%defattr(644,root,root,755)
%doc ocaml/examples/*.ml
%doc ocaml/examples/LICENSE-FOR-EXAMPLES
%{_libdir}/ocaml/nbd/*.a
%{_libdir}/ocaml/nbd/*.cmxa
%{_libdir}/ocaml/nbd/*.cmx
%{_libdir}/ocaml/nbd/*.mli
%{_mandir}/man3/libnbd-ocaml.3*
%{_mandir}/man3/NBD.3*
%{_mandir}/man3/NBD.*.3*

%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/libnbdmod*.so
%{py3_sitedir}/nbd.py
%{py3_sitedir}/nbdsh.py
%attr(755,root,root) %{_bindir}/nbdsh
%{_mandir}/man1/nbdsh.1*

%files -n nbdfuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nbdfuse
%{_mandir}/man1/nbdfuse.1*

%files bash-completion
%defattr(644,root,root,755)
%dir %{bash_compdir}
%{bash_compdir}/nbdcopy
%{bash_compdir}/nbdfuse
%{bash_compdir}/nbdinfo
%{bash_compdir}/nbdsh

