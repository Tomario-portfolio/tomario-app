# ホテル・部屋の初期データ。
# app.py の seed_hotels_and_rooms() が、ここに定義したホテル・部屋のうちDBに無いものだけを追加する。

# 地方 → 都道府県（検索画面のプルダウンと、/api/hotels の region 絞り込みで使う）
REGIONS = {
    '北海道': ['北海道'],
    '東北': ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
    '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
    '中部': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
    '近畿': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
    '中国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
    '四国': ['徳島県', '香川県', '愛媛県', '高知県'],
    '九州・沖縄': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'],
}

# 部屋の種類ごとの部屋番号・定員・説明・画像。料金はホテルごとに HOTELS で指定する
ROOM_TYPES = [
    ('シングル', ['101', '102'], 1, '落ち着いた雰囲気のシングルルームです。',
     'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80'),
    ('ダブル', ['201', '202'], 2, 'ゆったりとしたダブルルームです。',
     'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80'),
    ('スイート', ['301'], 3, '豪華なスイートルームです。特別なひとときをお過ごしください。',
     'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80'),
]

# (ホテル名, 都道府県, 住所, 説明, (シングル, ダブル, スイートの1泊料金), 画像URL)
# 先頭の3件は以前からあるホテル。名前で既存のレコードと突き合わせるため、名前は変えないこと
# 画像は Wikimedia Commons のパブリックドメイン／CC0 の写真（クレジット表記は不要）。各行のコメントは元の画像ページ
# 画像URLは255文字以内にすること（hotels.image_url が VARCHAR(255) のため）
HOTELS = [
    ('丸の内グランドホテル', '東京都', '東京都千代田区丸の内1-1-1',
     '都心の主要駅から徒歩圏内、ビジネスにも観光にも便利なホテルです。', (8000, 12000, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a0/Exterior_-_Tokyo_Station_Marunouchi_Building_-_DSC09896.JPG/960px-Exterior_-_Tokyo_Station_Marunouchi_Building_-_DSC09896.JPG'),  # https://commons.wikimedia.org/wiki/File:Exterior_-_Tokyo_Station_Marunouchi_Building_-_DSC09896.JPG
    ('京都東山旅館', '京都府', '京都府京都市東山区清水1-1-1',
     '古都の風情を感じられる、落ち着いた雰囲気のホテルです。', (7500, 13000, 26000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/HigashiyamaStreets7226.jpg/960px-HigashiyamaStreets7226.jpg'),  # https://commons.wikimedia.org/wiki/File:HigashiyamaStreets7226.jpg
    ('なんばグランドホテル', '大阪府', '大阪府大阪市中央区難波1-1-1',
     '繁華街に近く、食とショッピングを楽しむのに最適なホテルです。', (7000, 11000, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8e/Osaka_Dotonbori_yoru_02.jpg/960px-Osaka_Dotonbori_yoru_02.jpg'),  # https://commons.wikimedia.org/wiki/File:Osaka_Dotonbori_yoru_02.jpg

    # 北海道
    ('札幌大通ホテル', '北海道', '北海道札幌市中央区大通西1-1-1',
     '大通公園に面し、すすきのや時計台へ歩いて行けるホテルです。', (7500, 11500, 23000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b4/Sapporo_TV_Tower_and_NHK_Sapporo_20150914.jpg/960px-Sapporo_TV_Tower_and_NHK_Sapporo_20150914.jpg'),  # https://commons.wikimedia.org/wiki/File:Sapporo_TV_Tower_and_NHK_Sapporo_20150914.jpg
    ('函館ベイサイドホテル', '北海道', '北海道函館市末広町1-1-1',
     '赤レンガ倉庫群に近く、港の夜景を楽しめるホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3c/Hakodate_dock_red_brick_warehouses_1.jpg/960px-Hakodate_dock_red_brick_warehouses_1.jpg'),  # https://commons.wikimedia.org/wiki/File:Hakodate_dock_red_brick_warehouses_1.jpg
    ('小樽運河の宿', '北海道', '北海道小樽市港町1-1-1',
     '小樽運河のほとりに建つ、レトロな街並みになじむ宿です。', (8000, 13000, 25000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Otaru_Canal_Center.jpg/960px-Otaru_Canal_Center.jpg'),  # https://commons.wikimedia.org/wiki/File:Otaru_Canal_Center.jpg

    # 東北
    ('青森ねぶたホテル', '青森県', '青森県青森市安方1-1-1',
     'ねぶたの家ワ・ラッセに近い、駅前のホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e7/2025_Aomori_Nebuta_Festival_float_6.jpg/960px-2025_Aomori_Nebuta_Festival_float_6.jpg'),  # https://commons.wikimedia.org/wiki/File:2025_Aomori_Nebuta_Festival_float_6.jpg
    ('盛岡城跡ホテル', '岩手県', '岩手県盛岡市内丸1-1-1',
     '盛岡城跡公園のそばで、静かに過ごせるホテルです。', (6000, 9500, 18000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5b/Cherry_tree_and_Mount_Iwate_in_spring_2025.jpg/960px-Cherry_tree_and_Mount_Iwate_in_spring_2025.jpg'),  # https://commons.wikimedia.org/wiki/File:Cherry_tree_and_Mount_Iwate_in_spring_2025.jpg
    ('仙台青葉ホテル', '宮城県', '宮城県仙台市青葉区中央1-1-1',
     '仙台駅から徒歩圏内、牛たんの名店にも近いホテルです。', (7000, 10500, 20000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/67/Sendai_city_-_Hirose_river_2005.jpg/960px-Sendai_city_-_Hirose_river_2005.jpg'),  # https://commons.wikimedia.org/wiki/File:Sendai_city_-_Hirose_river_2005.jpg
    ('秋田竿燈ホテル', '秋田県', '秋田県秋田市中通1-1-1',
     '竿燈まつりの会場に近い、駅前のホテルです。', (6000, 9500, 18000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/97/Kakunodate_street.JPG/960px-Kakunodate_street.JPG'),  # https://commons.wikimedia.org/wiki/File:Kakunodate_street.JPG
    ('山形蔵王温泉旅館', '山形県', '山形県山形市蔵王温泉1-1-1',
     '樹氷とスキーで知られる蔵王の温泉旅館です。', (8000, 13000, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d9/Zao_L.Okama.JPG/960px-Zao_L.Okama.JPG'),  # https://commons.wikimedia.org/wiki/File:Zao_L.Okama.JPG
    ('会津若松鶴ヶ城ホテル', '福島県', '福島県会津若松市追手町1-1-1',
     '鶴ヶ城を望む、城下町散策の拠点に便利なホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3a/Tsuruga_Castle_2007.jpg/960px-Tsuruga_Castle_2007.jpg'),  # https://commons.wikimedia.org/wiki/File:Tsuruga_Castle_2007.jpg

    # 関東
    ('水戸偕楽園ホテル', '茨城県', '茨城県水戸市常磐町1-1-1',
     '梅の名所・偕楽園に近いホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Kairakuen_lake_senba_2021.jpg/960px-Kairakuen_lake_senba_2021.jpg'),  # https://commons.wikimedia.org/wiki/File:Kairakuen_lake_senba_2021.jpg
    ('日光東照宮の宿', '栃木県', '栃木県日光市山内1-1-1',
     '世界遺産・日光の社寺へ歩いて行ける宿です。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9f/Nikk%C5%8D_T%C5%8Dsh%C5%8D-g%C5%AB_4.jpg/960px-Nikk%C5%8D_T%C5%8Dsh%C5%8D-g%C5%AB_4.jpg'),  # https://commons.wikimedia.org/wiki/File:Nikk%C5%8D_T%C5%8Dsh%C5%8D-g%C5%AB_4.jpg
    ('草津湯畑旅館', '群馬県', '群馬県吾妻郡草津町草津1-1-1',
     '湯畑を囲む温泉街の中心にある旅館です。', (9000, 14000, 27000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/af/251130_Yubatake%2C_Kusatsu_12.jpg/960px-251130_Yubatake%2C_Kusatsu_12.jpg'),  # https://commons.wikimedia.org/wiki/File:251130_Yubatake,_Kusatsu_12.jpg
    ('大宮氷川ホテル', '埼玉県', '埼玉県さいたま市大宮区高鼻町1-1-1',
     '氷川神社の参道に近く、都心へのアクセスも良いホテルです。', (7000, 10500, 20000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/8/87/Hikawa_Jinja_Ninotorii_110221.jpg/960px-Hikawa_Jinja_Ninotorii_110221.jpg'),  # https://commons.wikimedia.org/wiki/File:Hikawa_Jinja_Ninotorii_110221.jpg
    ('幕張ベイホテル', '千葉県', '千葉県千葉市美浜区中瀬1-1-1',
     '幕張メッセや海浜公園に近いホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f9/Chiba_Port_Tower_%2829395363324%29.jpg/960px-Chiba_Port_Tower_%2829395363324%29.jpg'),  # https://commons.wikimedia.org/wiki/File:Chiba_Port_Tower_(29395363324).jpg
    ('新宿パークホテル', '東京都', '東京都新宿区西新宿1-1-1',
     '新宿駅西口から徒歩圏内、高層階から都心の夜景を望めるホテルです。', (9000, 14000, 28000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/Skyscrapers_Shinjuku_2007_rev.jpg/960px-Skyscrapers_Shinjuku_2007_rev.jpg'),  # https://commons.wikimedia.org/wiki/File:Skyscrapers_Shinjuku_2007_rev.jpg
    ('浅草雷門ホテル', '東京都', '東京都台東区浅草1-1-1',
     '雷門・仲見世通りまで歩いてすぐ、下町情緒を楽しめるホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f2/Kaminarimon_%28outer_gate%29%2C_Sensoji_Temple%2C_Akakusa%2C_Tokyo.jpg/960px-Kaminarimon_%28outer_gate%29%2C_Sensoji_Temple%2C_Akakusa%2C_Tokyo.jpg'),  # https://commons.wikimedia.org/wiki/File:Kaminarimon_(outer_gate),_Sensoji_Temple,_Akakusa,_Tokyo.jpg
    ('横浜みなとみらいホテル', '神奈川県', '神奈川県横浜市西区みなとみらい1-1-1',
     '港の景色と赤レンガ倉庫を楽しめるホテルです。', (9000, 14000, 28000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c7/Night_view_of_Yokohama_Minatomirai_21_from_Zou-no-hana_Park%EF%BC%881%EF%BC%89.jpg/960px-Night_view_of_Yokohama_Minatomirai_21_from_Zou-no-hana_Park%EF%BC%881%EF%BC%89.jpg'),  # https://commons.wikimedia.org/wiki/File:Night_view_of_Yokohama_Minatomirai_21_from_Zou-no-hana_Park%EF%BC%881%EF%BC%89.jpg

    # 中部
    ('新潟万代ホテル', '新潟県', '新潟県新潟市中央区万代1-1-1',
     '信濃川に近く、日本酒と海の幸を楽しめるホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Bandai_Bridge_20250612_184846.jpg/960px-Bandai_Bridge_20250612_184846.jpg'),  # https://commons.wikimedia.org/wiki/File:Bandai_Bridge_20250612_184846.jpg
    ('富山立山ホテル', '富山県', '富山県富山市桜町1-1-1',
     '立山連峰を望む、富山駅前のホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f2/Tateyama_Mountains_and_Mount_Anbo_from_Mount_Ibushi.jpg/960px-Tateyama_Mountains_and_Mount_Anbo_from_Mount_Ibushi.jpg'),  # https://commons.wikimedia.org/wiki/File:Tateyama_Mountains_and_Mount_Anbo_from_Mount_Ibushi.jpg
    ('金沢兼六ホテル', '石川県', '石川県金沢市兼六町1-1-1',
     '兼六園やひがし茶屋街の散策に便利なホテルです。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/20190705_Kenroku-en-7.jpg/960px-20190705_Kenroku-en-7.jpg'),  # https://commons.wikimedia.org/wiki/File:20190705_Kenroku-en-7.jpg
    ('福井恐竜の里ホテル', '福井県', '福井県福井市中央1-1-1',
     '恐竜博物館への観光拠点になる駅前のホテルです。', (6000, 9500, 18000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d3/Tojinbo_2010_05.jpg/960px-Tojinbo_2010_05.jpg'),  # https://commons.wikimedia.org/wiki/File:Tojinbo_2010_05.jpg
    ('河口湖富士ビューホテル', '山梨県', '山梨県南都留郡富士河口湖町船津1-1-1',
     '河口湖越しに富士山を望めるホテルです。', (9000, 14500, 28000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/2/24/Fuji_Kawaguchi_452.JPG/960px-Fuji_Kawaguchi_452.JPG'),  # https://commons.wikimedia.org/wiki/File:Fuji_Kawaguchi_452.JPG
    ('松本城下ホテル', '長野県', '長野県松本市丸の内1-1-1',
     '国宝・松本城に近い、城下町のホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f5/20190706_Matsumoto_Castle-8.jpg/960px-20190706_Matsumoto_Castle-8.jpg'),  # https://commons.wikimedia.org/wiki/File:20190706_Matsumoto_Castle-8.jpg
    ('飛騨高山古い町並みの宿', '岐阜県', '岐阜県高山市上三之町1-1-1',
     '古い町並みに溶け込む、飛騨高山の宿です。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fa/Looking_down_Kamisannomachi%2C_Takayama%2C_2016.jpg/960px-Looking_down_Kamisannomachi%2C_Takayama%2C_2016.jpg'),  # https://commons.wikimedia.org/wiki/File:Looking_down_Kamisannomachi,_Takayama,_2016.jpg
    ('熱海オーシャンホテル', '静岡県', '静岡県熱海市東海岸町1-1-1',
     '相模湾を望む、温泉付きのリゾートホテルです。', (9000, 14000, 27000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/62/Panorama_from_Atami_Castle.jpg/960px-Panorama_from_Atami_Castle.jpg'),  # https://commons.wikimedia.org/wiki/File:Panorama_from_Atami_Castle.jpg
    ('名古屋駅前グランドホテル', '愛知県', '愛知県名古屋市中村区名駅1-1-1',
     '名古屋駅から徒歩すぐ、出張にも観光にも便利なホテルです。', (8000, 12000, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3f/Nagoya_Station_JR_Central_Towers_and_JR_Gate_Tower.jpg/960px-Nagoya_Station_JR_Central_Towers_and_JR_Gate_Tower.jpg'),  # https://commons.wikimedia.org/wiki/File:Nagoya_Station_JR_Central_Towers_and_JR_Gate_Tower.jpg
    ('名古屋栄ホテル', '愛知県', '愛知県名古屋市中区栄1-1-1',
     'テレビ塔や大須商店街に近い、繁華街のホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/65/Nagoya_TV_Tower_%E5%90%8D%E5%8F%A4%E5%B1%8B%E3%83%86%E3%83%AC%E3%83%93%E5%A1%94_2021-12-04.jpg/960px-Nagoya_TV_Tower_%E5%90%8D%E5%8F%A4%E5%B1%8B%E3%83%86%E3%83%AC%E3%83%93%E5%A1%94_2021-12-04.jpg'),  # https://commons.wikimedia.org/wiki/File:Nagoya_TV_Tower_%E5%90%8D%E5%8F%A4%E5%B1%8B%E3%83%86%E3%83%AC%E3%83%93%E5%A1%94_2021-12-04.jpg
    ('名古屋城ホテル', '愛知県', '愛知県名古屋市中区三の丸1-1-1',
     '名古屋城を望む、落ち着いた環境のホテルです。', (8500, 13000, 25000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0f/Nagoya_Castle_%2875241%29.jpg/960px-Nagoya_Castle_%2875241%29.jpg'),  # https://commons.wikimedia.org/wiki/File:Nagoya_Castle_(75241).jpg

    # 近畿
    ('伊勢神宮おかげ横丁の宿', '三重県', '三重県伊勢市宇治中之切町1-1-1',
     '伊勢神宮・内宮とおかげ横丁へ歩いて行ける宿です。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/56/Ise_Mie_Okage_Yokocho_01.jpg/960px-Ise_Mie_Okage_Yokocho_01.jpg'),  # https://commons.wikimedia.org/wiki/File:Ise_Mie_Okage_Yokocho_01.jpg
    ('琵琶湖レイクホテル', '滋賀県', '滋賀県大津市浜大津1-1-1',
     '琵琶湖の湖畔に建つ、眺めの良いホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8a/Lake_Biwa_from_Omimaiko_beach.jpg/960px-Lake_Biwa_from_Omimaiko_beach.jpg'),  # https://commons.wikimedia.org/wiki/File:Lake_Biwa_from_Omimaiko_beach.jpg
    ('嵐山渡月橋旅館', '京都府', '京都府京都市右京区嵯峨天龍寺1-1-1',
     '渡月橋と竹林の小径に近い、四季の景色を楽しめる旅館です。', (9000, 15000, 30000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c2/Arashiyama%2C_Part_II_-_Arashiyama7534.jpg/960px-Arashiyama%2C_Part_II_-_Arashiyama7534.jpg'),  # https://commons.wikimedia.org/wiki/File:Arashiyama,_Part_II_-_Arashiyama7534.jpg
    ('京都駅前ホテル', '京都府', '京都府京都市下京区東塩小路町1-1-1',
     '京都駅から徒歩すぐ、市内観光の拠点に便利なホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/94/Nidec_Kyoto_Tower_2024-08.jpg/960px-Nidec_Kyoto_Tower_2024-08.jpg'),  # https://commons.wikimedia.org/wiki/File:Nidec_Kyoto_Tower_2024-08.jpg
    ('梅田スカイホテル', '大阪府', '大阪府大阪市北区梅田1-1-1',
     '大阪駅・梅田駅から徒歩圏内、ビジネスにも便利なホテルです。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3f/Umeda_Sky_Buildng.jpg/960px-Umeda_Sky_Buildng.jpg'),  # https://commons.wikimedia.org/wiki/File:Umeda_Sky_Buildng.jpg
    ('大阪ベイリゾートホテル', '大阪府', '大阪府大阪市此花区桜島1-1-1',
     'テーマパークや海遊館へのアクセスが良いリゾートホテルです。', (9000, 14000, 28000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f4/Kaiy%C5%ABkan.jpg/960px-Kaiy%C5%ABkan.jpg'),  # https://commons.wikimedia.org/wiki/File:Kaiy%C5%ABkan.jpg
    ('神戸北野ホテル', '兵庫県', '兵庫県神戸市中央区北野町1-1-1',
     '異人館街と港の夜景を楽しめるホテルです。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/20190901_Kobe_Port_Tower_and_Maritime_Museum-1.jpg/960px-20190901_Kobe_Port_Tower_and_Maritime_Museum-1.jpg'),  # https://commons.wikimedia.org/wiki/File:20190901_Kobe_Port_Tower_and_Maritime_Museum-1.jpg
    ('奈良公園ホテル', '奈良県', '奈良県奈良市登大路町1-1-1',
     '鹿の遊ぶ奈良公園や東大寺に近いホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/92/20190121_Nara_deer-1.jpg/960px-20190121_Nara_deer-1.jpg'),  # https://commons.wikimedia.org/wiki/File:20190121_Nara_deer-1.jpg
    ('白浜温泉リゾート', '和歌山県', '和歌山県西牟婁郡白浜町1-1-1',
     '白良浜を望む、温泉付きのリゾートホテルです。', (8500, 13500, 26000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e7/Shirahama_Beach_Feb2010.jpg/960px-Shirahama_Beach_Feb2010.jpg'),  # https://commons.wikimedia.org/wiki/File:Shirahama_Beach_Feb2010.jpg

    # 中国
    ('鳥取砂丘ホテル', '鳥取県', '鳥取県鳥取市福部町湯山1-1-1',
     '鳥取砂丘の観光に便利なホテルです。', (6000, 9500, 18000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f1/Tottori_Sand_Dunes.jpg/960px-Tottori_Sand_Dunes.jpg'),  # https://commons.wikimedia.org/wiki/File:Tottori_Sand_Dunes.jpg
    ('出雲大社門前の宿', '島根県', '島根県出雲市大社町杵築東1-1-1',
     '出雲大社の門前町にある宿です。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1c/Haiden_of_Izumo-taisha-1.JPG/960px-Haiden_of_Izumo-taisha-1.JPG'),  # https://commons.wikimedia.org/wiki/File:Haiden_of_Izumo-taisha-1.JPG
    ('倉敷美観地区ホテル', '岡山県', '岡山県倉敷市本町1-1-1',
     '白壁の町並みが続く倉敷美観地区のホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/65/Kurashiki_bikatiku_naka-bashi.JPG/960px-Kurashiki_bikatiku_naka-bashi.JPG'),  # https://commons.wikimedia.org/wiki/File:Kurashiki_bikatiku_naka-bashi.JPG
    ('広島平和公園ホテル', '広島県', '広島県広島市中区中島町1-1-1',
     '平和記念公園に近く、宮島への観光にも便利なホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/db/20181111_Itsukushima_Shrine_torii-2.jpg/960px-20181111_Itsukushima_Shrine_torii-2.jpg'),  # https://commons.wikimedia.org/wiki/File:20181111_Itsukushima_Shrine_torii-2.jpg
    ('下関海峡ホテル', '山口県', '山口県下関市唐戸町1-1-1',
     '関門海峡を望み、ふぐ料理も楽しめるホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f6/Shimonoseki_Cannons.JPG/960px-Shimonoseki_Cannons.JPG'),  # https://commons.wikimedia.org/wiki/File:Shimonoseki_Cannons.JPG

    # 四国
    ('徳島眉山ホテル', '徳島県', '徳島県徳島市新町1-1-1',
     '阿波おどり会館と眉山に近いホテルです。', (6000, 9500, 18000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/57/JMSDF_Awa_Odori_%288551282%29.jpg/960px-JMSDF_Awa_Odori_%288551282%29.jpg'),  # https://commons.wikimedia.org/wiki/File:JMSDF_Awa_Odori_(8551282).jpg
    ('高松うどん街道ホテル', '香川県', '香川県高松市サンポート1-1-1',
     '高松港に面し、讃岐うどん巡りの拠点になるホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/55/Ritsurin-Garden-M3566.jpg/960px-Ritsurin-Garden-M3566.jpg'),  # https://commons.wikimedia.org/wiki/File:Ritsurin-Garden-M3566.jpg
    ('道後温泉旅館', '愛媛県', '愛媛県松山市道後湯之町1-1-1',
     '道後温泉本館まで歩いてすぐの旅館です。', (8000, 12500, 24000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9a/Dogo_Onsen_01.jpg/960px-Dogo_Onsen_01.jpg'),  # https://commons.wikimedia.org/wiki/File:Dogo_Onsen_01.jpg
    ('高知はりまや橋ホテル', '高知県', '高知県高知市はりまや町1-1-1',
     'はりまや橋とひろめ市場に近いホテルです。', (6500, 10000, 19000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/94/Kochi_Castle%2C_enkei.jpg/960px-Kochi_Castle%2C_enkei.jpg'),  # https://commons.wikimedia.org/wiki/File:Kochi_Castle,_enkei.jpg

    # 九州・沖縄
    ('博多中洲ホテル', '福岡県', '福岡県福岡市博多区中洲1-1-1',
     '屋台が並ぶ中洲に近く、博多グルメを楽しめるホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d7/Fukuoka-Nakagawa.jpg/960px-Fukuoka-Nakagawa.jpg'),  # https://commons.wikimedia.org/wiki/File:Fukuoka-Nakagawa.jpg
    ('嬉野温泉旅館', '佐賀県', '佐賀県嬉野市嬉野町下宿1-1-1',
     '美肌の湯として知られる嬉野温泉の旅館です。', (7500, 12000, 23000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c3/Takeo_Spa.JPG/960px-Takeo_Spa.JPG'),  # https://commons.wikimedia.org/wiki/File:Takeo_Spa.JPG
    ('長崎グラバー園ホテル', '長崎県', '長崎県長崎市南山手町1-1-1',
     'グラバー園と長崎港の夜景を楽しめるホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a4/Nagasaki-Glover-Garden-5415.jpg/960px-Nagasaki-Glover-Garden-5415.jpg'),  # https://commons.wikimedia.org/wiki/File:Nagasaki-Glover-Garden-5415.jpg
    ('熊本城下ホテル', '熊本県', '熊本県熊本市中央区本丸1-1-1',
     '熊本城を望む、城下町のホテルです。', (7000, 10500, 20000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5c/Kumamoto_Castle_20230227_05.jpg/960px-Kumamoto_Castle_20230227_05.jpg'),  # https://commons.wikimedia.org/wiki/File:Kumamoto_Castle_20230227_05.jpg
    ('別府湯けむり旅館', '大分県', '大分県別府市北浜1-1-1',
     '湯けむりが立ちのぼる別府温泉の旅館です。', (7500, 12000, 23000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Umi_Jigoku_%28Sea_Hell%29_in_Beppu.jpg/960px-Umi_Jigoku_%28Sea_Hell%29_in_Beppu.jpg'),  # https://commons.wikimedia.org/wiki/File:Umi_Jigoku_(Sea_Hell)_in_Beppu.jpg
    ('宮崎青島リゾート', '宮崎県', '宮崎県宮崎市青島1-1-1',
     '青島と日南海岸を望む、南国のリゾートホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/Aoshima_Miyazaki_Japan_2007_08.jpg/960px-Aoshima_Miyazaki_Japan_2007_08.jpg'),  # https://commons.wikimedia.org/wiki/File:Aoshima_Miyazaki_Japan_2007_08.jpg
    ('鹿児島桜島ビューホテル', '鹿児島県', '鹿児島県鹿児島市城山町1-1-1',
     '錦江湾越しに桜島を望めるホテルです。', (7000, 11000, 21000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/31/Sakurajima-2.jpg/960px-Sakurajima-2.jpg'),  # https://commons.wikimedia.org/wiki/File:Sakurajima-2.jpg
    ('那覇国際通りホテル', '沖縄県', '沖縄県那覇市松尾1-1-1',
     '国際通りに面し、首里城や市場へのアクセスも良いホテルです。', (7500, 11500, 22000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/63/Kokusai_Dori_01.JPG/960px-Kokusai_Dori_01.JPG'),  # https://commons.wikimedia.org/wiki/File:Kokusai_Dori_01.JPG
    ('恩納ビーチリゾート', '沖縄県', '沖縄県国頭郡恩納村恩納1-1-1',
     '目の前に広がる白い砂浜と青い海を楽しめるリゾートホテルです。', (12000, 18000, 36000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/16/Tancha_Beach_in_Onna%2C_-20_maart_2017%2C_18-00.jpg/960px-Tancha_Beach_in_Onna%2C_-20_maart_2017%2C_18-00.jpg'),  # https://commons.wikimedia.org/wiki/File:Tancha_Beach_in_Onna,_-20_maart_2017,_18-00.jpg
    ('石垣島サンセットホテル', '沖縄県', '沖縄県石垣市新栄町1-1-1',
     '夕日の名所に建つ、離島観光の拠点になるホテルです。', (9000, 14000, 27000),
     'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5d/Kabirawan.jpg/960px-Kabirawan.jpg'),  # https://commons.wikimedia.org/wiki/File:Kabirawan.jpg
]
