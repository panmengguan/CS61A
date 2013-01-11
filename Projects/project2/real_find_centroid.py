def find_centroid(polygon):
    def poly_area(x=0):
        area = 0
        while x < len(polygon)-1:
            area+=(0.5)*(latitude(polygon[x])*longitude(polygon[x+1])-\
                   latitude(polygon[x+1])*longitude(polygon[x]))
            x+=1
        return abs(area)
        
    def cent_latitude(x = 0):
        cent_lat = 0
        while x < len(polygon)-1:

            cent_lat += (latitude(polygon[x])+latitude(polygon[x+1])*\
                         (latitude(polygon[x])*longitude(polygon[x+1])-\
                          latitude(polygon[x+1])*longitude(polygon[x])))
            x+=1
        return (cent_lat)/(6*poly_area())
    def cent_longitude(x = 0):
        cent_long = 0
        while x < len(polygon)-1:
            cent_long += (longitude(polygon[x])+longitude(polygon[x+1]))*\
                         (latitude(polygon[x])*longitude(polygon[x+1])-\
                          latitude(polygon[x+1]*longitude(polygon[x])))
            x+=1
        return (cent_long)/(6*poly_area())
    return cent_latitude(), cent_longitude(), poly_area()
            
            
