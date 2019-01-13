from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    config_url = "https://github.com/bincrafters/conan-config.git"
    
    builder = ConanMultiPackager(config_url=config_url)
    builder.add_common_builds(pure_c=False)
    builder.run()
