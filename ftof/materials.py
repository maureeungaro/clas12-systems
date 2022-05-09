from gemc_api_materials import GMaterial

def define_materials(configuration): 

    gmaterial = GMaterial("scintillator")
    gmaterial.description = "ftof scintillator material"
    gmaterial.density = 1.032
    gmaterial.addNAtoms("C", 9)
    gmaterial.addNAtoms("H", 10)
    gmaterial.publish(configuration)