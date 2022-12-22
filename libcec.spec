# TODO (for arm):
# - --enable-tda995x (needs nxp_hdmi SDK)
# - --enable-rpi (needs Raspberry Pi SDK)
# - package python module
#
# Conditional build:
%bcond_with	python		# python module
%bcond_with	static_libs	# static library build
#
Summary:	Pulse-Eight CEC adapter control library
Summary(pl.UTF-8):	Biblioteka sterowania adapterem CEC Pulse-Eight
Name:		libcec
Version:	6.0.2
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/Pulse-Eight/libcec/archive/%{name}-%{version}.tar.gz
# Source0-md5:	977e7f56279a85b52d4a2d08addb233e
URL:		http://libcec.pulse-eight.com/
BuildRequires:	cmake
BuildRequires:	libstdc++-devel >= 6:4.2
BuildRequires:	lockdev-devel >= 1.0
BuildRequires:	ncurses-devel
BuildRequires:	p8-platform-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	systemd-devel
BuildRequires:	udev-devel >= 1:151
BuildRequires:	xorg-lib-libXrandr-devel
%if %{with python}
BuildRequires:	python3-devel
BuildRequires:	swig
BuildRequires:	swig-python
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
Requires:	libstdc++-devel >= 6:4.2
Requires:	udev-devel >= 1:151

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

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
install -d build
cd build
%cmake \
	-DHAVE_LINUX_API=on \
	%{!?with_python:-DSKIP_PYTHON_WRAPPER:BOOL=ON} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove versioned binaries
rm $RPM_BUILD_ROOT%{_bindir}/cec-client $RPM_BUILD_ROOT/%{_bindir}/cecc-client
mv $RPM_BUILD_ROOT%{_bindir}/cec-client-%{version} $RPM_BUILD_ROOT/%{_bindir}/cec-client
mv $RPM_BUILD_ROOT%{_bindir}/cecc-client-%{version} $RPM_BUILD_ROOT/%{_bindir}/cecc-client

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING contains also general notes
%doc AUTHORS COPYING ChangeLog README.md
%attr(755,root,root) %{_libdir}/libcec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcec.so.6

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cec-client
%attr(755,root,root) %{_bindir}/cecc-client

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcec.so
%{_pkgconfigdir}/libcec.pc
%{_includedir}/libcec

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcec.a
%endif
