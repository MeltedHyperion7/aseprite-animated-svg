# Aseptite Animated SVG
Combine SVG files exported by Aseprite into a single animated file.

# Usage
Pass in the path to one of the files in the animation (it is assumed the files were numbered by Aseprite).  
```$ python3 aseprite-animated-svg.py /path/to/file1.svg```  
   
The script outputs the SVG markup to standard output. You can redirect it to a file to save it.  
```$ python3 aseprite-animated-svg.py /path/to/file1.svg > /path/to/out.svg```  