# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	Garbage collector for C and C++
Name:		gc
Version:	7.4.2
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
# Source0-md5:	12c05fd2811d989341d8c6d81f66af87
URL:		http://www.hboehm.info/gc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gc is a conservative garbage collector for C and C++. It is used as a
replacement for standard malloc() and free(). GC_malloc will attempt
to reclaim inaccessible space automatically by invoking a conservative
garbage collector at appropriate points.

%package devel
Summary:	Headers for conservative garbage collector
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers for conservative garbage collector

%package c++
Summary:	C++ interface to GC library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ interface to GC library.

%package c++-devel
Summary:	Header files for C++ interface for GC library
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for C++ interface for GC library.

%prep
%setup -q

%{__sed} -i -e 's/^dist_pkgdata_DATA/EXTRA_DIST/' doc/doc.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static	\
	--enable-cplusplus	\
	--enable-threads=posix
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

install -d $RPM_BUILD_ROOT%{_includedir}/gc/private
install -D doc/gc.man $RPM_BUILD_ROOT%{_mandir}/man3/gc.3

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%post	c++ -p /usr/sbin/ldconfig
%postun	c++ -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.QUICK doc/README.{linux,environment,macros}
%doc doc/*.html
%attr(755,root,root) %ghost %{_libdir}/libcord.so.1
%attr(755,root,root) %ghost %{_libdir}/libgc.so.1
%attr(755,root,root) %{_libdir}/libcord.so.*.*.*
%attr(755,root,root) %{_libdir}/libgc.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcord.so
%attr(755,root,root) %{_libdir}/libgc.so
%dir %{_includedir}/gc
%{_includedir}/gc.h
%{_includedir}/gc/cord.h
%{_includedir}/gc/gc.h
%{_includedir}/gc/gc_allocator.h
%{_includedir}/gc/gc_backptr.h
%{_includedir}/gc/gc_config_macros.h
%{_includedir}/gc/gc_disclaim.h
%{_includedir}/gc/gc_gcj.h
%{_includedir}/gc/gc_inline.h
%{_includedir}/gc/gc_mark.h
%{_includedir}/gc/gc_pthread_redirects.h
%{_includedir}/gc/gc_tiny_fl.h
%{_includedir}/gc/gc_typed.h
%{_includedir}/gc/gc_version.h
%{_includedir}/gc/javaxfc.h
%{_includedir}/gc/leak_detector.h
%{_includedir}/gc/private
%{_includedir}/gc/weakpointer.h

%{_pkgconfigdir}/bdw-gc.pc
%{_mandir}/man3/gc.3*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgccpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgccpp.so.1

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgccpp.so
%{_includedir}/gc/gc_cpp.h
%{_includedir}/gc_cpp.h

