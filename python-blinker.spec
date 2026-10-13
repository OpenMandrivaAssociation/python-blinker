%define module blinker
# NOTE Doc building depends on python modules: sphinxcontrib-log-cabinet and
# NOTE pallets_sphinx_themes, neither of which we have packaged as of 12/02/2026.
# NOTE Keep docs disabled until such a time as those BRs are packaged.
%bcond docs 0
%bcond tests 1

Name:		python-blinker
Version:	1.9.0
Release:	2
Summary:	Fast, simple object-to-object and broadcast signaling
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/blinker/
Source0:	https://files.pythonhosted.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(flit-core)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with docs}
BuildRequires:	python%{pyver}dist(sphinx)
# Unpackaged
#BuildRequires:	python%%{pyver}dist(sphinxcontrib-log-cabinet)
#BuildRequires:	python%%{pyver}dist(pallets_sphinx_themes)
%endif
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-asyncio)
%endif

%description
Blinker provides a fast dispatching system that allows any number
of interested parties to subscribe to events, or “signals”.

%prep -a
# Remove bundled egg-info
rm -rf %{module}.egg-info

%if %{with docs}
%install -a
#Make buildroot docdir
install -dpm 755 %{buildroot}%{_docdir}/%{name}
# Use sphinx-build to build html docs into buildroot docdir,
# Doc generation requires the module to be installed in order to run successfully.
PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}" \
    sphinx-build -b html docs %{buildroot}%{_docdir}/%{name}
# remove .buildinfo and .doctrees
rm -rf %{buildroot}%{_docdir}/%{name}/.buildinfo
rm -rf %{buildroot}%{_docdir}/%{name}/.doctrees
%endif

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest tests/
%endif

%files
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
%if %{with docs}
%{_docdir}/%{name}
%endif


