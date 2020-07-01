#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	QuarkXPress Import Library
Summary(pl.UTF-8):	Biblioteka do importu dokumentów QuarkXPress
Name:		libqxp
Version:	0.0.2
Release:	4
License:	MPL v2.0
Group:		Libraries
Source0:	https://dev-www.libreoffice.org/src/libqxp/%{name}-%{version}.tar.xz
# Source0-md5:	7011efa81fe8b6b1f2dd7d05d7bfb173
URL:		https://wiki.documentfoundation.org/DLP/Libraries/libqxp
BuildRequires:	boost-devel
BuildRequires:	libicu-devel
BuildRequires:	librevenge-devel >= 0.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libqxp is a library and a set of tools for reading and converting
QuarkXPress file format. It supports versions 3.1-4.1 currently.

%description -l pl.UTF-8
libqxp to biblioteka i zestaw narzędzi do odczytu i konwersji
formatu plików QuarkXPress. Obecnie obsługuje wersje 3.1-4.1.

%package devel
Summary:	Header files for libqxp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libqxp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	librevenge-devel >= 0.0
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for libqxp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libqxp.

%package static
Summary:	Static libqxp library
Summary(pl.UTF-8):	Statyczna biblioteka libqxp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libqxp library.

%description static -l pl.UTF-8
Statyczna biblioteka libqxp.

%package apidocs
Summary:	libqxp API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libqxp
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
libqxp API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libqxp.

%prep
%setup -q

%build
%configure \
	%{?with_static_libs:--enable-static} \
	--disable-silent-rules \
	--disable-werror
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libqxp-*.la
# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libqxp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/qxp2raw
%attr(755,root,root) %{_bindir}/qxp2svg
%attr(755,root,root) %{_bindir}/qxp2text
%attr(755,root,root) %{_libdir}/libqxp-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqxp-0.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqxp-0.0.so
%{_includedir}/libqxp-0.0
%{_pkgconfigdir}/libqxp-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqxp-0.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/html/*
