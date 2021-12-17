def violet_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    '''
    Function to change colour of word cloud
    '''
    return ("hsl(271, %d%%" % random.randint(60, 100)) + (", %d%%)" % random.randint(40, 80))


def handpicked_stopwords():
    '''
    Function returning a list of stopwords handpicked and updated while generating test wordclouds
    '''
    return ["people","women","girl","woman","time","thing","year","made","back","make","continue"
            "lot", "find", "day", "big", "know", "want", "start", "world","person","long","bring","country","run",
            "read","state","leave","live","happen","bit","million","cut","buy","put","set","end", "place","today"
            "story", "entire", "meet", "add", "call","game","high","continue","inside","door","email","watch","real",
            "week","fact","ask","spend","public","pull","turn","rest","fun","play","point","years","life","let","yeah",
            "open", "talk", "issue", "immediately","pass", "work","allow","hour","minute","importantly", "involve", "extra","wow",
            "tear", "clear", "pattern","making", "alive", "check", "lot", "reach", "night", "stage", "source", "beg", "ready","tell", 
            "left","right","room", "yeah", "see", "sort", "number", "show", "test","season", "demonstrate","realize", "weekend", "song", 
            "come", "theme", "view", "link", "early", "give","note", "explain", "choose","news","local", "global", "case",  "means"
            "united", "states","u.s","birthday","brother", "prime", "minister", "provide","hold","focus","hand","plan","loose","lose","saty"
            "virginia","west","thousand","billion","moment","speak","good","great","forward","backward","matter"
            "billion","thousand","hard","film","good","close","hear","american","african","change","u","s","united","state",
            "lose","loose","happy","important","white","visual","kobe","bryant","trillion","past","future","easy","matter","level","experience",
            "enjoy","month","group","step","amazing","reason","question","answer","stand","mind","wind","sun","sea","mountains"
            "castle", "mansion", "stop", "start", "idea","concept","form","ireland","north","sixty6","nightlife","belfast","telegraph","cuckoo",
            "nan", "nov", "dec", "cathedral", "story", "lady","roxy","write", "grow", "ago", "age", "include", "quarter","northern","december",
            "november","january", "today", "tomorrow","parlour","expect","win","sister","brother","decide", "national", "shine", "october", "february"
            "april", "may", "june", "july", "september", "garage", "alibi", "shiro", "onion", "friend", "remember", "book", "miss", "guy", "nice", "gallery",
            "line", "taxpayer", "walk", "half", "whole", "wait", "wrong", "lead", "program", "NaN","mom", "boy", "girl", "stuff", "school", "learn", "feel", "understand"
            "character", "young", "trouble", "event", "bad", "sound", "ira", "checkpoint", "sit", "head", "kind", "team", "bot", "mum","problem",
            "create", "botanic", "human", "deal", "term","mail","history","finally","daugther","think","stay","leave","face", "pick","special","city","indivisdual",
            "understand", "push","put","area","result","movie", "begin", "end"]