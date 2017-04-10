%{?scl:%scl_package glassfish-jax-rs-api}
%{!?scl:%global pkg_name %{name}}

%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
%global oname javax.ws.rs-api

Name:		%{?scl_prefix}glassfish-jax-rs-api
Version:	2.0.1
Release:	5%{?dist}
Summary:	JAX-RS API Specification (JSR 339)
License:	CDDL or GPLv2 with exceptions
URL:		http://jax-rs-spec.java.net/
# git clone git://java.net/jax-rs-spec~api glassfish-jax-rs-api
# (cd glassfish-jax-rs-api/ && git archive --format=tar --prefix=glassfish-jax-rs-api-2.0.1/ 2.0.1 | xz > ../glassfish-jax-rs-api-2.0.1.tar.xz)
Source0:	%{pkg_name}-%{namedversion}.tar.xz

BuildRequires:	%{?scl_prefix_java_common}junit
BuildRequires:	%{?scl_prefix_maven}jvnet-parent
BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix_maven}maven-resources-plugin
BuildRequires:	%{?scl_prefix_maven}spec-version-maven-plugin
%{?scl:Requires: %scl_runtime}
BuildArch:	noarch

%description
JAX-RS Java API for RESTful Web Services (JSR 339).

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{namedversion}
find . -name '*.jar' -delete
find . -name '*.class' -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin src/jax-rs-api

# Reporting mojo's can only be called from ReportDocumentRender
%pom_remove_plugin org.apache.maven.plugins:maven-jxr-plugin src/jax-rs-api
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin src/jax-rs-api
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin src/jax-rs-api
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin src/jax-rs-api
%pom_remove_plugin org.apache.maven.plugins:maven-deploy-plugin src/jax-rs-api

%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin' ]/pom:executions" src/jax-rs-api

%pom_xpath_remove "pom:build/pom:finalName" src/jax-rs-api
%{?scl:EOF}

sed -i "s|dvips|pdftex|" spec/spec.tex

sed -i '/check-module/d' src/jax-rs-api/pom.xml

cp -p src/etc/config/copyright.txt .
sed -i 's/\r//' copyright.txt src/examples/pom.xml

%build

(
cd src/jax-rs-api
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_file :%{oname} %{pkg_name}
%mvn_build
%{?scl:EOF}
)

%install

(
cd src/jax-rs-api
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}
)

%files -f src/jax-rs-api/.mfiles
%license copyright.txt

%files javadoc -f src/jax-rs-api/.mfiles-javadoc
%license copyright.txt

%changelog
* Mon Apr 10 2017 Tomas Repik <trepik@redhat.com> - 2.0.1-5
- scl conversion

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 08 2015 gil cattaneo <puntogil@libero.it> 2.0.1-1
- update to 2.0.1

* Tue Feb 03 2015 gil cattaneo <puntogil@libero.it> 2.0-7
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 2.0-3
- switch to XMvn
- minor changes to adapt to current guideline

* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 2.0-2
- rebuilt with spec-version-maven-plugin support

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.0-1
- update to 2.0

* Tue Mar 26 2013 gil cattaneo <puntogil@libero.it> 2.0-0.1.m16
- initial rpm
