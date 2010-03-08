#Module-Specific definitions
%define mod_name mod_icpquery
%define mod_conf B50_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Extend Apache's mod_rewrite by internal mapping functions using ICP
Name:		apache-%{mod_name}
Version:	2.0.2
Release: 	%mkrel 4
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/modicpquery
Source0:	http://modicpquery.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Apache mod_rewrite provides ways to map values to attributes using the
directive RewriteMap. RewriteMap can use flat mappings files, hashed
mapping files, internal functions and external rewriting programs.
One not well known feature of mod_rewrite is to extend this functionality
with internal functions, which can be defined in a seperate Apache module.
This allows to do some complex and time consuming mappings, since 
mapping requests do not have to be passed through one single pipe, as
in the case of an external rewrite program.

mod_icpquery is a package which can be used to find objects on caching
servers by sending an UDP query. This query conforms to RFC2186 also
known as ICP and can be handeld by various HTTP-caching servers such
as squid. A cache-server handling ICP should reply to an ICP-query
with an ICP-response indicating if it holds the desired object in its
cache or not. mod_icpquery is able to send UDP datagrams to a list of unicast
and/or multicast IP-addresses.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

