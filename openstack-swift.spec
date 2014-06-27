%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global release_name icehouse
%global milestone ...

Name:             openstack-swift
Version:          1.13.1
Release:          5%{?dist}
Summary:          OpenStack Object Storage (Swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/swift/%{release_name}/%{version}/+download/swift-%{version}.tar.gz

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
# Is it possible to supply an instance-style expirer unit for single-node?
Source6:          %{name}-proxy.service
Source61:         proxy-server.conf
Source62:         object-expirer.conf
Source20:         %{name}.tmpfs
Source7:          swift.conf

#
# patches_base=1.13.1
#
Patch0001: 0001-remove-runtime-requirement-on-pbr.patch
Patch0002: 0002-Add-fixes-for-building-the-doc-package.patch
Patch0003: 0003-Set-permissions-on-generated-ring-files.patch
Patch0004: 0004-properly-quote-www-authenticate-header-value.patch

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
Requires:         python-configobj
Requires:         python-eventlet >= 0.9.15
Requires:         python-greenlet >= 0.3.1
Requires:         python-paste-deploy
Requires:         python-simplejson
Requires:         pyxattr
Requires:         python-setuptools
Requires:         python-netifaces

BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils
Obsoletes:        openstack-swift-auth  <= 1.4.0

%description
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.

%package          account
Summary:          Account services for Swift
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      account
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package          container
Summary:          Container services for Swift
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      container
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package          object
Summary:          Object services for Swift
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         rsync >= 3.0

%description      object
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package          proxy
Summary:          A proxy server for Swift
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         python-keystoneclient
Requires:         openstack-swift-plugin-swift3

%description      proxy
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%package doc
Summary:          Documentation for %{name}
Group:            Documentation
%if 0%{?rhel} == 6
BuildRequires:    python-sphinx10 >= 1.0
%endif
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:    python-sphinx >= 1.0
%endif
# Required for generating docs (otherwise py-modindex.html is missing)
BuildRequires:    python-eventlet
BuildRequires:    pyxattr

%description      doc
OpenStack Object Storage (Swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}.

%prep
%setup -q -n swift-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1

#sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove bundled egg-info
rm -rf swift.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

# Remove dependency on pbr and set version as per rpm
sed -i 's/%RPMVERSION%/%{version}/; s/%RPMRELEASE%/%{release}/' swift/__init__.py

%build
%{__python} setup.py build
# Fails unless we create the build directory
mkdir -p doc/build
# Build docs
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{__python} setup.py build_sphinx
%endif
%if 0%{?rhel} == 6
export PYTHONPATH="$( pwd ):$PYTHONPATH"
SPHINX_DEBUG=1 sphinx-1.0-build -b html doc/source doc/build/html
%endif
# Fix hidden-file-or-dir warning
#rm doc/build/html/.buildinfo

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# systemd units
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-account.service
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_unitdir}/%{name}-account@.service
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_unitdir}/%{name}-account-replicator.service
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_unitdir}/%{name}-account-replicator@.service
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_unitdir}/%{name}-account-auditor.service
install -p -D -m 755 %{SOURCE26} %{buildroot}%{_unitdir}/%{name}-account-auditor@.service
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_unitdir}/%{name}-account-reaper.service
install -p -D -m 755 %{SOURCE28} %{buildroot}%{_unitdir}/%{name}-account-reaper@.service
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-container.service
install -p -D -m 755 %{SOURCE41} %{buildroot}%{_unitdir}/%{name}-container@.service
install -p -D -m 755 %{SOURCE43} %{buildroot}%{_unitdir}/%{name}-container-replicator.service
install -p -D -m 755 %{SOURCE44} %{buildroot}%{_unitdir}/%{name}-container-replicator@.service
install -p -D -m 755 %{SOURCE45} %{buildroot}%{_unitdir}/%{name}-container-auditor.service
install -p -D -m 755 %{SOURCE46} %{buildroot}%{_unitdir}/%{name}-container-auditor@.service
install -p -D -m 755 %{SOURCE47} %{buildroot}%{_unitdir}/%{name}-container-updater.service
install -p -D -m 755 %{SOURCE48} %{buildroot}%{_unitdir}/%{name}-container-updater@.service
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-object.service
install -p -D -m 755 %{SOURCE51} %{buildroot}%{_unitdir}/%{name}-object@.service
install -p -D -m 755 %{SOURCE53} %{buildroot}%{_unitdir}/%{name}-object-replicator.service
install -p -D -m 755 %{SOURCE54} %{buildroot}%{_unitdir}/%{name}-object-replicator@.service
install -p -D -m 755 %{SOURCE55} %{buildroot}%{_unitdir}/%{name}-object-auditor.service
install -p -D -m 755 %{SOURCE56} %{buildroot}%{_unitdir}/%{name}-object-auditor@.service
install -p -D -m 755 %{SOURCE57} %{buildroot}%{_unitdir}/%{name}-object-updater.service
install -p -D -m 755 %{SOURCE58} %{buildroot}%{_unitdir}/%{name}-object-updater@.service
install -p -D -m 755 %{SOURCE59} %{buildroot}%{_unitdir}/%{name}-object-expirer.service
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-proxy.service
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
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
install -p -D -m 660 %{SOURCE7} %{buildroot}%{_sysconfdir}/swift/swift.conf
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/account-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/container-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/object-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/proxy-server
# Swift run directories
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/tmpfiles.d/openstack-swift.conf
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

%clean
rm -rf %{buildroot}

%pre
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

%preun container
%systemd_preun %{name}-container.service
%systemd_preun %{name}-container-replicator.service
%systemd_preun %{name}-container-auditor.service
%systemd_preun %{name}-container-updater.service

%postun container
%systemd_postun %{name}-container.service
%systemd_postun %{name}-container-replicator.service
%systemd_postun %{name}-container-auditor.service
%systemd_postun %{name}-container-updater.service

%post object
%systemd_post %{name}-object.service
%systemd_post %{name}-object-replicator.service
%systemd_post %{name}-object-auditor.service
%systemd_post %{name}-object-updater.service

%preun object
%systemd_preun %{name}-object.service
%systemd_preun %{name}-object-replicator.service
%systemd_preun %{name}-object-auditor.service
%systemd_preun %{name}-object-updater.service

%postun object
%systemd_postun %{name}-object.service
%systemd_postun %{name}-object-replicator.service
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

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%doc etc/dispersion.conf-sample etc/drive-audit.conf-sample etc/object-expirer.conf-sample
%doc etc/swift.conf-sample
%{_mandir}/man5/dispersion.conf.5*
%{_mandir}/man1/swift-dispersion-populate.1*
%{_mandir}/man1/swift-dispersion-report.1*
%{_mandir}/man1/swift-get-nodes.1*
%{_mandir}/man1/swift-init.1*
%{_mandir}/man1/swift-orphans.1*
%{_mandir}/man1/swift-recon.1*
%{_mandir}/man1/swift-ring-builder.1*
%config(noreplace) %{_sysconfdir}/tmpfiles.d/openstack-swift.conf
%dir %{_sysconfdir}/swift
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/swift.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift
%dir %attr(0755, swift, root) %{_localstatedir}/cache/swift
%dir %attr(0755, swift, root) %{_sharedstatedir}/swift
%dir %{python_sitelib}/swift
%{_bindir}/swift-account-audit
%{_bindir}/swift-config
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{_bindir}/swift-recon*
%{_bindir}/swift-oldies
%{_bindir}/swift-orphans
%{_bindir}/swift-form-signature
%{_bindir}/swift-temp-url
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/cli
%{python_sitelib}/swift/common
%{python_sitelib}/swift/account
%{python_sitelib}/swift/obj
%{python_sitelib}/swift-%{version}*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%{_mandir}/man5/account-server.conf.5*
%{_mandir}/man1/swift-account-auditor.1*
%{_mandir}/man1/swift-account-info.1*
%{_mandir}/man1/swift-account-reaper.1*
%{_mandir}/man1/swift-account-replicator.1*
%{_mandir}/man1/swift-account-server.1*
%{_unitdir}/%{name}-account*.service
%dir %{_sysconfdir}/swift/account-server
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/account-server.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-info
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%{_mandir}/man5/container-server.conf.5*
%{_mandir}/man1/swift-container-auditor.1*
%{_mandir}/man1/swift-container-info.1*
%{_mandir}/man1/swift-container-replicator.1*
%{_mandir}/man1/swift-container-server.1*
%{_mandir}/man1/swift-container-sync.1*
%{_mandir}/man1/swift-container-updater.1*
%{_unitdir}/%{name}-container*.service
%dir %{_sysconfdir}/swift/container-server
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/container-server.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-info
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_bindir}/swift-container-sync
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/object-server.conf-sample etc/rsyncd.conf-sample
%{_mandir}/man5/object-server.conf.5*
%{_mandir}/man1/swift-object-auditor.1*
%{_mandir}/man1/swift-object-info.1*
%{_mandir}/man1/swift-object-replicator.1*
%{_mandir}/man1/swift-object-server.1*
%{_mandir}/man1/swift-object-updater.1*
%{_unitdir}/%{name}-object.service
%{_unitdir}/%{name}-object@.service
%{_unitdir}/%{name}-object-auditor.service
%{_unitdir}/%{name}-object-auditor@.service
%{_unitdir}/%{name}-object-replicator.service
%{_unitdir}/%{name}-object-replicator@.service
%{_unitdir}/%{name}-object-updater.service
%{_unitdir}/%{name}-object-updater@.service
%dir %{_sysconfdir}/swift/object-server
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/object-server.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample etc/object-expirer.conf-sample
%{_mandir}/man5/object-expirer.conf.5*
%{_mandir}/man5/proxy-server.conf.5*
%{_mandir}/man1/swift-object-expirer.1*
%{_mandir}/man1/swift-proxy-server.1*
%{_unitdir}/%{name}-object-expirer.service
%{_unitdir}/%{name}-proxy.service
%dir %{_sysconfdir}/swift/proxy-server
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/proxy-server.conf
%config(noreplace) %attr(640, root, swift) %{_sysconfdir}/swift/object-expirer.conf
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/proxy-server
%{_bindir}/swift-object-expirer
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Fri Jun 27 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.13.1-5
- Fix CVE-2014-3497, unquoted realm in WWW-Authenticate

* Tue Jun 24 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.13.1-4
- Move default ports from 600x to 620x (#1107907 and a dozen of others)

* Mon Jun 23 2014 Pete Zaitcev - 1.13.1-3
- Drop python-swiftclient to implement bz#1058131 in Rawhide

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 19 2014 Pádraig Brady <pbrady@redhat.com> - 1.13.1-1
- Update to Icehouse release

* Sat Apr 12 2014 Alan Pevec <apevec@redhat.com> 1.13.1-0.1.rc2
- Update to Icehouse milestone 1.13.1.rc2

* Fri Jan 31 2014 Alan Pevec <apevec@redhat.com> 1.12.0-1
- Update to Icehouse milestone 1.12.0

* Fri Jan 03 2014 Pádraig Brady <pbrady@redhat.com> 1.11.0-1
- Update to first icehouse release 1.11.0

* Wed Dec 04 2013 Pete Zaitcev <zaitcev@redhat.com> 1.10.0-3
- Change config modes to 640, like in every other OpenStack project

* Fri Oct 18 2013 Pádraig Brady <pbrady@redhat.com> 1.10.0-2
- Update to Havana GA
- Fix service startup issue due to bad depencency checking (#1020449)
- add swift home directory for signing_dir (#967631)

* Wed Oct 09 2013 Pádraig Brady <pbrady@redhat.com> 1.10.0-0.1.rc1
- Update to 1.10.0 RC1

* Mon Sep 23 2013 Pete Zaitcev <zaitcev@redhat.com> 1.9.1-2
- Move account/ to base package like we did for obj/ in 1.7.5-4

* Thu Sep 19 2013 Pete Zaitcev <zaitcev@redhat.com> 1.9.1-1
- Update to 1.9.1, includes CVE-2013-4155
- Includes unfortunately standards-compliant XML listings, to be fixed
- Reseller prefix in Keystone must end with an underscore
- Make only proxy depend on openstack-swift-plugin-swift3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Pete Zaitcev <zaitcev@redhat.com> 1.9.0-1
- Update to 1.9.0

* Fri Apr 05 2013 Derek Higgins <derekh@redhat.com> - 1.8.0-2
- change path to middleware in proxy conf file
- add dependency for python-keystoneclient for proxy

* Thu Apr 4 2013 Pete Zaitcev <zaitcev@redhat.com> 1.8.0-1
- Update to 1.8.0; this is the "Grizzly" release of OpenStack

* Mon Mar 18 2013 Pete Zaitcev <zaitcev@redhat.com> 1.7.6-2
- Move ownership of /var/cache/swift to main package per Zane's comments

* Sun Mar 10 2013 Alan Pevec <apevec@redhat.com> 1.7.6-1
- Update to 1.7.6

* Thu Feb 14 2013 Pete Zaitcev <zaitcev@redhat.com> - 1.7.5-4
- Fix the moved object-expirer so it runs with object is not installed

* Thu Feb 14 2013 Pete Zaitcev <zaitcev@redhat.com> - 1.7.5-3
- Add /var/cache/swift, by bz#870409, equally affects all Fedora versions

* Mon Jan 28 2013 Pete Zaitcev <zaitcev@redhat.com> - 1.7.5-2
- Drop dependency on python-webob, because Swift uses an in-tree swob now
- Update scriptlets to use macro systemd_postun and friends (bz#850016)
- Drop systemd-sysv-convert
- Relocate object-expirer into the proxy bundle
- Add the expirer configuration, multi-node only

* Mon Dec 03 2012 Derek Higgins <derekh@redhat.com> - 1.7.5-1
- Update to 1.7.5
- adding swift-bench-client
- removing dup dependency on python-netifaces
- changing README -> README.md

* Mon Nov 5 2012 Pete Zaitcev <zaitcev@redhat.com> - 1.7.4-2
- Add missing unit files bz#807170

* Thu Sep 27 2012 Derek Higgins <derekh@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Thu Sep 20 2012 Derek Higgins <derekh@redhat.com> 1.7.2-1
- Update to 1.7.2

* Fri Sep 14 2012 Derek Higgins <derekh@redhat.com> 1.7.0-2
- Adding config files

* Thu Sep 13 2012 Derek Higgins <derekh@redhat.com> 1.7.0-1
- Update to 1.7.0

* Mon Aug 13 2012 Alan Pevec <apevec@redhat.com> 1.6.0-1
- Update to 1.6.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Alan Pevec <apevec@redhat.com> 1.5.0-1
- Update to 1.5.0

* Thu Mar 22 2012 Alan Pevec <apevec@redhat.com> 1.4.8-1
- Update to 1.4.8

* Fri Mar 09 2012 Alan Pevec <apevec@redhat.com> 1.4.7-1
- Update to 1.4.7

* Mon Feb 13 2012 Alan Pevec <apevec@redhat.com> 1.4.6-1
- Update to 1.4.6
- Switch from SysV init scripts to systemd units rhbz#734594

* Thu Jan 26 2012 Alan Pevec <apevec@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Alan Pevec <apevec@redhat.com> 1.4.4-1
- Update to 1.4.4

* Wed Nov 23 2011 David Nalley <david@gnsa.us> -1.4.3-2
* fixed some missing requires

* Sat Nov 05 2011 David Nalley <david@gnsa.us> - 1.4.3-1
- Update to 1.4.3
- fix init script add, registration, deletion BZ 685155
- fixing BR to facilitate epel6 building

* Tue Aug 23 2011 David Nalley <david@gnsa.us> - 1.4.0-2
- adding uid:gid for bz 732693

* Wed Jun 22 2011 David Nalley <david@gnsa.us> - 1.4.1-1
- Update to 1.4.0
- change the name of swift binary from st to swift

* Sat Jun 04 2011 David Nalley <david@gnsa.us> - 1.4.0-1
- Update to 1.4.0

* Fri May 20 2011 David Nalley <david@gnsa.us> - 1.3.0-1
- Update to 1.3.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Silas Sewell <silas@sewell.ch> - 1.1.0-1
- Update to 1.1.0

* Sun Aug 08 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-5
- Update for new Python macro guidelines
- Use dos2unix instead of sed
- Make gecos field more descriptive

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-4
- Rename to openstack-swift

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-3
- Fix return value in swift-functions

* Tue Jul 27 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-2
- Add swift user
- Update init scripts

* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
