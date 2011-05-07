# Generated from haml-2.2.14.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname haml
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: An elegant, structured XHTML/XML templating engine
Name: rubygem-%{gemname}
Version: 2.2.24
Release: 2%{?dist}
Group: Development/Languages
License: MIT and WTFPL
URL: http://haml-lang.com/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source1: emacs-mode-init.el.in
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: rubygems
Requires: ruby(abi) = 1.8
# for html2haml
Requires: rubygem(hpricot)
Requires: emacs(bin)

BuildRequires: rubygems
BuildRequires: ruby
BuildRequires: rubygem(rails)
BuildRequires: rubygem(hpricot)
BuildRequires: emacs

BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Haml (HTML Abstraction Markup Language) is a layer on top of XHTML or XML
that's designed to express the structure of XHTML or XML documents in a
non-repetitive, elegant, easy way, using indentation rather than closing
tags and allowing Ruby to be embedded with ease.
It was originally envisioned as a plugin for Ruby on Rails, but it can
function as a stand-alone templating engine.


%prep

%build

%check
pushd %{buildroot}%{geminstdir}
# The following -path list is from Rakefile
find * \
 -path 'test/*/*_test.rb' \
 -not -path 'test/rails/*' \
 -not -path 'test/plugins/*' \
 -not -path 'test/haml/spec/*' | \
while read f
do
  ruby $f
done
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

rm %{buildroot}%{geminstdir}/.yardopts

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{geminstdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{geminstdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

# Set up emacs modes
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{pkg}
for mode in haml sass; do
  mv %{buildroot}/%{geminstdir}/extra/${mode}-mode.el %{buildroot}%{_emacs_sitelispdir}/${mode}-mode.el
  %{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/${mode}-mode.el
  install -Dpm 644 %{SOURCE1} %{buildroot}%{_emacs_sitestartdir}/${mode}-mode-init.el
  sed -i "s/%{mode}/${mode}/g" %{buildroot}%{_emacs_sitestartdir}/${mode}-mode-init.el
done
rm %{buildroot}%{geminstdir}/extra/update_watch.rb
rmdir %{buildroot}%{geminstdir}/extra

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/haml
%{_bindir}/html2haml
%{_bindir}/sass
%{_bindir}/css2sass
%dir %{geminstdir}
%{geminstdir}/Rakefile
%{geminstdir}/bin
%{geminstdir}/init.rb
%{geminstdir}/lib
%{geminstdir}/rails
%{geminstdir}/test
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/VERSION
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/README.md
%doc %{geminstdir}/VERSION_NAME
%doc %{geminstdir}/REVISION
%doc %{geminstdir}/CONTRIBUTING
%doc %{geminstdir}/REMEMBER
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{_emacs_sitelispdir}/*-mode.el*
%{_emacs_sitestartdir}/*-mode-init.el

%changelog
* Sat May  7 2011 Mark McLoughlin <markmc@redhat.com> - 2.2.24-2
- Package emacs modes correctly

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 2.2.24-1
- New upstream version - minor bugfixes and improvements.
- Drop unused sitelib macro.
- No backup files to cleanup now.

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.20-1
- update to new upstream release

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.16-1
- update to new upstream release
- get rid of test_files macro
- add shebang/permission handling from Jeroen van Meeuwen

* Fri Dec 04 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-2
- change %%define to %%global
- change license to "MIT and WTFPL" (test/haml/spec/README.md)
- add Requires on hpricot for html2haml
- change %%gemdir to %%geminstdir where appropriate

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-1
- Update to new upstream release
- URL changed by upstream

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.14-1
- Initial package
