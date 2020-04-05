from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os, shutil


class WaylandProtocolsConan(ConanFile):
    name = "wayland-protocols"
    description = "The Wayland-Protocols package contains additional Wayland protocols that add functionality outside of protocols already in the Wayland core."
    topics = ("conan", "wayland-protocols", "wayland")
    url = "https://github.com/bincrafters/conan-wayland-protocols"
    homepage = "https://wayland.freedesktop.org/"
    license = "MIT"
    generators = "pkg_config"

    settings = []
    options = {}
    default_options = {}

    _source_subfolder = "source_subfolder"
    _autotools = None

    requires = (
        "wayland/1.18.0@bincrafters/stable"
    )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(configure_dir= self._source_subfolder)
        return self._autotools

    def build(self):
        lib_path = self.deps_cpp_info['wayland'].rootpath
        for dirpath, _, filenames in os.walk(lib_path):
            for filename in filenames:
                if filename.endswith('.pc'):
                    shutil.copyfile(os.path.join(dirpath, filename), filename)
                    tools.replace_prefix_in_pc_file(filename, lib_path)
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        pass
