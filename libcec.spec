Summary:	Pulse-Eight CEC adapter control library
Summary(pl.UTF-8):	Biblioteka sterwania adapterem Pulse-Eight CEC
Name:		libcec
Version:	2.1.1
Release:	1
License:	GPL v2+
Group:		Libraries
URL:		http://libcec.pulse-eight.com/
Source0:	http://github.com/Pulse-Eight/libcec/archive/%{name}-%version.tar.gz
# Source0-md5:	0317e6b8895d54f8f035fde90b25dc2d
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	lockdev-devel
BuildRequires:	pkgconfig

%description
Pulse-Eight CEC adapter control library.

%description -l pl.UTF-8
Biblioteka sterwania adapterem Pulse-Eight CEC.

%package utils
Summary:	Utilities for Pulse-Eight CEC adapter control
Summary(pl.UTF-8):	Narzędla dla adaptera Pulse-Eight CEC
Group:		Base/Kernel
Requires:	%{name} = %{version}-%{release}

%description utils
With libcec you can access your Pulse-Eight CEC adapter.

This package contains the command-line tools to configure and test
your Pulse-Eight CEC adapter.

%package devel
Summary:	Header files for libcec library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcec
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcec library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcec.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.2

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cec-client

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_pkgconfigdir}/%{name}.pc
%{_includedir}/%{name}
