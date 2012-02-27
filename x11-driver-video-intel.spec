Name:		x11-driver-video-intel
Version:	2.18.0
Release:	1
Summary:	X.org driver for Intel graphics controllers
Group:		System/X11
License:	MIT
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-intel-%{version}.tar.bz2
# Mandriva patches
Patch100:	0100-Mandriva-fix-check-vt-switch.patch
# (cg) Disable for now as it hits an assert on Xserver 1.9
#Patch101: 0101-fix-NoneBG-support.patch
# Upstream patches

BuildRequires:	libx11-devel >= 1.0.0
BuildRequires:	libdrm-devel >= 2.4.22
BuildRequires:	libxvmc-devel >= 1.0.1
BuildRequires:	xcb-util-devel
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-server-devel >= 1.6.1-3
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libudev)
Requires(post):	update-alternatives >= 1.9.0
Requires(postun): update-alternatives >= 1.9.0
Requires:	x11-server-common %(xserver-sdk-abi-requires videodrv)

Conflicts:	xorg-x11-server < 7.0
Obsoletes:	x11-driver-video-intel13 <= 1.9.94

Obsoletes:	x11-driver-video-i810
Obsoletes:	x11-driver-video-i810-downscaling
Obsoletes:	x11-driver-video-intel-fast-i830

%description
x11-driver-video-intel is the X.org driver for Intel video chipsets.

%prep
%setup -qn xf86-video-intel-%{version}
%apply_patches

%build
%configure2_5x
%make

%install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/xorg/modules/drivers/intel-common/intel_drv.la
rm -f %{buildroot}%{_libdir}/xorg/modules/drivers/i810_drv.*
rm -f %{buildroot}%{_mandir}/man4/i810.4*

mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers/intel-common
mv %{buildroot}%{_libdir}/xorg/modules/drivers/intel_drv.* %{buildroot}%{_libdir}/xorg/modules/drivers/intel-common

# (cg) NB. Alternatives are used here due to the use of a now obsoleted
# fast-i830 subpackage for some netbook chipsets.
# The alternatives system currently remains but only one package will provide
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
%{_libdir}/libI810XvMC.so.1*
%{_libdir}/libIntelXvMC.so.1*
%dir %{_libdir}/xorg/modules/drivers/intel-common
%{_libdir}/xorg/modules/drivers/intel-common/intel_drv.*
%{_mandir}/man4/intel.4*
