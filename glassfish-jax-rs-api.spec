%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
%global oname javax.ws.rs-api
Name:          glassfish-jax-rs-api
Version:       2.0
Release:       1%{?dist}
Summary:       JAX-RS API Specification (JSR 339)
Group:         Development/Libraries
License:       CDDL or GPLv2 with exceptions
URL:           http://jax-rs-spec.java.net/
# git clone git://java.net/jax-rs-spec~git glassfish-jax-rs-api
# (cd glassfish-jax-rs-api/ && git archive --format=tar --prefix=glassfish-jax-rs-api-2.0/ 2.0 | xz > ../glassfish-jax-rs-api-2.0-src-git.tar.xz)
Source0:       %{name}-%{namedversion}-src-git.tar.xz

BuildRequires: java-devel
BuildRequires: jvnet-parent

# test deps
BuildRequires: junit

#BuildRequires: buildnumber-maven-plugin
BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit4

BuildRequires: make
BuildRequires: texlive-amsfonts
BuildRequires: texlive-base
BuildRequires: texlive-bibtex-bin
BuildRequires: texlive-cm
BuildRequires: texlive-courier
BuildRequires: texlive-dvips
BuildRequires: texlive-fancyhdr
BuildRequires: texlive-float
BuildRequires: texlive-framed
BuildRequires: texlive-graphics
BuildRequires: texlive-helvetic
BuildRequires: texlive-hyperref
BuildRequires: texlive-ifxetex
BuildRequires: texlive-latex-bin-bin
BuildRequires: texlive-latexconfig
BuildRequires: texlive-moreverb
BuildRequires: texlive-oberdiek
BuildRequires: texlive-pdftex-def
BuildRequires: texlive-psnfss
BuildRequires: texlive-texconfig
BuildRequires: texlive-times
BuildRequires: texlive-tools

Requires:      java
BuildArch:     noarch

%description
JAX-RS Java API for RESTful Web Services (JSR 339).

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package manual
Group:         Documentation
Summary:       Manual for %{name}

%description manual
This package contains documentation for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
find . -name '*.jar' -delete
find . -name '*.class' -delete

%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin src/jax-rs-api
%pom_remove_plugin org.glassfish.build:spec-version-maven-plugin src/jax-rs-api
# Reporting mojo's can only be called from ReportDocumentRender
%pom_remove_plugin org.apache.maven.plugins:maven-jxr-plugin src/jax-rs-api
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin src/jax-rs-api
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin src/jax-rs-api

%pom_xpath_remove "pom:build/pom:finalName" src/jax-rs-api
%pom_xpath_remove "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId ='maven-bundle-plugin']/pom:configuration/pom:instructions/pom:Bundle-Version"  src/jax-rs-api

sed -i "s|dvips|pdftex|" spec/spec.tex

cp -p src/etc/config/copyright.txt .
sed -i 's/\r//' copyright.txt src/examples/pom.xml

%build

mvn-rpmbuild -f src/jax-rs-api/pom.xml package javadoc:aggregate
cd spec
make clean all

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 src/jax-rs-api/target/%{oname}-%{namedversion}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 src/jax-rs-api/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr src/jax-rs-api/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc copyright.txt

%files javadoc
%{_javadocdir}/%{name}
%doc copyright.txt

%files manual
%doc copyright.txt spec/spec.pdf src/examples

%changelog
* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.0-1
- update to 2.0

* Tue Mar 26 2013 gil cattaneo <puntogil@libero.it> 2.0-0.1.m16
- initial rpm