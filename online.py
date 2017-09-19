from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods import posts
from urllib.request import urlopen
import urllib
import io
client = Client('http://actandcare.fr/xmlrpc.php', 'marie', 'mariaure1977')
images = client.call(media.GetMediaLibrary({'mime_type':'image/jpeg'}))
chs = client.call(posts.GetPosts({'post_type': 'tribe_venue','number':10000}))
imgs = []
class Image:
    def __init__(self, link, title):
        self.file = 0
        self.link = link
        self.title = title
        imgs.append(self)
    def setFile(self, file):
        self.file = file
for i in images:
    Image(i.link, i.title)
    
def getImages(d = [0,12]):
    data = []
    for img in imgs[d[0]:d[1]]:
        try:
            i = urlopen(img.link).read()
            imageFile = io.BytesIO(i)
            img.setFile(imageFile)
            data.append(img)
        except: print(img.link)
    return data

def getChs():
    data = []
    for ch in chs:
        data.append(ch.title)
    return data
    
def uploadImageFromUrl(url,name):
    fileName = name+url.split('.')[-1]
    urllib.urlretrieve(url, fileName)
    data = {
        'name': fileName,
        'type': 'image/'+url.split('.')[-1]
        }
    with open(fileName, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    response = client.call(media.UploadFile(data))
    
    
