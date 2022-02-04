%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global rhosp 0

%global common_desc \
OpenStack Object Storage (Swift) aggregates commodity servers to work together \
in clusters for reliable, redundant, and large-scale storage of static objects. \
Objects are written to multiple hardware devices in the data center, with the \
OpenStack software responsible for ensuring data replication and integrity \
across the cluster. Storage clusters can scale horizontally by adding new nodes, \
which are automatically configured. Should a node fail, OpenStack works to \
replicate its content from other active nodes. Because OpenStack uses software \
logic to ensure data replication and distribution across different devices, \
inexpensive commodity hard drives and servers can be used in lieu of more \
expensive equipment.

Name:             openstack-swift
Version:          XXX
Release:          XXX
Summary:          OpenStack Object Storage (Swift)

License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          https://tarballs.openstack.org/swift/swift-%{upstream_version}.tar.gz

Source2:          %{name}-account.service
Source21:         %{name}-account@.service
Source22:         account-server.conf
Source23:         %{name}-account-replicator.service
Source24:         %{name}-account-replicator@.service
Source25:         %{name}-account-auditor.service
Source26:         %{name}-account-auditor@.service
Source27:         %{name}-account-reaper.service
Source28:         %{name}-account-reaper@.service
Source4:          %{name}-container.service
Source41:         %{name}-container@.service
Source42:         container-server.conf
Source43:         %{name}-container-replicator.service
Source44:         %{name}-container-replicator@.service
Source45:         %{name}-container-auditor.service
Source46:         %{name}-container-auditor@.service
Source47:         %{name}-container-updater.service
Source48:         %{name}-container-updater@.service
Source49:         %{name}-container-sharder.service
# we seriously need to think about dropping the enumerated units - no sharder@
Source5:          %{name}-object.service
Source51:         %{name}-object@.service
Source52:         object-server.conf
Source53:         %{name}-object-replicator.service
Source54:         %{name}-object-replicator@.service
Source55:         %{name}-object-auditor.service
Source56:         %{name}-object-auditor@.service
Source57:         %{name}-object-updater.service
Source58:         %{name}-object-updater@.service
Source59:         %{name}-object-expirer.service
Source63:         %{name}-container-reconciler.service
Source6:          %{name}-proxy.service
Source61:         proxy-server.conf
Source62:         object-expirer.conf
Source64:         container-reconciler.conf
Source20:         %{name}.tmpfs
Source7:          swift.conf
Source71:         %{name}.rsyslog
Source72:         %{name}.logrotate
Source73:         %{name}-object-reconstructor.service
Source74:         %{name}-object-reconstructor@.service
Source75:         %{name}-container-sync.service
Source76:         %{name}-container-sync@.service
Source77:         internal-client.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/swift/swift-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:    openstack-macros
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    git-core
BuildRequires:    /usr/bin/pathfix.py

BuildRequires:    systemd
Obsoletes:        openstack-swift-auth  <= 1.4.0

# Required to compile translation files
BuildRequires:    python3-babel
# Required to build docs: doxygen invokes actual code and its imports
BuildRequires:    python3-keystoneclient

Requires:         python3-swift = %{version}-%{release}

%description
%{common_desc}

%package -n       python3-swift
Summary:          Python libraries for the OpenStack Object Storage (Swift)

Provides:         openstack-swift = %{version}-%{release}
Obsoletes:        openstack-swift < %{version}-%{release}
%{?python_provide:%python_provide python3-swift}

Requires:         python3-eventlet >= 0.25.0
Requires:         python3-greenlet >= 0.3.2
Requires:         python3-pyeclib >= 1.3.1
Requires:         python3-cryptography >= 2.0.2
Requires:         python3-oslo-config >= 2:5.1.0
Requires:         python3-castellan >= 0.7.0
Requires:         python3-requests >= 2.14.2
Requires:         python3-six >= 1.10.0

Requires:         python3-paste-deploy >= 2.0.0
Requires:         python3-pyxattr >= 0.4
Requires:         python3-netifaces >= 0.8
Requires:         python3-lxml >= 3.4.1

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
Requires(pre):    shadow-utils

%description -n   python3-swift
%{common_desc}

This package contains the %{name} Python library.

%package          account
Summary:          Account services for Swift

Requires:         python3-swift = %{version}-%{release}
Requires:         rsync >= 3.0

%description      account
%{common_desc}

This package contains the %{name} account server.

%package          container
Summary:          Container services for Swift

Requires:         python3-swift = %{version}-%{release}
Requires:         rsync >= 3.0

%description      container
%{common_desc}

This package contains the %{name} container server.

%package          object
Summary:          Object services for Swift

Requires:         python3-swift = %{version}-%{release}
Requires:         rsync >= 3.0

%description      object
%{common_desc}

This package contains the %{name} object server.

%package          proxy
Summary:          A proxy server for Swift

Requires:         python3-swift = %{version}-%{release}
Requires:         python3-keystoneclient
Requires:         python3-keystonemiddleware
Requires:         python3-ceilometermiddleware

%description      proxy
%{common_desc}

This package contains the %{name} proxy server.

%package -n python3-swift-tests
Summary:          Swift tests
Requires:         python3-swift = %{version}-%{release}
%{?python_provide:%python_provide python3-swift-tests}
Provides:         python-swift-tests = %{version}-%{release}

%description -n python3-swift-tests
%{common_desc}

This package contains the %{name} test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{name}

BuildRequires:    python3-sphinx >= 1.0
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-sphinxcontrib-rsvgconverter
# Required for generating docs (otherwise py-modindex.html is missing)
BuildRequires:    python3-eventlet
BuildRequires:    python3-pyeclib

BuildRequires:    python3-netifaces
BuildRequires:    python3-paste-deploy
BuildRequires:    python3-pyxattr
BuildRequires:    python3-lxml

%description      doc
%{common_desc}

This package contains documentation files for %{name}.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n swift-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}
# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/swift/locale --domain swift

%if 0%{?with_doc}
# Fails unless we create the build directory
mkdir -p doc/build
# Build docs
export PYTHONPATH=.
# NOTE(ykarel) Re-add -W option once following bz is fixed.
# bug: https://bugzilla.redhat.com/show_bug.cgi?id=1479804
# This requires sphinx that can deal with lxml and **kwargs. The one in
# CentOS 7 throws "Inline strong start-string without end-string."
sphinx-build -b html doc/source doc/build/html
# Fix hidden-file-or-dir warning
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}
# systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-account.service
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/%{name}-account@.service
install -p -D -m 644 %{SOURCE23} %{buildroot}%{_unitdir}/%{name}-account-replicator.service
install -p -D -m 644 %{SOURCE24} %{buildroot}%{_unitdir}/%{name}-account-replicator@.service
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_unitdir}/%{name}-account-auditor.service
install -p -D -m 644 %{SOURCE26} %{buildroot}%{_unitdir}/%{name}-account-auditor@.service
install -p -D -m 644 %{SOURCE27} %{buildroot}%{_unitdir}/%{name}-account-reaper.service
install -p -D -m 644 %{SOURCE28} %{buildroot}%{_unitdir}/%{name}-account-reaper@.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-container.service
install -p -D -m 644 %{SOURCE41} %{buildroot}%{_unitdir}/%{name}-container@.service
install -p -D -m 644 %{SOURCE43} %{buildroot}%{_unitdir}/%{name}-container-replicator.service
install -p -D -m 644 %{SOURCE44} %{buildroot}%{_unitdir}/%{name}-container-replicator@.service
install -p -D -m 644 %{SOURCE45} %{buildroot}%{_unitdir}/%{name}-container-auditor.service
install -p -D -m 644 %{SOURCE46} %{buildroot}%{_unitdir}/%{name}-container-auditor@.service
install -p -D -m 644 %{SOURCE47} %{buildroot}%{_unitdir}/%{name}-container-updater.service
install -p -D -m 644 %{SOURCE48} %{buildroot}%{_unitdir}/%{name}-container-updater@.service
install -p -D -m 644 %{SOURCE49} %{buildroot}%{_unitdir}/%{name}-container-sharder.service
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-object.service
install -p -D -m 644 %{SOURCE51} %{buildroot}%{_unitdir}/%{name}-object@.service
install -p -D -m 644 %{SOURCE53} %{buildroot}%{_unitdir}/%{name}-object-replicator.service
install -p -D -m 644 %{SOURCE54} %{buildroot}%{_unitdir}/%{name}-object-replicator@.service
install -p -D -m 644 %{SOURCE55} %{buildroot}%{_unitdir}/%{name}-object-auditor.service
install -p -D -m 644 %{SOURCE56} %{buildroot}%{_unitdir}/%{name}-object-auditor@.service
install -p -D -m 644 %{SOURCE57} %{buildroot}%{_unitdir}/%{name}-object-updater.service
install -p -D -m 644 %{SOURCE58} %{buildroot}%{_unitdir}/%{name}-object-updater@.service
install -p -D -m 644 %{SOURCE59} %{buildroot}%{_unitdir}/%{name}-object-expirer.service
install -p -D -m 644 %{SOURCE63} %{buildroot}%{_unitdir}/%{name}-container-reconciler.service
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-proxy.service
install -p -D -m 644 %{SOURCE73} %{buildroot}%{_unitdir}/%{name}-object-reconstructor.service
install -p -D -m 644 %{SOURCE74} %{buildroot}%{_unitdir}/%{name}-object-reconstructor@.service
install -p -D -m 644 %{SOURCE75} %{buildroot}%{_unitdir}/%{name}-container-sync.service
install -p -D -m 644 %{SOURCE76} %{buildroot}%{_unitdir}/%{name}-container-sync@.service
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/container-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/object-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/proxy-server
# Config files
install -p -D -m 660 %{SOURCE22} %{buildroot}%{_sysconfdir}/swift/account-server.conf
install -p -D -m 660 %{SOURCE42} %{buildroot}%{_sysconfdir}/swift/container-server.conf
install -p -D -m 660 %{SOURCE52} %{buildroot}%{_sysconfdir}/swift/object-server.conf
install -p -D -m 660 %{SOURCE61} %{buildroot}%{_sysconfdir}/swift/proxy-server.conf
install -p -D -m 660 %{SOURCE62} %{buildroot}%{_sysconfdir}/swift/object-expirer.conf
install -p -D -m 660 %{SOURCE64} %{buildroot}%{_sysconfdir}/swift/container-reconciler.conf
install -p -D -m 660 %{SOURCE7} %{buildroot}%{_sysconfdir}/swift/swift.conf
install -p -D -m 660 %{SOURCE77} %{buildroot}%{_sysconfdir}/swift/internal-client.conf
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/account-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/container-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/object-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/proxy-server
# syslog
install -d -m 755 %{buildroot}%{_localstatedir}/log/swift
install -p -D -m 644 %{SOURCE71} %{buildroot}%{_sysconfdir}/rsyslog.d/openstack-swift.conf
install -p -D -m 644 %{SOURCE72} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-swift
# Swift run directories
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_tmpfilesdir}/openstack-swift.conf
# Install recon directory
install -d -m 755 %{buildroot}%{_localstatedir}/cache/swift
# Install home directory
install -d -m 755 %{buildroot}%{_sharedstatedir}/swift
# man pages
install -d -m 755 %{buildroot}%{_mandir}/man5
for m in doc/manpages/*.5; do
  install -p -m 0644 $m %{buildroot}%{_mandir}/man5
done
install -d -m 755 %{buildroot}%{_mandir}/man1
for m in doc/manpages/*.1; do
  install -p -m 0644 $m %{buildroot}%{_mandir}/man1
done

# tests
mkdir -p %{buildroot}%{_datadir}/swift/test
cp -r test %{buildroot}%{python3_sitelib}/swift/test

# Remove unnecessary shebangs
sed -i '1{/^#!/d}' %{buildroot}%{python3_sitelib}/swift/test/probe/test_object_partpower_increase.py
sed -i '1{/^#!/d}' %{buildroot}%{python3_sitelib}/swift/test/functional/test_symlink.py
# Remove executable bit to avoid rpmlint failures
chmod -x %{buildroot}%{python3_sitelib}/swift/test/probe/test_object_partpower_increase.py
chmod -x %{buildroot}%{python3_sitelib}/swift/test/functional/test_symlink.py

# Install i18n files
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/swift/locale/*/LC_*/swift*po
rm -f %{buildroot}%{python3_sitelib}/swift/locale/*pot
mv %{buildroot}%{python3_sitelib}/swift/locale %{buildroot}%{_datadir}/locale

# Fix shebangs for Python 3-only distros
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/swift/test

# Find language files
%find_lang swift --all-name

%clean
rm -rf %{buildroot}

%pre -n python3-swift
getent group swift >/dev/null || groupadd -r swift -g 160
getent passwd swift >/dev/null || \
useradd -r -g swift -u 160 -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%post account
%systemd_post %{name}-account.service
%systemd_post %{name}-account-replicator.service
%systemd_post %{name}-account-auditor.service
%systemd_post %{name}-account-reaper.service

%preun account
%systemd_preun %{name}-account.service
%systemd_preun %{name}-account-replicator.service
%systemd_preun %{name}-account-auditor.service
%systemd_preun %{name}-account-reaper.service

%postun account
%systemd_postun %{name}-account.service
%systemd_postun %{name}-account-replicator.service
%systemd_postun %{name}-account-auditor.service
%systemd_postun %{name}-account-reaper.service

%post container
%systemd_post %{name}-container.service
%systemd_post %{name}-container-replicator.service
%systemd_post %{name}-container-auditor.service
%systemd_post %{name}-container-updater.service
%systemd_post %{name}-container-sync.service
%systemd_post %{name}-container-sharder.service

%preun container
%systemd_preun %{name}-container.service
%systemd_preun %{name}-container-replicator.service
%systemd_preun %{name}-container-auditor.service
%systemd_preun %{name}-container-updater.service
%systemd_preun %{name}-container-sync.service
%systemd_preun %{name}-container-sharder.service

%postun container
%systemd_postun %{name}-container.service
%systemd_postun %{name}-container-replicator.service
%systemd_postun %{name}-container-auditor.service
%systemd_postun %{name}-container-updater.service
%systemd_postun %{name}-container-sync.service
%systemd_postun %{name}-container-sharder.service

%post object
%systemd_post %{name}-object.service
%systemd_post %{name}-object-replicator.service
%systemd_post %{name}-object-reconstructor.service
%systemd_post %{name}-object-auditor.service
%systemd_post %{name}-object-updater.service

%preun object
%systemd_preun %{name}-object.service
%systemd_preun %{name}-object-replicator.service
%systemd_preun %{name}-object-reconstructor.service
%systemd_preun %{name}-object-auditor.service
%systemd_preun %{name}-object-updater.service

%postun object
%systemd_postun %{name}-object.service
%systemd_postun %{name}-object-replicator.service
%systemd_postun %{name}-object-reconstructor.service
%systemd_postun %{name}-object-auditor.service
%systemd_postun %{name}-object-updater.service

%post proxy
%systemd_post %{name}-proxy.service
%systemd_post %{name}-object-expirer.service

%preun proxy
%systemd_preun %{name}-proxy.service
%systemd_preun %{name}-object-expirer.service

%postun proxy
%systemd_postun %{name}-proxy.service
%systemd_postun %{name}-object-expirer.service

%post -n python3-swift
/usr/bin/kill -HUP `cat /var/run/syslogd.pid 2>/dev/null` 2>/dev/null || :

%files -n python3-swift -f swift.lang
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst
%doc etc/*-sample
%{_mandir}/man5/dispersion.conf.5*
%{_mandir}/man1/swift-account-audit.1*
%{_mandir}/man1/swift-ring-builder-analyzer.1*
%{_mandir}/man1/swift-config.1*
%{_mandir}/man1/swift-dispersion-populate.1*
%{_mandir}/man1/swift-dispersion-report.1*
%{_mandir}/man1/swift-drive-audit.1*
%{_mandir}/man1/swift-form-signature.1*
%{_mandir}/man1/swift-get-nodes.1*
%{_mandir}/man1/swift-init.1*
%{_mandir}/man1/swift-oldies.1.*
%{_mandir}/man1/swift-orphans.1*
%{_mandir}/man1/swift-recon.1*
%{_mandir}/man1/swift-recon-cron.1*
%{_mandir}/man1/swift-ring-builder.1*
%{_mandir}/man1/swift-ring-composer.1*
%{_mandir}/man5/swift.conf.5*
%{_mandir}/man5/container-sync-realms.conf.5*
%{_tmpfilesdir}/openstack-swift.conf
%dir %attr(0755, swift, swift)%{_sysconfdir}/swift
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/swift.conf
%config(noreplace) %{_sysconfdir}/rsyslog.d/openstack-swift.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-swift
%dir %{_localstatedir}/log/swift
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift
%dir %attr(0755, swift, swift) %{_localstatedir}/cache/swift
%dir %attr(0755, swift, root) %{_sharedstatedir}/swift
%dir %{python3_sitelib}/swift
%{_bindir}/swift-account-audit
%{_bindir}/swift-config
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{_bindir}/swift-drive-audit
%{_bindir}/swift-form-signature
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-manage-shard-ranges
%{_bindir}/swift-oldies
%{_bindir}/swift-orphans
%{_bindir}/swift-recon
%{_bindir}/swift-recon-cron
%{_bindir}/swift-reconciler-enqueue
%{_bindir}/swift-ring-builder
%{_bindir}/swift-ring-builder-analyzer
%{_bindir}/swift-ring-composer
%{python3_sitelib}/swift
%{python3_sitelib}/swift-%{upstream_version}-py?.*.egg-info
%exclude %{python3_sitelib}/swift/test

%files -n python3-swift-tests
%license LICENSE
%{python3_sitelib}/swift/test

%files account
%defattr(-,root,root,-)
%{_mandir}/man5/account-server.conf.5*
%{_mandir}/man1/swift-account-auditor.1*
%{_mandir}/man1/swift-account-info.1*
%{_mandir}/man1/swift-account-reaper.1*
%{_mandir}/man1/swift-account-replicator.1*
%{_mandir}/man1/swift-account-server.1*
%{_unitdir}/%{name}-account*.service
%dir %{_sysconfdir}/swift/account-server
%config(noreplace) %attr(640, swift, swift) %{_sysconfdir}/swift/account-server.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-info
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server

%files container
%defattr(-,root,root,-)
%{_mandir}/man5/container-server.conf.5*
%{_mandir}/man1/swift-container-auditor.1*
%{_mandir}/man1/swift-container-info.1*
%{_mandir}/man1/swift-container-replicator.1*
%{_mandir}/man1/swift-container-server.1*
%{_mandir}/man1/swift-container-sync.1*
%{_mandir}/man1/swift-container-updater.1*
%{_unitdir}/%{name}-container*.service
%dir %{_sysconfdir}/swift/container-server
%config(noreplace) %attr(640, swift, swift) %{_sysconfdir}/swift/container-server.conf
%config(noreplace) %attr(640, swift, swift) %{_sysconfdir}/swift/internal-client.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-deleter
%{_bindir}/swift-container-info
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_bindir}/swift-container-sync
%{_bindir}/swift-container-sharder

%files object
%defattr(-,root,root,-)
%{_mandir}/man5/object-server.conf.5*
%{_mandir}/man1/swift-object-auditor.1*
%{_mandir}/man1/swift-object-info.1*
%{_mandir}/man1/swift-object-reconstructor.1*
%{_mandir}/man1/swift-object-replicator.1*
%{_mandir}/man1/swift-object-server.1*
%{_mandir}/man1/swift-object-updater.1*
%{_unitdir}/%{name}-object.service
%{_unitdir}/%{name}-object@.service
%{_unitdir}/%{name}-object-auditor.service
%{_unitdir}/%{name}-object-auditor@.service
%{_unitdir}/%{name}-object-replicator.service
%{_unitdir}/%{name}-object-replicator@.service
%{_unitdir}/%{name}-object-reconstructor.service
%{_unitdir}/%{name}-object-reconstructor@.service
%{_unitdir}/%{name}-object-updater.service
%{_unitdir}/%{name}-object-updater@.service
%dir %{_sysconfdir}/swift/object-server
%config(noreplace) %attr(640, swift, swift) %{_sysconfdir}/swift/object-server.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-relinker
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{_bindir}/swift-object-reconstructor

%files proxy
%defattr(-,root,root,-)
%{_mandir}/man5/object-expirer.conf.5*
%{_mandir}/man5/proxy-server.conf.5*
%{_mandir}/man5/container-reconciler.conf.5*
%{_mandir}/man1/swift-container-reconciler.1*
%{_mandir}/man1/swift-object-expirer.1*
%{_mandir}/man1/swift-proxy-server.1*
%{_mandir}/man1/swift-reconciler-enqueue.1*
%{_mandir}/man1/swift-object-relinker.1*
%{_unitdir}/%{name}-container-reconciler.service
%{_unitdir}/%{name}-object-expirer.service
%{_unitdir}/%{name}-proxy.service
%dir %{_sysconfdir}/swift/proxy-server
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/container-reconciler.conf
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/proxy-server.conf
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/object-expirer.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/proxy-server
%{_bindir}/swift-container-reconciler
%{_bindir}/swift-object-expirer
%{_bindir}/swift-proxy-server

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc doc/build/html
%license  LICENSE
%endif

%changelog
