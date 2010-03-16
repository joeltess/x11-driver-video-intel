# (anssi) The unversioned symlink of XvMC library must be present in
# %{_libdir} during normal use, as libXvMC uses that name for dlopening.
# Our devel requires finder catches that, hence this exception:
%define _requires_exceptions devel(
%define _disable_ld_no_undefined 1

Name: x11-driver-video-intel
Version: 2.10.902
Release: %mkrel 2
Summary: X.org driver for Intel graphics controllers
Group: System/X11
URL: http://xorg.freedesktop.org
Source: http://xorg.freedesktop.org/releases/individual/driver/xf86-video-intel-%{version}.tar.bz2
License: MIT
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: libx11-devel >= 1.0.0
BuildRequires: libdrm-devel >= 2.4.6
BuildRequires: libxvmc-devel >= 1.0.1
BuildRequires: xcb-util-devel
BuildRequires: x11-proto-devel >= 1.0.0
BuildRequires: x11-server-devel >= 1.6.1-3
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: GL-devel
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives >= 1.9.0

Conflicts: xorg-x11-server < 7.0
Obsoletes: x11-driver-video-intel13 <= 1.9.94

Obsoletes: x11-driver-video-i810
Obsoletes: x11-driver-video-i810-downscaling
Obsoletes: x11-driver-video-intel-fast-i830

# Mandriva patches
Patch300: 0300-Mandriva-fix-check-vt-switch.patch
Patch301: 0301-fix-NoneBG-support.patch

%description
x11-driver-video-intel is the X.org driver for Intel video chipsets.

%prep
%setup -q -n xf86-video-intel-%{version}

%patch300 -p1
#patch301 -p1

# Make sure duplicated code isn't compiled and only the server version is used
rm -fr src/modes

%build
autoreconf -ifs
%configure
%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_libdir}/xorg/modules/drivers/i810_drv.*
rm -f %{buildroot}%{_mandir}/man4/i810.4*

mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers/intel-common
mv %{buildroot}%{_libdir}/xorg/modules/drivers/intel_drv.* %{buildroot}%{_libdir}/xorg/modules/drivers/intel-common

%clean
rm -rf %{buildroot}

# (cg) NB. Alternatives are used here due to the use of a now obsoleted
# fast-i830 subpackage for some netbook chipsets.
# The alternatives system currently remains but only one pacakge will provide
# the 'alternative'. I will leave this in place for a while just incase
# we need to resurrect a chip-specific package again in the near future
# but if it proves unnecessary it should be tidied up.

# use posttrans so that files from old package are removed first
%posttrans
%{_sbindir}/update-alternatives \
  --install %{_libdir}/xorg/modules/drivers/intel_drv.so x11-intel-so %{_libdir}/xorg/modules/drivers/intel-common/intel_drv.so 20 \
  --slave   %{_libdir}/xorg/modules/drivers/intel_drv.la x11-intel-la %{_libdir}/xorg/modules/drivers/intel-common/intel_drv.la

%postun
[ $1 = 0 ] || exit 0
%{_sbindir}/update-alternatives --remove x11-intel-so %{_libdir}/xorg/modules/drivers/intel-common/intel_drv.so

%files
%defattr(-,root,root)
%{_libdir}/libI810XvMC.la
%{_libdir}/libI810XvMC.so
%{_libdir}/libI810XvMC.so.1
%{_libdir}/libI810XvMC.so.1.0.0
%{_libdir}/libIntelXvMC.la
%{_libdir}/libIntelXvMC.so
%{_libdir}/libIntelXvMC.so.1
%{_libdir}/libIntelXvMC.so.1.0.0
%dir %{_libdir}/xorg/modules/drivers/intel-common
%{_libdir}/xorg/modules/drivers/intel-common/intel_drv.*
#%{_libdir}/xorg/modules/drivers/ch7017.*
#%{_libdir}/xorg/modules/drivers/ch7xxx.*
#%{_libdir}/xorg/modules/drivers/ivch.*
#%{_libdir}/xorg/modules/drivers/sil164.*
#%{_libdir}/xorg/modules/drivers/tfp410.*
%{_mandir}/man4/intel.4*
