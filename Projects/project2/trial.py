def find_centroid(polygon):
    poly_len = len(polygon)-1 #Number of points in the polygon list

    #finds the sum of general function to make the center x and center y
     
    """
    def summation(f):
        counter = 0
        total = 0
        while counter < poly_len:
            total += f(counter)
            counter += 1
        return total
    
    #finding area 
    def area(counter):
        lat_i = latitude(polygon[counter])
        lat_i2 = latitude(polygon[counter+1])
        long_i = longitude(polygon[counter])
        long_i2 = longitude(polygon[counter+1])
        return ((lat_i*long_i2)-(lat_i2*long_i))
    if area == 0:
        return latitude(polygon[0]) , longitude(polygon[0]) , 0

    def c_lat(counter):
        lat_i = latitude(polygon[counter])
        lat_i2 = latitude(polygon[counter+1])
        long_i = longitude(polygon[counter])
        long_i2 = longitude(polygon[counter+1])
        return (long_i2 *lat_i-long_i*lat_i2)*(lat_i + lat_i2)

    def c_long(counter):
        lat_i = latitude(polygon[counter])
        lat_i2 = latitude(polygon[counter+1])
        long_i = longitude(polygon[counter])
        long_i2 = longitude(polygon[counter+1])
        return (((long_i + long_i2)*(lat_i*long_i2 - lat_i2 * long_i)))
    return summation(c_lat)/(6*area), summation(c_long)/(6*area), abs(1/2(summation(area)))"""
#try number 2
    """area, c_lat, c_long = 0,0,0
    counter = 0
    while counter < poly_len:
        lat_i = latitude(polygon[counter])
        lat_i2 = latitude(polygon[counter+1])
        long_i = longitude(polygon[counter])
        long_i2 = longitude(polygon[counter+1])
        area += (0.5)*((lat_i*long_i2)-(lat_i2*long_i))
        if area == 0:
            return latitude(polygon[0]) , longitude(polygon[0]) , 0
        c_lat += ((long_i2 *lat_i- long_i*lat_i2)*(lat_i + lat_i2))                
        c_long += ((long_i + long_i2)*(lat_i*long_i2 - lat_i2 * long_i))
        counter += 1
    return c_lat/(6*area), c_long/(6*area), abs(area)"""

#try 3
    def summation(f):
        total = 0
        nonlocal counter
        while counter < poly_len:
            total += f(counter)
            counter += 1
        return total

    def 

