#!/usr/bin/env python3
"""
Generate kanji data JSON for the Japanese Kanji web app.
Uses the 常用漢字 (Jōyō Kanji) list with readings and common compounds.
"""
import json

# 常用漢字 data: each entry has on'yomi, kun'yomi, meaning, and common compounds
# Format: "kanji": {"on": [...], "kun": [...], "meaning": "...", "compounds": [{"word":"...", "reading":"...", "meaning":"..."}, ...]}

joyo_kanji = {
    "一": {"on": ["イチ","イツ"], "kun": ["ひと","ひと.つ"], "meaning": "one", "compounds": [
        {"word":"一つ","reading":"ひとつ","meaning":"one thing"},
        {"word":"一人","reading":"ひとり","meaning":"one person"},
        {"word":"一番","reading":"いちばん","meaning":"number one, best"},
        {"word":"一月","reading":"いちがつ","meaning":"January"},
        {"word":"一緒","reading":"いっしょ","meaning":"together"},
        {"word":"一度","reading":"いちど","meaning":"once"}
    ]},
    "二": {"on": ["ニ","ジ"], "kun": ["ふた","ふた.つ"], "meaning": "two", "compounds": [
        {"word":"二つ","reading":"ふたつ","meaning":"two things"},
        {"word":"二人","reading":"ふたり","meaning":"two people"},
        {"word":"二月","reading":"にがつ","meaning":"February"},
        {"word":"二度","reading":"にど","meaning":"twice"},
        {"word":"二階","reading":"にかい","meaning":"second floor"}
    ]},
    "三": {"on": ["サン","ザン"], "kun": ["み","み.つ"], "meaning": "three", "compounds": [
        {"word":"三つ","reading":"みっつ","meaning":"three things"},
        {"word":"三人","reading":"さんにん","meaning":"three people"},
        {"word":"三月","reading":"さんがつ","meaning":"March"},
        {"word":"三時","reading":"さんじ","meaning":"three o'clock"},
        {"word":"三角","reading":"さんかく","meaning":"triangle"}
    ]},
    "四": {"on": ["シ"], "kun": ["よ","よ.つ","よん"], "meaning": "four", "compounds": [
        {"word":"四つ","reading":"よっつ","meaning":"four things"},
        {"word":"四月","reading":"しがつ","meaning":"April"},
        {"word":"四時","reading":"よじ","meaning":"four o'clock"},
        {"word":"四方","reading":"しほう","meaning":"all directions"},
        {"word":"四季","reading":"しき","meaning":"four seasons"}
    ]},
    "五": {"on": ["ゴ"], "kun": ["いつ","いつ.つ"], "meaning": "five", "compounds": [
        {"word":"五つ","reading":"いつつ","meaning":"five things"},
        {"word":"五月","reading":"ごがつ","meaning":"May"},
        {"word":"五時","reading":"ごじ","meaning":"five o'clock"},
        {"word":"五十","reading":"ごじゅう","meaning":"fifty"},
        {"word":"五感","reading":"ごかん","meaning":"five senses"}
    ]},
    "六": {"on": ["ロク","リク"], "kun": ["む","む.つ","ろく"], "meaning": "six", "compounds": [
        {"word":"六つ","reading":"むっつ","meaning":"six things"},
        {"word":"六月","reading":"ろくがつ","meaning":"June"},
        {"word":"六時","reading":"ろくじ","meaning":"six o'clock"},
        {"word":"六十","reading":"ろくじゅう","meaning":"sixty"},
        {"word":"六角","reading":"ろっかく","meaning":"hexagon"}
    ]},
    "七": {"on": ["シチ"], "kun": ["なな","なな.つ","しち"], "meaning": "seven", "compounds": [
        {"word":"七つ","reading":"ななつ","meaning":"seven things"},
        {"word":"七月","reading":"しちがつ","meaning":"July"},
        {"word":"七時","reading":"しちじ","meaning":"seven o'clock"},
        {"word":"七十","reading":"しちじゅう","meaning":"seventy"},
        {"word":"七夕","reading":"たなばた","meaning":"Tanabata festival"}
    ]},
    "八": {"on": ["ハチ"], "kun": ["や","や.つ","よう"], "meaning": "eight", "compounds": [
        {"word":"八つ","reading":"やっつ","meaning":"eight things"},
        {"word":"八月","reading":"はちがつ","meaning":"August"},
        {"word":"八時","reading":"はちじ","meaning":"eight o'clock"},
        {"word":"八十","reading":"はちじゅう","meaning":"eighty"},
        {"word":"八方","reading":"はっぽう","meaning":"all directions"}
    ]},
    "九": {"on": ["キュウ","ク"], "kun": ["ここの","ここの.つ"], "meaning": "nine", "compounds": [
        {"word":"九つ","reading":"ここのつ","meaning":"nine things"},
        {"word":"九月","reading":"くがつ","meaning":"September"},
        {"word":"九時","reading":"くじ","meaning":"nine o'clock"},
        {"word":"九十","reading":"きゅうじゅう","meaning":"ninety"},
        {"word":"九州","reading":"きゅうしゅう","meaning":"Kyushu"}
    ]},
    "十": {"on": ["ジュウ","ジッ"], "kun": ["とお","と"], "meaning": "ten", "compounds": [
        {"word":"十","reading":"じゅう","meaning":"ten"},
        {"word":"十月","reading":"じゅうがつ","meaning":"October"},
        {"word":"十分","reading":"じゅっぷん","meaning":"ten minutes"},
        {"word":"十字","reading":"じゅうじ","meaning":"cross"},
        {"word":"数十","reading":"すうじゅう","meaning":"tens of"}
    ]},
    "百": {"on": ["ヒャク","ビャク"], "kun": ["もも"], "meaning": "hundred", "compounds": [
        {"word":"百","reading":"ひゃく","meaning":"hundred"},
        {"word":"百人","reading":"ひゃくにん","meaning":"100 people"},
        {"word":"百年","reading":"ひゃくねん","meaning":"100 years"},
        {"word":"百貨店","reading":"ひゃっかてん","meaning":"department store"},
        {"word":"数百","reading":"すうひゃく","meaning":"several hundred"}
    ]},
    "千": {"on": ["セン"], "kun": ["ち"], "meaning": "thousand", "compounds": [
        {"word":"千","reading":"せん","meaning":"thousand"},
        {"word":"千人","reading":"せんにん","meaning":"1000 people"},
        {"word":"千年","reading":"せんねん","meaning":"1000 years"},
        {"word":"千円","reading":"せんえん","meaning":"1000 yen"},
        {"word":"数千","reading":"すうせん","meaning":"several thousand"}
    ]},
    "万": {"on": ["マン","バン"], "kun": ["よろず"], "meaning": "ten thousand", "compounds": [
        {"word":"万","reading":"まん","meaning":"ten thousand"},
        {"word":"万人","reading":"まんにん","meaning":"all people"},
        {"word":"万年筆","reading":"まんねんひつ","meaning":"fountain pen"},
        {"word":"一万","reading":"いちまん","meaning":"10,000"},
        {"word":"数万","reading":"すうまん","meaning":"tens of thousands"}
    ]},
    "年": {"on": ["ネン"], "kun": ["とし"], "meaning": "year", "compounds": [
        {"word":"今年","reading":"ことし","meaning":"this year"},
        {"word":"去年","reading":"きょねん","meaning":"last year"},
        {"word":"来年","reading":"らいねん","meaning":"next year"},
        {"word":"年齢","reading":"ねんれい","meaning":"age"},
        {"word":"年間","reading":"ねんかん","meaning":"one year period"},
        {"word":"少年","reading":"しょうねん","meaning":"boy, youth"}
    ]},
    "月": {"on": ["ゲツ","ガツ"], "kun": ["つき"], "meaning": "month, moon", "compounds": [
        {"word":"今月","reading":"こんげつ","meaning":"this month"},
        {"word":"先月","reading":"せんげつ","meaning":"last month"},
        {"word":"来月","reading":"らいげつ","meaning":"next month"},
        {"word":"月曜日","reading":"げつようび","meaning":"Monday"},
        {"word":"月光","reading":"げっこう","meaning":"moonlight"},
        {"word":"満月","reading":"まんげつ","meaning":"full moon"}
    ]},
    "日": {"on": ["ニチ","ジツ"], "kun": ["ひ","か"], "meaning": "day, sun", "compounds": [
        {"word":"今日","reading":"きょう","meaning":"today"},
        {"word":"昨日","reading":"きのう","meaning":"yesterday"},
        {"word":"明日","reading":"あした","meaning":"tomorrow"},
        {"word":"日本","reading":"にほん","meaning":"Japan"},
        {"word":"毎日","reading":"まいにち","meaning":"every day"},
        {"word":"日光","reading":"にっこう","meaning":"sunlight"},
        {"word":"日記","reading":"にっき","meaning":"diary"},
        {"word":"休日","reading":"きゅうじつ","meaning":"holiday"}
    ]},
    "時": {"on": ["ジ"], "kun": ["とき"], "meaning": "time", "compounds": [
        {"word":"時間","reading":"じかん","meaning":"time, hour"},
        {"word":"時計","reading":"とけい","meaning":"clock, watch"},
        {"word":"一時","reading":"いちじ","meaning":"one o'clock"},
        {"word":"同時","reading":"どうじ","meaning":"simultaneous"},
        {"word":"時代","reading":"じだい","meaning":"era, age"},
        {"word":"時々","reading":"ときどき","meaning":"sometimes"}
    ]},
    "分": {"on": ["ブン","フン","ブ"], "kun": ["わ.ける","わ.かれる","わ.かる"], "meaning": "divide, part, minute", "compounds": [
        {"word":"一分","reading":"いっぷん","meaning":"one minute"},
        {"word":"十分","reading":"じゅっぷん","meaning":"ten minutes"},
        {"word":"自分","reading":"じぶん","meaning":"oneself"},
        {"word":"半分","reading":"はんぶん","meaning":"half"},
        {"word":"分かる","reading":"わかる","meaning":"to understand"},
        {"word":"分ける","reading":"わける","meaning":"to divide"}
    ]},
    "秒": {"on": ["ビョウ"], "kun": [], "meaning": "second", "compounds": [
        {"word":"一秒","reading":"いちびょう","meaning":"one second"},
        {"word":"数秒","reading":"すうびょう","meaning":"a few seconds"},
        {"word":"秒速","reading":"びょうそく","meaning":"per second"},
        {"word":"何秒","reading":"なんびょう","meaning":"how many seconds"}
    ]},
    "週": {"on": ["シュウ"], "kun": [], "meaning": "week", "compounds": [
        {"word":"今週","reading":"こんしゅう","meaning":"this week"},
        {"word":"先週","reading":"せんしゅう","meaning":"last week"},
        {"word":"来週","reading":"らいしゅう","meaning":"next week"},
        {"word":"毎週","reading":"まいしゅう","meaning":"every week"},
        {"word":"週末","reading":"しゅうまつ","meaning":"weekend"},
        {"word":"一週間","reading":"いっしゅうかん","meaning":"one week"}
    ]},
    "曜": {"on": ["ヨウ"], "kun": [], "meaning": "weekday", "compounds": [
        {"word":"日曜日","reading":"にちようび","meaning":"Sunday"},
        {"word":"月曜日","reading":"げつようび","meaning":"Monday"},
        {"word":"火曜日","reading":"かようび","meaning":"Tuesday"},
        {"word":"水曜日","reading":"すいようび","meaning":"Wednesday"},
        {"word":"木曜日","reading":"もくようび","meaning":"Thursday"},
        {"word":"金曜日","reading":"きんようび","meaning":"Friday"},
        {"word":"土曜日","reading":"どようび","meaning":"Saturday"}
    ]},
    "上": {"on": ["ジョウ","シャン"], "kun": ["うえ","あ.げる","のぼ.る","かみ"], "meaning": "above, up", "compounds": [
        {"word":"上","reading":"うえ","meaning":"above"},
        {"word":"上げる","reading":"あげる","meaning":"to raise"},
        {"word":"登る","reading":"のぼる","meaning":"to climb"},
        {"word":"上手","reading":"じょうず","meaning":"skillful"},
        {"word":"以上","reading":"いじょう","meaning":"more than"},
        {"word":"午前","reading":"ごぜん","meaning":"morning, AM"},
        {"word":"上昇","reading":"じょうしょう","meaning":"rise"},
        {"word":"上司","reading":"じょうし","meaning":"boss"}
    ]},
    "下": {"on": ["カ","ゲ"], "kun": ["した","さ.げる","お.りる","くだ.る"], "meaning": "below, down", "compounds": [
        {"word":"下","reading":"した","meaning":"below"},
        {"word":"下げる","reading":"さげる","meaning":"to lower"},
        {"word":"下手","reading":"へた","meaning":"unskillful"},
        {"word":"以下","reading":"いか","meaning":"less than"},
        {"word":"午後","reading":"ごご","meaning":"afternoon, PM"},
        {"word":"下降","reading":"かこう","meaning":"descent"},
        {"word":"地下","reading":"ちか","meaning":"underground"},
        {"word":"部下","reading":"ぶか","meaning":"subordinate"}
    ]},
    "中": {"on": ["チュウ"], "kun": ["なか","うち","あた.る"], "meaning": "middle, inside", "compounds": [
        {"word":"中","reading":"なか","meaning":"inside"},
        {"word":"中国","reading":"ちゅうごく","meaning":"China"},
        {"word":"中学","reading":"ちゅうがく","meaning":"middle school"},
        {"word":"中心","reading":"ちゅうしん","meaning":"center"},
        {"word":"途中","reading":"とちゅう","meaning":"on the way"},
        {"word":"中古","reading":"ちゅうこ","meaning":"used, second-hand"},
        {"word":"中止","reading":"ちゅうし","meaning":"suspension"},
        {"word":"中学生","reading":"ちゅうがくせい","meaning":"middle school student"}
    ]},
    "大": {"on": ["ダイ","タイ"], "kun": ["おお","おお.きい"], "meaning": "big, large", "compounds": [
        {"word":"大きい","reading":"おおきい","meaning":"big"},
        {"word":"大学","reading":"だいがく","meaning":"university"},
        {"word":"大人","reading":"おとな","meaning":"adult"},
        {"word":"大切","reading":"たいせつ","meaning":"important"},
        {"word":"大変","reading":"たいへん","meaning":"very, terrible"},
        {"word":"大使","reading":"たいし","meaning":"ambassador"},
        {"word":"大会","reading":"たいかい","meaning":"convention"},
        {"word":"大手","reading":"おおて","meaning":"major company"}
    ]},
    "小": {"on": ["ショウ"], "kun": ["ちい.さい","こ","お"], "meaning": "small, little", "compounds": [
        {"word":"小さい","reading":"ちいさい","meaning":"small"},
        {"word":"小学","reading":"しょうがく","meaning":"elementary school"},
        {"word":"小学生","reading":"しょうがくせい","meaning":"elementary student"},
        {"word":"時間","reading":"じかん","meaning":"hour"},
        {"word":"小説","reading":"しょうせつ","meaning":"novel"},
        {"word":"少年","reading":"しょうねん","meaning":"boy"},
        {"word":"小包","reading":"こづつみ","meaning":"parcel"},
        {"word":"小鳥","reading":"ことり","meaning":"small bird"}
    ]},
    "山": {"on": ["サン"], "kun": ["やま"], "meaning": "mountain", "compounds": [
        {"word":"山","reading":"やま","meaning":"mountain"},
        {"word":"富士山","reading":"ふじさん","meaning":"Mt. Fuji"},
        {"word":"火山","reading":"かざん","meaning":"volcano"},
        {"word":"山川","reading":"さんせん","meaning":"mountains and rivers"},
        {"word":"山田","reading":"やまだ","meaning":"Yamada (surname)"},
        {"word":"登山","reading":"とざん","meaning":"mountain climbing"},
        {"word":"山脈","reading":"さんみゃく","meaning":"mountain range"}
    ]},
    "川": {"on": ["セン"], "kun": ["かわ"], "meaning": "river", "compounds": [
        {"word":"川","reading":"かわ","meaning":"river"},
        {"word":"河川","reading":"かせん","meaning":"rivers"},
        {"word":"冰川","reading":"ひょうせん","meaning":"glacier"},
        {"word":"川崎","reading":"かわさき","meaning":"Kawasaki"},
        {"word":"小川","reading":"おがわ","meaning":"stream"},
        {"word":"川辺","reading":"かわべ","meaning":"riverside"}
    ]},
    "田": {"on": ["デン"], "kun": ["た"], "meaning": "rice field", "compounds": [
        {"word":"田","reading":"た","meaning":"rice field"},
        {"word":"田中","reading":"たなか","meaning":"Tanaka (surname)"},
        {"word":"田舎","reading":"いなか","meaning":"countryside"},
        {"word":"水田","reading":"すいでん","meaning":"paddy field"},
        {"word":"田地","reading":"でんち","meaning":"farmland"},
        {"word":"油田","reading":"ゆでん","meaning":"oil field"}
    ]},
    "口": {"on": ["コウ","ク"], "kun": ["くち"], "meaning": "mouth", "compounds": [
        {"word":"口","reading":"くち","meaning":"mouth"},
        {"word":"人口","reading":"じんこう","meaning":"population"},
        {"word":"出口","reading":"でぐち","meaning":"exit"},
        {"word":"入口","reading":"いりぐち","meaning":"entrance"},
        {"word":"口座","reading":"こうざ","meaning":"account"},
        {"word":"口約束","reading":"くちやくそく","meaning":"verbal promise"},
        {"word":"早口","reading":"はやくち","meaning":"fast speech"}
    ]},
    "目": {"on": ["モク","ボク"], "kun": ["め","ま"], "meaning": "eye", "compounds": [
        {"word":"目","reading":"め","meaning":"eye"},
        {"word":"目的","reading":"もくてき","meaning":"purpose"},
        {"word":"目標","reading":"もくひょう","meaning":"goal"},
        {"word":"注目","reading":"ちゅうもく","meaning":"attention"},
        {"word":"目前","reading":"もくぜん","meaning":"before one's eyes"},
        {"word":"一目","reading":"ひとめ","meaning":"one glance"},
        {"word":"番組","reading":"ばんぐみ","meaning":"TV program"}
    ]},
    "耳": {"on": ["ジ"], "kun": ["みみ"], "meaning": "ear", "compounds": [
        {"word":"耳","reading":"みみ","meaning":"ear"},
        {"word":"耳鼻科","reading":"じびか","meaning":"ENT department"},
        {"word":"早耳","reading":"はやみみ","meaning":"quick hearing"},
        {"word":"片耳","reading":"かたみみ","meaning":"one ear"},
        {"word":"耳鳴り","reading":"みみなり","meaning":"tinnitus"}
    ]},
    "手": {"on": ["シュ"], "kun": ["て","た"], "meaning": "hand", "compounds": [
        {"word":"手","reading":"て","meaning":"hand"},
        {"word":"上手","reading":"じょうず","meaning":"skillful"},
        {"word":"下手","reading":"へた","meaning":"unskillful"},
        {"word":"手紙","reading":"てがみ","meaning":"letter"},
        {"word":"手術","reading":"しゅじゅつ","meaning":"surgery"},
        {"word":"手段","reading":"しゅだん","meaning":"means"},
        {"word":"選手","reading":"せんしゅ","meaning":"athlete"},
        {"word":"手伝い","reading":"てつだい","meaning":"help"}
    ]},
    "足": {"on": ["ソク"], "kun": ["あし","た.りる","た.す"], "meaning": "foot, leg, sufficient", "compounds": [
        {"word":"足","reading":"あし","meaning":"foot, leg"},
        {"word":"足りる","reading":"たりる","meaning":"to be sufficient"},
        {"word":"不足","reading":"ふそく","meaning":"insufficient"},
        {"word":"満足","reading":"まんぞく","meaning":"satisfaction"},
        {"word":"遠足","reading":"えんそく","meaning":"excursion"},
        {"word":"補足","reading":"ほそく","meaning":"supplement"}
    ]},
    "人": {"on": ["ジン","ニン"], "kun": ["ひと"], "meaning": "person", "compounds": [
        {"word":"人","reading":"ひと","meaning":"person"},
        {"word":"日本人","reading":"にほんじん","meaning":"Japanese person"},
        {"word":"人間","reading":"にんげん","meaning":"human being"},
        {"word":"人口","reading":"じんこう","meaning":"population"},
        {"word":"人生","reading":"じんせい","meaning":"life"},
        {"word":"人民","reading":"じんみん","meaning":"people"},
        {"word":"他人","reading":"たにん","meaning":"other person"},
        {"word":"大人","reading":"おとな","meaning":"adult"},
        {"word":"恋人","reading":"こいびと","meaning":"lover"}
    ]},
    "男": {"on": ["ダン","ナン"], "kun": ["おとこ"], "meaning": "man", "compounds": [
        {"word":"男","reading":"おとこ","meaning":"man"},
        {"word":"男性","reading":"だんせい","meaning":"male"},
        {"word":"男子","reading":"だんし","meaning":"boy"},
        {"word":"男女","reading":"だんじょ","meaning":"men and women"},
        {"word":"長男","reading":"ちょうなん","meaning":"eldest son"},
        {"word":"男の子","reading":"おとこのこ","meaning":"boy"}
    ]},
    "女": {"on": ["ジョ","ニョ"], "kun": ["おんな","め"], "meaning": "woman", "compounds": [
        {"word":"女","reading":"おんな","meaning":"woman"},
        {"word":"女性","reading":"じょせい","meaning":"female"},
        {"word":"女子","reading":"じょし","meaning":"girl"},
        {"word":"男女","reading":"だんじょ","meaning":"men and women"},
        {"word":"彼女","reading":"かのじょ","meaning":"she, girlfriend"},
        {"word":"女の子","reading":"おんなのこ","meaning":"girl"},
        {"word":"女王","reading":"じょおう","meaning":"queen"}
    ]},
    "子": {"on": ["シ","ス"], "kun": ["こ"], "meaning": "child", "compounds": [
        {"word":"子","reading":"こ","meaning":"child"},
        {"word":"子供","reading":"こども","meaning":"children"},
        {"word":"学生","reading":"がくせい","meaning":"student"},
        {"word":"女子","reading":"じょし","meaning":"girl"},
        {"word":"男子","reading":"だんし","meaning":"boy"},
        {"word":"椅子","reading":"いす","meaning":"chair"},
        {"word":"様子","reading":"ようす","meaning":"appearance"},
        {"word":"原子","reading":"げんし","meaning":"atom"}
    ]},
    "心": {"on": ["シン"], "kun": ["こころ"], "meaning": "heart, mind", "compounds": [
        {"word":"心","reading":"こころ","meaning":"heart, mind"},
        {"word":"心配","reading":"しんぱい","meaning":"worry"},
        {"word":"安心","reading":"あんしん","meaning":"relief"},
        {"word":"中心","reading":"ちゅうしん","meaning":"center"},
        {"word":"心理","reading":"しんり","meaning":"psychology"},
        {"word":"決心","reading":"けっしん","meaning":"determination"},
        {"word":"感動","reading":"かんどう","meaning":"being moved"},
        {"word":"心臓","reading":"しんぞう","meaning":"heart (organ)"}
    ]},
    "水": {"on": ["スイ"], "kun": ["みず"], "meaning": "water", "compounds": [
        {"word":"水","reading":"みず","meaning":"water"},
        {"word":"水曜日","reading":"すいようび","meaning":"Wednesday"},
        {"word":"水道","reading":"すいどう","meaning":"water supply"},
        {"word":"水泳","reading":"すいえい","meaning":"swimming"},
        {"word":"水平","reading":"すいへい","meaning":"level, horizontal"},
        {"word":"水田","reading":"すいでん","meaning":"paddy field"},
        {"word":"雨水","reading":"あまみず","meaning":"rainwater"},
        {"word":"洪水","reading":"こうずい","meaning":"flood"}
    ]},
    "火": {"on": ["カ"], "kun": ["ひ","ほ"], "meaning": "fire", "compounds": [
        {"word":"火","reading":"ひ","meaning":"fire"},
        {"word":"火曜日","reading":"かようび","meaning":"Tuesday"},
        {"word":"火山","reading":"かざん","meaning":"volcano"},
        {"word":"花火","reading":"はなび","meaning":"fireworks"},
        {"word":"火災","reading":"かさい","meaning":"fire disaster"},
        {"word":"消火","reading":"しょうか","meaning":"fire extinguishing"},
        {"word":"炎","reading":"ほのお","meaning":"flame"}
    ]},
    "木": {"on": ["モク","ボク"], "kun": ["き","こ"], "meaning": "tree, wood", "compounds": [
        {"word":"木","reading":"き","meaning":"tree"},
        {"word":"木曜日","reading":"もくようび","meaning":"Thursday"},
        {"word":"木材","reading":"もくざい","meaning":"lumber"},
        {"word":"大木","reading":"たいぼく","meaning":"large tree"},
        {"word":"木工","reading":"もっこう","meaning":"woodworking"},
        {"word":"樹木","reading":"じゅもく","meaning":"trees"},
        {"word":"木造","reading":"もくぞう","meaning":"wooden structure"}
    ]},
    "金": {"on": ["キン","コン"], "kun": ["かね","かな"], "meaning": "gold, money", "compounds": [
        {"word":"金","reading":"かね","meaning":"money"},
        {"word":"金曜日","reading":"きんようび","meaning":"Friday"},
        {"word":"お金","reading":"おかね","meaning":"money"},
        {"word":"金色","reading":"きんいろ","meaning":"gold color"},
        {"word":"銀行","reading":"ぎんこう","meaning":"bank"},
        {"word":"金額","reading":"きんがく","meaning":"amount of money"},
        {"word":"税金","reading":"ぜいきん","meaning":"tax"},
        {"word":"賞金","reading":"しょうきん","meaning":"prize money"}
    ]},
    "土": {"on": ["ド","ト"], "kun": ["つち"], "meaning": "earth, soil", "compounds": [
        {"word":"土","reading":"つち","meaning":"soil"},
        {"word":"土曜日","reading":"どようび","meaning":"Saturday"},
        {"word":"土地","reading":"とち","meaning":"land"},
        {"word":"国土","reading":"こくど","meaning":"national territory"},
        {"word":"土木","reading":"どぼく","meaning":"civil engineering"},
        {"word":"粘土","reading":"ねんど","meaning":"clay"},
        {"word":"本土","reading":"ほんど","meaning":"mainland"}
    ]},
    "天": {"on": ["テン"], "kun": ["あめ","あま","そら"], "meaning": "heaven, sky", "compounds": [
        {"word":"天気","reading":"てんき","meaning":"weather"},
        {"word":"天国","reading":"てんごく","meaning":"heaven"},
        {"word":"天才","reading":"てんさい","meaning":"genius"},
        {"word":"天然","reading":"てんねん","meaning":"natural"},
        {"word":"天皇","reading":"てんのう","meaning":"Emperor"},
        {"word":"天文","reading":"てんもん","meaning":"astronomy"},
        {"word":"天使","reading":"てんし","meaning":"angel"},
        {"word":"晴天","reading":"せいてん","meaning":"clear sky"}
    ]},
    "気": {"on": ["キ","ケ"], "kun": [], "meaning": "spirit, energy, air", "compounds": [
        {"word":"天気","reading":"てんき","meaning":"weather"},
        {"word":"元気","reading":"げんき","meaning":"energetic"},
        {"word":"病気","reading":"びょうき","meaning":"illness"},
        {"word":"気分","reading":"きぶん","meaning":"mood"},
        {"word":"空気","reading":"くうき","meaning":"air"},
        {"word":"電気","reading":"でんき","meaning":"electricity"},
        {"word":"蒸気","reading":"じょうき","meaning":"steam"},
        {"word":"勇気","reading":"ゆうき","meaning":"courage"}
    ]},
    "生": {"on": ["セイ","ショウ"], "kun": ["い.きる","う.まれる","なま"], "meaning": "life, birth, raw", "compounds": [
        {"word":"生きる","reading":"いきる","meaning":"to live"},
        {"word":"生まれる","reading":"うまれる","meaning":"to be born"},
        {"word":"学生","reading":"がくせい","meaning":"student"},
        {"word":"先生","reading":"せんせい","meaning":"teacher"},
        {"word":"生活","reading":"せいかつ","meaning":"life, living"},
        {"word":"生産","reading":"せいさん","meaning":"production"},
        {"word":"人生","reading":"じんせい","meaning":"life"},
        {"word":"誕生日","reading":"たんじょうび","meaning":"birthday"},
        {"word":"生ビール","reading":"なまビール","meaning":"draft beer"}
    ]},
    "学": {"on": ["ガク"], "kun": ["まな.ぶ"], "meaning": "study, learning", "compounds": [
        {"word":"学ぶ","reading":"まなぶ","meaning":"to learn"},
        {"word":"学校","reading":"がっこう","meaning":"school"},
        {"word":"学生","reading":"がくせい","meaning":"student"},
        {"word":"大学","reading":"だいがく","meaning":"university"},
        {"word":"科学","reading":"かがく","meaning":"science"},
        {"word":"文学","reading":"ぶんがく","meaning":"literature"},
        {"word":"数学","reading":"すうがく","meaning":"mathematics"},
        {"word":"入学","reading":"にゅうがく","meaning":"enrollment"},
        {"word":"卒業","reading":"そつぎょう","meaning":"graduation"}
    ]},
    "校": {"on": ["コウ"], "kun": [], "meaning": "school", "compounds": [
        {"word":"学校","reading":"がっこう","meaning":"school"},
        {"word":"高校","reading":"こうこう","meaning":"high school"},
        {"word":"中学校","reading":"ちゅうがっこう","meaning":"middle school"},
        {"word":"小学校","reading":"しょうがっこう","meaning":"elementary school"},
        {"word":"大学校","reading":"だいがっこう","meaning":"academy"},
        {"word":"校長","reading":"こうちょう","meaning":"principal"},
        {"word":"校庭","reading":"こうてい","meaning":"schoolyard"}
    ]},
    "先": {"on": ["セン"], "kun": ["さき","まず"], "meaning": "before, ahead, previous", "compounds": [
        {"word":"先","reading":"さき","meaning":"ahead"},
        {"word":"先生","reading":"せんせい","meaning":"teacher"},
        {"word":"先月","reading":"せんげつ","meaning":"last month"},
        {"word":"先週","reading":"せんしゅう","meaning":"last week"},
        {"word":"先日","reading":"せんじつ","meaning":"the other day"},
        {"word":"先輩","reading":"せんぱい","meaning":"senior"},
        {"word":"先進","reading":"せんしん","meaning":"advanced"},
        {"word":"優先","reading":"ゆうせん","meaning":"priority"}
    ]},
    "後": {"on": ["コウ","ゴ"], "kun": ["あと","うし.ろ","おく.れる"], "meaning": "after, behind", "compounds": [
        {"word":"後","reading":"あと","meaning":"after"},
        {"word":"後ろ","reading":"うしろ","meaning":"behind"},
        {"word":"最後","reading":"さいご","meaning":"last"},
        {"word":"午後に","reading":"ごごに","meaning":"in the afternoon"},
        {"word":"後悔","reading":"こうかい","meaning":"regret"},
        {"word":"以後","reading":"いご","meaning":"after this"},
        {"word":"背後","reading":"はいご","meaning":"back, rear"},
        {"word":"落後","reading":"らくご","meaning":"falling behind"}
    ]},
    "前": {"on": ["ゼン"], "kun": ["まえ"], "meaning": "before, front", "compounds": [
        {"word":"前","reading":"まえ","meaning":"front"},
        {"word":"午前","reading":"ごぜん","meaning":"morning, AM"},
        {"word":"以前","reading":"いぜん","meaning":"before"},
        {"word":"最前","reading":"さいぜん","meaning":"foremost"},
        {"word":"前進","reading":"ぜんしん","meaning":"advance"},
        {"word":"前提","reading":"ぜんてい","meaning":"premise"},
        {"word":"全額","reading":"ぜんがく","meaning":"full amount"},
        {"word":"日前","reading":"にちまえ","meaning":"days ago"}
    ]},
    "左": {"on": ["サ","シャ"], "kun": ["ひだり"], "meaning": "left", "compounds": [
        {"word":"左","reading":"ひだり","meaning":"left"},
        {"word":"左右","reading":"さゆう","meaning":"left and right"},
        {"word":"左手","reading":"ひだりて","meaning":"left hand"},
        {"word":"左側","reading":"ひだりがわ","meaning":"left side"},
        {"word":"左翼","reading":"さよく","meaning":"left wing"}
    ]},
    "右": {"on": ["ウ","ユ"], "kun": ["みぎ"], "meaning": "right", "compounds": [
        {"word":"右","reading":"みぎ","meaning":"right"},
        {"word":"左右","reading":"さゆう","meaning":"left and right"},
        {"word":"右手","reading":"みぎて","meaning":"right hand"},
        {"word":"右側","reading":"みぎがわ","meaning":"right side"},
        {"word":"右翼","reading":"うよく","meaning":"right wing"}
    ]},
    "東": {"on": ["トウ"], "kun": ["ひがし"], "meaning": "east", "compounds": [
        {"word":"東","reading":"ひがし","meaning":"east"},
        {"word":"東京","reading":"とうきょう","meaning":"Tokyo"},
        {"word":"東洋","reading":"とうよう","meaning":"Orient"},
        {"word":"東方","reading":"とうほう","meaning":"eastern direction"},
        {"word":"東北","reading":"とうほく","meaning":"Tohoku"},
        {"word":"東西","reading":"とうざい","meaning":"east and west"}
    ]},
    "西": {"on": ["セイ","サイ"], "kun": ["にし"], "meaning": "west", "compounds": [
        {"word":"西","reading":"にし","meaning":"west"},
        {"word":"西洋","reading":"せいよう","meaning":"Western"},
        {"word":"西方","reading":"せいほう","meaning":"western direction"},
        {"word":"関西","reading":"かんさい","meaning":"Kansai"},
        {"word":"東西","reading":"とうざい","meaning":"east and west"},
        {"word":"西欧","reading":"せいおう","meaning":"Western Europe"}
    ]},
    "南": {"on": ["ナン","ナ"], "kun": ["みなみ"], "meaning": "south", "compounds": [
        {"word":"南","reading":"みなみ","meaning":"south"},
        {"word":"南方","reading":"なんぽう","meaning":"southern direction"},
        {"word":"南米","reading":"なんべい","meaning":"South America"},
        {"word":"東南","reading":"とうなん","meaning":"southeast"},
        {"word":"南北","reading":"なんぼく","meaning":"north and south"},
        {"word":"指南","reading":"しなん","meaning":"guidance"}
    ]},
    "北": {"on": ["ホク"], "kun": ["きた"], "meaning": "north", "compounds": [
        {"word":"北","reading":"きた","meaning":"north"},
        {"word":"北方","reading":"ほっぽう","meaning":"northern direction"},
        {"word":"東北","reading":"とうほく","meaning":"Tohoku"},
        {"word":"北海道","reading":"ほっかいどう","meaning":"Hokkaido"},
        {"word":"南北","reading":"なんぼく","meaning":"north and south"},
        {"word":"北極","reading":"ほっきょく","meaning":"North Pole"}
    ]},
    "本": {"on": ["ホン"], "kun": ["もと"], "meaning": "book, origin, main", "compounds": [
        {"word":"本","reading":"ほん","meaning":"book"},
        {"word":"日本","reading":"にほん","meaning":"Japan"},
        {"word":"本当","reading":"ほんとう","meaning":"truth, real"},
        {"word":"基本","reading":"きほん","meaning":"basic"},
        {"word":"本人","reading":"ほんにん","meaning":"the person themselves"},
        {"word":"本日","reading":"ほんじつ","meaning":"today"},
        {"word":"絵本","reading":"えほん","meaning":"picture book"},
        {"word":"原稿","reading":"げんこう","meaning":"manuscript"}
    ]},
    "名": {"on": ["メイ","ミョウ"], "kun": ["な"], "meaning": "name", "compounds": [
        {"word":"名前","reading":"なまえ","meaning":"name"},
        {"word":"有名","reading":"ゆうめい","meaning":"famous"},
        {"word":"地名","reading":"ちめい","meaning":"place name"},
        {"word":"名人","reading":"めいじん","meaning":"master"},
        {"word":"名誉","reading":"めいよ","meaning":"honor"},
        {"word":"名称","reading":"めいしょう","meaning":"designation"},
        {"word":"名所","reading":"めいしょ","meaning":"famous place"}
    ]},
    "高": {"on": ["コウ"], "kun": ["たか.い","たか"], "meaning": "tall, high", "compounds": [
        {"word":"高い","reading":"たかい","meaning":"high, tall"},
        {"word":"高校","reading":"こうこう","meaning":"high school"},
        {"word":"最高","reading":"さいこう","meaning":"best, highest"},
        {"word":"高級","reading":"こうきゅう","meaning":"high class"},
        {"word":"高度","reading":"こうど","meaning":"altitude"},
        {"word":"高速","reading":"こうそく","meaning":"high speed"},
        {"word":"高原","reading":"こうげん","meaning":"plateau"},
        {"word":"身長","reading":"しんちょう","meaning":"height"}
    ]},
    "低": {"on": ["テイ"], "kun": ["ひく.い","ひく"], "meaning": "low", "compounds": [
        {"word":"低い","reading":"ひくい","meaning":"low"},
        {"word":"最低","reading":"さいてい","meaning":"lowest"},
        {"word":"低下","reading":"ていか","meaning":"decline"},
        {"word":"低温","reading":"ていおん","meaning":"low temperature"},
        {"word":"低学年","reading":"ていがくねん","meaning":"lower grades"}
    ]},
    "長": {"on": ["チョウ"], "kun": ["なが.い","なが"], "meaning": "long, leader", "compounds": [
        {"word":"長い","reading":"ながい","meaning":"long"},
        {"word":"社長","reading":"しゃちょう","meaning":"company president"},
        {"word":"部長","reading":"ぶちょう","meaning":"department head"},
        {"word":"長男","reading":"ちょうなん","meaning":"eldest son"},
        {"word":"成長","reading":"せいちょう","meaning":"growth"},
        {"word":"長期","reading":"ちょうき","meaning":"long term"},
        {"word":"長所","reading":"ちょうしょ","meaning":"strong point"},
        {"word":"校長","reading":"こうちょう","meaning":"principal"}
    ]},
    "短": {"on": ["タン"], "kun": ["みじか.い"], "meaning": "short", "compounds": [
        {"word":"短い","reading":"みじかい","meaning":"short"},
        {"word":"短期","reading":"たんき","meaning":"short term"},
        {"word":"短所","reading":"たんしょ","meaning":"weak point"},
        {"word":"短文","reading":"たんぶん","meaning":"short sentence"},
        {"word":"短縮","reading":"たんしゅく","meaning":"shortening"}
    ]},
    "広": {"on": ["コウ"], "kun": ["ひろ.い","ひろ"], "meaning": "wide, broad", "compounds": [
        {"word":"広い","reading":"ひろい","meaning":"wide"},
        {"word":"広告","reading":"こうこく","meaning":"advertisement"},
        {"word":"広場","reading":"ひろば","meaning":"plaza"},
        {"word":"拡大","reading":"かくだい","meaning":"expansion"},
        {"word":"広報","reading":"こうほう","meaning":"public relations"},
        {"word":"広島","reading":"ひろしま","meaning":"Hiroshima"}
    ]},
    "白": {"on": ["ハク","ビャク"], "kun": ["しろ","しら"], "meaning": "white", "compounds": [
        {"word":"白い","reading":"しろい","meaning":"white"},
        {"word":"白人","reading":"はくじん","meaning":"Caucasian"},
        {"word":"明白","reading":"めいはく","meaning":"obvious"},
        {"word":"告白","reading":"こくはく","meaning":"confession"},
        {"word":"白紙","reading":"はくし","meaning":"blank paper"},
        {"word":"白黒","reading":"しろくろ","meaning":"black and white"}
    ]},
    "黒": {"on": ["コク"], "kun": ["くろ","くろ.い"], "meaning": "black", "compounds": [
        {"word":"黒い","reading":"くろい","meaning":"black"},
        {"word":"黒人","reading":"こくじん","meaning":"Black person"},
        {"word":"黒板","reading":"こくばん","meaning":"blackboard"},
        {"word":"暗黒","reading":"あんこく","meaning":"darkness"},
        {"word":"白黒","reading":"しろくろ","meaning":"black and white"},
        {"word":"黒髪","reading":"くろかみ","meaning":"black hair"}
    ]},
    "赤": {"on": ["セキ","シャク"], "kun": ["あか","あか.い"], "meaning": "red", "compounds": [
        {"word":"赤い","reading":"あかい","meaning":"red"},
        {"word":"赤ちゃん","reading":"あかちゃん","meaning":"baby"},
        {"word":"赤十字","reading":"せきじゅうじ","meaning":"Red Cross"},
        {"word":"赤道","reading":"せきどう","meaning":"equator"},
        {"word":"赤字","reading":"あかじ","meaning":"deficit"},
        {"word":"赤信号","reading":"あかしんごう","meaning":"red light"}
    ]},
    "青": {"on": ["セイ","ショウ"], "kun": ["あお","あお.い"], "meaning": "blue, green", "compounds": [
        {"word":"青い","reading":"あおい","meaning":"blue"},
        {"word":"青年","reading":"せいねん","meaning":"youth"},
        {"word":"青空","reading":"あおぞら","meaning":"blue sky"},
        {"word":"青春","reading":"せいしゅん","meaning":"youth, spring"},
        {"word":"信号","reading":"しんごう","meaning":"traffic signal"},
        {"word":"青天","reading":"せいてん","meaning":"clear sky"}
    ]},
    "色": {"on": ["ショク","シキ"], "kun": ["いろ"], "meaning": "color", "compounds": [
        {"word":"色","reading":"いろ","meaning":"color"},
        {"word":"色々","reading":"いろいろ","meaning":"various"},
        {"word":"景色","reading":"けしき","meaning":"scenery"},
        {"word":"特色","reading":"とくしょく","meaning":"characteristic"},
        {"word":"色彩","reading":"しきさい","meaning":"colors"},
        {"word":"顔色","reading":"かおいろ","meaning":"complexion"}
    ]},
    "花": {"on": ["カ","ケ"], "kun": ["はな"], "meaning": "flower", "compounds": [
        {"word":"花","reading":"はな","meaning":"flower"},
        {"word":"花火","reading":"はなび","meaning":"fireworks"},
        {"word":"花園","reading":"かえん","meaning":"flower garden"},
        {"word":"開花","reading":"かいか","meaning":"blooming"},
        {"word":"花瓶","reading":"かびん","meaning":"vase"},
        {"word":"花見","reading":"はなみ","meaning":"cherry blossom viewing"},
        {"word":"桜花","reading":"おうか","meaning":"cherry blossom"}
    ]},
    "草": {"on": ["ソウ"], "kun": ["くさ"], "meaning": "grass", "compounds": [
        {"word":"草","reading":"くさ","meaning":"grass"},
        {"word":"草原","reading":"そうげん","meaning":"grassland"},
        {"word":"雑草","reading":"ざっそう","meaning":"weeds"},
        {"word":"草木","reading":"そうもく","meaning":"plants"},
        {"word":"草花","reading":"くさばな","meaning":"flowers"},
        {"word":"草稿","reading":"そうこう","meaning":"draft"}
    ]},
    "虫": {"on": ["チュウ"], "kun": ["むし"], "meaning": "insect", "compounds": [
        {"word":"虫","reading":"むし","meaning":"insect"},
        {"word":"昆虫","reading":"こんちゅう","meaning":"insects"},
        {"word":"害虫","reading":"がいちゅう","meaning":"pest"},
        {"word":"虫歯","reading":"むしば","meaning":"cavity"},
        {"word":"毛虫","reading":"けむし","meaning":"caterpillar"},
        {"word":"蛍","reading":"ほたる","meaning":"firefly"}
    ]},
    "魚": {"on": ["ギョ"], "kun": ["さかな","うお"], "meaning": "fish", "compounds": [
        {"word":"魚","reading":"さかな","meaning":"fish"},
        {"word":"魚市場","reading":"うおいちば","meaning":"fish market"},
        {"word":"金魚","reading":"きんぎょ","meaning":"goldfish"},
        {"word":"鮮魚","reading":"せんぎょ","meaning":"fresh fish"},
        {"word":"魚介類","reading":"ぎょかいるい","meaning":"seafood"},
        {"word":"熱帯魚","reading":"ねったいぎょ","meaning":"tropical fish"}
    ]},
    "鳥": {"on": ["チョウ"], "kun": ["とり"], "meaning": "bird", "compounds": [
        {"word":"鳥","reading":"とり","meaning":"bird"},
        {"word":"小鳥","reading":"ことり","meaning":"small bird"},
        {"word":"野鳥","reading":"やちょう","meaning":"wild bird"},
        {"word":"鳥居","reading":"とりい","meaning":"shrine gate"},
        {"word":"渡り鳥","reading":"わたりどり","meaning":"migratory bird"},
        {"word":"白鳥","reading":"はくちょう","meaning":"swan"}
    ]},
    "犬": {"on": ["ケン"], "kun": ["いぬ"], "meaning": "dog", "compounds": [
        {"word":"犬","reading":"いぬ","meaning":"dog"},
        {"word":"子犬","reading":"こいぬ","meaning":"puppy"},
        {"word":"番犬","reading":"ばんけん","meaning":"watchdog"},
        {"word":"盲導犬","reading":"もうどうけん","meaning":"guide dog"},
        {"word":"狩猟犬","reading":"しゅりょうけん","meaning":"hunting dog"}
    ]},
    "猫": {"on": ["ビョウ"], "kun": ["ねこ"], "meaning": "cat", "compounds": [
        {"word":"猫","reading":"ねこ","meaning":"cat"},
        {"word":"子猫","reading":"こねこ","meaning":"kitten"},
        {"word":"野良猫","reading":"のらねこ","meaning":"stray cat"},
        {"word":"黒猫","reading":"くろねこ","meaning":"black cat"},
        {"word":"愛猫","reading":"あいびょう","meaning":"pet cat"}
    ]},
    "車": {"on": ["シャ"], "kun": ["くるま"], "meaning": "car, vehicle", "compounds": [
        {"word":"車","reading":"くるま","meaning":"car"},
        {"word":"電車","reading":"でんしゃ","meaning":"train"},
        {"word":"自動車","reading":"じどうしゃ","meaning":"automobile"},
        {"word":"自転車","reading":"じてんしゃ","meaning":"bicycle"},
        {"word":"車庫","reading":"しゃこ","meaning":"garage"},
        {"word":"停車","reading":"ていしゃ","meaning":"stopping"},
        {"word":"発車","reading":"はっしゃ","meaning":"departure"}
    ]},
    "道": {"on": ["ドウ"], "kun": ["みち"], "meaning": "road, path, way", "compounds": [
        {"word":"道","reading":"みち","meaning":"road"},
        {"word":"道路","reading":"どうろ","meaning":"road"},
        {"word":"道具","reading":"どうぐ","meaning":"tool"},
        {"word":"北海道","reading":"ほっかいどう","meaning":"Hokkaido"},
        {"word":"武道","reading":"ぶどう","meaning":"martial arts"},
        {"word":"茶道","reading":"さどう","meaning":"tea ceremony"},
        {"word":"歩道","reading":"ほどう","meaning":"sidewalk"},
        {"word":"案内","reading":"あんない","meaning":"guidance"}
    ]},
    "国": {"on": ["コク"], "kun": ["くに"], "meaning": "country", "compounds": [
        {"word":"国","reading":"くに","meaning":"country"},
        {"word":"外国","reading":"がいこく","meaning":"foreign country"},
        {"word":"国際","reading":"こくさい","meaning":"international"},
        {"word":"中国","reading":"ちゅうごく","meaning":"China"},
        {"word":"韓国","reading":"かんこく","meaning":"South Korea"},
        {"word":"アメリカ合衆国","reading":"アメリカがっしゅうこく","meaning":"USA"},
        {"word":"国立","reading":"こくりつ","meaning":"national"},
        {"word":"国民","reading":"こくみん","meaning":"citizens"}
    ]},
    "語": {"on": ["ゴ"], "kun": ["かた.る"], "meaning": "language, word", "compounds": [
        {"word":"日本語","reading":"にほんご","meaning":"Japanese language"},
        {"word":"英語","reading":"えいご","meaning":"English"},
        {"word":"中国語","reading":"ちゅうごくご","meaning":"Chinese"},
        {"word":"言葉","reading":"ことば","meaning":"words"},
        {"word":"物語","reading":"ものがたり","meaning":"story"},
        {"word":"会話","reading":"かいわ","meaning":"conversation"},
        {"word":"文法","reading":"ぶんぽう","meaning":"grammar"},
        {"word":"言語","reading":"げんご","meaning":"language"}
    ]},
    "文": {"on": ["ブン","モン"], "kun": ["ふみ"], "meaning": "writing, sentence", "compounds": [
        {"word":"文章","reading":"ぶんしょう","meaning":"sentence, writing"},
        {"word":"文字","reading":"もじ","meaning":"character"},
        {"word":"文学","reading":"ぶんがく","meaning":"literature"},
        {"word":"文化","reading":"ぶんか","meaning":"culture"},
        {"word":"文明","reading":"ぶんめい","meaning":"civilization"},
        {"word":"作文","reading":"さくぶん","meaning":"composition"},
        {"word":"論文","reading":"ろんぶん","meaning":"thesis"},
        {"word":"日文","reading":"にちぶん","meaning":"Japanese text"}
    ]},
    "字": {"on": ["ジ"], "kun": ["あざ"], "meaning": "character, letter", "compounds": [
        {"word":"文字","reading":"もじ","meaning":"character"},
        {"word":"漢字","reading":"かんじ","meaning":"kanji"},
        {"word":"数字","reading":"すうじ","meaning":"numeral"},
        {"word":"名字","reading":"みょうじ","meaning":"surname"},
        {"word":"字幕","reading":"じまく","meaning":"subtitle"},
        {"word":"字体","reading":"じたい","meaning":"font"},
        {"word":"習字","reading":"しゅうじ","meaning":"calligraphy"}
    ]},
    "音": {"on": ["オン","イン"], "kun": ["おと","ね"], "meaning": "sound", "compounds": [
        {"word":"音","reading":"おと","meaning":"sound"},
        {"word":"音楽","reading":"おんがく","meaning":"music"},
        {"word":"音声","reading":"おんせい","meaning":"voice"},
        {"word":"騒音","reading":"そうおん","meaning":"noise"},
        {"word":"録音","reading":"ろくおん","meaning":"recording"},
        {"word":"防音","reading":"ぼうおん","meaning":"soundproofing"},
        {"word":"音色","reading":"ねいろ","meaning":"tone color"}
    ]},
    "楽": {"on": ["ガク","ラク"], "kun": ["たの.しい","たの.しむ"], "meaning": "music, pleasure, easy", "compounds": [
        {"word":"楽しい","reading":"たのしい","meaning":"fun"},
        {"word":"音楽","reading":"おんがく","meaning":"music"},
        {"word":"楽勝","reading":"らくしょう","meaning":"easy win"},
        {"word":"快適","reading":"かいてき","meaning":"comfortable"},
        {"word":"楽器","reading":"がっき","meaning":"musical instrument"},
        {"word":"遊園地","reading":"ゆうえんち","meaning":"amusement park"},
        {"word":"安楽","reading":"あんらく","meaning":"ease"}
    ]},
    "食": {"on": ["ショク"], "kun": ["た.べる","く.う"], "meaning": "eat, food", "compounds": [
        {"word":"食べる","reading":"たべる","meaning":"to eat"},
        {"word":"食事","reading":"しょくじ","meaning":"meal"},
        {"word":"食堂","reading":"しょくどう","meaning":"dining hall"},
        {"word":"朝食","reading":"ちょうしょく","meaning":"breakfast"},
        {"word":"昼食","reading":"ちゅうしょく","meaning":"lunch"},
        {"word":"夕食","reading":"ゆうしょく","meaning":"dinner"},
        {"word":"食べ物","reading":"たべもの","meaning":"food"},
        {"word":"試食","reading":"ししょく","meaning":"tasting"}
    ]},
    "飲": {"on": ["イン"], "kun": ["の.む"], "meaning": "drink", "compounds": [
        {"word":"飲む","reading":"のむ","meaning":"to drink"},
        {"word":"飲み物","reading":"のみもの","meaning":"beverage"},
        {"word":"飲食","reading":"いんしょく","meaning":"eating and drinking"},
        {"word":"飲料","reading":"いんりょう","meaning":"drinks"},
        {"word":"飲酒","reading":"いんしゅ","meaning":"drinking alcohol"},
        {"word":"過飲","reading":"かいん","meaning":"overdrinking"}
    ]},
    "話": {"on": ["ワ"], "kun": ["はな.す","はなし"], "meaning": "talk, story", "compounds": [
        {"word":"話す","reading":"はなす","meaning":"to speak"},
        {"word":"電話","reading":"でんわ","meaning":"telephone"},
        {"word":"会話","reading":"かいわ","meaning":"conversation"},
        {"word":"話題","reading":"わだい","meaning":"topic"},
        {"word":"神話","reading":"しんわ","meaning":"myth"},
        {"word":"昔話","reading":"むかしばなし","meaning":"old tale"},
        {"word":"世話","reading":"せわ","meaning":"care"},
        {"word":"冗談","reading":"じょうだん","meaning":"joke"}
    ]},
    "読": {"on": ["ドク","トク"], "kun": ["よ.む"], "meaning": "read", "compounds": [
        {"word":"読む","reading":"よむ","meaning":"to read"},
        {"word":"読書","reading":"どくしょ","meaning":"reading"},
        {"word":"読み方","reading":"よみかた","meaning":"way of reading"},
        {"word":"読者","reading":"どくしゃ","meaning":"reader"},
        {"word":"講読","reading":"こうどく","meaning":"reading"},
        {"word":"音読","reading":"おんどく","meaning":"reading aloud"},
        {"word":"黙読","reading":"もくどく","meaning":"silent reading"}
    ]},
    "書": {"on": ["ショ"], "kun": ["か.く"], "meaning": "write, book", "compounds": [
        {"word":"書く","reading":"かく","meaning":"to write"},
        {"word":"図書館","reading":"としょかん","meaning":"library"},
        {"word":"教科書","reading":"きょうかしょ","meaning":"textbook"},
        {"word":"辞書","reading":"じしょ","meaning":"dictionary"},
        {"word":"書類","reading":"しょるい","meaning":"documents"},
        {"word":"秘書","reading":"ひしょ","meaning":"secretary"},
        {"word":"書道","reading":"しょどう","meaning":"calligraphy"},
        {"word":"新書","reading":"しんしょ","meaning":"new book"}
    ]},
    "見": {"on": ["ケン"], "kun": ["み.る","み.える","み.せる"], "meaning": "see, look", "compounds": [
        {"word":"見る","reading":"みる","meaning":"to see"},
        {"word":"見える","reading":"みえる","meaning":"to be visible"},
        {"word":"意見","reading":"いけん","meaning":"opinion"},
        {"word":"見学","reading":"けんがく","meaning":"field trip"},
        {"word":"発見","reading":"はっけん","meaning":"discovery"},
        {"word":"見物","reading":"けんぶつ","meaning":"sightseeing"},
        {"word":"花見","reading":"はなみ","meaning":"hanami"},
        {"word":"予見","reading":"よけん","meaning":"foresight"}
    ]},
    "聞": {"on": ["ブン","モン"], "kun": ["き.く","き.こえる"], "meaning": "hear, listen, ask", "compounds": [
        {"word":"聞く","reading":"きく","meaning":"to hear, to ask"},
        {"word":"聞こえる","reading":"きこえる","meaning":"to be audible"},
        {"word":"新聞","reading":"しんぶん","meaning":"newspaper"},
        {"word":"質問","reading":"しつもん","meaning":"question"},
        {"word":"伝聞","reading":"でんぶん","meaning":"hearsay"},
        {"word":"聞き手","reading":"ききて","meaning":"listener"},
        {"word":"見聞","reading":"けんぶん","meaning":"information"}
    ]},
    "行": {"on": ["コウ","ギョウ"], "kun": ["い.く","おこな.う"], "meaning": "go, carry out", "compounds": [
        {"word":"行く","reading":"いく","meaning":"to go"},
        {"word":"行う","reading":"おこなう","meaning":"to conduct"},
        {"word":"行動","reading":"こうどう","meaning":"action"},
        {"word":"旅行","reading":"りょこう","meaning":"travel"},
        {"word":"銀行","reading":"ぎんこう","meaning":"bank"},
        {"word":"行列","reading":"ぎょうれつ","meaning":"line, queue"},
        {"word":"実行","reading":"じっこう","meaning":"execution"},
        {"word":"通行","reading":"つうこう","meaning":"passage"}
    ]},
    "来": {"on": ["ライ"], "kun": ["く.る","きた.る"], "meaning": "come", "compounds": [
        {"word":"来る","reading":"くる","meaning":"to come"},
        {"word":"来年","reading":"らいねん","meaning":"next year"},
        {"word":"来月","reading":"らいげつ","meaning":"next month"},
        {"word":"来週","reading":"らいしゅう","meaning":"next week"},
        {"word":"未来","reading":"みらい","meaning":"future"},
        {"word":"外来","reading":"がいらい","meaning":"foreign"},
        {"word":"以来","reading":"いらい","meaning":"since"},
        {"word":"本来","reading":"ほんらい","meaning":"originally"}
    ]},
    "出": {"on": ["シュツ"], "kun": ["で.る","だ.す"], "meaning": "exit, put out", "compounds": [
        {"word":"出る","reading":"でる","meaning":"to exit"},
        {"word":"出す","reading":"だす","meaning":"to put out"},
        {"word":"出口","reading":"でぐち","meaning":"exit"},
        {"word":"出発","reading":"しゅっぱつ","meaning":"departure"},
        {"word":"出席","reading":"しゅっせき","meaning":"attendance"},
        {"word":"出版","reading":"しゅっぱん","meaning":"publishing"},
        {"word":"外出","reading":"がいしゅつ","meaning":"going out"},
        {"word":"提出","reading":"ていしゅつ","meaning":"submission"}
    ]},
    "入": {"on": ["ニュウ"], "kun": ["はい.る","い.れる"], "meaning": "enter, put in", "compounds": [
        {"word":"入る","reading":"はいる","meaning":"to enter"},
        {"word":"入れる","reading":"いれる","meaning":"to put in"},
        {"word":"入口","reading":"いりぐち","meaning":"entrance"},
        {"word":"入学","reading":"にゅうがく","meaning":"enrollment"},
        {"word":"入社","reading":"にゅうしゃ","meaning":"joining a company"},
        {"word":"収入","reading":"しゅうにゅう","meaning":"income"},
        {"word":"入力","reading":"にゅうりょく","meaning":"input"},
        {"word":"加入","reading":"かにゅう","meaning":"joining"}
    ]},
    "開": {"on": ["カイ"], "kun": ["ひら.く","あ.ける"], "meaning": "open", "compounds": [
        {"word":"開ける","reading":"あける","meaning":"to open"},
        {"word":"開く","reading":"ひらく","meaning":"to open"},
        {"word":"開発","reading":"かいはつ","meaning":"development"},
        {"word":"開始","reading":"かいし","meaning":"start"},
        {"word":"公開","reading":"こうかい","meaning":"public opening"},
        {"word":"開催","reading":"かいさい","meaning":"holding an event"},
        {"word":"開放","reading":"かいほう","meaning":"opening"},
        {"word":"開花","reading":"かいか","meaning":"blooming"}
    ]},
    "閉": {"on": ["ヘイ"], "kun": ["と.じる","し.める"], "meaning": "close, shut", "compounds": [
        {"word":"閉める","reading":"しめる","meaning":"to close"},
        {"word":"閉じる","reading":"とじる","meaning":"to close"},
        {"word":"閉鎖","reading":"へいさ","meaning":"closure"},
        {"word":"密閉","reading":"みっぺい","meaning":"sealing"},
        {"word":"閉店","reading":"へいてん","meaning":"closing shop"},
        {"word":"閉会","reading":"へいかい","meaning":"closing ceremony"}
    ]},
    "立": {"on": ["リツ"], "kun": ["た.つ","た.てる"], "meaning": "stand", "compounds": [
        {"word":"立つ","reading":"たつ","meaning":"to stand"},
        {"word":"立てる","reading":"たてる","meaning":"to set up"},
        {"word":"独立","reading":"どくりつ","meaning":"independence"},
        {"word":"立場","reading":"たちば","meaning":"position"},
        {"word":"成立","reading":"せいりつ","meaning":"establishment"},
        {"word":"立体","reading":"りったい","meaning":"solid body"},
        {"word":"国立","reading":"こくりつ","meaning":"national"},
        {"word":"設立","reading":"せつりつ","meaning":"establishment"}
    ]},
    "休": {"on": ["キュウ"], "kun": ["やす.む","やす.める"], "meaning": "rest", "compounds": [
        {"word":"休む","reading":"やすむ","meaning":"to rest"},
        {"word":"休み","reading":"やすみ","meaning":"rest, holiday"},
        {"word":"休憩","reading":"きゅうけい","meaning":"break"},
        {"word":"休暇","reading":"きゅうか","meaning":"vacation"},
        {"word":"休日","reading":"きゅうじつ","meaning":"holiday"},
        {"word":"定休日","reading":"ていきゅうび","meaning":"regular holiday"},
        {"word":"夏休み","reading":"なつやすみ","meaning":"summer vacation"}
    ]},
    "言": {"on": ["ゲン","ゴン"], "kun": ["い.う","こと"], "meaning": "say, word", "compounds": [
        {"word":"言う","reading":"いう","meaning":"to say"},
        {"word":"言葉","reading":"ことば","meaning":"words"},
        {"word":"言語","reading":"げんご","meaning":"language"},
        {"word":"発言","reading":"はつげん","meaning":"statement"},
        {"word":"宣言","reading":"せんげん","meaning":"declaration"},
        {"word":"言論","reading":"げんろん","meaning":"speech"},
        {"word":"無言","reading":"むごん","meaning":"silence"},
        {"word":"名言","reading":"めいげん","meaning":"famous saying"}
    ]},
    "思": {"on": ["シ"], "kun": ["おも.う"], "meaning": "think", "compounds": [
        {"word":"思う","reading":"おもう","meaning":"to think"},
        {"word":"考え","reading":"かんがえ","meaning":"thought"},
        {"word":"意思","reading":"いし","meaning":"intention"},
        {"word":"思想","reading":"しそう","meaning":"thought, ideology"},
        {"word":"思い出","reading":"おもいで","meaning":"memories"},
        {"word":"不思議","reading":"ふしぎ","meaning":"mysterious"},
        {"word":"思考","reading":"しこう","meaning":"thinking"},
        {"word":"沉思","reading":"ちんし","meaning":"deep thought"}
    ]},
    "考": {"on": ["コウ"], "kun": ["かんが.える"], "meaning": "think, consider", "compounds": [
        {"word":"考える","reading":"かんがえる","meaning":"to think"},
        {"word":"考え","reading":"かんがえ","meaning":"thought"},
        {"word":"試験","reading":"しけん","meaning":"exam"},
        {"word":"参考","reading":"さんこう","meaning":"reference"},
        {"word":"考古学","reading":"こうこがく","meaning":"archaeology"},
        {"word":"思考","reading":"しこう","meaning":"thinking"},
        {"word":"考察","reading":"こうさつ","meaning":"consideration"}
    ]},
    "知": {"on": ["チ"], "kun": ["し.る"], "meaning": "know", "compounds": [
        {"word":"知る","reading":"しる","meaning":"to know"},
        {"word":"知識","reading":"ちしき","meaning":"knowledge"},
        {"word":"通知","reading":"つうち","meaning":"notice"},
        {"word":"知人","reading":"ちじん","meaning":"acquaintance"},
        {"word":"認知","reading":"にんち","meaning":"recognition"},
        {"word":"知恵","reading":"ちえ","meaning":"wisdom"},
        {"word":"周知","reading":"しゅうち","meaning":"well-known"},
        {"word":"知事","reading":"ちじ","meaning":"governor"}
    ]},
    "感": {"on": ["カン"], "kun": [], "meaning": "feel, sense", "compounds": [
        {"word":"感じる","reading":"かんじる","meaning":"to feel"},
        {"word":"感動","reading":"かんどう","meaning":"being moved"},
        {"word":"感謝","reading":"かんしゃ","meaning":"gratitude"},
        {"word":"感覚","reading":"かんかく","meaning":"sense"},
        {"word":"感情","reading":"かんじょう","meaning":"emotion"},
        {"word":"感想","reading":"かんそう","meaning":"impression"},
        {"word":"敏感","reading":"びんかん","meaning":"sensitive"},
        {"word":"五感","reading":"ごかん","meaning":"five senses"}
    ]},
    "情": {"on": ["ジョウ","セイ"], "kun": ["なさ.け"], "meaning": "feeling, emotion", "compounds": [
        {"word":"感情","reading":"かんじょう","meaning":"emotion"},
        {"word":"情報","reading":"じょうほう","meaning":"information"},
        {"word":"事情","reading":"じじょう","meaning":"circumstances"},
        {"word":"愛情","reading":"あいじょう","meaning":"love"},
        {"word":"友情","reading":"ゆうじょう","meaning":"friendship"},
        {"word":"同情","reading":"どうじょう","meaning":"sympathy"},
        {"word":"情熱","reading":"じょうねつ","meaning":"passion"},
        {"word":"人情","reading":"にんじょう","meaning":"humanity"}
    ]},
    "意": {"on": ["イ"], "kun": [], "meaning": "idea, mind, will", "compounds": [
        {"word":"意味","reading":"いみ","meaning":"meaning"},
        {"word":"意見","reading":"いけん","meaning":"opinion"},
        {"word":"意識","reading":"いしき","meaning":"consciousness"},
        {"word":"意外","reading":"いがい","meaning":"unexpected"},
        {"word":"注意","reading":"ちゅうい","meaning":"caution"},
        {"word":"同意","reading":"どうい","meaning":"agreement"},
        {"word":"生意気","reading":"なまいき","meaning":"impudent"},
        {"word":"用意","reading":"ようい","meaning":"preparation"}
    ]},
    "味": {"on": ["ミ"], "kun": ["あじ","あじ.わう"], "meaning": "taste, flavor", "compounds": [
        {"word":"味","reading":"あじ","meaning":"taste"},
        {"word":"美味しい","reading":"おいしい","meaning":"delicious"},
        {"word":"味わう","reading":"あじわう","meaning":"to savor"},
        {"word":"趣味","reading":"しゅみ","meaning":"hobby"},
        {"word":"興味","reading":"きょうみ","meaning":"interest"},
        {"word":"味方","reading":"みかた","meaning":"ally"},
        {"word":"一味","reading":"ひとあじ","meaning":"different taste"}
    ]},
    "力": {"on": ["リョク","リキ"], "kun": ["ちから"], "meaning": "power, strength", "compounds": [
        {"word":"力","reading":"ちから","meaning":"power"},
        {"word":"努力","reading":"どりょく","meaning":"effort"},
        {"word":"能力","reading":"のうりょく","meaning":"ability"},
        {"word":"協力","reading":"きょうりょく","meaning":"cooperation"},
        {"word":"強力","reading":"きょうりょく","meaning":"powerful"},
        {"word":"体力","reading":"たいりょく","meaning":"physical strength"},
        {"word":"学力","reading":"がくりょく","meaning":"academic ability"},
        {"word":"圧力","reading":"あつりょく","meaning":"pressure"}
    ]},
    "体": {"on": ["タイ","テイ"], "kun": ["からだ"], "meaning": "body", "compounds": [
        {"word":"体","reading":"からだ","meaning":"body"},
        {"word":"体育","reading":"たいいく","meaning":"physical education"},
        {"word":"体験","reading":"たいけん","meaning":"experience"},
        {"word":"体制","reading":"たいせい","meaning":"system"},
        {"word":"体調","reading":"たいちょう","meaning":"condition"},
        {"word":"体重","reading":"たいじゅう","meaning":"body weight"},
        {"word":"全体","reading":"ぜんたい","meaning":"whole"},
        {"word":"身体","reading":"しんたい","meaning":"body"}
    ]},
    "顔": {"on": ["ガン"], "kun": ["かお"], "meaning": "face", "compounds": [
        {"word":"顔","reading":"かお","meaning":"face"},
        {"word":"笑顔","reading":"えがお","meaning":"smile"},
        {"word":"顔色","reading":"かおいろ","meaning":"complexion"},
        {"word":"顔面","reading":"がんめん","meaning":"face"},
        {"word":"洗顔","reading":"せんがん","meaning":"face washing"},
        {"word":"素顔","reading":"すがお","meaning":"natural face"}
    ]},
    "頭": {"on": ["トウ","ズ"], "kun": ["あたま","かしら"], "meaning": "head", "compounds": [
        {"word":"頭","reading":"あたま","meaning":"head"},
        {"word":"頭痛","reading":"ずつう","meaning":"headache"},
        {"word":"先頭","reading":"せんとう","meaning":"head, lead"},
        {"word":"年頭","reading":"ねんとう","meaning":"beginning of year"},
        {"word":"頭脳","reading":"ずのう","meaning":"brain"},
        {"word":"街頭","reading":"がいとう","meaning":"street"},
        {"word":"冒頭","reading":"ぼうとう","meaning":"beginning"}
    ]},
    "声": {"on": ["セイ"], "kun": ["こえ","こわ"], "meaning": "voice", "compounds": [
        {"word":"声","reading":"こえ","meaning":"voice"},
        {"word":"音声","reading":"おんせい","meaning":"sound"},
        {"word":"大声","reading":"おおごえ","meaning":"loud voice"},
        {"word":"小声","reading":"こごえ","meaning":"whisper"},
        {"word":"声優","reading":"せいゆう","meaning":"voice actor"},
        {"word":"悲鳴","reading":"ひめい","meaning":"scream"}
    ]},
    "光": {"on": ["コウ"], "kun": ["ひかり","ひか.る"], "meaning": "light", "compounds": [
        {"word":"光","reading":"ひかり","meaning":"light"},
        {"word":"光る","reading":"ひかる","meaning":"to shine"},
        {"word":"日光","reading":"にっこう","meaning":"sunlight"},
        {"word":"月光","reading":"げっこう","meaning":"moonlight"},
        {"word":"観光","reading":"かんこう","meaning":"sightseeing"},
        {"word":"光線","reading":"こうせん","meaning":"beam"},
        {"word":"栄光","reading":"えいこう","meaning":"glory"},
        {"word":"光速","reading":"こうそく","meaning":"speed of light"}
    ]},
    "風": {"on": ["フウ","フ"], "kun": ["かぜ"], "meaning": "wind, style", "compounds": [
        {"word":"風","reading":"かぜ","meaning":"wind"},
        {"word":"風景","reading":"ふうけい","meaning":"scenery"},
        {"word":"台風","reading":"たいふう","meaning":"typhoon"},
        {"word":"和風","reading":"わふう","meaning":"Japanese style"},
        {"word":"洋風","reading":"ようふう","meaning":"Western style"},
        {"word":"風呂","reading":"ふろ","meaning":"bath"},
        {"word":"風味","reading":"ふうみ","meaning":"flavor"},
        {"word":"通風","reading":"つうふう","meaning":"ventilation"}
    ]},
    "雨": {"on": ["ウ"], "kun": ["あめ","あま"], "meaning": "rain", "compounds": [
        {"word":"雨","reading":"あめ","meaning":"rain"},
        {"word":"大雨","reading":"おおあめ","meaning":"heavy rain"},
        {"word":"梅雨","reading":"つゆ","meaning":"rainy season"},
        {"word":"雨天","reading":"うてん","meaning":"rainy weather"},
        {"word":"雨水","reading":"あまみず","meaning":"rainwater"},
        {"word":"豪雨","reading":"ごうう","meaning":"torrential rain"},
        {"word":"霧雨","reading":"きりさめ","meaning":"drizzle"}
    ]},
    "雪": {"on": ["セツ"], "kun": ["ゆき"], "meaning": "snow", "compounds": [
        {"word":"雪","reading":"ゆき","meaning":"snow"},
        {"word":"大雪","reading":"おおゆき","meaning":"heavy snow"},
        {"word":"雪景色","reading":"ゆきげしき","meaning":"snow scene"},
        {"word":"降雪","reading":"こうせつ","meaning":"snowfall"},
        {"word":"積雪","reading":"せきせつ","meaning":"snow accumulation"},
        {"word":"初雪","reading":"はつゆき","meaning":"first snow"}
    ]},
    "石": {"on": ["セキ","シャク"], "kun": ["いし"], "meaning": "stone", "compounds": [
        {"word":"石","reading":"いし","meaning":"stone"},
        {"word":"石炭","reading":"せきたん","meaning":"coal"},
        {"word":"石油","reading":"せきゆ","meaning":"oil"},
        {"word":"宝石","reading":"ほうせき","meaning":"jewel"},
        {"word":"岩石","reading":"がんせき","meaning":"rock"},
        {"word":"石鹸","reading":"せっけん","meaning":"soap"},
        {"word":"磁石","reading":"じしゃく","meaning":"magnet"}
    ]},
    "竹": {"on": ["チク"], "kun": ["たけ"], "meaning": "bamboo", "compounds": [
        {"word":"竹","reading":"たけ","meaning":"bamboo"},
        {"word":"竹林","reading":"ちくりん","meaning":"bamboo grove"},
        {"word":"竹馬","reading":"ちくば","meaning":"stilts"},
        {"word":"腐竹","reading":"ふちく","meaning":"rotten bamboo"},
        {"word":"竹刀","reading":"しない","meaning":"bamboo sword"}
    ]},
    "糸": {"on": ["シ"], "kun": ["いと"], "meaning": "thread", "compounds": [
        {"word":"糸","reading":"いと","meaning":"thread"},
        {"word":"絹糸","reading":"けんし","meaning":"silk thread"},
        {"word":"毛糸","reading":"けいと","meaning":"yarn"},
        {"word":"綿糸","reading":"めんし","meaning":"cotton thread"},
        {"word":"糸口","reading":"いとぐち","meaning":"clue"},
        {"word":"赤い糸","reading":"あかいいと","meaning":"red thread of fate"}
    ]},
    "紙": {"on": ["シ"], "kun": ["かみ"], "meaning": "paper", "compounds": [
        {"word":"紙","reading":"かみ","meaning":"paper"},
        {"word":"和紙","reading":"わし","meaning":"Japanese paper"},
        {"word":"白紙","reading":"はくし","meaning":"blank paper"},
        {"word":"折り紙","reading":"おりがみ","meaning":"origami"},
        {"word":"画用紙","reading":"がようし","meaning":"drawing paper"},
        {"word":"厚紙","reading":"あつがみ","meaning":"cardboard"},
        {"word":"包装紙","reading":"ほうそうし","meaning":"wrapping paper"}
    ]},
    "門": {"on": ["モン"], "kun": ["かど"], "meaning": "gate", "compounds": [
        {"word":"門","reading":"もん","meaning":"gate"},
        {"word":"学校","reading":"がっこう","meaning":"school"},
        {"word":"専門","reading":"せんもん","meaning":"specialty"},
        {"word":"入門","reading":"にゅうもん","meaning":"initiation"},
        {"word":"門戸","reading":"もんこ","meaning":"doorway"},
        {"word":"一門","reading":"いちもん","meaning":"family, clan"},
        {"word":"鳥居","reading":"とりい","meaning":"shrine gate"}
    ]},
    "間": {"on": ["カン","ケン"], "kun": ["あいだ","ま"], "meaning": "interval, space", "compounds": [
        {"word":"間","reading":"あいだ","meaning":"between"},
        {"word":"時間","reading":"じかん","meaning":"time"},
        {"word":"空間","reading":"くうかん","meaning":"space"},
        {"word":"人間","reading":"にんげん","meaning":"human"},
        {"word":"瞬間","reading":"しゅんかん","meaning":"moment"},
        {"word":"期間","reading":"きかん","meaning":"period"},
        {"word":"世間","reading":"せけん","meaning":"society"},
        {"word":"仲間","reading":"なかま","meaning":"companion"}
    ]},
    "家": {"on": ["カ","ケ"], "kun": ["いえ","や","うち"], "meaning": "house, home", "compounds": [
        {"word":"家","reading":"いえ","meaning":"house"},
        {"word":"家族","reading":"かぞく","meaning":"family"},
        {"word":"家庭","reading":"かてい","meaning":"home"},
        {"word":"大家","reading":"おおや","meaning":"landlord"},
        {"word":"作家","reading":"さっか","meaning":"author"},
        {"word":"画家","reading":"がか","meaning":"painter"},
        {"word":"建築家","reading":"けんちくか","meaning":"architect"},
        {"word":"実家","reading":"じっか","meaning":"parents' home"}
    ]},
    "室": {"on": ["シツ"], "kun": ["むろ"], "meaning": "room", "compounds": [
        {"word":"教室","reading":"きょうしつ","meaning":"classroom"},
        {"word":"事務室","reading":"じむしつ","meaning":"office"},
        {"word":"寝室","reading":"しんしつ","meaning":"bedroom"},
        {"word":"研究室","reading":"けんきゅうしつ","meaning":"laboratory"},
        {"word":"待合室","reading":"まちあいしつ","meaning":"waiting room"},
        {"word":"室内","reading":"しつない","meaning":"indoor"},
        {"word":"王室","reading":"おうしつ","meaning":"royal family"}
    ]},
    "町": {"on": ["チョウ"], "kun": ["まち"], "meaning": "town", "compounds": [
        {"word":"町","reading":"まち","meaning":"town"},
        {"word":"町内","reading":"ちょうない","meaning":"neighborhood"},
        {"word":"下町","reading":"したまち","meaning":"old town"},
        {"word":"町並み","reading":"まちなみ","meaning":"townscape"},
        {"word":"商店街","reading":"しょうてんがい","meaning":"shopping street"},
        {"word":"町長","reading":"ちょうちょう","meaning":"mayor"}
    ]},
    "村": {"on": ["ソン"], "kun": ["むら"], "meaning": "village", "compounds": [
        {"word":"村","reading":"むら","meaning":"village"},
        {"word":"村民","reading":"そんみん","meaning":"villager"},
        {"word":"農村","reading":"のうそん","meaning":"farming village"},
        {"word":"漁村","reading":"ぎょそん","meaning":"fishing village"},
        {"word":"山村","reading":"さんそん","meaning":"mountain village"},
        {"word":"村長","reading":"そんちょう","meaning":"village chief"}
    ]},
    "森": {"on": ["シン"], "kun": ["もり"], "meaning": "forest", "compounds": [
        {"word":"森","reading":"もり","meaning":"forest"},
        {"word":"森林","reading":"しんりん","meaning":"forest"},
        {"word":"森羅万象","reading":"しんらばんしょう","meaning":"all nature"},
        {"word":"密林","reading":"みつりん","meaning":"dense forest"},
        {"word":"原始林","reading":"げんしりん","meaning":"primeval forest"}
    ]},
    "林": {"on": ["リン"], "kun": ["はやし"], "meaning": "woods, grove", "compounds": [
        {"word":"林","reading":"はやし","meaning":"woods"},
        {"word":"森林","reading":"しんりん","meaning":"forest"},
        {"word":"林業","reading":"りんぎょう","meaning":"forestry"},
        {"word":"竹林","reading":"ちくりん","meaning":"bamboo grove"},
        {"word":"小林","reading":"こばやし","meaning":"Kobayashi (surname)"},
        {"word":"山林","reading":"さんりん","meaning":"mountain forest"}
    ]},
    "海": {"on": ["カイ"], "kun": ["うみ"], "meaning": "sea, ocean", "compounds": [
        {"word":"海","reading":"うみ","meaning":"sea"},
        {"word":"海外","reading":"かいがい","meaning":"overseas"},
        {"word":"海岸","reading":"かいがん","meaning":"coast"},
        {"word":"海水","reading":"かいすい","meaning":"seawater"},
        {"word":"海運","reading":"かいうん","meaning":"shipping"},
        {"word":"航海","reading":"こうかい","meaning":"navigation"},
        {"word":"日本海","reading":"にほんかい","meaning":"Sea of Japan"},
        {"word":"地中海","reading":"ちちゅうかい","meaning":"Mediterranean Sea"}
    ]},
    "空": {"on": ["クウ"], "kun": ["そら","あ.く","から"], "meaning": "sky, empty", "compounds": [
        {"word":"空","reading":"そら","meaning":"sky"},
        {"word":"空気","reading":"くうき","meaning":"air"},
        {"word":"空港","reading":"くうこう","meaning":"airport"},
        {"word":"青空","reading":"あおぞら","meaning":"blue sky"},
        {"word":"空白","reading":"くうはく","meaning":"blank"},
        {"word":"空虚","reading":"くうきょ","meaning":"emptiness"},
        {"word":"航空","reading":"こうくう","meaning":"aviation"},
        {"word":"夜空","reading":"よぞら","meaning":"night sky"}
    ]},
    "星": {"on": ["セイ","ショウ"], "kun": ["ほし"], "meaning": "star", "compounds": [
        {"word":"星","reading":"ほし","meaning":"star"},
        {"word":"星座","reading":"せいざ","meaning":"constellation"},
        {"word":"惑星","reading":"わくせい","meaning":"planet"},
        {"word":"衛星","reading":"えいせい","meaning":"satellite"},
        {"word":"流星","reading":"りゅうせい","meaning":"meteor"},
        {"word":"星空","reading":"ほしぞら","meaning":"starry sky"},
        {"word":"一番星","reading":"いちばんぼし","meaning":"evening star"}
    ]},
    "電": {"on": ["デン"], "kun": [], "meaning": "electricity", "compounds": [
        {"word":"電気","reading":"でんき","meaning":"electricity"},
        {"word":"電話","reading":"でんわ","meaning":"telephone"},
        {"word":"電車","reading":"でんしゃ","meaning":"train"},
        {"word":"電子","reading":"でんし","meaning":"electron"},
        {"word":"電池","reading":"でんち","meaning":"battery"},
        {"word":"映画","reading":"えいが","meaning":"movie"},
        {"word":"電源","reading":"でんげん","meaning":"power source"},
        {"word":"発電","reading":"はつでん","meaning":"power generation"}
    ]},
    "社": {"on": ["シャ"], "kun": ["やしろ"], "meaning": "company, shrine", "compounds": [
        {"word":"会社","reading":"かいしゃ","meaning":"company"},
        {"word":"社会","reading":"しゃかい","meaning":"society"},
        {"word":"神社","reading":"じんじゃ","meaning":"shrine"},
        {"word":"社長","reading":"しゃちょう","meaning":"president"},
        {"word":"社員","reading":"しゃいん","meaning":"employee"},
        {"word":"入社","reading":"にゅうしゃ","meaning":"joining a company"},
        {"word":"退社","reading":"たいしゃ","meaning":"leaving a company"},
        {"word":"公社","reading":"こうしゃ","meaning":"public corporation"}
    ]},
    "工": {"on": ["コウ","ク"], "kun": [], "meaning": "work, construction", "compounds": [
        {"word":"工場","reading":"こうじょう","meaning":"factory"},
        {"word":"工作","reading":"こうさく","meaning":"craft"},
        {"word":"工業","reading":"こうぎょう","meaning":"industry"},
        {"word":"工事","reading":"こうじ","meaning":"construction"},
        {"word":"工夫","reading":"くふう","meaning":"device"},
        {"word":"加工","reading":"かこう","meaning":"processing"},
        {"word":"人工","reading":"じんこう","meaning":"artificial"},
        {"word":"工学","reading":"こうがく","meaning":"engineering"}
    ]},
    "作": {"on": ["サク","サ"], "kun": ["つく.る"], "meaning": "make, create", "compounds": [
        {"word":"作る","reading":"つくる","meaning":"to make"},
        {"word":"作品","reading":"さくひん","meaning":"work of art"},
        {"word":"作業","reading":"さぎょう","meaning":"work"},
        {"word":"作家","reading":"さっか","meaning":"author"},
        {"word":"作曲","reading":"さっきょく","meaning":"composition"},
        {"word":"製作","reading":"せいさく","meaning":"manufacture"},
        {"word":"動作","reading":"どうさ","meaning":"movement"},
        {"word":"耕作","reading":"こうさく","meaning":"cultivation"}
    ]},
    "仕": {"on": ["シ","ジ"], "kun": ["つか.える"], "meaning": "serve, do", "compounds": [
        {"word":"仕事","reading":"しごと","meaning":"work"},
        {"word":"仕方","reading":"しかた","meaning":"way of doing"},
        {"word":"仕上げる","reading":"しあげる","meaning":"to finish"},
        {"word":"仕分け","reading":"しわけ","meaning":"sorting"},
        {"word":"仕入れ","reading":"しいれ","meaning":"stocking"},
        {"word":"仕官","reading":"しかん","meaning":"government service"}
    ]},
    "事": {"on": ["ジ","ズ"], "kun": ["こと"], "meaning": "matter, thing", "compounds": [
        {"word":"事","reading":"こと","meaning":"thing, matter"},
        {"word":"事故","reading":"じこ","meaning":"accident"},
        {"word":"事件","reading":"じけん","meaning":"incident"},
        {"word":"事情","reading":"じじょう","meaning":"circumstances"},
        {"word":"事実","reading":"じじつ","meaning":"fact"},
        {"word":"事務所","reading":"じむしょ","meaning":"office"},
        {"word":"大事","reading":"だいじ","meaning":"important"},
        {"word":"返事","reading":"へんじ","meaning":"reply"}
    ]},
    "物": {"on": ["ブツ","モツ"], "kun": ["もの"], "meaning": "thing, object", "compounds": [
        {"word":"物","reading":"もの","meaning":"thing"},
        {"word":"動物","reading":"どうぶつ","meaning":"animal"},
        {"word":"植物","reading":"しょくぶつ","meaning":"plant"},
        {"word":"建物","reading":"たてもの","meaning":"building"},
        {"word":"買い物","reading":"かいもの","meaning":"shopping"},
        {"word":"贈り物","reading":"おくりもの","meaning":"gift"},
        {"word":"物語","reading":"ものがたり","meaning":"story"},
        {"word":"物件","reading":"ぶっけん","meaning":"property"}
    ]},
    "品": {"on": ["ヒン","ホン"], "kun": ["しな"], "meaning": "product, quality", "compounds": [
        {"word":"品物","reading":"しなもの","meaning":"goods"},
        {"word":"商品","reading":"しょうひん","meaning":"product"},
        {"word":"作品","reading":"さくひん","meaning":"work of art"},
        {"word":"品質","reading":"ひんしつ","meaning":"quality"},
        {"word":"食品","reading":"しょくひん","meaning":"food products"},
        {"word":"製品","reading":"せいひん","meaning":"manufactured goods"},
        {"word":"上品","reading":"じょうひん","meaning":"elegant"},
        {"word":"下品","reading":"げひん","meaning":"vulgar"}
    ]},
    "商": {"on": ["ショウ"], "kun": [], "meaning": "commerce", "compounds": [
        {"word":"商人","reading":"しょうにん","meaning":"merchant"},
        {"word":"商業","reading":"しょうぎょう","meaning":"commerce"},
        {"word":"商品","reading":"しょうひん","meaning":"product"},
        {"word":"商店","reading":"しょうてん","meaning":"shop"},
        {"word":"商社","reading":"しょうしゃ","meaning":"trading company"},
        {"word":"商談","reading":"しょうだん","meaning":"business talk"},
        {"word":"商標","reading":"しょうひょう","meaning":"trademark"}
    ]},
    "買": {"on": ["バイ"], "kun": ["か.う"], "meaning": "buy", "compounds": [
        {"word":"買う","reading":"かう","meaning":"to buy"},
        {"word":"買い物","reading":"かいもの","meaning":"shopping"},
        {"word":"売買","reading":"ばいばい","meaning":"buying and selling"},
        {"word":"購入","reading":"こうにゅう","meaning":"purchase"},
        {"word":"買収","reading":"ばいしゅう","meaning":"acquisition"},
        {"word":"買い手","reading":"かいて","meaning":"buyer"}
    ]},
    "売": {"on": ["バイ"], "kun": ["う.る"], "meaning": "sell", "compounds": [
        {"word":"売る","reading":"うる","meaning":"to sell"},
        {"word":"売上","reading":"うりあげ","meaning":"sales"},
        {"word":"売り場","reading":"うりば","meaning":"sales floor"},
        {"word":"販売","reading":"はんばい","meaning":"sale"},
        {"word":"売買","reading":"ばいばい","meaning":"buying and selling"},
        {"word":"売り切れ","reading":"うりきれ","meaning":"sold out"},
        {"word":"安売り","reading":"やすうり","meaning":"discount sale"}
    ]},
    "友": {"on": ["ユウ"], "kun": ["とも"], "meaning": "friend", "compounds": [
        {"word":"友達","reading":"ともだち","meaning":"friend"},
        {"word":"友人","reading":"ゆうじん","meaning":"friend"},
        {"word":"友好","reading":"ゆうこう","meaning":"friendship"},
        {"word":"友情","reading":"ゆうじょう","meaning":"friendship"},
        {"word":"親友","reading":"しんゆう","meaning":"close friend"},
        {"word":"学友","reading":"がくゆう","meaning":"school friend"},
        {"word":"戦友","reading":"せんゆう","meaning":"comrade"}
    ]},
    "父": {"on": ["フ"], "kun": ["ちち","とう"], "meaning": "father", "compounds": [
        {"word":"父","reading":"ちち","meaning":"father"},
        {"word":"お父さん","reading":"おとうさん","meaning":"father"},
        {"word":"父親","reading":"ちちおや","meaning":"father"},
        {"word":"祖父","reading":"そふ","meaning":"grandfather"},
        {"word":"父母","reading":"ふぼ","meaning":"parents"},
        {"word":"義父","reading":"ぎふ","meaning":"stepfather"}
    ]},
    "母": {"on": ["ボ"], "kun": ["はは","かあ"], "meaning": "mother", "compounds": [
        {"word":"母","reading":"はは","meaning":"mother"},
        {"word":"お母さん","reading":"おかあさん","meaning":"mother"},
        {"word":"母親","reading":"ははおや","meaning":"mother"},
        {"word":"祖母","reading":"そぼ","meaning":"grandmother"},
        {"word":"父母","reading":"ふぼ","meaning":"parents"},
        {"word":"母校","reading":"ぼこう","meaning":"alma mater"},
        {"word":"母語","reading":"ぼご","meaning":"native language"}
    ]},
    "兄": {"on": ["ケイ","キョウ"], "kun": ["あに"], "meaning": "older brother", "compounds": [
        {"word":"兄","reading":"あに","meaning":"older brother"},
        {"word":"お兄さん","reading":"おにいさん","meaning":"older brother"},
        {"word":"兄弟","reading":"きょうだい","meaning":"siblings"},
        {"word":"兄貴","reading":"あにき","meaning":"big bro"},
        {"word":"従兄","reading":"いとこ","meaning":"cousin"}
    ]},
    "弟": {"on": ["テイ","ダイ"], "kun": ["おとうと"], "meaning": "younger brother", "compounds": [
        {"word":"弟","reading":"おとうと","meaning":"younger brother"},
        {"word":"お弟さん","reading":"おとうとさん","meaning":"younger brother"},
        {"word":"兄弟","reading":"きょうだい","meaning":"siblings"},
        {"word":"弟子","reading":"でし","meaning":"disciple"},
        {"word":"従弟","reading":"いとこ","meaning":"cousin"}
    ]},
    "姉": {"on": ["シ"], "kun": ["あね"], "meaning": "older sister", "compounds": [
        {"word":"姉","reading":"あね","meaning":"older sister"},
        {"word":"お姉さん","reading":"おねえさん","meaning":"older sister"},
        {"word":"姉妹","reading":"しまい","meaning":"sisters"},
        {"word":"姉弟","reading":"してい","meaning":"older sister and younger brother"},
        {"word":"従姉","reading":"いとこ","meaning":"cousin"}
    ]},
    "妹": {"on": ["マイ"], "kun": ["いもうと"], "meaning": "younger sister", "compounds": [
        {"word":"妹","reading":"いもうと","meaning":"younger sister"},
        {"word":"お妹さん","reading":"いもうとさん","meaning":"younger sister"},
        {"word":"姉妹","reading":"しまい","meaning":"sisters"},
        {"word":"兄妹","reading":"きょうまい","meaning":"brother and sister"},
        {"word":"従妹","reading":"いとこ","meaning":"cousin"}
    ]},
    "夫": {"on": ["フ","フウ"], "kun": ["おっと"], "meaning": "husband", "compounds": [
        {"word":"夫","reading":"おっと","meaning":"husband"},
        {"word":"夫婦","reading":"ふうふ","meaning":"married couple"},
        {"word":"夫人","reading":"ふじん","meaning":"wife, lady"},
        {"word":"丈夫","reading":"じょうぶ","meaning":"strong"},
        {"word":"功夫","reading":"カンフー","meaning":"kung fu"},
        {"word":"人夫","reading":"にんぷ","meaning":"laborer"}
    ]},
    "妻": {"on": ["サイ"], "kun": ["つま"], "meaning": "wife", "compounds": [
        {"word":"妻","reading":"つま","meaning":"wife"},
        {"word":"夫婦","reading":"ふうふ","meaning":"married couple"},
        {"word":"妻子","reading":"さいし","meaning":"wife and children"},
        {"word":"妻帯","reading":"さいたい","meaning":"married"},
        {"word":"愛妻","reading":"あいさい","meaning":"beloved wife"}
    ]},
    "愛": {"on": ["アイ"], "kun": ["いと.しい"], "meaning": "love", "compounds": [
        {"word":"愛","reading":"あい","meaning":"love"},
        {"word":"愛情","reading":"あいじょう","meaning":"love"},
        {"word":"恋愛","reading":"れんあい","meaning":"romantic love"},
        {"word":"愛国","reading":"あいこく","meaning":"patriotism"},
        {"word":"愛犬","reading":"あいけん","meaning":"pet dog"},
        {"word":"愛猫","reading":"あいびょう","meaning":"pet cat"},
        {"word":"可愛","reading":"かわいい","meaning":"cute"},
        {"word":"親愛","reading":"しんあい","meaning":"dear"}
    ]},
    "恋": {"on": ["レン"], "kun": ["こい","こい.しい"], "meaning": "romance, longing", "compounds": [
        {"word":"恋","reading":"こい","meaning":"love"},
        {"word":"恋人","reading":"こいびと","meaning":"lover"},
        {"word":"恋愛","reading":"れんあい","meaning":"romantic love"},
        {"word":"失恋","reading":"しつれん","meaning":"heartbreak"},
        {"word":"初恋","reading":"はつこい","meaning":"first love"},
        {"word":"片思い","reading":"かたおもい","meaning":"unrequited love"},
        {"word":"恋しい","reading":"こいしい","meaning":"longed for"}
    ]},
    "夢": {"on": ["ム"], "kun": ["ゆめ"], "meaning": "dream", "compounds": [
        {"word":"夢","reading":"ゆめ","meaning":"dream"},
        {"word":"悪夢","reading":"あくむ","meaning":"nightmare"},
        {"word":"夢中","reading":"むちゅう","meaning":"absorbed in"},
        {"word":"夢想","reading":"むそう","meaning":"daydream"},
        {"word":"幻夢","reading":"げんむ","meaning":"illusion"},
        {"word":"夢物語","reading":"ゆめものがたり","meaning":"dream story"}
    ]},
    "死": {"on": ["シ"], "kun": ["し.ぬ"], "meaning": "death", "compounds": [
        {"word":"死ぬ","reading":"しぬ","meaning":"to die"},
        {"word":"死亡","reading":"しぼう","meaning":"death"},
        {"word":"死者","reading":"ししゃ","meaning":"the dead"},
        {"word":"必死","reading":"ひっし","meaning":"desperate"},
        {"word":"死刑","reading":"しけい","meaning":"death penalty"},
        {"word":"生死","reading":"せいし","meaning":"life and death"},
        {"word":"死体","reading":"したい","meaning":"corpse"}
    ]},
    "病": {"on": ["ビョウ"], "kun": ["やまい","や.む"], "meaning": "illness", "compounds": [
        {"word":"病気","reading":"びょうき","meaning":"illness"},
        {"word":"病院","reading":"びょういん","meaning":"hospital"},
        {"word":"患者","reading":"かんじゃ","meaning":"patient"},
        {"word":"症状","reading":"しょうじょう","meaning":"symptoms"},
        {"word":"重病","reading":"じゅうびょう","meaning":"serious illness"},
        {"word":"病室","reading":"びょうしつ","meaning":"hospital room"},
        {"word":"看病","reading":"かんびょう","meaning":"nursing"}
    ]},
    "薬": {"on": ["ヤク"], "kun": ["くすり"], "meaning": "medicine", "compounds": [
        {"word":"薬","reading":"くすり","meaning":"medicine"},
        {"word":"薬局","reading":"やっきょく","meaning":"pharmacy"},
        {"word":"薬剤","reading":"やくざい","meaning":"drug"},
        {"word":"処方薬","reading":"しょほうやく","meaning":"prescription medicine"},
        {"word":"漢方薬","reading":"かんぽうやく","meaning":"Chinese herbal medicine"},
        {"word":"薬品","reading":"やくひん","meaning":"chemicals"},
        {"word":"毒薬","reading":"どくやく","meaning":"poison"}
    ]},
    "医": {"on": ["イ"], "kun": [], "meaning": "medicine, doctor", "compounds": [
        {"word":"医者","reading":"いしゃ","meaning":"doctor"},
        {"word":"医学","reading":"いがく","meaning":"medical science"},
        {"word":"医院","reading":"いいん","meaning":"clinic"},
        {"word":"医師","reading":"いし","meaning":"physician"},
        {"word":"医療","reading":"いりょう","meaning":"medical care"},
        {"word":"歯科医","reading":"しかい","meaning":"dentist"},
        {"word":"獣医","reading":"じゅうい","meaning":"veterinarian"}
    ]},
    "院": {"on": ["イン"], "kun": [], "meaning": "institution", "compounds": [
        {"word":"病院","reading":"びょういん","meaning":"hospital"},
        {"word":"学院","reading":"がくいん","meaning":"academy"},
        {"word":"寺院","reading":"じいん","meaning":"temple"},
        {"word":"入院","reading":"にゅういん","meaning":"hospitalization"},
        {"word":"退院","reading":"たいいん","meaning":"discharge"},
        {"word":"大学院","reading":"だいがくいん","meaning":"graduate school"},
        {"word":"裁判所","reading":"さいばんしょ","meaning":"court"}
    ]},
    "政": {"on": ["セイ","ショウ"], "kun": ["まつりごと"], "meaning": "politics, government", "compounds": [
        {"word":"政治","reading":"せいじ","meaning":"politics"},
        {"word":"政府","reading":"せいふ","meaning":"government"},
        {"word":"政策","reading":"せいさく","meaning":"policy"},
        {"word":"政党","reading":"せいとう","meaning":"political party"},
        {"word":"行政","reading":"ぎょうせい","meaning":"administration"},
        {"word":"市政","reading":"しせい","meaning":"city administration"},
        {"word":"政治家","reading":"せいじか","meaning":"politician"}
    ]},
    "治": {"on": ["ジ","チ"], "kun": ["なお.す","おさ.める"], "meaning": "govern, cure", "compounds": [
        {"word":"治す","reading":"なおす","meaning":"to cure"},
        {"word":"治療","reading":"ちりょう","meaning":"treatment"},
        {"word":"治安","reading":"ちあん","meaning":"public order"},
        {"word":"自治","reading":"じち","meaning":"self-government"},
        {"word":"明治","reading":"めいじ","meaning":"Meiji era"},
        {"word":"治水","reading":"ちすい","meaning":"flood control"},
        {"word":"統治","reading":"とうち","meaning":"rule"}
    ]},
    "法": {"on": ["ホウ"], "kun": [], "meaning": "law, method", "compounds": [
        {"word":"法律","reading":"ほうりつ","meaning":"law"},
        {"word":"方法","reading":"ほうほう","meaning":"method"},
        {"word":"憲法","reading":"けんぽう","meaning":"constitution"},
        {"word":"刑法","reading":"けいほう","meaning":"criminal law"},
        {"word":"司法","reading":"しほう","meaning":"judiciary"},
        {"word":"不法","reading":"ふほう","meaning":"illegal"},
        {"word":"文法","reading":"ぶんぽう","meaning":"grammar"},
        {"word":"作法","reading":"さほう","meaning":"manners"}
    ]},
    "経": {"on": ["ケイ","キョウ"], "kun": ["へ.る"], "meaning": "pass through, manage", "compounds": [
        {"word":"経験","reading":"けいけん","meaning":"experience"},
        {"word":"経済","reading":"けいざい","meaning":"economy"},
        {"word":"経営","reading":"けいえい","meaning":"management"},
        {"word":"経由","reading":"けいゆ","meaning":"via"},
        {"word":"神経","reading":"しんけい","meaning":"nerve"},
        {"word":"経過","reading":"けいか","meaning":"progress"},
        {"word":"聖書","reading":"せいしょ","meaning":"Bible"},
        {"word":"経費","reading":"けいひ","meaning":"expenses"}
    ]},
    "済": {"on": ["サイ"], "kun": ["す.む"], "meaning": "settle, finish", "compounds": [
        {"word":"済む","reading":"すむ","meaning":"to finish"},
        {"word":"経済","reading":"けいざい","meaning":"economy"},
        {"word":"返済","reading":"へんさい","meaning":"repayment"},
        {"word":"救済","reading":"きゅうさい","meaning":"relief"},
        {"word":"未済","reading":"みさい","meaning":"unfinished"},
        {"word":"決済","reading":"けっさい","meaning":"settlement"}
    ]},
    "民": {"on": ["ミン"], "kun": ["たみ"], "meaning": "people", "compounds": [
        {"word":"国民","reading":"こくみん","meaning":"citizens"},
        {"word":"民主","reading":"みんしゅ","meaning":"democracy"},
        {"word":"民族","reading":"みんぞく","meaning":"ethnic group"},
        {"word":"民間","reading":"みんかん","meaning":"private sector"},
        {"word":"市民","reading":"しみん","meaning":"citizen"},
        {"word":"住民","reading":"じゅうみん","meaning":"resident"},
        {"word":"人民","reading":"じんみん","meaning":"people"},
        {"word":"民俗","reading":"みんぞく","meaning":"folk customs"}
    ]},
    "部": {"on": ["ブ"], "kun": [], "meaning": "part, department", "compounds": [
        {"word":"部分","reading":"ぶぶん","meaning":"part"},
        {"word":"全部","reading":"ぜんぶ","meaning":"all"},
        {"word":"部長","reading":"ぶちょう","meaning":"department head"},
        {"word":"外部","reading":"がいぶ","meaning":"outside"},
        {"word":"内部","reading":"ないぶ","meaning":"inside"},
        {"word":"学部","reading":"がくぶ","meaning":"faculty"},
        {"word":"部屋","reading":"へや","meaning":"room"},
        {"word":"本部","reading":"ほんぶ","meaning":"headquarters"}
    ]},
    "活": {"on": ["カツ"], "kun": ["い.きる"], "meaning": "live, active", "compounds": [
        {"word":"生活","reading":"せいかつ","meaning":"life"},
        {"word":"活動","reading":"かつどう","meaning":"activity"},
        {"word":"活躍","reading":"かつやく","meaning":"active participation"},
        {"word":"活用","reading":"かつよう","meaning":"application"},
        {"word":"活力","reading":"かつりょく","meaning":"vitality"},
        {"word":"復活","reading":"ふっかつ","meaning":"revival"},
        {"word":"生活費","reading":"せいかつひ","meaning":"living expenses"}
    ]},
    "動": {"on": ["ドウ"], "kun": ["うご.く","うご.かす"], "meaning": "move", "compounds": [
        {"word":"動く","reading":"うごく","meaning":"to move"},
        {"word":"動物","reading":"どうぶつ","meaning":"animal"},
        {"word":"運動","reading":"うんどう","meaning":"exercise"},
        {"word":"動作","reading":"どうさ","meaning":"movement"},
        {"word":"動画","reading":"どうが","meaning":"video"},
        {"word":"自動","reading":"じどう","meaning":"automatic"},
        {"word":"労働","reading":"ろうどう","meaning":"labor"},
        {"word":"感動","reading":"かんどう","meaning":"being moved"}
    ]},
    "働": {"on": ["ドウ"], "kun": ["はたら.く"], "meaning": "work", "compounds": [
        {"word":"働く","reading":"はたらく","meaning":"to work"},
        {"word":"労働","reading":"ろうどう","meaning":"labor"},
        {"word":"共働き","reading":"ともばたらき","meaning":"both spouses working"},
        {"word":"働き手","reading":"はたらきて","meaning":"worker"},
        {"word":"残業","reading":"ざんぎょう","meaning":"overtime"}
    ]},
    "運": {"on": ["ウン"], "kun": ["はこ.ぶ"], "meaning": "carry, luck, fortune", "compounds": [
        {"word":"運ぶ","reading":"はこぶ","meaning":"to carry"},
        {"word":"運動","reading":"うんどう","meaning":"exercise"},
        {"word":"運転","reading":"うんてん","meaning":"driving"},
        {"word":"運命","reading":"うんめい","meaning":"fate"},
        {"word":"運勢","reading":"うんせい","meaning":"fortune"},
        {"word":"運送","reading":"うんそう","meaning":"transport"},
        {"word":"幸運","reading":"こううん","meaning":"good luck"},
        {"word":"不運","reading":"ふうん","meaning":"bad luck"}
    ]},
    "転": {"on": ["テン"], "kun": ["ころ.ぶ"], "meaning": "turn, change", "compounds": [
        {"word":"転ぶ","reading":"ころぶ","meaning":"to fall"},
        {"word":"回転","reading":"かいてん","meaning":"rotation"},
        {"word":"運転","reading":"うんてん","meaning":"driving"},
        {"word":"転職","reading":"てんしょく","meaning":"changing jobs"},
        {"word":"移動","reading":"いどう","meaning":"movement"},
        {"word":"反転","reading":"はんてん","meaning":"reversal"},
        {"word":"好転","reading":"こうてん","meaning":"improvement"},
        {"word":"急転","reading":"きゅうてん","meaning":"sudden turn"}
    ]},
    "進": {"on": ["シン"], "kun": ["すす.む","すす.める"], "meaning": "advance, progress", "compounds": [
        {"word":"進む","reading":"すすむ","meaning":"to advance"},
        {"word":"進化","reading":"しんか","meaning":"evolution"},
        {"word":"進行","reading":"しんこう","meaning":"progress"},
        {"word":"進学","reading":"しんがく","meaning":"advancing to higher school"},
        {"word":"前進","reading":"ぜんしん","meaning":"advance"},
        {"word":"推進","reading":"すいしん","meaning":"propulsion"},
        {"word":"進路","reading":"しんろ","meaning":"course, career"},
        {"word":"進歩","reading":"しんぽ","meaning":"progress"}
    ]},
    "歩": {"on": ["ホ","ブ"], "kun": ["ある.く","あゆ.む"], "meaning": "walk", "compounds": [
        {"word":"歩く","reading":"あるく","meaning":"to walk"},
        {"word":"散歩","reading":"さんぽ","meaning":"walk, stroll"},
        {"word":"歩道","reading":"ほどう","meaning":"sidewalk"},
        {"word":"徒歩","reading":"とほ","meaning":"walking"},
        {"word":"一歩","reading":"いっぽ","meaning":"one step"},
        {"word":"進歩","reading":"しんぽ","meaning":"progress"},
        {"word":"歩行者","reading":"ほこうしゃ","meaning":"pedestrian"}
    ]},
    "走": {"on": ["ソウ"], "kun": ["はし.る"], "meaning": "run", "compounds": [
        {"word":"走る","reading":"はしる","meaning":"to run"},
        {"word":"走行","reading":"そうこう","meaning":"running"},
        {"word":"競争","reading":"きょうそう","meaning":"competition"},
        {"word":"逃走","reading":"とうそう","meaning":"escape"},
        {"word":"疾走","reading":"しっそう","meaning":"sprinting"},
        {"word":"脱走","reading":"だっそう","meaning":"escape"},
        {"word":"走り書き","reading":"はしりがき","meaning":"hasty writing"}
    ]},
    "止": {"on": ["シ"], "kun": ["と.まる","と.める","や.める"], "meaning": "stop", "compounds": [
        {"word":"止まる","reading":"とまる","meaning":"to stop"},
        {"word":"止める","reading":"とめる","meaning":"to stop something"},
        {"word":"禁止","reading":"きんし","meaning":"prohibition"},
        {"word":"停止","reading":"ていし","meaning":"suspension"},
        {"word":"中止","reading":"ちゅうし","meaning":"suspension"},
        {"word":"防止","reading":"ぼうし","meaning":"prevention"},
        {"word":"休止","reading":"きゅうし","meaning":"pause"},
        {"word":"歯止め","reading":"はどめ","meaning":"brake"}
    ]},
    "住": {"on": ["ジュウ"], "kun": ["す.む"], "meaning": "live, reside", "compounds": [
        {"word":"住む","reading":"すむ","meaning":"to live"},
        {"word":"住所","reading":"じゅうしょ","meaning":"address"},
        {"word":"住宅","reading":"じゅうたく","meaning":"housing"},
        {"word":"住民","reading":"じゅうみん","meaning":"resident"},
        {"word":"居住","reading":"きょじゅう","meaning":"residence"},
        {"word":"移住","reading":"いじゅう","meaning":"migration"},
        {"word":"住居","reading":"じゅうきょ","meaning":"dwelling"}
    ]},
    "座": {"on": ["ザ"], "kun": ["すわ.る"], "meaning": "sit, seat", "compounds": [
        {"word":"座る","reading":"すわる","meaning":"to sit"},
        {"word":"座席","reading":"ざせき","meaning":"seat"},
        {"word":"講座","reading":"こうざ","meaning":"lecture course"},
        {"word":"銀河座","reading":"ぎんがざ","meaning":"galaxy constellation"},
        {"word":"正座","reading":"せいざ","meaning":"formal sitting"},
        {"word":"台座","reading":"だいざ","meaning":"pedestal"},
        {"word":"満員御礼","reading":"まんいんおんれい","meaning":"full house"}
    ]},
    "待": {"on": ["タイ"], "kun": ["ま.つ"], "meaning": "wait", "compounds": [
        {"word":"待つ","reading":"まつ","meaning":"to wait"},
        {"word":"期待","reading":"きたい","meaning":"expectation"},
        {"word":"招待","reading":"しょうたい","meaning":"invitation"},
        {"word":"待遇","reading":"たいぐう","meaning":"treatment"},
        {"word":"待ち合わせ","reading":"まちあわせ","meaning":"meeting up"},
        {"word":"待合室","reading":"まちあいしつ","meaning":"waiting room"},
        {"word":"歓迎","reading":"かんげい","meaning":"welcome"}
    ]},
    "持": {"on": ["ジ"], "kun": ["も.つ"], "meaning": "hold, have", "compounds": [
        {"word":"持つ","reading":"もつ","meaning":"to hold"},
        {"word":"気持ち","reading":"きもち","meaning":"feeling"},
        {"word":"所持","reading":"しょじ","meaning":"possession"},
        {"word":"維持","reading":"いじ","meaning":"maintenance"},
        {"word":"支持","reading":"しじ","meaning":"support"},
        {"word":"持続","reading":"じぞく","meaning":"continuation"},
        {"word":"手持ち","reading":"てもち","meaning":"on hand"},
        {"word":"持ち主","reading":"もちぬし","meaning":"owner"}
    ]},
    "使": {"on": ["シ"], "kun": ["つか.う"], "meaning": "use", "compounds": [
        {"word":"使う","reading":"つかう","meaning":"to use"},
        {"word":"使用","reading":"しよう","meaning":"use"},
        {"word":"大使","reading":"たいし","meaning":"ambassador"},
        {"word":"使者","reading":"ししゃ","meaning":"messenger"},
        {"word":"使い","reading":"つかい","meaning":"errand"},
        {"word":"行使","reading":"こうし","meaning":"exercise"},
        {"word":"使節","reading":"しせつ","meaning":"envoy"}
    ]},
    "届": {"on": ["カイ"], "kun": ["とど.ける","とど.く"], "meaning": "deliver, reach", "compounds": [
        {"word":"届ける","reading":"とどける","meaning":"to deliver"},
        {"word":"届く","reading":"とどく","meaning":"to reach"},
        {"word":"郵便","reading":"ゆうびん","meaning":"mail"},
        {"word":"配達","reading":"はいたつ","meaning":"delivery"},
        {"word":"届け出","reading":"とどけで","meaning":"notification"},
        {"word":"年賀状","reading":"ねんがじょう","meaning":"New Year card"}
    ]},
    "送": {"on": ["ソウ"], "kun": ["おく.る"], "meaning": "send", "compounds": [
        {"word":"送る","reading":"おくる","meaning":"to send"},
        {"word":"放送","reading":"ほうそう","meaning":"broadcasting"},
        {"word":"送信","reading":"そうしん","meaning":"transmission"},
        {"word":"輸送","reading":"ゆそう","meaning":"transport"},
        {"word":"配送","reading":"はいそう","meaning":"delivery"},
        {"word":"送別","reading":"そうべつ","meaning":"farewell"},
        {"word":"追送","reading":"ついそう","meaning":"forwarding"}
    ]},
    "受": {"on": ["ジュ"], "kun": ["う.ける"], "meaning": "receive", "compounds": [
        {"word":"受ける","reading":"うける","meaning":"to receive"},
        {"word":"授業","reading":"じゅぎょう","meaning":"class, lesson"},
        {"word":"受験","reading":"じゅけん","meaning":"taking an exam"},
        {"word":"受付","reading":"うけつけ","meaning":"reception"},
        {"word":"受信","reading":"じゅしん","meaning":"reception"},
        {"word":"受身","reading":"うけみ","meaning":"passive"},
        {"word":"受け入れ","reading":"うけいれ","meaning":"acceptance"}
    ]},
    "取": {"on": ["シュ"], "kun": ["と.る"], "meaning": "take", "compounds": [
        {"word":"取る","reading":"とる","meaning":"to take"},
        {"word":"取材","reading":"しゅざい","meaning":"coverage"},
        {"word":"取得","reading":"しゅとく","meaning":"acquisition"},
        {"word":"取り消し","reading":"とりけし","meaning":"cancellation"},
        {"word":"引き取り","reading":"ひきとり","meaning":"taking over"},
        {"word":"取り扱い","reading":"とりあつかい","meaning":"handling"},
        {"word":"選択","reading":"せんたく","meaning":"selection"}
    ]},
    "引": {"on": ["イン"], "kun": ["ひ.く","ひ.ける"], "meaning": "pull, draw", "compounds": [
        {"word":"引く","reading":"ひく","meaning":"to pull"},
        {"word":"引用","reading":"いんよう","meaning":"quotation"},
        {"word":"引力","reading":"いんりょく","meaning":"gravity"},
        {"word":"引き出し","reading":"ひきだし","meaning":"drawer"},
        {"word":"割引","reading":"わりびき","meaning":"discount"},
        {"word":"引っ越し","reading":"ひっこし","meaning":"moving"},
        {"word":"紹介","reading":"しょうかい","meaning":"introduction"}
    ]},
    "切": {"on": ["セツ","サイ"], "kun": ["き.る","き.れる"], "meaning": "cut", "compounds": [
        {"word":"切る","reading":"きる","meaning":"to cut"},
        {"word":"大切","reading":"たいせつ","meaning":"important"},
        {"word":"親切","reading":"しんせつ","meaning":"kind"},
        {"word":"一切","reading":"いっさい","meaning":"everything"},
        {"word":"切断","reading":"せつだん","meaning":"cutting off"},
        {"word":"切り替え","reading":"きりかえ","meaning":"switching"},
        {"word":"手切り","reading":"てぎり","meaning":"manual cutting"}
    ]},
    "打": {"on": ["ダ"], "kun": ["う.つ"], "meaning": "hit, strike", "compounds": [
        {"word":"打つ","reading":"うつ","meaning":"to hit"},
        {"word":"野球","reading":"やきゅう","meaning":"baseball"},
        {"word":"打ち上げ","reading":"うちあげ","meaning":"launch"},
        {"word":"打ち合わせ","reading":"うちあわせ","meaning":"meeting"},
        {"word":"衝撃","reading":"しょうげき","meaning":"shock"},
        {"word":"打撃","reading":"だげき","meaning":"blow"},
        {"word":"一打","reading":"いちだ","meaning":"one stroke"}
    ]},
    "投": {"on": ["トウ"], "kun": ["な.げる"], "meaning": "throw", "compounds": [
        {"word":"投げる","reading":"なげる","meaning":"to throw"},
        {"word":"投票","reading":"とうひょう","meaning":"voting"},
        {"word":"投資","reading":"とうし","meaning":"investment"},
        {"word":"投稿","reading":"とうこう","meaning":"post, submission"},
        {"word":"投手","reading":"とうしゅ","meaning":"pitcher"},
        {"word":"投入","reading":"とうにゅう","meaning":"input"},
        {"word":"投降","reading":"とうこう","meaning":"surrender"}
    ]},
    "押": {"on": ["オウ"], "kun": ["お.す"], "meaning": "push", "compounds": [
        {"word":"押す","reading":"おす","meaning":"to push"},
        {"word":"押し入れ","reading":"おしいれ","meaning":"closet"},
        {"word":"押印","reading":"おういん","meaning":"seal stamp"},
        {"word":"圧倒","reading":"あっとう","meaning":"overwhelming"},
        {"word":"抑圧","reading":"よくあつ","meaning":"oppression"},
        {"word":"押し掛け","reading":"おしかけ","meaning":"uninvited visit"}
    ]},
    "放": {"on": ["ホウ"], "kun": ["はな.す","はな.つ"], "meaning": "release, let go", "compounds": [
        {"word":"放す","reading":"はなす","meaning":"to release"},
        {"word":"解放","reading":"かいほう","meaning":"liberation"},
        {"word":"開放","reading":"かいほう","meaning":"opening"},
        {"word":"放出","reading":"ほうしゅつ","meaning":"emission"},
        {"word":"放棄","reading":"ほうき","meaning":"abandonment"},
        {"word":"放課後","reading":"ほうかご","meaning":"after school"},
        {"word":"自由奔放","reading":"じゆうほんぽう","meaning":"free and unrestrained"}
    ]},
    "教": {"on": ["キョウ"], "kun": ["おし.える","おそ.わる"], "meaning": "teach", "compounds": [
        {"word":"教える","reading":"おしえる","meaning":"to teach"},
        {"word":"教育","reading":"きょういく","meaning":"education"},
        {"word":"教師","reading":"きょうし","meaning":"teacher"},
        {"word":"教室","reading":"きょうしつ","meaning":"classroom"},
        {"word":"教会","reading":"きょうかい","meaning":"church"},
        {"word":"宗教","reading":"しゅうきょう","meaning":"religion"},
        {"word":"教科書","reading":"きょうかしょ","meaning":"textbook"},
        {"word":"教授","reading":"きょうじゅ","meaning":"professor"}
    ]},
    "育": {"on": ["イク"], "kun": ["そだ.つ","そだ.てる"], "meaning": "nurture, grow", "compounds": [
        {"word":"育てる","reading":"そだてる","meaning":"to raise"},
        {"word":"教育","reading":"きょういく","meaning":"education"},
        {"word":"育児","reading":"いくじ","meaning":"childcare"},
        {"word":"育成","reading":"いくせい","meaning":"training"},
        {"word":"生育","reading":"せいいく","meaning":"growth"},
        {"word":"保育","reading":"ほいく","meaning":"childcare"},
        {"word":"体育","reading":"たいいく","meaning":"physical education"},
        {"word":"飼育","reading":"しいく","meaning":"breeding"}
    ]},
    "習": {"on": ["シュウ"], "kun": ["なら.う"], "meaning": "learn, practice", "compounds": [
        {"word":"習う","reading":"ならう","meaning":"to learn"},
        {"word":"練習","reading":"れんしゅう","meaning":"practice"},
        {"word":"習慣","reading":"しゅうかん","meaning":"habit"},
        {"word":"学習","reading":"がくしゅう","meaning":"study"},
        {"word":"自習","reading":"じしゅう","meaning":"self-study"},
        {"word":"復習","reading":"ふくしゅう","meaning":"review"},
        {"word":"予習","reading":"よしゅう","meaning":"preparation"},
        {"word":"習字","reading":"しゅうじ","meaning":"calligraphy"}
    ]},
    "練": {"on": ["レン"], "kun": ["ね.る"], "meaning": "practice, train", "compounds": [
        {"word":"練習","reading":"れんしゅう","meaning":"practice"},
        {"word":"訓練","reading":"くんれん","meaning":"training"},
        {"word":"熟練","reading":"じゅくれん","meaning":"skilled"},
        {"word":"試練","reading":"しれん","meaning":"trial"},
        {"word":"鍛練","reading":"たんれん","meaning":"tempering"},
        {"word":"練る","reading":"ねる","meaning":"to knead, to refine"}
    ]},
    "試": {"on": ["シ"], "kun": ["こころ.みる","ため.す"], "meaning": "test, try", "compounds": [
        {"word":"試験","reading":"しけん","meaning":"exam"},
        {"word":"試合","reading":"しあい","meaning":"match, game"},
        {"word":"試し","reading":"ためし","meaning":"trial"},
        {"word":"試食","reading":"ししょく","meaning":"tasting"},
        {"word":"試着","reading":"しちゃく","meaning":"trying on clothes"},
        {"word":"実験","reading":"じっけん","meaning":"experiment"},
        {"word":"面接","reading":"めんせつ","meaning":"interview"}
    ]},
    "験": {"on": ["ケン"], "kun": [], "meaning": "test, examine", "compounds": [
        {"word":"試験","reading":"しけん","meaning":"exam"},
        {"word":"経験","reading":"けいけん","meaning":"experience"},
        {"word":"実験","reading":"じっけん","meaning":"experiment"},
        {"word":"受験","reading":"じゅけん","meaning":"taking an exam"},
        {"word":"体験","reading":"たいけん","meaning":"experience"},
        {"word":"検証","reading":"けんしょう","meaning":"verification"},
        {"word":"予備試験","reading":"よびしけん","meaning":"preliminary exam"}
    ]},
    "問": {"on": ["モン"], "kun": ["と.う"], "meaning": "ask, question", "compounds": [
        {"word":"問題","reading":"もんだい","meaning":"problem, question"},
        {"word":"質問","reading":"しつもん","meaning":"question"},
        {"word":"訪問","reading":"ほうもん","meaning":"visit"},
        {"word":"疑問","reading":"ぎもん","meaning":"doubt"},
        {"word":"問い","reading":"とい","meaning":"question"},
        {"word":"学問","reading":"がくもん","meaning":"scholarship"},
        {"word":"問答","reading":"もんどう","meaning":"questions and answers"}
    ]},
    "答": {"on": ["トウ"], "kun": ["こた.える"], "meaning": "answer", "compounds": [
        {"word":"答える","reading":"こたえる","meaning":"to answer"},
        {"word":"答え","reading":"こたえ","meaning":"answer"},
        {"word":"回答","reading":"かいとう","meaning":"reply"},
        {"word":"解答","reading":"かいとう","meaning":"solution"},
        {"word":"答案","reading":"とうあん","meaning":"answer sheet"},
        {"word":"応答","reading":"おうとう","meaning":"response"},
        {"word":"正答","reading":"せいとう","meaning":"correct answer"}
    ]},
    "説": {"on": ["セツ","ゼイ"], "kun": ["と.く"], "meaning": "explain, theory", "compounds": [
        {"word":"説明","reading":"せつめい","meaning":"explanation"},
        {"word":"小説","reading":"しょうせつ","meaning":"novel"},
        {"word":"理論","reading":"りろん","meaning":"theory"},
        {"word":"演説","reading":"えんぜつ","meaning":"speech"},
        {"word":"解説","reading":"かいせつ","meaning":"commentary"},
        {"word":"仮説","reading":"かせつ","meaning":"hypothesis"},
        {"word":"定説","reading":"ていせつ","meaning":"established theory"},
        {"word":"異説","reading":"いせつ","meaning":"different theory"}
    ]},
    "題": {"on": ["ダイ"], "kun": [], "meaning": "topic, title", "compounds": [
        {"word":"問題","reading":"もんだい","meaning":"problem"},
        {"word":"課題","reading":"かだい","meaning":"assignment"},
        {"word":"主題","reading":"しゅだい","meaning":"theme"},
        {"word":"話題","reading":"わだい","meaning":"topic"},
        {"word":"題名","reading":"だいめい","meaning":"title"},
        {"word":"出題","reading":"しゅつだい","meaning":"setting a question"},
        {"word":"難題","reading":"なんだい","meaning":"difficult problem"}
    ]},
    "質": {"on": ["シツ","シ"], "kun": [], "meaning": "quality, substance", "compounds": [
        {"word":"品質","reading":"ひんしつ","meaning":"quality"},
        {"word":"質量","reading":"しつりょう","meaning":"mass"},
        {"word":"物質","reading":"ぶっしつ","meaning":"matter"},
        {"word":"質問","reading":"しつもん","meaning":"question"},
        {"word":"素質","reading":"そしつ","meaning":"aptitude"},
        {"word":"本質","reading":"ほんしつ","meaning":"essence"},
        {"word":"実質","reading":"じっしつ","meaning":"substance"},
        {"word":"人質","reading":"ひとじち","meaning":"hostage"}
    ]},
    "量": {"on": ["リョウ"], "kun": [], "meaning": "quantity, amount", "compounds": [
        {"word":"量","reading":"りょう","meaning":"quantity"},
        {"word":"大量","reading":"たいりょう","meaning":"large quantity"},
        {"word":"少量","reading":"しょうりょう","meaning":"small quantity"},
        {"word":"数量","reading":"すうりょう","meaning":"quantity