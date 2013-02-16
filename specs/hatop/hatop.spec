# norootforbuild

Name:           hatop
Version:        0.7.7
Release:        1%{?dist}
License:        GPLv3
Group:          Productivity/Networking/Web/Proxy
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  python
Url:            http://hatop.googlecode.com
Source:         %{name}-%{version}.tar.gz
Conflicts:      haproxy < 1.4

Summary:        Interactive ncurses client for the HAProxy unix socket
%description
HATop's appearance is similar to top(1). It supports various modes
for detailed statistics of all configured proxies and services in near
realtime. In addition, it features an interactive CLI for the haproxy
unix socket. This allows administrators to control the given haproxy
instance (change server weight, put servers into maintenance mode, ...)
directly out of hatop and monitor the results immediately.

%package doc
Summary:        Documentation for %{name}
Group:          Productivity/Networking/Web/Proxy
Requires:       %{name} = %{version}
%description doc
HATop's appearance is similar to top(1). It supports various modes
for detailed statistics of all configured proxies and services in near
realtime. In addition, it features an interactive CLI for the haproxy
unix socket. This allows administrators to control the given haproxy
instance (change server weight, put servers into maintenance mode, ...)
directly out of hatop and monitor the results immediately.

This package contains additional documentation for %{name}, under
  %{_docdir}/%{name}/docs/

%prep
%setup -q -n %{name}-%{version}

%build
# change shebang to use %__python instead of /usr/bin/env python:
%__sed -i -r '1s|^#! *(.+)/python(.*)$|#!%__python|' bin/hatop

%install
%{__install} -D -m 0755 bin/hatop %{buildroot}%{_sbindir}/hatop
%__install -D -m0644 man/hatop.1 "%{buildroot}%{_mandir}/man1/hatop.1"

>docfiles.main.lst
%__install -d "%{buildroot}%{_docdir}/%{name}"
for f in CHANGES HACKING KEYBINDS LICENSE README; do
    %__install -m0644 "$f" "%{buildroot}%{_docdir}/%{name}/"
    ff=$(basename "$f")
    echo "%doc %{_docdir}/%{name}/$ff" >>docfiles.main.lst
done

%__rm -f doc/Makefile doc/*.py
%__rm -rf doc/build doc/templates
>docfiles.doc.lst
for x in doc/*; do
    [ -e "$x" ] || continue
    xx=$(basename "$x")
    %__cp -a "$x" "%{buildroot}%{_docdir}/%{name}/"
    echo "%doc %{_docdir}/%{name}/$xx" >>docfiles.doc.lst
done

%clean
%{?buildroot:%{__rm} -rf %{buildroot}}

%files -f docfiles.main.lst
%defattr(-,root,root,-)
%{_sbindir}/hatop
%doc %{_mandir}/man1/hatop.1*
%dir %{_docdir}/%{name}

%files doc -f docfiles.doc.lst
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}

%changelog
* Sat Feb 16 2013 Bjarne Saltbaek <arnebjarne72@hotmail.com> - 0.7.7-1
- Initial package.
