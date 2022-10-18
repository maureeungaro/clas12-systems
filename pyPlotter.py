import numpy as np
import matplotlib.pyplot as plt


def get_digitized_bank(var_name, filename) -> [float]:
    """ Parse the digitized variable variableName from filename and return a vector of floats

    Example ft_cal digitized banK:

      Detector <ft_cal> Digitized Bank {
         Hit address: ih->18, iv->15 {
             adc: 5525
             component: 325
             hitn: 1
             layer: 1
             order: 0
             ped: 0
             sector: 1
             time: 7.10433
         }
         Hit address: ih->18, iv->16 {
             adc: 4533
             component: 347
             hitn: 2
             layer: 1
             order: 0
             ped: 0
             sector: 1
             time: 7.14856
         }
      }

    """

    # Open the file
    f = open(filename, "r")

    # Read the file
    lines = f.readlines()

    # Close the file
    f.close()

    # Initialize the vector
    vec = []

    # Loop over the lines
    for line in lines:
        # Find the variableName
        if var_name in line:
            # Get the value
            value = line.split(":")[1].split("{")[0].strip()

            # Append the value to the vector
            vec.append(value)

    # Return the vector
    return vec


def main():
    # Get the digitized bank
    N = 1000

# Get the digitized bank
    adc = get_digitized_bank("adc", "events.txt")
    com = get_digitized_bank("component", "events.txt")

    # x is the first N numbers in adc
    x = adc[:N]
    y = com[:N]


    area=np.pi*(15*np.random.rand(N))**2
    colors=np.random.rand(N)
    plt.scatter(x,y, s=area, c=colors, alpha=0.5)
    plt.show()

if __name__ == "__main__":
    main()
