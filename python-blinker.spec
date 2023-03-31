# Created by pyp2rpm-2.0.0
%global pypi_name blinker
%global with_python2 0
%define version 1.4

Name:           python-blinker
Version:        %{version}
Release:        2
Group:          Development/Python
Summary:        Fast, simple object-to-object and broadcast signaling

License:        MIT
URL:            http://pythonhosted.org/blinker/
Source0:        https://pypi.python.org/packages/1b/51/e2a9f3b757eb802f61dc1f2b09c8c99f6eb01cf06416c0671253536517b6/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
 
%if %{?with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
%endif # if with_python2


%description
Blinker provides a fast dispatching system that allows any number of interested parties to subscribe to events, or “signals”.

%if 0%{?with_python2}
%package -n     python2-%{pypi_name}
Summary:        Fast, simple object-to-object and broadcast signaling

%description -n python2-%{pypi_name}
Blinker provides a fast dispatching system that allows any number of interested parties to subscribe to events, or “signals”.
%endif # with_python2


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs 
sphinx-build -C docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python2}
rm -rf %{py2dir}
cp -a . %{py2dir}
find %{py2dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
# generate html docs 
sphinx-build2 docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%endif # with_python2


%build
%{__python3} setup.py build

%if 0%{?with_python2}
pushd %{py2dir}
%{__python} setup.py build
popd
%endif # with_python2


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python2}
pushd %{py2dir}
%{__python} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python2

%{__python3} setup.py install --skip-build --root %{buildroot}


%files
%doc html README.md LICENSE
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%if 0%{?with_python2}
%files -n python2-%{pypi_name}
%doc html README.md LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python2

