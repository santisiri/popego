import os
import getopt, sys

path = './popserver/public/css/widget/themes/'
templatePath = path + "templates/"
basefiles = ['widget_COLOR.css','widget_content_COLOR.css','card_bubble_COLOR.css','card_bubble_COLOR_ie6.css','card_content_COLOR.css'] 

def createThemes(colors):
    for bname in basefiles:
        bfile = open(templatePath + bname, "r")
        for color in colors:
            bfile.seek(0)
            createFile(bfile, bname, color)
        bfile.close()
    
def createFile(basefile, basename, color):
    newfile = open(path + basename.replace('COLOR', color), "w")
    
    for line in basefile:
        newfile.write(line.replace('COLOR', color))
        
    newfile.close()
 

def usage():
  print sys.argv[0] + " [--default-themes|--colors=color1,color2,...]"


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdc", ["help", "colors=", "default-themes"] )
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    
    if(len(opts) == 0):
      usage()
      sys.exit(2)

    colors = None
    
    for o, a in opts:
        if o in ("-h", "--help"):
          usage()
          sys.exit()
        if o == "--colors":
          colors = a.split(",")
        if o in ("-d","--default-themes"):
          colors = ['0d6d6d', '3d3d3d', '4d8000', '6aac28', '9e9e9e', '013c76',\
                    '129fc2', '0159b1', '666666', '993300', 'a9d103', 'aa0000',\
                    'ac20ac', 'c01258', 'dddddd', 'e4e40a', 'e23d14', 'e72510', 'ff900a', 'ff3366']

    createThemes(colors)


if __name__ == "__main__":
    main()



