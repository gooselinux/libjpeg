Summary: A library for manipulating JPEG image format files
Name: libjpeg
Version: 6b
Release: 46%{?dist}
License: IJG
Group: System Environment/Libraries
URL: http://www.ijg.org/

Source0: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.gz
Source1: configure.in

Patch1: jpeg-c++.patch
Patch4: libjpeg-cflags.patch
Patch5: libjpeg-buf-oflo.patch
Patch6: libjpeg-autoconf.patch

BuildRequires: autoconf libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

%package devel
Summary: Development tools for programs which will use the libjpeg library
Group: Development/Libraries
Requires: libjpeg = %{version}-%{release}

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package static
Summary: Static JPEG image format file library
Group: Development/Libraries
Requires: libjpeg-devel = %{version}-%{release}

%description static
The libjpeg-static package contains the statically linkable version of libjpeg.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%prep
%setup -q -n jpeg-6b

%patch1 -p1 -b .c++
%patch4 -p1 -b .cflags
%patch5 -p1 -b .oflo
%patch6 -p1

# For long-obsolete reasons, libjpeg 6b doesn't ship with a configure.in.
# We need to re-autoconf though, in order to update libtool support,
# so supply configure.in.
cp %{SOURCE1} configure.in

# libjpeg 6b includes a horribly obsolete version of libtool.
# Blow it away and replace with build system's version.
rm -f config.guess config.sub ltmain.sh ltconfig aclocal.m4
cp /usr/share/aclocal/libtool.m4 aclocal.m4
# this is conditional so we can build with either libtool 2.2 or 1.5
if [ -f /usr/share/aclocal/ltoptions.m4 ]; then
  cat /usr/share/aclocal/ltoptions.m4 \
      /usr/share/aclocal/ltversion.m4 \
      /usr/share/aclocal/ltsugar.m4 \
      /usr/share/aclocal/lt~obsolete.m4 \
    >>aclocal.m4
fi
# this hack is so we can build with either libtool 2.2 or 1.5
libtoolize --install || libtoolize

autoconf

%build
%configure --enable-shared --enable-static

make libdir=%{_libdir} %{?_smp_mflags}

LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH make test

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{include,bin}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%makeinstall

# Work around the broken makefiles...
mv $RPM_BUILD_ROOT%{_mandir}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# We don't ship .la files.
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc usage.doc README
%{_libdir}/libjpeg.so.*
%{_bindir}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%doc libjpeg.doc coderules.doc structure.doc wizard.doc example.c
%{_libdir}/*.so
/usr/include/*.h

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6b-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6b-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Tom Lane <tgl@redhat.com> - 6b-44
- Fix libtool hacking so it also works with libtool 2.2.  (For the
  moment the specfile still also works with libtool 1.5, but that can
  go away eventually.)

* Thu Sep 25 2008 Tom Lane <tgl@redhat.com> - 6b-43
- Revert to using .gz instead of .bz2 tarball
Resolves: #463903

* Thu Jun 19 2008 Tom Lane <tgl@redhat.com> - 6b-42
- Work around autoconf 2.62 breakage
Resolves: #449471
Related: #449245

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6b-41
- Autorebuild for GCC 4.3

* Sun Jan 13 2008 Tom Lane <tgl@redhat.com> - 6b-40
- Rip out the long-obsolete version of libtool that shipped with libjpeg 6b,
  and instead use the build system's libtool.  This obsoletes most of the
  patches we were carrying.
- Fix configure script to #define the various HAVE_FOO macros as 1, not empty,
  for better compatibility with most other autoconf-using packages.  (This
  requires importing the original IJG configure.in, which was not shipped
  in libjpeg-6b for reasons that no longer seem very good.)
Resolves: #427616

* Wed Aug 22 2007 Tom Lane <tgl@redhat.com> - 6b-39
- Update License tag
- Rebuild to fix Fedora toolchain issues

* Mon Jun 25 2007 Tom Lane <tgl@redhat.com> - 6b-38
- Initial review of package by new (old?) maintainer; marginal specfile cleanup
- Restore libjpeg.a to distribution, in a separate -static subpackage
Resolves: #186060, #215537
- Fix non-security-significant buffer overrun in wrjpgcom, per Lubomir Kundrak
Resolves: #226965
- Apply patch4 that was added by previous maintainer, but never applied
Resolves: #244778
Related: #238936
- Fix inter-RPM dependencies to include release
Resolves: #238780

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 6b-37
- Use CFLAGS consistently

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6b-36.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6b-36.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6b-36.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 6b-36
- Don't ship static libraries

* Sun Mar  6 2005 Matthias Clasen <mclasen@redhat.com> - 6b-35
- Remove .la files (#145971)

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 6b-34
- Rebuild with gcc4

* Thu Oct  7 2004 Matthias Clasen <mclasen@redhat.com> - 6b-33
- Add URL.  (#134791)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Sep 25 2003 Jeremy Katz <katzj@redhat.com> 6b-30
- rebuild to fix gzipped file md5sums (#91211)

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not set rpath

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 6b-27
- Add libjpeg-shared.patch to fix shlibs on powerpc

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared lib

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan  6 2003 Jonathan Blandford <jrb@redhat.com>
- add docs, #76508

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 6b-23
- Merge in multilib changes
- _smp_mflags

* Tue Sep 10 2002 Than Ngo <than@redhat.com> 6b-22
- use %%_libdir

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 6b-19
- Fix bug #59011

* Mon Jan 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 6b-18
- Fix bug #58982

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jul 24 2001 Bill Nottingham <notting@redhat.com>
- require libjpeg = %%{version}

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- rebuilt with the fixed fileutils
- use %%{_tmppath}

* Wed Nov  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix a typo (strip -R .comment, not .comments)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify
- add some C++ tweaks to the headers as suggested by bug #9822)

* Wed May  5 2000 Bill Nottingham <notting@redhat.com>
- configure tweaks for ia64; remove alpha patch (it's pointless)

* Sat Feb  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild to get compressed man pages
- fix description
- some minor tweaks to the spec file
- add docs
- fix build on alpha (alphaev6 stuff)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- patch to build on arm
- build for glibc 2.1

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries

* Mon Aug  3 1998 Jeff Johnson <jbj@redhat.com>
- fix buildroot problem.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Thu Jun 04 1998 Marc Ewing <marc@redhat.com>
- up to release 4
- remove patch that set (improper) soname - libjpeg now does it itself

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- fixed build on manhattan

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 6b

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- new package to remove jpeg stuff from libgr and put in it's own package
