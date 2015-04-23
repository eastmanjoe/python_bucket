#!/usr/bin/python
# -*- coding: utf-8 -*-
import pip

if __name__ == '__main__':
    installed_packages = pip.get_installed_distributions()
    installed_packages_list =
        sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

    print(installed_packages_list)