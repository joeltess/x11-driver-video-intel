# (anssi) The unversioned symlink of XvMC library must be present in
# %{_libdir} during normal use, as libXvMC uses that name for dlopening.
# Our devel requires finder catches that, hence this exception:
%define _requires_exceptions devel(
%define _disable_ld_no_undefined 1

Name: x11-driver-video-intel
Version: 2.11.0
Release: %mkrel 3
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
BuildRequires: libudev-devel
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives >= 1.9.0

Conflicts: xorg-x11-server < 7.0
Obsoletes: x11-driver-video-intel13 <= 1.9.94

Obsoletes: x11-driver-video-i810
Obsoletes: x11-driver-video-i810-downscaling
Obsoletes: x11-driver-video-intel-fast-i830

# Upstream patches
Patch100:0100-i830-render-use-tiling-bits-where-possible.patch
Patch101:0101-i915-render-use-tiling-bits-where-possible.patch
Patch102:0102-uxa-Extract-sub-region-from-in-memory-buffers.patch
Patch103:0103-uxa-Transform-composites-with-a-simple-translation-i.patch
Patch104:0104-uxa-Rearrange-checking-and-preparing-of-composite-te.patch
Patch105:0105-uxa-i915-Handle-SourcePict-through-uxa_composite.patch
Patch106:0106-uxa-Protect-against-valid-SourcePict-in-uxa_acquire_.patch
Patch107:0107-uxa-Recheck-texture-after-acquiring-pattern.patch
Patch108:0108-i830-Remove-incorrectly-mapped-tex-formats.patch
Patch109:0109-uxa-Parse-BGRA-pixel-formats.patch
Patch110:0110-uxa-Disable-compatible-src-xrgb-and-dst-argb.patch
Patch111:0111-uxa-Check-the-w-scaling-component-is-1-for-an-transl.patch
Patch112:0112-uxa-Avoid-using-blits-when-with-PictFilterConvolutio.patch
Patch113:0113-i830-Encode-surface-bpp-into-format.patch

# Mandriva patches
Patch300: 0300-Mandriva-fix-check-vt-switch.patch
Patch301: 0301-fix-NoneBG-support.patch
Patch302: 0302-Add-mbp_backlight-to-the-backlight-interfaces-as-req.patch

# Fedora patches
Patch0400: 0400-send-randr-hotplug-events.patch

%description
x11-driver-video-intel is the X.org driver for Intel video chipsets.

%prep
%setup -q -n xf86-video-intel-%{version}

%apply_patches

autoreconf -ifs
%build
%configure2_5x
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
