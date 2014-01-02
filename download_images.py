from pattern.web import Bing, IMAGE
import urllib

engine = Bing()

for counter, result in enumerate(engine.search('meme', type=IMAGE)):
    try:
        urllib.urlretrieve(result.url, "images/%s.jpg" % counter)
    except:
        pass