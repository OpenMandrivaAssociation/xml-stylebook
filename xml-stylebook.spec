Name:          xml-stylebook
Version:       1.0
Release:       0.8.b3_xalan2.svn313293
Summary:       Apache XML Stylebook
Group:         Development/Java
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

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: java-javadoc
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: xml-commons-apis
BuildRequires: jaxp_parser_impl
BuildRequires: fonts-ttf-dejavu
Requires:      java
Requires:      jpackage-utils
Requires:      xml-commons-apis
Requires:      jaxp_parser_impl

%description
Apache XML Stylebook is a HTML documentation generator.

%package       javadoc
Summary:       API documentation for %{name}
Group:         Development/Java
Requires:      java-javadoc

%description   javadoc
%{summary}.

%package       demo
Summary:       Examples for %{name}
Group:         Development/Java
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
rm -rf %{buildroot}

# jars
install -pD -T bin/stylebook-%{version}-b3_xalan-2.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do \
  ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name}) 

# examples
install -d %{buildroot}%{_datadir}/%{name}
cp -pr docs %{buildroot}%{_datadir}/%{name}
cp -pr styles %{buildroot}%{_datadir}/%{name}
cp -pr results %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name} 

