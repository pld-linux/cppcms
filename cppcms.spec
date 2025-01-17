#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	gcrypt		# libgcrypt instead of openssl

Summary:	CppCMS - C++ Web Framework
Summary(pl.UTF-8):	CppCMS - szkielet WWW w C++
Name:		cppcms
Version:	1.2.1
Release:	2
License:	MIT
Group:		Applications/Networking
#Source0Download: https://github.com/artyom-beilis/cppcms/tags
Source0:	https://github.com/artyom-beilis/cppcms/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	638892c22c2520837eef754d50206b51
URL:		http://cppcms.com/
BuildRequires:	cmake >= 2.6
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
%if %{with gcrypt}
BuildRequires:	libgcrypt-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CppCMS is a Free High Performance Web Development Framework (not a
CMS) aimed at Rapid Web Application Development. It differs from most
other web development frameworks like: Python Django, Java Servlets in
the following ways:
- It is designed and tuned to handle extremely high loads.
- It uses modern C++ as the primary development language in order to
  achieve the first goal.
- It is designed for developing both Web Sites and Web Services.

%description -l pl.UTF-8
CppCMS to wolnodostępny, wydajny szkielet do tworzenia usług WWW (nie
CMS), którego celem jest szybkie tworzenie aplikacji WWW. Główne
różnice w stosunku do większości innych szkieletów WWW, jak Python
Django czy Java Servlets to:
- jest zaprojektowany i dostrojony do obsługi bardzo dużych obciążeń;
- używa nowoczesnego C++ jako głównego języka do osiągnięcia
  pierwszego celu;
- jest zaprojektowany do tworzenia zarówno stron, jak i usług WWW.

%package devel
Summary:	Header files for CppCMS libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek CppCMS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CppCMS libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek CppCMS.

%package static
Summary:	Static CppCMS libraries
Summary(pl.UTF-8):	Biblioteki statyczne CppCMS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CppCMS libraries.

%description static -l pl.UTF-8
Biblioteki statyczne CppCMS.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' bin/cppcms_run
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' bin/cppcms_tmpl_cc

%build
install -d build
cd build
%cmake .. \
	-DLIBDIR=%{_lib} \
	%{?with_gcrypt:-DDISABLE_OPENSSL=ON} \
	%{!?with_static_libs:-DDISABLE_STATIC=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MIT.TXT THIRD_PARTY_SOFTWARE.TXT
%attr(755,root,root) %{_bindir}/cppcms_config_find_param
%attr(755,root,root) %{_bindir}/cppcms_make_key
%attr(755,root,root) %{_bindir}/cppcms_run
%attr(755,root,root) %{_bindir}/cppcms_scale
%attr(755,root,root) %{_bindir}/cppcms_tmpl_cc
%attr(755,root,root) %{_libdir}/libbooster.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbooster.so.0
%attr(755,root,root) %{_libdir}/libcppcms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcppcms.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbooster.so
%attr(755,root,root) %{_libdir}/libcppcms.so
%{_includedir}/booster
%{_includedir}/cppcms

%files static
%defattr(644,root,root,755)
%{_libdir}/libbooster.a
%{_libdir}/libcppcms.a
