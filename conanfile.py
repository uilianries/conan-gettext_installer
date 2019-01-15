#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class GettextInstallerConan(ConanFile):
    name = "gettext_installer"
    version = "0.19.8.1"
    description = "Keep it short"
    topics = ("conan", "gettext", "installer", "gnu", "internationalization")
    url = "https://github.com/bincrafters/conan-gettext_installer"
    homepage = "https://www.gnu.org/software/gettext/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-3.0"
    exports = ["LICENSE.md"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _autotools = None

    def source(self):
        source_url = "https://ftp.gnu.org/pub/gnu/gettext"
        sha256 = "ff942af0e438ced4a8b0ea4b0b6e0d6d657157c5e2364de57baa279c1c125c43"
        tools.get("{}/gettext-{}.tar.gz".format(source_url, self.version), sha256=sha256)
        extracted_dir = "gettext-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(args=["--enable-static", "--enable-shared=no"])
        return self._autotools

    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()
        for dir_name in ["lib", "include", "share"]:
            shutil.rmtree(os.path.join(self.package_folder, dir_name), ignore_errors=True)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
