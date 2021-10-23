import Tokens

integers = {
    '一' : 1,
    '二' : 2,
    '三' : 3,
    '四' : 4,
    '五' : 5,
    '六' : 6,
    '七' : 7,
    '八' : 8,
    '九' : 9,
    '十' : 10,
    '百' : 100,
    '千' : 1000,
    '万' : 10000
}

honorifics = [
    "さん",
    "ちゃん",
    "さま",
    "くん",
    "たん",
    "せんぱい",
    "せんせい",
    "先生",
    "先輩",
    "君",
    "様",
    "王女様",
    "殿",
    "どの",
    "との",
    "ばか", #I know, not really an honorific :)
    "ぱいせん"
]

romajiHonorifics = { # ASM doesnt allow hiragana, kanji, etc. so we have to romajify them :(
    "さん" : "san",
    "ちゃん" : "chan",
    "さま" : "sama",
    "くん" : "kun",
    "たん" : "tan",
    "せんぱい" : "senpai",
    "せんせい" : "sensei",
    "先生" : "sensei_k",
    "先輩" : "senpai_k",
    "君" : "kun_k",
    "様" : "sama_k",
    "王女様" : "oujosama_k",
    "殿" : "dono_k",
    "どの" : "dono",
    "との" : "tono",
    "ばか" : "baka",
    "ぱいせん" : "paisen"
}

fileExtensions = [
    ".sadge",
    ".pain",
    ".suffering",
    ".painandsuffering",
    ".yabe",
    ".crabs",
    ".plankton",
    ".planktonthrowsitback",
    ".formula",
    ".theformula"
]
