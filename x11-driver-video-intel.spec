# X.org drivers use symbols from the X server
%global _disable_ld_no_undefined 1
%define snapshot 20151201

Summary:	X.org driver for Intel graphics controllers
Name:		x11-driver-video-intel
Version:	2.99.917
Group:		System/X11
License:	MIT
URL:		http://xorg.freedesktop.org
%if "%snapshot" == ""
Release:        5
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-intel-%{version}.tar.bz2
%else
Release:	6.%{snapshot}.4
# rm -rf xf86-video-intel && git clone git://anongit.freedesktop.org/xorg/driver/xf86-video-intel && cd xf86-video-intel/
# git archive --prefix=xf86-video-intel-$(date +%Y%m%d)/ --format=tar HEAD | xz > ../xf86-video-intel-$(date +%Y%m%d).tar.xz
Source0:        xf86-video-intel-%{snapshot}.tar.xz
%endif
# For now, Intel GPUs only exist in x86 boards... Remove this if Intel
# ever comes up with a PCIE graphics card or an ARM SoC with an Intel
# GPU...
ExclusiveArch:	%{ix86} x86_64
# Mandriva patches
Patch100:	0100-Mandriva-fix-check-vt-switch.patch
# (cg) Disable for now as it hits an assert on Xserver 1.9
#Patch101: 0101-fix-NoneBG-support.patch
# Upstream patches

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(udev) >= 186
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xorg-macros)
BuildRequires:	pkgconfig(xorg-server) >= 1.18
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xvmc)
# For intel-virtual-output
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(xfont)
Requires(post,postun):	update-alternatives >= 1.9.0
Requires:	x11-server-common %(xserver-sdk-abi-requires videodrv)
Requires:	udev

Conflicts:	xorg-x11-server < 7.0
Obsoletes:	x11-driver-video-intel13 <= 1.9.94
Obsoletes:	x11-driver-video-i810
Obsoletes:	x11-driver-video-i810-downscaling
Obsoletes:	x11-driver-video-intel-fast-i830
# (tpg) this is needed to get vaapi works out of box
Requires:	vaapi-driver-intel
Requires:	%{_lib}dri-drivers-intel

%description
x11-driver-video-intel is the X.org driver for Intel video chipsets.

%prep
%if "%snapshot" != ""
%setup -qn xf86-video-intel-%{snapshot}
%else
%setup -qn xf86-video-intel-%{version}
%endif

%apply_patches

%build
%if "%snapshot" != ""
./autogen.sh
%endif

# As of Xorg 1.15 and clang 3.5-212807, the X server crashes on startup if
# a driver is built with clang. Let's force gcc for now.
# (tpg) let's try with clang
#CC=gcc CXX=g++ \

CFLAGS="`echo %{optflags} |sed -e 's,-D_FORTIFY_SOURCE=2 -fstack-protector,,;s,-flto,,'`" \
%configure \
		--enable-dri \
		--enable-sna \
		--with-default-accel=sna \
		--enable-kms-only \
		--with-default-dri=3

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
%{_bindir}/intel-virtual-output
%optional %{_libdir}/libI810XvMC.so.1*
%{_libdir}/libIntelXvMC.so.1*
%dir %{_libdir}/xorg/modules/drivers/intel-common
%{_libdir}/xorg/modules/drivers/intel-common/intel_drv.*
%{_mandir}/man4/intel.4*
%{_mandir}/man4/intel-virtual-output.4*
%{_libexecdir}/xf86-video-intel-backlight-helper
%{_datadir}/polkit-1/actions/org.x.xf86-video-intel.backlight-helper.policy
