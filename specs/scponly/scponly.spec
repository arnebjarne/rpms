%define _hardened_build 1
Summary: Restricted shell for ssh based file services
Name: scponly
Version: 4.8
Release: 1%{?dist}
License: BSD
Group: Applications/Internet
URL: http://sublimation.org/scponly/
Source: http://downloads.sf.net/scponly/scponly-%{version}.tgz
Patch0: scponly-install.patch
Patch1: scponly-4.8-elif-gcc44.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

# Checks only for location of binaries
BuildRequires: openssh-clients >= 3.4
BuildRequires: openssh-server
BuildRequires: rsync

%description
scponly is an alternative 'shell' for system administrators 
who would like to provide access to remote users to both 
read and write local files without providing any remote 
execution priviledges. Functionally, it is best described 
as a wrapper to the "tried and true" ssh suite of applications. 

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# config.guess in tarball lacks ppc64
cp -p /usr/lib/rpm/config.{guess,sub} .
%configure --enable-scp-compat --enable-winscp-compat --enable-chrooted-binary

%{__make} %{?_smp_mflags} \
	OPTS="%{optflags}"

# Remove executable bit so the debuginfo does not hae executable source files
chmod 0644 scponly.c scponly.h helper.c

%install
%{__rm} -rf %{buildroot}

# 
sed -i "s|%{_prefix}/local/|%{_prefix}/|g" scponly.8* INSTALL README
make install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(0644, root, root, 0755)
%doc AUTHOR CHANGELOG CONTRIB COPYING INSTALL README TODO BUILDING-JAILS.TXT
%doc SECURITY
%defattr(-, root, root, 0755)
%doc %{_mandir}/man8/scponly.8*
%{_bindir}/scponly
%{_sbindir}/scponlyc
%dir %{_sysconfdir}/scponly/
%config(noreplace) %{_sysconfdir}/scponly/*

%changelog
* Sun May 12 2013 Bjarne Saltbaek <arnebjarne72@hotmail.com> - 4.8-1
- Updated to 4.8.
- Grabbed from http://pkgs.fedoraproject.org/cgit/scponly.git

* Sun May 27 2007 Dag Wieers <dag@wieers.com> - 4.6-4
- Added chrooted binary.

* Mon Mar 27 2006 Matthias Saou <http://freshrpms.net/> 4.6-3
- Enable rsync and scp/winscp compatibility.
- Add change from Extras to fix /usr/local in docs.
- Include (ugly) patch to fix long rsync options (may be missing options).

* Thu Mar 09 2006 Dag Wieers <dag@wieers.com> - 4.6-2
- Use make install and added %%{_sysconfdir}/scponly/debuglevel.
- Added setup_chroot helper scripts as documentation.

* Tue Feb 21 2006 Matthias Saou <http://freshrpms.net/> 4.6-1
- Update to 4.6.

* Tue May 10 2005 Dag Wieers <dag@wwieers.com> - 4.1-1
- Updated to release 4.1.

* Thu Mar 03 2005 Dag Wieers <dag@wwieers.com> - 4.0-1
- Initial package. (using DAR)
