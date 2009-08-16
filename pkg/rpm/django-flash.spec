%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           django-flash
Version:        1.6
Release:        1%{?dist}
Summary:        Rails-like flash messages support for Django

Group:          Development/Languages
License:        BSD
URL:            http://djangoflash.destaquenet.com/
Source0:        http://pypi.python.org/packages/source/d/django-flash/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools
Requires:       Django


%description
Django-Flash is a simple Django extension that provides support for Rails-like
flash messages. The flash is a temporary storage that has one special property:
by default, values stored into the flash during the processing of a request
will be available during the processing of the immediately following request.
Once that second request has been processed, those values are removed
automatically from the storage.


%prep
%setup -q
find -name '._*' -exec rm {} \;


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README doc/source/*.rst
%{python_sitelib}/*


%changelog
* Wed Aug 12 2009 Francesco Crippa <fcrippa@byte-code.com> 1.6-1
- Fixed a bug in which messages are prematurely removed from the flash when
  they are replaced using flash.now in some circumstances
- Added the FLASH_IGNORE_MEDIA setting to let the user choose whether
  requests to static files should be ignored
* Wed Aug 12 2009 Francesco Crippa <fcrippa@byte-code.com> 1.5.3-1
- Initial RPM package
