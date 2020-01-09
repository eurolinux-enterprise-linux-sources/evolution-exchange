%define intltool_version 0.35.5
%define libsoup_version 2.28.2-4

%define evo_base_version 2.32
%define eds_api_version 1.2

# Make sure the evolution package is upgraded first, or else this variable
# will come up empty and lead to the following libtool error.
#
#      libtool: link: only absolute run-paths are allowed
#
# The error is caused by the -R ${plibdir} substitution below; -R requires
# an argument and libtool does not complain until late in the game.  Seems
# like it could be smarter about this.
%define plibdir %(pkg-config evolution-shell --variable=privlibdir 2>/dev/null)

%define evo_ews_name evolution-ews-gnome-3-0.gitcc16df2

### Abstract ###

Name: evolution-exchange
Version: 2.32.3
Release: 18%{?dist}
Group: Applications/Productivity
Summary: Evolution plugin to interact with MS Exchange Server
License: GPLv2+
URL: http://projects.gnome.org/evolution/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source: http://download.gnome.org/sources/%{name}/2.32/%{name}-%{version}.tar.bz2
Source1: evolution-ews-gnome-3-0.gitcc16df2.tar.gz

Provides: evolution-connector = %{version}-%{release}
Obsoletes: evolution-connector < %{version}-%{release}

### Patches ###

Patch01: evolution-exchange-2.10.1-fix-64bit-acinclude.patch

# Forgot to include some architecture documents in the tarball.
# Remove references to them in evolution-exchange-docs.sgml to
# avoid a build break.
Patch02: evolution-exchange-2.32.3-unshipped-arch-docs.patch

# Translation updates
Patch03: evolution-exchange-2.32.3-translation-updates-eex.patch

# Address some of the Coverity scan issues
Patch04: evolution-exchange-2.32.3-covscan-issues-eex.patch

## evolution-ews patches, with offset 100 ##

# sync (backport) 3.8.2 changes with gnome-3-0 branch at git commit cc16df2
Patch101: evolution-ews-gnome-3-0.gitcc16df2-sync-with-3.8.2.patch

# sync ews with 3.8.3 changes
Patch102: evolution-ews-gnome-3-0.gitcc16df2-sync-with-3.8.3.patch

# ews check for account completion blocks an account with None receiving type
Patch103: evolution-ews-gnome-3-0.gitcc16df2-account-type-check.patch

# RH bug #984531
Patch104: evolution-ews-gnome-3-0.gitcc16df2-book-double-free-crash.patch

# sync ews with 3.8.4 changes, except of GNOME-bug #703181
Patch105: evolution-ews-gnome-3-0.gitcc16df2-sync-with-3.8.4.patch

# RH bug #984961
Patch106: evolution-ews-gnome-3-0.gitcc16df2-multiple-contacts-remove.patch

# RH bug #985015
Patch107: evolution-ews-gnome-3-0.gitcc16df2-empty-search-hides-contacts.patch

# sync ews with 3.8.5 changes
Patch108: evolution-ews-gnome-3-0.gitcc16df2-sync-with-3.8.5.patch

# Translation updates
Patch109: evolution-ews-gnome-3-0.gitcc16df2-translation-updates-ews.patch

# regression of GNOME bug #702922
Patch110: evolution-ews-gnome-3-0.gitcc16df2-3.8.5-create-appointments.patch

# RH bug #1006336
Patch111: evolution-ews-gnome-3-0.gitcc16df2-get-attachments-prototype-fix.patch

# RH bug #1009470
Patch112: evolution-ews-gnome-3-0.gitcc16df2-no-offline-sync-gal-crash.patch

# RH bug #1005888
Patch113: evolution-ews-gnome-3-0.gitcc16df2-no-alarm-after-start-capability.patch

# RH bug #1018301
Patch114: evolution-ews-gnome-3-0.gitcc16df2-free-busy-fetch-and-crash.patch

# RH bug #1019434
Patch115: evolution-ews-gnome-3-0.gitcc16df2-searchable-gal.patch

# RH bug #1160279
Patch116: evolution-ews-gnome-3-0.gitcc16df2-camel-session-global-variable.patch

# RH bug 976364
Patch117: evolution-ews-gnome-3-0.gitcc16df2-translation-updates-ews2.patch

### Dependencies ###

Requires: gnutls
Requires: openldap

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: db4-devel
BuildRequires: evolution-data-server-devel >= 2.32.3-9
BuildRequires: evolution-devel >= 2.32.3-27
BuildRequires: gettext
BuildRequires: gnome-common
BuildRequires: gnutls-devel
BuildRequires: gtk-doc
BuildRequires: intltool >= %{intltool_version}
BuildRequires: libsoup-devel >= %{libsoup_version}
BuildRequires: libtool >= 1.5
BuildRequires: openldap-evolution-devel
BuildRequires: openssl-devel
BuildRequires: krb5-devel

%description
This package enables added functionality to Evolution when used with a 
Microsoft Exchange Server 2003. It contains also Exchange Web Services (EWS)
connector, which can connect to Microsoft Exchange 2007 and later servers.

%prep
%setup -q -n evolution-exchange-%{version}
%patch01 -p1 -b .fix-64bit-acinclude
%patch02 -p1 -b .unshipped-arch-docs
%patch03 -p1 -b .translation-updates-eex
%patch04 -p1 -b .covscan-issues-eex

# evolution-ews setup - is as unpacked a subdirectory of evolution

%setup -T -D -a 1

pushd %{evo_ews_name}
%patch101 -p1 -b .sync-with-3.8.2
%patch102 -p1 -b .sync-with-3.8.3
%patch103 -p1 -b .account-type-check
%patch104 -p1 -b .book-double-free-crash
%patch105 -p1 -b .sync-with-3.8.4
%patch106 -p1 -b .multiple-contacts-remove
%patch107 -p1 -b .empty-search-hides-contacts
%patch108 -p1 -b .sync-with-3.8.5
%patch109 -p1 -b .translation-updates-ews
%patch110 -p1 -b .3.8.5-create-appointments
%patch111 -p1 -b .get-attachments-prototype-fix
%patch112 -p1 -b .no-offline-sync-gal-crash
%patch113 -p1 -b .no-alarm-after-start-capability
%patch114 -p1 -b .free-busy-fetch-and-crash
%patch115 -p1 -b .searchable-gal
%patch116 -p1 -b .camel-session-global-variable
%patch117 -p1 -b .translation-updates-ews2

popd

%build
export CPPFLAGS="-I%{_includedir}/et"
export CFLAGS="$RPM_OPT_FLAGS -DLDAP_DEPRECATED -fPIC"
# Set LIBS so that configure will be able to link with static LDAP libraries,
# which depend on Cyrus SASL and OpenSSL.
if pkg-config openssl ; then
	export LIBS="-lsasl2 `pkg-config --libs openssl`"
else
	export LIBS="-lsasl2 -lssl -lcrypto"
fi

# newer versions of openldap are built with Mozilla NSS crypto, so also need
# those libs to link with the static ldap libs
if pkg-config nss ; then
    export LIBS="$LIBS `pkg-config --libs nss`"
else
    export LIBS="$LIBS -lssl3 -lsmime3 -lnss3 -lnssutil3 -lplds4 -lplc4 -lnspr4"
fi

# Regenerate configure to pick up acinclude.m4 changes.
autoreconf --force --install

%configure \
  --enable-gtk-doc \
  --with-openldap=%{_libdir}/evolution-openldap \
  --with-static-ldap \
  --with-krb5=%{_prefix}

make %{?_smp_mflags} LDFLAGS="-R %{plibdir}"

# evolution-ews build part

pushd %{evo_ews_name}
autoreconf --force --install
%configure --with-internal-lzx
make %{?_smp_mflags}
popd

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libebookbackendexchange.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libecalbackendexchange.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelexchange.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution/%{evo_base_version}/plugins/liborg-gnome-exchange-operations.la

%find_lang evolution-exchange-%{evo_base_version}

# evolution-ews install part

pushd %{evo_ews_name}
make install DESTDIR=$RPM_BUILD_ROOT

# Remove files we don't want packaged (no devel subpackage).
rm -r $RPM_BUILD_ROOT%{_includedir}/evolution-data-server-%{eds_api_version}/
rm -r $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/evolution-exchange
rm $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-%{eds_api_version}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-%{eds_api_version}/*.so
rm $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-%{eds_api_version}/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/evolution/%{evo_base_version}/plugins/*.la
rm $RPM_BUILD_ROOT%{_libdir}/evolution/%{evo_base_version}/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libeews-1.2.la
rm $RPM_BUILD_ROOT%{_libdir}/libeews-1.2.so
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libeews-1.2.pc

%find_lang evolution-ews

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{evo_ews_name}
cp COPYING $RPM_BUILD_ROOT%{_defaultdocdir}/%{evo_ews_name}/
cp NEWS $RPM_BUILD_ROOT%{_defaultdocdir}/%{evo_ews_name}/
cp README $RPM_BUILD_ROOT%{_defaultdocdir}/%{evo_ews_name}/
popd

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/apps_exchange_addressbook-%{evo_base_version}.schemas > /dev/null

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files -f evolution-exchange-%{evo_base_version}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS docs/active-directory
%doc docs/autoconfig docs/debug docs/forms
%doc docs/http
%{_bindir}/exchange-connector-setup-%{evo_base_version}
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelexchange.so
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelexchange.urls
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libebookbackendexchange.so
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libecalbackendexchange.so
%{_libdir}/evolution/%{evo_base_version}/plugins/liborg-gnome-exchange-operations.so
%{_libdir}/evolution/%{evo_base_version}/plugins/org-gnome-exchange-operations.eplug
%{_datadir}/evolution/%{evo_base_version}/errors/org-gnome-exchange-operations.error

%dir %{_datadir}/evolution-exchange
%dir %{_datadir}/evolution-exchange/%{evo_base_version}
%dir %{_datadir}/evolution-exchange/%{evo_base_version}/images
%dir %{_datadir}/evolution-exchange/%{evo_base_version}/ui
%{_datadir}/evolution-exchange/%{evo_base_version}/images/*
%{_datadir}/evolution-exchange/%{evo_base_version}/ui/*
%{_sysconfdir}/gconf/schemas/apps_exchange_addressbook-%{evo_base_version}.schemas

# evolution-ews files - part of main evolution rpm

# replaces the %doc section for evolution-ews
%{_defaultdocdir}/%{evo_ews_name}/*
%{_libdir}/libeews-1.2.so.*
%{_libdir}/evolution-data-server-%{eds_api_version}/libewsutils.so.*
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libebookbackendews.so
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libecalbackendews.so
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelews.so
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelews.urls
%{_libdir}/evolution/%{evo_base_version}/modules/module-ews-ui-config.so
%{_libdir}/evolution/%{evo_base_version}/plugins/liborg-gnome-exchange-ews.so
%{_libdir}/evolution/%{evo_base_version}/plugins/org-gnome-exchange-ews.eplug
%{_datadir}/locale/*/*/evolution-ews.mo

%changelog
* Mon Mar 07 2016 Milan Crha <mcrha@redhat.com> - 2.32.3-18.el6
- Add patch for RH bug #976364 (evolution-ews update translations)

* Mon Jan 05 2015 Milan Crha <mcrha@redhat.com> - 2.32.3-17.el6
- Add patch for RH bug #1160279 (evolution-ews runtime issue with Camel session global variable)

* Fri Oct 18 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-16.el6
- Add patch for RH bug #1019434 (evolution-ews searchable GAL)

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-15.el6
- Add patch for RH bug #1018301 (evolution-ews crash and broken Free/Busy fetch)

* Wed Sep 18 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-14.el6
- Add patch for RH bug #1009470 (evolution-ews crash when GAL not marked for offline sync)
- Add patch for RH bug #1005888 (evolution-ews add 'no-alarm-after-start' calendar capability)

* Tue Sep 10 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-13.el6
- Add patch for RH bug #1006336 (evolution-ews fails to download attachments)

* Fri Aug 23 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-12.el6
- Do not ship gtk-doc files (RH bug #1000325)

* Fri Aug 16 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-11.el6
- Add patch to regression of GNOME bug #702922 (Cannot create appointments)

* Wed Aug 14 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-10.el6
- Add patch for some issues found by Coverity scan in evolution-exchange

* Wed Aug 14 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-9.el6
- Update translation patch for evolution-exchange

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-8.el6
- Add patches for translation updates

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-7.el6
- Add patch for evolution-ews to match 3.8.5 upstream release

* Thu Jul 25 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-6.el6
- Update patch for evolution-ews to match 3.8.4 upstream release (RH bug #988356)

* Wed Jul 24 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-5.el6
- Add patch for evolution-ews to match 3.8.4 upstream release
- Add patch for RH bug #984961 (evolution-ews multiple contacts remove hang)
- Add patch for RH bug #985015 (evolution-ews empty search hides contacts)

* Mon Jul 15 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-4.el6
- Add patch for RH bug #984531 (evolution-ews double-free in book backend)

* Mon Jul 08 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-3.el6
- Add patch for evolution-ews to fix account type check in new account wizard

* Mon Jun 10 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-2.el6
- Add patch for evolution-ews to match 3.8.3 upstream release

* Thu Jun 06 2013 Milan Crha <mcrha@redhat.com> - 2.32.3-1.el6
- Rebase to 2.32.3
- Bundle evolution-ews as part of this, with feature parity of its 3.8.2 release

* Wed Mar 31 2010 Matthew Barnes <mbarnes@redhat.com> - 2.28.3-2.el6
- Don't install libtool archives (RH bug #564489).

* Tue Mar 02 2010 Matthew Barnes <mbarnes@redhat.com> - 2.28.3-1.el6
- Update to 2.28.3

* Wed Jan 13 2010 Milan Crha <mcrha@redhat.com> - 2.28.2-3.el6
- Remove .m4 extension from a patch

* Wed Jan 13 2010 Milan Crha <mcrha@redhat.com> - 2.28.2-2.el6
- Correct Source URL
- Disable build on s390/s390x, because evolution is too

* Mon Dec 14 2009 Milan Crha <mcrha@redhat.com> - 2.28.2-1.fc12
- Update to 2.28.2

* Mon Oct 19 2009 Milan Crha <mcrha@redhat.com> - 2.28.1-1.fc12
- Update to 2.28.1

* Mon Sep 21 2009 Milan Crha <mcrha@redhat.com> - 2.28.0-1.fc12
- Update to 2.28.0

* Mon Sep 07 2009 Milan Crha <mcrha@redhat.com> - 2.27.92-1.fc12
- Update to 2.27.92

* Sun Aug 30 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.91-3.fc12
- Rebuild again.

* Thu Aug 27 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.91-2.fc12
- Rebuild with old OpenSSL, er something...

* Mon Aug 24 2009 Milan Crha <mcrha@redhat.com> - 2.27.91-1.fc12
- Update to 2.27.91

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.27.90-2
- rebuilt with new openssl

* Mon Aug 10 2009 Milan Crha <mcrha@redhat.com> - 2.27.90-1.fc12
- Update to 2.27.90

* Mon Jul 27 2009 Milan Crha <mcrha@redhat.com> - 2.27.5-1.fc12
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.4-1.fc12
- Update to 2.27.4

* Wed Jul 01 2009 Milan Crha <mcrha@redhat.com> - 2.27.3-2.fc12
- Rebuild against newer gcc

* Mon Jun 15 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.3-1.fc12
- Update to 2.27.3

* Fri May 29 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.2-2.fc12
- Remove patch for GNOME bug #443022 (obsolete).

* Fri May 29 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.2-1.fc12
- Update to 2.27.2
- Remove strict_build_settings since the settings are used upstream now.

* Mon May 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.1-1.fc12
- Update to 2.27.1
- Bump evo_major to 2.28.

* Mon Apr 13 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.1-1.fc11
- Update to 2.26.1

* Mon Mar 16 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.0-1.fc11
- Update to 2.26.0

* Mon Mar 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.92-1.fc11
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.91-1.fc11
- Update to 2.25.91

* Fri Feb 06 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.90-2.fc11
- Update BuildRoot, License, Source and URL tags.
- Require gnome-common so we don't have to patch it out.

* Mon Feb 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.90-1.fc11
- Update to 2.25.90

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.5-1.fc11
- Update to 2.25.5
- Ditch eds_version and evo_version and use our own version.  This will
  keep evolution, evolution-exchange and evolution-data-server versions
  in lockstep from now on.

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.25.4-2.fc11
- rebuild with new openssl

* Tue Jan 06 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.4-1.fc11
- Update to 2.25.4

* Mon Dec 15 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-1.fc11
- Update to 2.25.3

* Mon Dec 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.2-1.fc11
- Update to 2.25.2

* Mon Nov 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.1-1.fc11
- Update to 2.25.1
- Bump evo_major to 2.26.
- Bump evo_version and eds_version to 2.25.1.

* Tue Oct 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.1-2.fc10
- Bump eds_version to 2.24.1 (unfortunately).

* Tue Oct 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.1-1.fc10
- Update to 2.24.1

* Mon Sep 22 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.0-1.fc10
- Update to 2.24.0

* Thu Sep 18 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.92-2.fc10
- Fix unowned directories (RH bug #462346).

* Mon Sep 08 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.92-1.fc10
- Update to 2.23.92

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.91-1.fc10
- Update to 2.23.91
- Add -Werror to CFLAGS.

* Wed Aug 20 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.90-1.fc10
- Update to 2.23.90
- Bump eds_version to 2.23.90.1.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.6-1.fc10
- Update to 2.23.6

* Mon Jul 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.5-1.fc10
- Update to 2.23.5
- Bump eds_version to 2.23.5.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-2
- fix license tag
- fix source url

* Mon Jun 16 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.4-1.fc10
- Update to 2.23.4

* Mon Jun 02 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.3-1.fc10
- Update to 2.23.3

* Mon May 12 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.2-1.fc10
- Update to 2.23.2

* Mon Apr 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-1.fc10
- Update to 2.23.1
- Bump evo_major to 2.24.
- Bump evo_version to 2.23.1.
- Bump eds_version to 2.23.1.

* Mon Apr 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.1-1.fc9
- Update to 2.22.1

* Mon Mar 10 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.0-1.fc9
- Update to 2.22.0

* Mon Feb 25 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.92-1.fc9
- Update to 2.21.92
- Disable -Werror since libical now insists on emitting #warnings.

* Wed Feb 13 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.91-2.fc9
- Rebuild against libsoup 2.3.2.

* Mon Feb 11 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.91-1.fc9
- Update to 2.21.91
- Disable strict-aliasing due to GNOME bug #316221 and GCC 4.3.

* Mon Jan 28 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.90-1.fc9
- Update to 2.21.90
- Update build requirements.

* Mon Jan 14 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.5-1.fc9
- Update to 2.21.5

* Mon Dec 17 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.4-1.fc9
- Update to 2.21.4
- Bump eds_version to 2.21.4 for new Camel functions.

* Wed Dec 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.3-2.fc9
- Bump eds_version to 2.21.3.

* Mon Dec 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.3-1.fc9
- Update to 2.21.3

* Mon Nov 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.2-1.fc9
- Update to 2.21.2

* Sun Nov 04 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-2.fc9
- Remove obsolete patches.

* Mon Oct 29 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-1.fc9
- Update to 2.21.1
- Remove redundant requirements.
- Bump evo_version and eds_version to 2.21.1.

* Mon Oct 15 2007 Milan Crha <mcrha@redhat.com> - 2.12.1-1.fc8
- Update to 2.12.1
- Removed evolution-exchange-2.11.92-compilation-breakage.patch (fixed upstream).
- Removed evolution-exchange-2.12.0-warnings.patch (fixed upstream).

* Mon Sep 17 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-1.fc8
- Update to 2.12.0

* Mon Sep 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.92-1.fc8
- Update to 2.11.92

* Tue Aug 28 2007 Milan Crha <mcrha@redhat.com> - 2.11.91-1.fc8
- Update to 2.11.91
- Removed patch for GNOME bug #466987 (fixed upstream).

* Wed Aug 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.90-1.fc8
- Update to 2.11.90
- Add patch for GNOME bug #466987 (glibc redefines "open").
- Remove -DGNOME_DISABLE_DEPRECATED since GnomeDruid is now deprecated.

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.6.1-1.fc8
- Update to 2.11.6.1
- Remove patch for GNOME bug #380534 (fixed upstream).

* Fri Jul 27 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.5-2.fc8
- Add patch for GNOME bug #380534 (clarify version requirements).

* Mon Jul 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.5-1.fc8
- Update to 2.11.5

* Mon Jun 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.4-1.fc8
- Update to 2.11.4
- Remove patch for GNOME bug #444101 (fixed upstream).

* Wed Jun 06 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3.1-2.fc8
- Rename package to evolution-exchange, obsoletes evolution-connector.

* Mon Jun 04 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3.1-1.fc8
- Update to 2.11.3.1
- Add patch for GNOME bug #444101 (new compiler warnings).
- Remove patch for GNOME bug #439579 (fixed upstream).

* Fri Jun 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.2-2.fc8
- List static ldap libraries in the proper order.
- Compile with -Werror.

* Fri May 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.2-1.fc8
- Update to 2.11.2
- Bump evo_version to 2.11.0, eds_version to 1.11.0, and evo_major to 2.12.
- Remove evolution-exchange-2.5.3-fix-marshaller.patch (obsolete).
- Remove patch for GNOME bug #405916 (fixed upstream).

* Thu Apr 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-3.fc7
- Regenerate configure to pick up 64-bit changes to acinclude.m4.
- Require autoconf and automake to build.

* Thu Apr 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-2.fc7
- Fix a misnamed macro (RH bug #237807).

* Mon Apr 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-1.fc7
- Update to 2.10.1
- Add -Wdeclaration-after-statement to strict build settings.

* Mon Mar 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-1.fc7
- Update to 2.10.0

* Tue Feb 27 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.92-2.fc7
- Add missing libgnomeprint22 requirements.
- Add flag to disable deprecated GNOME symbols.

* Mon Feb 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.92-1.fc7
- Update to 2.9.92
- Reverting -Werror due to bonobo-i18n.h madness.
- Add minimum version to intltool requirement (currently >= 0.35.5).

* Mon Feb 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.91-2.fc7
- Fix some 64-bit compiler warnings.

* Mon Feb 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.91-1.fc7
- Update to 2.9.91
- Compile with -Werror.
- Add BuildRequires db4-devel.
- Add flags to disable deprecated Pango and GTK+ symbols.
- Add patch for GNOME bug #405916 (fix all compiler warnings).
- Remove patch for GNOME bug #360240 (superseded).

* Sun Jan 21 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-2.fc7
- Revise evolution-exchange-2.7.2-no_gnome_common.patch so that we no longer
  have to run autoconf before building.

* Mon Jan 08 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-1.fc7
- Update to 2.9.5
- Remove patch for GNOME bug #357660 (fixed upstream).

* Tue Dec 19 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.4-1.fc7
- Update to 2.9.4
- Require evolution-data-server-1.9.4.

* Mon Dec 04 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-1.fc7
- Update to 2.9.3
- Require evolution-data-server-1.9.3.
- Add %post section to install new schemas file.
- Remove evolution-exchange-2.8.1-bump-requirements.patch (fixed upstream).

* Tue Oct 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-2.fc7
- Add patch and rebuild for next Evolution development cycle.

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-1.fc7
- Update to 2.8.1
- Use stricter build settings.
- Add patch for Gnome.org bug #360340 ("unused variable" warnings).

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.8.0-3.fc6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-2.fc6
- Add patch for Gnome.org bug #357660.

* Mon Sep  4 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-1.fc6
- Update to 2.8.0
- Remove patch for Gnome.org bug #349949 (fixed upstream).

* Mon Aug 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-1
- Update to 2.7.92

* Mon Aug  7 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-2
- Rebuild against correct evolution-data-server.

* Mon Aug  7 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-1
- Update to 2.7.91

* Sat Aug  5 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.90-3
- Fix eds_major (bumped it when I shouldn't have).

* Sat Aug  5 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.90-1
- Update to 2.7.90

* Wed Jul 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.7.3-2.1
- rebuild

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.3-2
- Rebuild 

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Wed May 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.2-2
- Add BuildRequires for gtk-doc (closes #192251).
- Require specific versions of GNU Autotools packages for building.
- Various spec file cleanups.

* Wed May 17 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.2-1
- Update to 2.7.2
- Update spec file to run the autotools itself after patching.
- Remove evolution-exchange-2.7.1-fix_version.patch; fixed upstream.
- Remove unused or obsolete patches:
  evolution-connector-2.0.2-domain-fix.patch
  evolution-connector-2.7.2-generated-autotool.patch
  ximian-connector-2.1.4-fix-convenience-libraries.patch
  ximian-connector-2.2.2-install-debug-utilities.patch
  ximian-connector-2.2.2-noinst-ltlibraries.patch
- Add evolution-exchange-2.7.2-no_gnome_common.patch; removes
  GNOME_COMPILE_WARNINGS from configure.in.

* Sun May 14 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.1-2
- Forgot to add evolution-exchange-2.7.1-fix_version.patch to CVS.

* Fri May 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.1-1
- Update to 2.7.1
- Add some comments about the `plibdir' variable.
- Add --enable-gtk-doc to the `configure' invocation.
- Add temporary patch evolution-exchange-2.7.1-fix_version.patch.

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.6.1-2
- Update to 2.6.1

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.com> - 2.6.0-1
- 2.6.0

* Tue Feb 28 2006 Ray Strode <rstrode@redhat.com> - 2.5.92-1
- 2.5.92

* Wed Feb 15 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.91-1
- 2.5.91
- fix missing declarations (patch 301)

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 2.5.9.0-2.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.9.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.9.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Ray Strode <rstrode@redhat.com> - 2.5.9.0-2
- add builddeps (bug 137879)

* Mon Jan 30 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.9.0-1
- 2.5.9.0
- regenerate patch 200
- enable parallel make

* Wed Jan 25 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.5.1-1
- 2.5.5.1
- regenerate patch 200

* Wed Jan  4 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-1
- 2.5.4

* Mon Dec 19 2005 David Malcolm <dmalcolm@redhat.com> - 2.5.3-1
- 2.5.3
- regenerate patch 200
- add patch to use correct marshalling code (patch 300)
- dropped glob of etspec files

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 David Malcolm <dmalcolm@redhat.com> - 2.5.2-1
- 2.5.2
- bump evo_major from 2.4 to 2.6
- bump evolution requirement from 2.4.1 to 2.5.2 to ensure we get an appropriate
  underlying version of evolution
- regenerate patch 200

* Fri Dec  2 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.2-1
- 2.4.2
- regenerate patch 200; forcing regeneration of intltool scripts to 
  keep them in sync with our aclocal/intltool.m4
 
* Tue Nov 29 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-3
- add -DLDAP_DEPRECATED to CFLAGS (#172999)

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 2.4.1-2
- rebuilt with new openssl

* Tue Oct 18 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-1
- 2.4.1
- bump evolution requirement to 2.4.1 and libsoup requirement to 2.2.6.1
- fix URL to point to 2.4, not 2.3

* Thu Sep 15 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-2
- rebuild for new e-d-s

* Wed Sep  7 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.0-1
- 2.4.0
- Regenerated patch 200

* Wed Aug 24 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.8-1
- 2.3.8
- Regenerated patch 200
- Add -Werror-implicit-function-declaration to CFLAGS; make it use RPM_OPT_FLAGS

* Mon Aug 15 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.7-2
- rebuild

* Tue Aug  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.7-1
- 2.3.7
- Bump evolution requirement from 2.3.5.1 to 2.3.7
- Bump libsoup requirement from 2.2.2 to 2.2.5
- Remove ximian-connector-2.0.4-fix-sync-callback.patch; a slightly modified 
  version of this is now in the upstream tarball (#139393)

* Mon Aug  8 2005 Tomas Mraz <tmraz@redhat.com> - 2.3.6-3
- rebuild with new gnutls

* Mon Aug  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6-2
- bump evo_major from 2.2 to 2.4
- Removed the various test programs (they no longer exist in the upstream 
  tarball)
- Renamed more instances of "ximian-connector" to "evolution-exchange" as
  appropriate.

* Thu Jul 28 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6-1
- 2.3.6

* Tue Jul 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.5-2
- increase evolution requirement to 2.3.5.1

* Mon Jul 25 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.5-1
- 2.3.5
- Changed various references to source tarball name from ximian-connector to
  evolution-exchange and updated the URL
- Remove Patch101 and Patch102 from autotool source patches and regenerate 
  resulting post-autotool patch

* Wed May 18 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-5
- add Aaron Gaudio's patch to fix PDA syncronization (#139393)

* Tue May 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-4
- Install the debug utilities from the "lib" subdirectory; renumber patches 
  accordingly; regenerate the generated patch

* Wed May  4 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-3
- updated noinst patch: libexchange is now a convenience library again; use -R
syntax to express path to Evolution's private libraries rather than -Wl since
libtool cannot properly intrepret the latter; regenerated resulting patch.

* Mon May  2 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-2
- disabling noinst patch as not yet applied

* Mon Apr 11 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-1
- 2.2.2

* Thu Mar 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.1-1
- 2.2.1
- Regenerated autotool patch

* Wed Mar  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-1
- 2.2.0
- Updated evolution dependency to 2.2.0

* Tue Mar  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-3
- reapply the 64bit multilib LDAP patch, and regenerate the autotool patch accordingly

* Tue Mar  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-2
- actually remove the convenience library patches this time

* Wed Feb  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-1
- Update from unstable upstream 2.1.5 to 2.1.6
- Require evolution 2.1.6
- Removed patches for convenience libraries as these are now upstream

* Wed Feb  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.5-1
- Update from unstable upstream 2.1.4 to 2.1.5
- Require evolution 2.1.5

* Mon Feb  7 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.4-3
- Patch to fix non-portable usage of convenience libraries; reorganised the hand-edited vs generated patches (generated patch is 990K in size)
- Add "-Wl" to make arguments to escape usage of -rpath so it is seen by linker, but not by libtool,
enabling libexchange.la to install below /usr/lib/evolution-data-server-1.2/camel-providers, rather
than /usr/lib/evolution/2.2

* Mon Jan 31 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.4-2
- Split out the 64-bit acinclude.m4 patch into two patches, one containing the "actual" patch; the other containing all of the regenerated autotool results.
- Actually apply the 64-bit acinclude.m4 fix this time.

* Wed Jan 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.4-1
- Update from stable upstream 2.0.3 to unstable upstream 2.1.4
- Update evo_major from 2.0 to 2.2
- Added eds_major definition
- Require evolution 2.1.4
- Require libsoup 2.2.2
- Re-enable s390 architectures
- Cope with camel-providers now being stored below evolution-data-server, rather than evolution.
- Remove .a files from camel-providers subdir
- Removed various docs no longer present

* Wed Dec 15 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.3-1
- Update from upstream 2.0.2 to 2.0.3
- The fix for bugs #139134 and #141419 is now in the upstream tarball; removing the patch

* Tue Nov 30 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-2
- Added domain-fix.patch to fix bugs #139134 and #141419

* Tue Oct 12 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-1
- Update from 2.0.1 to 2.0.2
- exclude s390/s390x architecture for now due to Mozilla build problems
- refresh the autogenerated parts of the 64bit fix patch to patch over the latest version of autogenerated files from upstream

* Fri Oct  1 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-5
- added explicit gnutls requirement

* Fri Oct  1 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-4
- set libsoup requirement to be 2.2.0-2, to ensure gnutls support has been added

* Fri Oct  1 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-3
- added requirement on libsoup

* Fri Oct  1 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-2
- rebuild

* Thu Sep 30 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-1
- update from 2.0.0 to 2.0.1
- update required version of evolution from 1.5.94.1 to 2.0.1
- refresh the autogenerated parts of the 64bit fix patch to patch over the latest version of autogenerated files from upstream

* Mon Sep 20 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Tue Sep 14 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.0-1
- update from 1.5.94.1 to 2.0.0
- update source FTP location from 1.5 to 2.0

* Wed Sep  1 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.94.1-1
- update tarball and evolution-version from 1.5.93 to 1.5.94.1
- convert various occurrences of "1.5" in paths to "2.0" to reflect reorganisations of evolution and the connector
- refresh the autogenerated parts of the 64bit fix patch to patch over the latest version of autogenerated files from upstream

* Wed Aug 25 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.93-1
- updated from 1.5.92 to 1.5.93
- removed patch to compile against Evolution 1.5.93 (no longer needed; also was causing bug #130840)
- removed patch for LDAP detection
- added a patch to acinclude.m4 and configure.in to detect and use correct library paths (together with patching the files generated by autotools)

* Mon Aug 23 2004 Nalin Dahyabhai <nalin@redhat.com> - 1.5.92-3
- change macro names to not use "-"
- fix configure on multilib systems

* Fri Aug 20 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.92-2
- exclude ppc64 architecture due to Mozilla build problems

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 1.5.92-1
- Require a version of openldap-devel which provides evolution-specific libs.
- Use the evolution-specific static libraries from openldap-devel, taking into
  account the value of gcc's multidir setting.
- Set $LIBS before running configure so that libldap's dependencies get pulled
  in and we don't accidentally link against the system-wide copy, which would
  make all of this hoop jumping pointless.
- Tag translation files as language-specific using %%{find_lang}.
- Update to 1.5.92.
- Patch to compile against Evolution 1.5.93.

* Mon Jul 26 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.91-1
- Updated to version 1.5.91; updated evolution version to 1.5.91

* Tue Jul  6 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.90-1
- Updated to version 1.5.90; updated evolution version to 1.5.90

* Mon Jun 21 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9-2
- actually uploaded the source tarball this time

* Mon Jun 21 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9-1
- 1.5.9 - first version for the 1.5.* series of Evolution: use revised LDAP detection, fix a build problem in migr-test, use -rpath with evolution 1.5's privlibdir

* Thu May 13 2004 David Malcolm <dmalcolm@redhat.com> - 1.4.7-1
- downgrade to version 1.4.7 for now; add various open-ldap requirements and configuration options

* Thu May 13 2004 David Malcolm <dmalcolm@redhat.com> - 1.4.7.1-1
- updated version to 1.4.7.1

* Wed May 12 2004 David Malcolm <dmalcolm@redhat.com> - 1.4.7-1
- added ldconfig foo; build requires evolution-devel

* Tue May 11 2004 Tom "spot" Callaway <tcallawa@redhat.com>
- initial package
