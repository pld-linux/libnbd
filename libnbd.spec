# TODO: golang
Summary:	NBD client library in userspace
Summary(pl.UTF-8):	Biblioteka klienta NBD w przestrzeni użytkownika
Name:		libnbd
Version:	1.6.2
Release:	0.1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.libguestfs.org/libnbd/1.6-stable/%{name}-%{version}.tar.gz
# Source0-md5:	dee634a684171133110432186b738853
URL:		https://github.com/libguestfs/libnbd
BuildRequires:	bash-completion-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gnutls-devel >= 3.3.0
BuildRequires:	jq
BuildRequires:	libfuse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ocamldoc
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# The Python module happens to be called lib*.so.  Don't scan it and
# have a bogus "Provides: libnbdmod.*".
%define		_noautoprovfiles	%{py3_sitedir}/libnbdmod.*

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

%description -l pl.UTF-8
NBD - Network Block Device - to protokół pozwalający na dostęp do
urządzeń blokowych (dysków twardych i rzeczy dyskopodobnych) po sieci.

Ten pakiet zawiera bibliotekę klienta NBD w przestrzeni użytkownika -
prostą bibliotekę do pisania klientów NBD.

Główne cechy to:
- API synchroniczne i asynchroniczne, zarówno w celu ułatwienia
  użycia, jak i pisania nieblokujących, wielowątkowych klientów
- wysoka wydajność
- minimalne zależności dla podstawowej biblioteki
- dobrze udokumentowane, stabilne API
- wiązania do kilku języków programowania

%package devel
Summary:	Development headers for NBD library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki NBD
License:	LGPL v2+ and BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development headers for NBD library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki NBD.

%package -n ocaml-%{name}
Summary:	OCaml language bindings for NBD library
Summary(pl.UTF-8):	Wiązania OCamla do biblioteki NBD
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-%{name}
This package contains OCaml language bindings for NBD library.

%description -n ocaml-%{name} -l pl.UTF-8
Ten pakiet zawiera wiązania OCamla do biblioteki NBD.

%package -n ocaml-%{name}-devel
Summary:	OCaml language development package for NBD library
Summary(pl.UTF-8):	Pakiet programistyczny wiązań OCamla do biblioteki NBD
Group:		Development/Libraries
Requires:	ocaml-%{name} = %{version}-%{release}

%description -n ocaml-%{name}-devel
This package contains OCaml language development package for NBD
library. Install this if you want to compile OCaml software which uses
NBD.

%description -n ocaml-%{name}-devel -l pl.UTF-8
Pakiet programistyczny wiązań OCamla do biblioteki NBD. Należy go
zainstalować, aby móc kompilować programy w OCamlu wykorzystujące NBD.

%package -n python3-%{name}
Summary:	Python 3 bindings for NBD library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki NBD
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-%{name}
This package contains Python 3 bindings for NBD library.

%description -n python3-%{name} -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona do biblioteki NBD.

%package -n nbdfuse
Summary:	FUSE support for NBD library
Summary(pl.UTF-8):	Obsługa FUSE do biblioteki NBD
License:	LGPL v2+ and BSD
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description -n nbdfuse
This package contains FUSE support for NBD library.

%description -n nbdfuse -l pl.UTF-8
Ten pakiet zawiera obsługę FUSE do biblioteki NBD.

%package -n bash-completion-%{name}
Summary:	Bash tab-completion for NBD utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla narzędzi NBD
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
Obsoletes:	libnbd-bash-completion < 1.6.2
BuildArch:	noarch

%description -n bash-completion-%{name}
Install this package if you want intelligent bash tab-completion for
NBD utilities (nbdcopy, nbdfuse, nbdinfo, nbdsh).

%description -n bash-completion-%{name} -l pl.UTF
Ten pakiet należy zainstalować, aby uzyskać inteligentne dopełnianie
parametrów dla narzędzi NBD (nbdcopy, nbdfuse, nbdinfo, nbdsh).

%prep
%setup -q

%build
%configure \
	PYTHON=%{__python3} \
	--enable-fuse \
	--disable-golang \
	--enable-ocaml \
	--enable-python \
	--disable-static \
	--with-python-installdir=%{py3_sitedir} \
	--with-tls-priority=@LIBNBD,SYSTEM

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# Delete libtool crap.
find $RPM_BUILD_ROOT -name '*.la' -delete

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.owner

# Delete the golang man page since we're not distributing the bindings.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/libnbd-golang.3*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING.LIB README
%attr(755,root,root) %{_bindir}/nbdcopy
%attr(755,root,root) %{_bindir}/nbdinfo
%attr(755,root,root) %{_libdir}/libnbd.so.*.*.*
%ghost %{_libdir}/libnbd.so.0
%{_mandir}/man1/nbdcopy.1*
%{_mandir}/man1/nbdinfo.1*

%files devel
%defattr(644,root,root,755)
%doc TODO examples/*.c examples/LICENSE-FOR-EXAMPLES
%{_libdir}/libnbd.so
%{_includedir}/libnbd.h
%{_pkgconfigdir}/libnbd.pc
%{_mandir}/man3/libnbd.3*
%{_mandir}/man1/libnbd-release-notes-1.*.1*
%{_mandir}/man3/libnbd-security.3*
%{_mandir}/man3/nbd_*.3*

%files -n ocaml-%{name}
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/nbd
%{_libdir}/ocaml/nbd/META
%{_libdir}/ocaml/nbd/NBD.cma
%{_libdir}/ocaml/nbd/NBD.cmi
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlnbd.so

%files -n ocaml-%{name}-devel
%defattr(644,root,root,755)
%doc ocaml/examples/*.ml ocaml/examples/LICENSE-FOR-EXAMPLES
%{_libdir}/ocaml/nbd/NBD.cmx
%{_libdir}/ocaml/nbd/NBD.mli
%{_libdir}/ocaml/nbd/libmlnbd.a
%{_libdir}/ocaml/nbd/mlnbd.a
%{_libdir}/ocaml/nbd/mlnbd.cmxa
%{_mandir}/man3/libnbd-ocaml.3*
%{_mandir}/man3/NBD.3*
%{_mandir}/man3/NBD.*.3*

%files -n python3-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nbdsh
%attr(755,root,root) %{py3_sitedir}/libnbdmod.cpython-*.so
%{py3_sitedir}/nbd.py
%{py3_sitedir}/nbdsh.py
%{py3_sitedir}/__pycache__/nbd.cpython-*.py[co]
%{py3_sitedir}/__pycache__/nbdsh.cpython-*.py[co]
%{_mandir}/man1/nbdsh.1*

%files -n nbdfuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nbdfuse
%{_mandir}/man1/nbdfuse.1*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/nbdcopy
%{bash_compdir}/nbdfuse
%{bash_compdir}/nbdinfo
%{bash_compdir}/nbdsh
