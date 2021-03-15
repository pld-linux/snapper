Summary:	Tool for filesystem snapshot management
Name:		snapper
Version:	0.8.15
Release:	1
License:	GPL v2
Source0:	https://github.com/openSUSE/snapper/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df0e34b092bde0d8447360adc7bffb3a
URL:		http://snapper.io
Patch0:		remove-ext4-info-xml.patch
Patch1:		json-c.patch
Patch2:		systemd-install.patch
BuildRequires:	acl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	btrfs-progs-devel
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext
BuildRequires:	json-c-devel
BuildRequires:	libmount-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pam-devel
BuildRequires:	systemd-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	diffutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains snapper, a tool for filesystem snapshot
management.

%package libs
Summary:	Library for filesystem snapshot management
Requires:	btrfs-progs
Requires:	util-linux

%description libs
This package contains the snapper shared library for filesystem
snapshot management.

%package devel
Summary:	Header files and development libraries for %{name}-libs
Requires:	%{name}-libs = %{version}-%{release}
Requires:	acl-devel
Requires:	boost-devel
Requires:	btrfs-progs-devel
Requires:	libmount-devel
Requires:	libstdc++-devel
Requires:	libxml2-devel

%description devel
This package contains header files and documentation for developing
with snapper.

%package -n pam-pam_snapper
Summary:	PAM module for calling snapper
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_snapper
A PAM module for calling snapper during user login and logout.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# use libexecdir
find -type f -exec sed -i -e "s|/usr/lib/snapper|%{_libexecdir}/%{name}|g" {} ';'

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-ext4 \
	--disable-zypp \
	--enable-selinux

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig,%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p data/sysconfig.snapper $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
cp -p examples/c/*.c examples/c++-lib/*.cc $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT{%{_libdir}/*.la,/%{_lib}/security/*.la}
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/cron.*
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
# Testsuite here only
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/snapper

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f snapper.lang
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/snapper
%attr(755,root,root) %{_sbindir}/mksubvolume
%attr(755,root,root) %{_sbindir}/snapperd
%config(noreplace) /etc/logrotate.d/snapper
%config(noreplace) /etc/dbus-1/system.d/org.opensuse.Snapper.conf
%{_datadir}/dbus-1/system-services/org.opensuse.Snapper.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/installation-helper
%{_libexecdir}/%{name}/systemd-helper
%{systemdunitdir}/%{name}-*.timer
%{systemdunitdir}/%{name}-*.service
%{systemdunitdir}/snapperd.service
%{_mandir}/man5/snapper-configs.5*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/mksubvolume.8*
%{_mandir}/man8/snapperd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsnapper.so.*.*.*
%ghost %{_libdir}/libsnapper.so.5
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/configs
%dir %{_sysconfdir}/%{name}/config-templates
%config(noreplace) %{_sysconfdir}/%{name}/config-templates/default
%dir %{_sysconfdir}/%{name}/filters
%config(noreplace) %{_sysconfdir}/%{name}/filters/*.txt
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsnapper.so
%{_includedir}/%{name}
%{_examplesdir}/%{name}-%{version}

%files -n pam-pam_snapper
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_snapper.so
%dir %{_prefix}/lib/pam_snapper
%attr(755,root,root) %{_prefix}/lib/pam_snapper/*.sh
%{_mandir}/man8/pam_snapper.8*
