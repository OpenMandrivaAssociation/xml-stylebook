Name:          xml-stylebook
Version:       1.0
Release:       0.313293.2
Summary:       Apache XML Stylebook

License:       ASL 1.1
URL:           https://xml.apache.org/

# How to generate this tarball:
#  $ svn export http://svn.apache.org/repos/asf/xml/stylebook/trunk/@313293 xml-stylebook-1.0
#  $ tar zcf xml-stylebook-1.0.tar.gz xml-stylebook-1.0
Source0:       %{name}-%{version}.tar.gz

# Patch to fix an NPE in Xalan-J2's docs generation (from JPackage)
Patch0:        %{name}-image-printer.patch

# Patch the build script to build javadocs
Patch1:        %{name}-build-javadoc.patch

BuildArch:     noarch

BuildRequires: java-devel >= 1.6.0
BuildRequires: java-javadoc
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

%package       demo
Summary:       Examples for %{name}

Requires:      %{name} = %{version}-%{release}

%description   demo
Examples demonstrating the use of %{name}.

%prep
%autosetup -p0
# Welcome to the 21st century...
sed -i -e 's,source="1.5",source="1.8",g;s,target="1.5",target="1.8",g' build.xml

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
export CLASSPATH="%{_datadir}/java/xml-commons-apis.jar:%{_datadir}/java/xerces-j2.jar"
ant

# Build the examples (this serves as a good test suite)
pushd docs
rm run.bat
java -classpath "$CLASSPATH:../bin/stylebook-%{version}-b3_xalan-2.jar" \
  org.apache.stylebook.StyleBook "targetDirectory=../results" book.xml ../styles/apachexml
popd

%install
# jars
install -pD -T bin/stylebook-%{version}-b3_xalan-2.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# examples
install -d %{buildroot}%{_datadir}/%{name}
cp -pr docs %{buildroot}%{_datadir}/%{name}
cp -pr styles %{buildroot}%{_datadir}/%{name}
cp -pr results %{buildroot}%{_datadir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/*

%files demo
%{_datadir}/%{name} 
