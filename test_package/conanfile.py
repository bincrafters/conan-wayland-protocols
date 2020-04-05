from conans import ConanFile
import os


class TestPackageConan(ConanFile):

    def test(self):
        self.run('wayland-scanner client-header --strict %s /dev/null' % os.path.join(self.deps_cpp_info['wayland-protocols'].rootpath, "share", "wayland-protocols", "stable", "viewporter", "viewporter.xml"), run_environment=True)
