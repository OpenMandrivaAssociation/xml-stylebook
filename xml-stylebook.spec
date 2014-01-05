%{?_javapackages_macros:%_javapackages_macros}
Name:          xml-stylebook
Version:       1.0
Release:       0.14.b3_xalan2.svn313293.0%{?dist}
Summary:       Apache XML Stylebook

License:       ASL 1.1
URL:           http://xml.apache.org/

# How to generate this tarball:
#  $ svn export http://svn.apache.org/repos/asf/xml/stylebook/trunk/@313293 xml-stylebook-1.0
#  $ tar zcf xml-stylebook-1.0.tar.gz xml-stylebook-1.0
Source0:       %{name}-%{version}.tar.gz

# Patch to fix an NPE in Xalan-J2's docs generation (from JPackage)
Patch0:        %{name}-image-printer.patch

# Patch the build script to build javadocs
Patch1:        %{name}-build-javadoc.patch

BuildArch:     noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java-javadoc
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: xml-commons-apis
BuildRequires: xerces-j2
%if 0%{?fedora}
BuildRequires: dejavu-sans-fonts
%else
BuildRequires: fontconfig
BuildRequires: fonts-ttf-dejavu
%endif
Requires:      java
Requires:      jpackage-utils
Requires:      xml-commons-apis
Requires:      xerces-j2

%description
Apache XML Stylebook is a HTML documentation generator.

%package       javadoc
Summary:       API documentation for %{name}

Requires:      java-javadoc

%description   javadoc
%{summary}.

%package       demo
Summary:       Examples for %{name}

Requires:      %{name} = %{version}-%{release}

%description   demo
Examples demonstrating the use of %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

# Remove bundled binaries
rm -r bin/*.jar

# Don't include this sample theme because it contains an errant font
rm -r styles/christmas/

# Make sure upstream hasn't sneaked in any jars we don't know about
JARS=""
for j in `find -name "*.jar"`; do
  if [ ! -L $j ]; then
    JARS="$JARS $j"
  fi
done
if [ ! -z "$JARS" ]; then
   echo "These jars should be deleted and symlinked to system jars: $JARS"
   exit 1
fi

%build
ant

# Build the examples (this serves as a good test suite)
pushd docs
rm run.bat
java -classpath "$(build-classpath xml-commons-apis):$(build-classpath jaxp_parser_impl):../bin/stylebook-%{version}-b3_xalan-2.jar" \
  org.apache.stylebook.StyleBook "targetDirectory=../results" book.xml ../styles/apachexml
popd

%install
# jars
install -pD -T bin/stylebook-%{version}-b3_xalan-2.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# examples
install -d %{buildroot}%{_datadir}/%{name}
cp -pr docs %{buildroot}%{_datadir}/%{name}
cp -pr styles %{buildroot}%{_datadir}/%{name}
cp -pr results %{buildroot}%{_datadir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/*

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name} 

%changelog
* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.14.b3_xalan2.svn313293
- Prefer xerces-j2 instead of gcj for providing jaxp_parser_impl

* Sat Aug 10 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.13.b3_xalan2.svn313293
- Update for newer guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.12.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.11.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.10.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.b3_xalan2.svn313293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.7.b3_xalan2.svn313293
- Really fix FTBFS this time.

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.6.b3_xalan2.svn313293
- Fix FTBFS due to ant upgrade.

* Sat Jun 12 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.5.b3_xalan2.svn313293
- Link to local java API docs properly and fix requires on javadoc package.
- Build with source and target levels of 1.5 so we don't have to require 1.6.

* Thu Apr 22 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.4.b3_xalan2.svn313293
- Remove font from demo package to comply with guidelines. RHBZ #567912

* Mon Jan 11 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.3.b3_xalan2.svn313293
- Build the examples (this serves as a good test suite.)
- Patch the build script to build javadocs.
- Add a build dep on a font package because the JDK is missing a dependency
  to function correctly in headless mode. See RHBZ #478480 and #521523.

* Tue Jan 5 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.2.b3_xalan2.svn313293
- Add patch from JPackage to fix NPE in Xalan-J2 doc generation.

* Tue Jan 5 2010 Mat Booth <fedora@matbooth.co.uk> - 1.0-0.1.b3_xalan2.svn313293
- Initial stab at packaging trunk version of stylebook.

