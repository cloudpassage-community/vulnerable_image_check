import vulnerable_image_check

# Build config
config = vulnerable_image_check.ConfigHelper()

# get a halo object for api methods wrapper
halo = vulnerable_image_check.HaloGeneral(config)

vulnerable_image_check.VulnerableImageCheck(halo)
