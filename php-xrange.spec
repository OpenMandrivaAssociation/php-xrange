%define modname xrange
%define soname %{modname}.so
%define inifile A74_%{modname}.ini

Summary:	Numeric iterator primitives
Name:		php-%{modname}
Version:	1.3.2
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/xrange/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
xrange is a compiled extension that provides numeric iteration primitives to
PHP on top of SPL. It includes a lean numeric range generator / iterator,
modeled after Python's xrange() function. It's intended to provide an
alternative for all numeric iteration and looping.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}/var/log/httpd

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
Classes = XRangeIterator
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml tests CREDITS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Mon Jul 30 2012 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-1mdv2012.0
+ Revision: 811430
- 1.3.2

* Sun May 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-14
+ Revision: 799734
- fix build
- rebuilt for php-5.3.2
- rebuilt for php-5.3.2RC1
- rebuilt against php-5.3.1
- rebuild
- rebuilt for php-5.3.0RC2

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-6mdv2009.1
+ Revision: 346708
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-5mdv2009.1
+ Revision: 341849
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-4mdv2009.1
+ Revision: 323144
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-3mdv2009.1
+ Revision: 310321
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2009.0
+ Revision: 238474
- rebuild

* Mon Mar 03 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2008.1
+ Revision: 177874
- 1.3.1

* Wed Feb 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3-1mdv2008.1
+ Revision: 175685
- import php-xrange

