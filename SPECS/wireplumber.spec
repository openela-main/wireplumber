Name:       wireplumber
Version:    0.4.14
Release:    1%{?dist}
Summary:    A modular session/policy manager for PipeWire

License:    MIT
URL:        https://pipewire.pages.freedesktop.org/wireplumber/
Source0:    https://gitlab.freedesktop.org/pipewire/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2

## upstream patches

## upstreamable patches

## fedora patches

BuildRequires:  gettext
BuildRequires:  meson gcc pkgconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libspa-0.2) >= 0.2
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.26
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd-devel >= 184
BuildRequires:  pkgconfig(lua)
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-lxml doxygen
BuildRequires:  systemd-rpm-macros
%{?systemd_ordering}

# Make sure that we have -libs package in the same version
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Provides:       pipewire-session-manager
Conflicts:      pipewire-session-manager

%package        libs
Summary:        Libraries for WirePlumber clients
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with WirePlumber.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description
WirePlumber is a modular session/policy manager for PipeWire and a
GObject-based high-level library that wraps PipeWire's API, providing
convenience for writing the daemon's modules as well as external tools for
managing PipeWire.

%prep
%autosetup -p1

%build
%meson -Dsystem-lua=true \
       -Ddoc=disabled \
       -Dsystemd=enabled \
       -Dsystemd-user-service=true \
       -Dintrospection=enabled \
       -Delogind=disabled
%meson_build

%install
%meson_install

# Create local config skeleton
mkdir -p %{buildroot}%{_sysconfdir}/wireplumber/{bluetooth.lua.d,common,main.lua.d,policy.lua.d}

%find_lang %{name}

%posttrans
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%triggerun -- fedora-release < 35
# When upgrading to Fedora Linux 35, transition to WirePlumber by default
if [ -x "/bin/systemctl" ]; then
    /bin/systemctl --no-reload preset --global %{name}.service || :
fi

%files
%license LICENSE
%{_bindir}/wireplumber
%{_bindir}/wpctl
%{_bindir}/wpexec
%dir %{_sysconfdir}/wireplumber
%dir %{_sysconfdir}/wireplumber/bluetooth.lua.d
%dir %{_sysconfdir}/wireplumber/common
%dir %{_sysconfdir}/wireplumber/main.lua.d
%dir %{_sysconfdir}/wireplumber/policy.lua.d
%{_datadir}/wireplumber/
%{_userunitdir}/wireplumber.service
%{_userunitdir}/wireplumber@.service

%files libs -f %{name}.lang
%license LICENSE
%dir %{_libdir}/wireplumber-0.4/
%{_libdir}/wireplumber-0.4/libwireplumber-*.so
%{_libdir}/libwireplumber-0.4.so.*
%{_libdir}/girepository-1.0/Wp-0.4.typelib

%files devel
%{_includedir}/wireplumber-0.4/
%{_libdir}/libwireplumber-0.4.so
%{_libdir}/pkgconfig/wireplumber-0.4.pc
%{_datadir}/gir-1.0/Wp-0.4.gir

%changelog
* Wed Mar 22 2023 Wim Taymans <wtaymans@redhat.com> - 0.4.14-1
- Update to version 0.4.14
  Resolves: rhbz#2180783

* Fri Feb 18 2022 Wim Taymans <wtaymans@redhat.com> - 0.4.8-1
- Update to version 0.4.8
  Resolves: rhbz#2055692

* Wed Nov 17 2021 Neal Gompa <ngompa@centosproject.org> - 0.4.5-1
- Update to version 0.4.5
  Resolves: rhbz#2022695

* Tue Nov 16 2021 Neal Gompa <ngompa@centosproject.org> - 0.4.1-3
- Obsolete pipewire-media-session
  Related: rhbz#2022694

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- Initial package (#1976012)
