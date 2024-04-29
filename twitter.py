import httpx
import html

def sift(s):
    b = True
    buf = ""
    for i in range(len(s)):
        if s[i] == '<':
            b = False
        elif s[i - 1] == '>':
            b = True
        if b:
            buf = buf + s[i]

    return buf


class Data_X:
    def __init__(self):
        pass

    def __capture_url(self, s):
        n0 = s.find('twitter.com')
        if n0 == -1:
            n0 = s.find('x.com')
            if n0 == -1:
                return None

        u = s[n0:]
        
        try:
            n1 = u.find('status/')
        except Exception as err:
            print('Bad url: ', err)
            return None
        else:
            t = 'https://publish.twitter.com/oembed?url='
            return t + 'https://' + u[:n1 + 26]
    
    def get_data(self, s):
        s = self.__capture_url(s)
        if s == None:
            return None
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = httpx.get(s, headers=headers)
        except Exception as err:
            print(f"URL {s} not reachable:\n", err)
            return None
        
        try:
            r = r.json()
        except Exception as err:
            print(f"URL {s} not reachable:\n", err)
            return None
        
        try:
            coment = r['html']
            coment = html.unescape(coment)                       
            coment = coment.replace('<br>', '\r')
            coment = sift(coment)
        except Exception as err:
            print(err)
            return None
        
        return coment


def twitter(e):
    for x in e.tokens.read_privmsg():
        s = x[3]
                
        data = Data_X()
        s = data.get_data(s)
        if s: 
            chan = x[2] 
            msg = " " + "𝕏 " + "🛈 "+ s 
            e.sender.action(chan, msg)

