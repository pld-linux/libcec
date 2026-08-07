# TODO (for arm):
# - --enable-tda995x (needs nxp_hdmi SDK)
# - --enable-rpi (needs Raspberry Pi SDK)
#
# Conditional build:
%bcond_without	python		# python module
%bcond_without	static_libs	# static library
#
Summary:	Pulse-Eight CEC adapter control library
Summary(pl.UTF-8):	Biblioteka sterowania adapterem CEC Pulse-Eight
Name:		libcec
Version:	8.1.6
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/Pulse-Eight/libcec/releases
Source0:	https://github.com/Pulse-Eight/libcec/archive/%{name}-%{version}.tar.gz
# Source0-md5:	eb458dcef5cc3dcf6067f9cdee4bb387
URL:		http://libcec.pulse-eight.com/
BuildRequires:	cmake >= 3.12.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	systemd-devel
BuildRequires:	udev-devel >= 1:151
BuildRequires:	xorg-lib-libXrandr-devel
%if %{with python}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	swig >= 2
BuildRequires:	swig-python >= 2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pulse-Eight CEC adapter control library.

%description -l pl.UTF-8
Biblioteka sterowania adapterem CEC firmy Pulse-Eight.

%package utils
Summary:	Utilities for Pulse-Eight CEC adapter control
Summary(pl.UTF-8):	Narzędla dla adaptera CEC Pulse-Eight
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
With libcec you can access your Pulse-Eight CEC adapter.

This package contains the command-line tools to configure and test
your Pulse-Eight CEC adapter.

%description utils -l pl.UTF-8
libcec pozwala na dostęp do adaptera CEC firmy Pulse-Eight.

Ten pakiet zawiera narzędzie linii poleceń do konfiguracji i
testowania adaptera CEC Pulse-Eight.

%package devel
Summary:	Header files for libcec library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcec
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for libcec library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcec.

%package static
Summary:	Static libcec library
Summary(pl.UTF-8):	Statyczna biblioteka libcec
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcec library.

%description static -l pl.UTF-8
Statyczna biblioteka libcec.

%package -n python3-libcec
Summary:	Python wrapper for libcec library
Summary(pl.UTF-8):	Obudowanie Pythonowe dla biblioteki libcec
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-libcec
Python wrapper for libcec library.

%description -n python3-libcec -l pl.UTF-8
Obudowanie Pythonowe dla biblioteki libcec.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DHAVE_LINUX_API=on \
	-DPYTHON_USE_VERSION=3 \
	%{!?with_python:-DSKIP_PYTHON_WRAPPER:BOOL=ON} \
	%{!?with_static_libs:-DDISABLE_STATIC:BOOL=ON} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp debian/cec-client.1 $RPM_BUILD_ROOT%{_mandir}/man1/cec-client.1

# Remove versioned binaries
%{__rm} $RPM_BUILD_ROOT%{_bindir}/cec-client $RPM_BUILD_ROOT/%{_bindir}/cecc-client
%{__mv} $RPM_BUILD_ROOT%{_bindir}/cec-client-%{version} $RPM_BUILD_ROOT/%{_bindir}/cec-client
%{__mv} $RPM_BUILD_ROOT%{_bindir}/cecc-client-%{version} $RPM_BUILD_ROOT/%{_bindir}/cecc-client

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# LICENSE.md contains also general notes
%doc AUTHORS LICENSE.md README.md debian/changelog.in
%attr(755,root,root) %{_libdir}/libcec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcec.so.8

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cec-client
%attr(755,root,root) %{_bindir}/cecc-client
%{_mandir}/man1/cec-client.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcec.so
%{_pkgconfigdir}/libcec.pc
%{_includedir}/libcec
%{_libdir}/cmake/libcec

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcec.a
%endif

%if %{with python}
%files -n python3-libcec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pyCecClient
%attr(755,root,root) %{py3_sitedir}/_pycec.so
%{py3_sitedir}/cec.py
%{py3_sitedir}/__pycache__/cec.cpython-*.py[co]
%endif
