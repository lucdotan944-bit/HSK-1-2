"""
HSK 1 & 2 vocabulary data (HSK 3.0 standard)
with Vietnamese translations for Vietnamese learners
"""
import os
import re
import sqlite3
import json

_BULK_VOCAB_PATH = os.path.join(os.path.dirname(__file__), "data", "hsk_vocab_full.json")

HSK1_WORDS = [
    # Pronouns
    ("我", "wǒ", "tôi, mình", 1, "手"),
    ("你", "nǐ", "bạn, anh/chị", 1, "亻"),
    ("他", "tā", "anh ấy, cậu ấy", 1, "亻"),
    ("她", "tā", "cô ấy, chị ấy", 1, "女"),
    ("它", "tā", "nó (vật)", 1, "宀"),
    ("我们", "wǒ men", "chúng tôi, chúng ta", 1, "手"),
    ("你们", "nǐ men", "các bạn", 1, "亻"),
    ("他们", "tā men", "họ (nam)", 1, "亻"),
    ("大家", "dà jiā", "mọi người", 1, "大"),

    # Numbers
    ("一", "yī", "một", 1, "一"),
    ("二", "èr", "hai", 1, "二"),
    ("三", "sān", "ba", 1, "一"),
    ("四", "sì", "bốn", 1, "囗"),
    ("五", "wǔ", "năm", 1, "二"),
    ("六", "liù", "sáu", 1, "八"),
    ("七", "qī", "bảy", 1, "一"),
    ("八", "bā", "tám", 1, "八"),
    ("九", "jiǔ", "chín", 1, "丿"),
    ("十", "shí", "mười", 1, "十"),
    ("零", "líng", "số không", 1, "雨"),
    ("百", "bǎi", "trăm", 1, "白"),
    ("千", "qiān", "nghìn", 1, "十"),
    ("半", "bàn", "một nửa", 1, "十"),
    ("几", "jǐ", "mấy, vài", 1, "几"),
    ("多少", "duō shǎo", "bao nhiêu", 1, "大"),
    ("很多", "hěn duō", "rất nhiều", 1, "彳"),

    # Basic verbs
    ("是", "shì", "là, phải", 1, "日"),
    ("有", "yǒu", "có", 1, "月"),
    ("在", "zài", "ở, đang", 1, "土"),
    ("吃", "chī", "ăn", 1, "口"),
    ("喝", "hē", "uống", 1, "口"),
    ("看", "kàn", "xem, nhìn", 1, "目"),
    ("听", "tīng", "nghe", 1, "口"),
    ("说", "shuō", "nói", 1, "讠"),
    ("读", "dú", "đọc", 1, "讠"),
    ("写", "xiě", "viết", 1, "冖"),
    ("去", "qù", "đi (đến)", 1, "厶"),
    ("来", "lái", "đến, lại", 1, "来"),
    ("做", "zuò", "làm", 1, "亻"),
    ("买", "mǎi", "mua", 1, "乙"),
    ("卖", "mài", "bán", 1, "十"),
    ("叫", "jiào", "gọi, tên là", 1, "口"),
    ("会", "huì", "biết, sẽ", 1, "人"),
    ("能", "néng", "có thể", 1, "月"),
    ("想", "xiǎng", "muốn, nghĩ", 1, "心"),
    ("要", "yào", "muốn, cần", 1, "覀"),
    ("喜欢", "xǐ huān", "thích", 1, "口"),
    ("爱", "ài", "yêu", 1, "爫"),
    ("学习", "xué xí", "học tập", 1, "子"),
    ("工作", "gōng zuò", "làm việc", 1, "工"),
    ("睡觉", "shuì jiào", "ngủ", 1, "目"),
    ("起床", "qǐ chuáng", "thức dậy", 1, "走"),
    ("上课", "shàng kè", "lên lớp", 1, "一"),
    ("回家", "huí jiā", "về nhà", 1, "囗"),
    ("知道", "zhī dào", "biết", 1, "矢"),
    ("认识", "rèn shi", "quen biết", 1, "讠"),

    # Nouns
    ("人", "rén", "người", 1, "人"),
    ("男人", "nán rén", "đàn ông", 1, "田"),
    ("女人", "nǚ rén", "phụ nữ", 1, "女"),
    ("孩子", "hái zi", "đứa trẻ", 1, "子"),
    ("朋友", "péng you", "bạn bè", 1, "月"),
    ("名字", "míng zi", "tên", 1, "口"),
    ("水", "shuǐ", "nước", 1, "水"),
    ("茶", "chá", "trà", 1, "艹"),
    ("咖啡", "kā fēi", "cà phê", 1, "口"),
    ("米饭", "mǐ fàn", "cơm", 1, "米"),
    ("菜", "cài", "rau, món ăn", 1, "艹"),
    ("水果", "shuǐ guǒ", "trái cây", 1, "水"),
    ("书", "shū", "sách", 1, "乙"),
    ("书包", "shū bāo", "cặp sách", 1, "乙"),
    ("笔", "bǐ", "bút", 1, "竹"),
    ("桌子", "zhuō zi", "cái bàn", 1, "木"),
    ("椅子", "yǐ zi", "cái ghế", 1, "木"),
    ("房间", "fáng jiān", "căn phòng", 1, "户"),
    ("学校", "xué xiào", "trường học", 1, "子"),
    ("医院", "yī yuàn", "bệnh viện", 1, "匚"),
    ("商店", "shāng diàn", "cửa hàng", 1, "口"),
    ("家", "jiā", "nhà, gia đình", 1, "宀"),
    ("钱", "qián", "tiền", 1, "金"),
    ("时间", "shí jiān", "thời gian", 1, "日"),
    ("今天", "jīn tiān", "hôm nay", 1, "人"),
    ("明天", "míng tiān", "ngày mai", 1, "日"),
    ("昨天", "zuó tiān", "hôm qua", 1, "日"),
    ("早上", "zǎo shang", "buổi sáng", 1, "日"),
    ("中午", "zhōng wǔ", "buổi trưa", 1, "丨"),
    ("晚上", "wǎn shang", "buổi tối", 1, "日"),
    ("现在", "xiàn zài", "bây giờ", 1, "王"),
    ("星期", "xīng qī", "tuần", 1, "日"),
    ("年", "nián", "năm", 1, "干"),
    ("月", "yuè", "tháng", 1, "月"),
    ("日", "rì", "ngày", 1, "日"),
    ("号", "hào", "ngày (trong tháng)", 1, "口"),
    ("点", "diǎn", "giờ", 1, "火"),
    ("分钟", "fēn zhōng", "phút", 1, "刀"),
    ("衣服", "yī fu", "quần áo", 1, "衣"),
    ("天气", "tiān qì", "thời tiết", 1, "大"),
    ("汉语", "hàn yǔ", "tiếng Trung", 1, "氵"),
    ("中文", "zhōng wén", "tiếng Trung (văn viết)", 1, "丨"),

    # Adjectives
    ("好", "hǎo", "tốt, ngon", 1, "女"),
    ("大", "dà", "to, lớn", 1, "大"),
    ("小", "xiǎo", "nhỏ, bé", 1, "小"),
    ("多", "duō", "nhiều", 1, "大"),
    ("少", "shǎo", "ít", 1, "小"),
    ("高", "gāo", "cao", 1, "高"),
    ("矮", "ǎi", "thấp", 1, "矢"),
    ("冷", "lěng", "lạnh", 1, "冫"),
    ("热", "rè", "nóng", 1, "灬"),
    ("漂亮", "piào liang", "đẹp", 1, "示"),
    ("好看", "hǎo kàn", "đẹp mắt", 1, "女"),
    ("快乐", "kuài lè", "vui vẻ", 1, "忄"),
    ("高兴", "gāo xìng", "vui mừng", 1, "高"),
    ("忙", "máng", "bận", 1, "忄"),
    ("累", "lèi", "mệt", 1, "糸"),
    ("饿", "è", "đói", 1, "饣"),
    ("渴", "kě", "khát", 1, "氵"),
    ("对", "duì", "đúng", 1, "寸"),
    ("错", "cuò", "sai", 1, "金"),
    ("新", "xīn", "mới", 1, "斤"),
    ("老", "lǎo", "già, cũ", 1, "老"),

    # Question words & Particles
    ("什么", "shén me", "cái gì", 1, "亻"),
    ("谁", "shéi", "ai", 1, "讠"),
    ("哪里", "nǎ lǐ", "ở đâu", 1, "口"),
    ("怎么", "zěn me", "thế nào, làm sao", 1, "心"),
    ("为什么", "wèi shén me", "tại sao", 1, "丶"),
    ("什么时候", "shén me shí hou", "khi nào, lúc nào", 1, "亻"),
    ("的", "de", "của (trợ từ)", 1, "白"),
    ("了", "le", "rồi (trợ từ)", 1, "乙"),
    ("吗", "ma", "phải không? (trợ từ)", 1, "口"),
    ("呢", "ne", "thì sao? (trợ từ)", 1, "口"),
    ("不", "bù", "không", 1, "一"),
    ("很", "hěn", "rất", 1, "彳"),
    ("也", "yě", "cũng", 1, "乙"),
    ("都", "dōu", "đều", 1, "阝"),
    ("和", "hé", "và, với", 1, "口"),
    ("还", "hái", "còn, vẫn", 1, "辶"),
    ("太", "tài", "quá", 1, "大"),
    ("最", "zuì", "nhất", 1, "曰"),
    ("真", "zhēn", "thật", 1, "目"),
    ("请", "qǐng", "mời, xin", 1, "讠"),
    ("谢谢", "xiè xie", "cảm ơn", 1, "讠"),
    ("不客气", "bú kè qi", "không có gì, đừng khách sáo", 1, "一"),
    ("对不起", "duì bu qǐ", "xin lỗi", 1, "寸"),
    ("没关系", "méi guān xi", "không sao", 1, "氵"),
    ("再见", "zài jiàn", "tạm biệt", 1, "冂"),
    ("可以", "kě yǐ", "có thể, được", 1, "口"),
    ("但是", "dàn shì", "nhưng", 1, "亻"),
    ("非常", "fēi cháng", "rất, vô cùng", 1, "非"),
    ("一共", "yí gòng", "tổng cộng", 1, "一"),
    
    # Colors
    ("红色", "hóng sè", "màu đỏ", 1, "纟"),
    ("白色", "bái sè", "màu trắng", 1, "白"),
    ("黑色", "hēi sè", "màu đen", 1, "黑"),
    ("蓝色", "lán sè", "màu xanh lam", 1, "艹"),
    ("绿色", "lǜ sè", "màu xanh lá", 1, "纟"),
    ("黄色", "huáng sè", "màu vàng", 1, "黄"),
]

HSK2_WORDS = [
    # More verbs
    ("帮助", "bāng zhù", "giúp đỡ", 2, "巾"),
    ("变成", "biàn chéng", "trở thành", 2, "又"),
    ("出现", "chū xiàn", "xuất hiện", 2, "凵"),
    ("打扫", "dǎ sǎo", "quét dọn", 2, "扌"),
    ("打算", "dǎ suàn", "dự định", 2, "扌"),
    ("带", "dài", "mang, đem", 2, "巾"),
    ("担心", "dān xīn", "lo lắng", 2, "扌"),
    ("发现", "fā xiàn", "phát hiện", 2, "又"),
    ("告诉", "gào su", "nói cho", 2, "口"),
    ("害怕", "hài pà", "sợ hãi", 2, "宀"),
    ("检查", "jiǎn chá", "kiểm tra", 2, "木"),
    ("教", "jiāo", "dạy", 2, "攵"),
    ("决定", "jué dìng", "quyết định", 2, "冫"),
    ("开", "kāi", "mở, lái (xe)", 2, "廾"),
    ("开始", "kāi shǐ", "bắt đầu", 2, "廾"),
    ("哭", "kū", "khóc", 2, "口"),
    ("离开", "lí kāi", "rời khỏi", 2, "亠"),
    ("练习", "liàn xí", "luyện tập", 2, "纟"),
    ("旅行", "lǚ xíng", "du lịch", 2, "方"),
    ("拿", "ná", "cầm, lấy", 2, "手"),
    ("跑步", "pǎo bù", "chạy bộ", 2, "足"),
    ("请客", "qǐng kè", "mời khách, chiêu đãi", 2, "讠"),
    ("让", "ràng", "để cho, nhường", 2, "讠"),
    ("送", "sòng", "tặng, tiễn", 2, "辶"),
    ("踢足球", "tī zú qiú", "đá bóng", 2, "足"),
    ("游泳", "yóu yǒng", "bơi", 2, "氵"),
    ("用完", "yòng wán", "dùng hết", 2, "用"),
    ("遇到", "yù dào", "gặp phải", 2, "辶"),
    ("愿意", "yuàn yì", "sẵn lòng", 2, "心"),
    ("掉", "diào", "rơi, mất", 2, "扌"),

    # More nouns
    ("办公室", "bàn gōng shì", "văn phòng", 2, "力"),
    ("报纸", "bào zhǐ", "báo", 2, "扌"),
    ("词典", "cí diǎn", "từ điển", 2, "讠"),
    ("答案", "dá àn", "đáp án", 2, "竹"),
    ("蛋糕", "dàn gāo", "bánh ngọt", 2, "米"),
    ("地方", "dì fang", "nơi, địa phương", 2, "土"),
    ("电话", "diàn huà", "điện thoại", 2, "田"),
    ("电脑", "diàn nǎo", "máy tính", 2, "田"),
    ("电影", "diàn yǐng", "phim ảnh", 2, "田"),
    ("动物园", "dòng wù yuán", "sở thú", 2, "力"),
    ("风俗", "fēng sú", "phong tục", 2, "风"),
    ("公司", "gōng sī", "công ty", 2, "八"),
    ("公园", "gōng yuán", "công viên", 2, "八"),
    ("故事", "gù shi", "câu chuyện", 2, "攵"),
    ("顾客", "gù kè", "khách hàng", 2, "页"),
    ("关系", "guān xi", "quan hệ", 2, "丷"),
    ("国家", "guó jiā", "đất nước", 2, "囗"),
    ("海滩", "hǎi tān", "bãi biển", 2, "氵"),
    ("黑板", "hēi bǎn", "bảng đen", 2, "黑"),
    ("机场", "jī chǎng", "sân bay", 2, "木"),
    ("机会", "jī huì", "cơ hội", 2, "木"),
    ("礼物", "lǐ wù", "quà tặng", 2, "礻"),
    ("邻居", "lín jū", "hàng xóm", 2, "阝"),
    ("门", "mén", "cửa", 2, "门"),
    ("密码", "mì mǎ", "mật mã", 2, "宀"),
    ("内容", "nèi róng", "nội dung", 2, "冂"),
    ("年级", "nián jí", "khối lớp", 2, "干"),
    ("牛奶", "niú nǎi", "sữa bò", 2, "牛"),
    ("妻子", "qī zi", "vợ", 2, "女"),
    ("身体", "shēn tǐ", "cơ thể", 2, "身"),
    ("生日", "shēng rì", "sinh nhật", 2, "生"),
    ("声音", "shēng yīn", "âm thanh", 2, "士"),
    ("世界", "shì jiè", "thế giới", 2, "一"),
    ("手机", "shǒu jī", "điện thoại di động", 2, "手"),
    ("数字", "shù zì", "chữ số", 2, "攵"),
    ("太阳", "tài yáng", "mặt trời", 2, "大"),
    ("图书馆", "tú shū guǎn", "thư viện", 2, "囗"),
    ("外国人", "wài guó rén", "người nước ngoài", 2, "夕"),
    ("晚饭", "wǎn fàn", "bữa tối", 2, "日"),
    ("网站", "wǎng zhàn", "trang web", 2, "冂"),
    ("微信", "wēi xìn", "WeChat", 2, "彳"),
    ("问题", "wèn tí", "vấn đề, câu hỏi", 2, "门"),
    ("习惯", "xí guàn", "thói quen", 2, "乙"),
    ("小心", "xiǎo xīn", "cẩn thận", 2, "小"),
    ("笑话", "xiào hua", "chuyện cười", 2, "竹"),
    ("信息", "xìn xī", "tin tức, thông tin", 2, "亻"),
    ("眼睛", "yǎn jīng", "mắt", 2, "目"),
    ("颜色", "yán sè", "màu sắc", 2, "页"),
    ("钥匙", "yào shi", "chìa khóa", 2, "金"),
    ("意思", "yì si", "ý nghĩa", 2, "心"),
    ("因为", "yīn wèi", "bởi vì", 2, "囗"),
    ("音乐", "yīn yuè", "âm nhạc", 2, "音"),
    ("时候", "shí hou", "lúc, thời điểm", 2, "日"),
    ("知识", "zhī shi", "kiến thức", 2, "矢"),
    ("中间", "zhōng jiān", "ở giữa", 2, "丨"),

    # More adjectives
    ("安静", "ān jìng", "yên tĩnh", 2, "宀"),
    ("保护", "bǎo hù", "bảo vệ", 2, "亻"),
    ("方便", "fāng biàn", "tiện lợi", 2, "方"),
    ("放心", "fàng xīn", "yên tâm", 2, "攵"),
    ("干净", "gān jìng", "sạch sẽ", 2, "干"),
    ("重要", "zhòng yào", "quan trọng", 2, "里"),
    ("着急", "zháo jí", "sốt ruột, lo lắng", 2, "目"),
    ("一样", "yí yàng", "giống nhau", 2, "一"),
    ("认真", "rèn zhēn", "nghiêm túc, chăm chỉ", 2, "讠"),
    ("清楚", "qīng chu", "rõ ràng", 2, "氵"),
    ("容易", "róng yì", "dễ dàng", 2, "宀"),
    ("舒服", "shū fu", "thoải mái, dễ chịu", 2, "舌"),
    ("危险", "wēi xiǎn", "nguy hiểm", 2, "卩"),
    ("有名", "yǒu míng", "nổi tiếng", 2, "月"),
    ("努力", "nǔ lì", "cố gắng", 2, "力"),

    # Conjunctions & Grammar
    ("不但", "bú dàn", "không những", 2, "一"),
    ("而且", "ér qiě", "mà còn", 2, "而"),
    ("或者", "huò zhě", "hoặc là", 2, "戈"),
    ("虽然", "suī rán", "mặc dù", 2, "口"),
    ("如果", "rú guǒ", "nếu như", 2, "女"),
    ("因为...所以", "yīn wèi...suǒ yǐ", "bởi vì...cho nên", 2, "囗"),
    ("然后", "rán hòu", "sau đó", 2, "灬"),
    ("已经", "yǐ jīng", "đã (xong)", 2, "己"),
    ("以前", "yǐ qián", "trước đây", 2, "己"),
    ("以后", "yǐ hòu", "sau này", 2, "己"),
    ("经常", "jīng cháng", "thường xuyên", 2, "纟"),
    ("总是", "zǒng shì", "luôn luôn", 2, "心"),
    ("特别", "tè bié", "đặc biệt", 2, "牛"),
    ("可能", "kě néng", "có thể", 2, "口"),
]

_bulk_words_cache = None

# Hand-curated Vietnamese meanings for bulk-imported words whose dictionary-derived
# meanings were wrong for learners: CC-CEDICT artifacts ("LT:個|个[ge4]", "biến thể
# của..."), sino-viet readings pasted as meanings ("ba ba", "kỵ xa"), slang/rare
# senses listed first (吧 "quán bar", 药 "lá của cây diên vĩ"), or missing the
# HSK-level sense entirely (着 the aspect particle, 重 "nặng"). First sense listed
# is always the one an HSK 1-2 learner needs. Applied on top of the JSON in
# load_bulk_words(), so regenerating data/hsk_vocab_full.json keeps these fixes.
MEANING_OVERRIDES = {
    # --- HSK 1 ---
    "爱好": "sở thích, yêu thích",
    "爸爸": "bố, ba, cha",
    "白": "trắng, màu trắng, sáng",
    "班": "lớp, lớp học, ca làm việc, tổ, nhóm",
    "吧": "nhé, nhỉ, đi (trợ từ cuối câu: đề nghị, phỏng đoán)",
    "帮": "giúp, giúp đỡ",
    "包": "túi, bao, gói, bọc",
    "包子": "bánh bao",
    "杯": "cốc, ly, chén (lượng từ đồ uống)",
    "北": "phía bắc, hướng bắc",
    "本": "quyển, cuốn (lượng từ cho sách vở), vốn, gốc",
    "别": "đừng, chớ, khác",
    "病": "bệnh, ốm, bị bệnh",
    "比": "so với, hơn (dùng trong câu so sánh), so sánh, tỉ số",
    "车": "xe, xe cộ",
    "差": "kém, tệ, thiếu, khác biệt",
    "床": "giường",
    "从": "từ (chỉ điểm xuất phát: 从…到…), theo",
    "次": "lần, lượt (lượng từ), thứ",
    "打": "đánh, đập, chơi (bóng), gọi (điện thoại)",
    "第": "thứ (tiền tố số thứ tự: 第一 thứ nhất)",
    "地": "trợ từ kết cấu (sau trạng ngữ, trước động từ), đất, mặt đất (dì)",
    "弟弟": "em trai",
    "电": "điện",
    "东": "phía đông, hướng đông",
    "东西": "đồ, đồ vật, thứ",
    "儿子": "con trai (con của mình)",
    "饭": "cơm, bữa cơm, bữa ăn",
    "分": "phút, điểm (số), xu, chia, phân chia",
    "干": "làm (gàn: 干活), khô (gān: 干净)",
    "歌": "bài hát",
    "哥哥": "anh trai",
    "个": "cái, chiếc (lượng từ thông dụng nhất)",
    "跟": "với, cùng, theo, gót chân",
    "关": "đóng, tắt, cửa ải",
    "关上": "đóng lại, tắt (đèn, cửa)",
    "国": "nước, quốc gia",
    "好玩儿": "vui, thú vị, hay ho",
    "后": "sau, phía sau",
    "后天": "ngày kia, ngày mốt",
    "花": "hoa, bông hoa, tiêu (tiền)",
    "回": "về, trở về, lần (lượng từ), trả lời",
    "鸡蛋": "trứng gà",
    "间": "gian, phòng, căn (lượng từ), giữa, khoảng",
    "教学楼": "tòa nhà học, giảng đường",
    "姐姐": "chị gái",
    "就": "thì, liền, ngay, chính là",
    "考": "thi, kiểm tra",
    "课": "bài học, tiết học, môn học",
    "口": "miệng, nhân khẩu (lượng từ cho người trong nhà)",
    "块": "đồng (tiền, khẩu ngữ: 三块钱), miếng, cục, tảng (lượng từ)",
    "老人": "người già, cụ già",
    "老师": "giáo viên, thầy giáo, cô giáo",
    "里": "trong, bên trong, dặm (500 mét)",
    "楼": "tòa nhà, lầu, tầng",
    "路": "đường, con đường, tuyến (xe)",
    "妈妈": "mẹ, má",
    "毛": "hào (1/10 tệ), lông, tóc",
    "没": "không, chưa (phủ định: 没有)",
    "没事儿": "không sao, không có gì, rảnh",
    "妹妹": "em gái",
    "们": "(hậu tố số nhiều: 我们 chúng tôi, 你们 các bạn)",
    "面条儿": "mì, mì sợi",
    "哪": "nào, cái nào, đâu",
    "那": "kia, đó, cái kia, vậy thì",
    "奶": "sữa, cho bú",
    "奶奶": "bà nội",
    "男孩儿": "bé trai, cậu bé",
    "男": "nam, đàn ông, con trai",
    "您": "ngài, ông, bà (cách gọi \"bạn\" kính trọng)",
    "女": "nữ, phụ nữ, con gái",
    "女儿": "con gái (con của mình)",
    "女孩儿": "bé gái, cô bé",
    "票": "vé, phiếu",
    "跑": "chạy, chạy trốn",
    "前天": "hôm kia (hai ngày trước)",
    "球": "quả bóng, bóng",
    "肉": "thịt",
    "山": "núi, ngọn núi",
    "商场": "trung tâm thương mại, cửa hàng bách hóa",
    "上": "trên, phía trên, lên, đi (học, làm: 上学, 上班), trước (上个月)",
    "生病": "bị ốm, bị bệnh",
    "生气": "tức giận, giận, cáu",
    "手": "tay, bàn tay",
    "树": "cây, cây cối",
    "岁": "tuổi (lượng từ chỉ tuổi: 五岁 5 tuổi)",
    "她们": "họ, các cô ấy (nữ)",
    "天": "ngày, trời, bầu trời",
    "同学": "bạn học, bạn cùng lớp",
    "先": "trước, trước tiên, đầu tiên",
    "先生": "ông, ngài, quý ông, chồng",
    "洗手间": "nhà vệ sinh, toilet",
    "笑": "cười, mỉm cười",
    "小孩儿": "trẻ con, đứa trẻ",
    "小姐": "cô, quý cô (xưng hô lịch sự)",
    "小朋友": "bạn nhỏ, các cháu (gọi trẻ em)",
    "小学生": "học sinh tiểu học",
    "星期天": "Chủ nhật",
    "行": "được, ổn (xíng: 行!), đi, hàng, dòng (háng)",
    "学生": "học sinh, sinh viên",
    "页": "trang (sách)",
    "一下儿": "một chút, một lát, thử xem (làm gì đó nhẹ nhàng, nhanh)",
    "一点儿": "một chút, một ít",
    "用": "dùng, sử dụng",
    "有的": "có (người, cái)..., một số",
    "右": "bên phải, phía phải",
    "雨": "mưa",
    "元": "tệ, đồng (đơn vị tiền: 十元 10 tệ), nguyên",
    "早": "sớm, buổi sáng",
    "早饭": "bữa sáng, cơm sáng",
    "再": "lại, lần nữa, rồi mới",
    "站": "đứng, trạm, bến, ga",
    "找": "tìm, tìm kiếm, trả lại (tiền thừa)",
    "这": "này, cái này",
    "着": "đang... (trợ từ chỉ trạng thái đang diễn ra: 坐着 đang ngồi)",
    "正": "đúng, chính, đang (正在)",
    "重": "nặng (zhòng), quan trọng, lặp lại (chóng)",
    "子": "con, hạt, (hậu tố danh từ: 桌子, 椅子)",
    "左": "bên trái, phía trái",
    "坐": "ngồi, đi (xe, tàu, máy bay: 坐车)",
    # --- HSK 2 ---
    "背": "cõng, đeo, vác (bēi), lưng, học thuộc lòng (bèi)",
    "笔记本": "sổ tay, vở ghi, máy tính xách tay (laptop)",
    "遍": "lần, lượt (lượng từ cho hành động trọn vẹn: 再说一遍), khắp",
    "草": "cỏ, bãi cỏ",
    "超市": "siêu thị",
    "船": "thuyền, tàu thủy",
    "词": "từ, từ ngữ",
    "蛋": "trứng",
    "道": "con đường, đạo lý, lượng từ (món ăn, đề bài, cánh cửa)",
    "灯": "đèn",
    "店": "cửa hàng, tiệm, quán",
    "队": "đội, hàng ngũ",
    "份": "phần, suất, bản (lượng từ: báo, quà, hồ sơ)",
    "干活儿": "làm việc, lao động",
    "公共汽车": "xe buýt",
    "公交车": "xe buýt",
    "狗": "chó, con chó",
    "海": "biển, đại dương",
    "河": "sông, con sông",
    "湖": "hồ",
    "画": "vẽ, bức tranh",
    "鸡": "gà, con gà",
    "加": "cộng, thêm, thêm vào",
    "假": "giả (jiǎ), kỳ nghỉ (jià: 放假)",
    "交": "nộp, giao, kết (bạn: 交朋友)",
    "脚": "bàn chân, chân",
    "街": "phố, đường phố",
    "节": "ngày lễ (节日), tiết (học), đốt, lượng từ (tiết học, toa tàu)",
    "借": "mượn, vay, cho mượn",
    "举": "giơ lên, nâng, nêu (ví dụ: 举例)",
    "句": "câu (lượng từ cho câu nói: 一句话)",
    "快点儿": "nhanh lên, mau lên",
    "脸": "mặt, khuôn mặt",
    "留": "ở lại, giữ lại, để lại (lời nhắn), du học (留学)",
    "留学生": "du học sinh",
    "老朋友": "bạn cũ, bạn lâu năm",
    "绿": "xanh lá cây, màu xanh lục",
    "猫": "mèo, con mèo",
    "米": "gạo, mét (đơn vị đo)",
    "鸟": "chim, con chim",
    "碰": "chạm, đụng, va, tình cờ gặp",
    "瓶": "chai, lọ, bình",
    "墙": "tường, bức tường",
    "骑车": "đi xe đạp, đạp xe",
    "人数": "số người",
    "生词": "từ mới",
    "市": "thành phố, chợ",
    "提": "xách, nêu ra, đề cập, nhắc đến",
    "腿": "chân, đùi",
    "碗": "bát, chén, lượng từ (một bát cơm: 一碗饭)",
    "万": "vạn, mười nghìn",
    "喂": "a lô (nghe điện thoại), này, cho ăn",
    "洗衣机": "máy giặt",
    "笑话儿": "chuyện cười, truyện cười",
    "鞋": "giày, đôi giày",
    "信": "thư, lá thư, tin, tin tưởng",
    "雪": "tuyết",
    "眼": "mắt, con mắt",
    "药": "thuốc, dược phẩm",
    "夜": "đêm, ban đêm",
    "音乐会": "buổi hòa nhạc",
    "有空儿": "rảnh, có thời gian rảnh",
    "鱼": "cá, con cá",
    "院": "sân, viện (bệnh viện, học viện)",
    "云": "mây, đám mây",
    "咱": "chúng ta, chúng mình (gồm cả người nghe)",
    "占": "chiếm, chiếm giữ",
    "纸": "giấy, tờ giấy",
    "字典": "từ điển",
    "座": "chỗ ngồi, tòa, ngọn, quả (lượng từ: núi, tòa nhà)",
}

# CC-CEDICT artifacts to strip from bulk meanings: measure-word refs ("LT:個|个[ge4]"),
# variant-of notes ("biến thể của 幫|帮[bang1]"), cross-references, and slang senses.
_SEG_DROP_PREFIXES = ("biến thể", "dùng trong", "viết tắt của", "xem ", "lt:", "lượng từ:")
_SEG_DROP_SUBSTRINGS = ("tiếng lóng", "dương vật", "mại dâm", "cắm sừng", "gái điếm")
_CJK_RE = re.compile(r"[一-鿿]")
_PINYIN_REF_RE = re.compile(r"\[[a-zA-Z0-9üū:·\- ]+\]")


def _split_top_level(text):
    """Split a CEDICT-style meanings string on commas that are outside parentheses."""
    segs, buf, depth = [], [], 0
    for ch in text:
        if ch in "(（":
            depth += 1
        elif ch in ")）":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            segs.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        segs.append("".join(buf).strip())
    return [s for s in segs if s]


def clean_bulk_meanings(meanings, sino_viet=""):
    """Strip dictionary artifacts from a bulk-imported meanings string and put
    plain senses before register-marked ("(văn học)...") ones. Returns "" if
    nothing survives — callers should then fall back (base word / sino_viet)."""
    plain, marked = [], []
    for seg in _split_top_level(meanings):
        low = seg.lower()
        if _CJK_RE.search(seg) or _PINYIN_REF_RE.search(seg):
            continue
        if low.startswith(_SEG_DROP_PREFIXES) or any(s in low for s in _SEG_DROP_SUBSTRINGS):
            continue
        (marked if seg.startswith("(") else plain).append(seg)
    seen, out = set(), []
    for seg in plain + marked:
        key = seg.lower()
        if key not in seen:
            seen.add(key)
            out.append(seg)
    return ", ".join(out[:5])


def _bulk_meanings(w, base_meanings):
    """Final meanings for one bulk word: hand override > cleaned > er-hua base >
    sino_viet > original with CJK/pinyin refs stripped."""
    simplified = w["simplified"]
    if simplified in MEANING_OVERRIDES:
        return MEANING_OVERRIDES[simplified]
    cleaned = clean_bulk_meanings(w["meanings"], w.get("sino_viet", ""))
    if cleaned:
        return cleaned
    if simplified.endswith("儿"):
        base = base_meanings.get(simplified[:-1])
        if base:
            return base
    return w.get("sino_viet") or _PINYIN_REF_RE.sub("", _CJK_RE.sub("", w["meanings"])).strip(" ,;|")


def load_bulk_words():
    """HSK 3-9 words (plus any HSK1/2 words beyond the hand-curated set below),
    generated offline by scripts/build_hsk_vocab.py from public HSK 3.0 word
    lists + Han-Viet/meaning dictionaries — see that script's docstring for
    sources. Already excludes anything duplicating HSK1_WORDS/HSK2_WORDS."""
    global _bulk_words_cache
    if _bulk_words_cache is None:
        if os.path.exists(_BULK_VOCAB_PATH):
            with open(_BULK_VOCAB_PATH, encoding="utf-8") as f:
                data = json.load(f)
            # First pass so er-hua words (面条儿) can fall back to their base
            # word's cleaned meaning (面条) in the second pass.
            base_meanings = {
                w["simplified"]: MEANING_OVERRIDES.get(w["simplified"])
                or clean_bulk_meanings(w["meanings"], w.get("sino_viet", ""))
                for w in data
            }
            _bulk_words_cache = [
                (w["simplified"], w["pinyin"], _bulk_meanings(w, base_meanings), w["hsk_level"], "")
                for w in data
            ]
        else:
            _bulk_words_cache = []
    return _bulk_words_cache

def get_words():
    return HSK1_WORDS + HSK2_WORDS + load_bulk_words()

def get_hsk1():
    return HSK1_WORDS

def get_hsk2():
    return HSK2_WORDS

# Example sentences: word -> [chinese_sentence, vietnamese_translation]
EXAMPLE_SENTENCES = {
    # Pronouns
    "我": ["我是越南人。", "Tôi là người Việt Nam."],
    "你": ["你叫什么名字？", "Bạn tên là gì?"],
    "他": ["他是我的同学。", "Anh ấy là bạn cùng lớp của tôi."],
    "她": ["她是老师。", "Cô ấy là giáo viên."],
    "它": ["它是一只猫。", "Nó là một con mèo."],
    "我们": ["我们去学校。", "Chúng tôi đi đến trường."],
    "你们": ["你们好！", "Các bạn khỏe không!"],
    "他们": ["他们是朋友。", "Họ là bạn bè."],
    "大家": ["大家好！", "Chào mọi người!"],

    # Numbers & Quantity
    "一": ["我有一个苹果。", "Tôi có một quả táo."],
    "二": ["我今年二十岁。", "Năm nay tôi hai mươi tuổi."],
    "三": ["我们有三本书。", "Chúng tôi có ba quyển sách."],
    "四": ["桌子上有四杯茶。", "Trên bàn có bốn tách trà."],
    "五": ["我买了五个面包。", "Tôi đã mua năm cái bánh mì."],
    "六": ["他有六个朋友。", "Anh ấy có sáu người bạn."],
    "七": ["现在七点了。", "Bây giờ là bảy giờ."],
    "八": ["我八点上班。", "Tôi đi làm lúc tám giờ."],
    "九": ["他九点睡觉。", "Anh ấy đi ngủ lúc chín giờ."],
    "十": ["十个人来了。", "Mười người đã đến."],
    "多少": ["这个多少钱？", "Cái này bao nhiêu tiền?"],
    "很多": ["教室里有很多学生。", "Trong lớp có rất nhiều học sinh."],

    # Basic Verbs
    "是": ["我是学生。", "Tôi là học sinh."],
    "有": ["我有一辆车。", "Tôi có một chiếc xe hơi."],
    "在": ["我在家。", "Tôi ở nhà."],
    "吃": ["我在吃饭。", "Tôi đang ăn cơm."],
    "喝": ["他想喝水。", "Anh ấy muốn uống nước."],
    "看": ["我在看电视。", "Tôi đang xem tivi."],
    "听": ["我喜欢听音乐。", "Tôi thích nghe nhạc."],
    "说": ["他会说中文。", "Anh ấy biết nói tiếng Trung."],
    "读": ["我在读书。", "Tôi đang đọc sách."],
    "写": ["她正在写字。", "Cô ấy đang viết chữ."],
    "去": ["我要去商店。", "Tôi muốn đi cửa hàng."],
    "来": ["他来了。", "Anh ấy đã đến."],
    "做": ["你在做什么？", "Bạn đang làm gì?"],
    "买": ["我想买这本书。", "Tôi muốn mua quyển sách này."],
    "卖": ["这家店卖水果。", "Cửa hàng này bán trái cây."],
    "叫": ["我叫小明。", "Tôi tên là Tiểu Minh."],
    "会": ["我会说中文。", "Tôi biết nói tiếng Trung."],
    "能": ["你能帮我吗？", "Bạn có thể giúp tôi không?"],
    "想": ["我想去中国。", "Tôi muốn đi Trung Quốc."],
    "要": ["我要一杯咖啡。", "Tôi muốn một cốc cà phê."],
    "喜欢": ["我喜欢学中文。", "Tôi thích học tiếng Trung."],
    "爱": ["我爱你。", "Anh yêu em."],
    "学习": ["我每天都在学习。", "Tôi học tập mỗi ngày."],
    "工作": ["他在公司工作。", "Anh ấy làm việc ở công ty."],
    "睡觉": ["我十点睡觉。", "Tôi đi ngủ lúc mười giờ."],
    "起床": ["我每天六点起床。", "Tôi thức dậy lúc sáu giờ mỗi ngày."],
    "上课": ["我们八点上课。", "Chúng tôi lên lớp lúc tám giờ."],
    "回家": ["我五点回家。", "Tôi về nhà lúc năm giờ."],
    "知道": ["我知道这件事。", "Tôi biết việc này."],
    "认识": ["我认识他。", "Tôi quen biết anh ấy."],

    # Nouns - People & Places
    "人": ["他是好人。", "Anh ấy là người tốt."],
    "朋友": ["她是我的朋友。", "Cô ấy là bạn của tôi."],
    "名字": ["你叫什么名字？", "Bạn tên là gì?"],
    "家": ["我家有三个人。", "Nhà tôi có ba người."],
    "学校": ["学校很大。", "Trường học rất lớn."],
    "医院": ["他在医院工作。", "Anh ấy làm việc ở bệnh viện."],
    "商店": ["商店开门了。", "Cửa hàng đã mở cửa."],
    "房间": ["我的房间很小。", "Phòng của tôi rất nhỏ."],

    # Food & Drink
    "水": ["请给我一杯水。", "Làm ơn cho tôi một cốc nước."],
    "茶": ["你喝不喝茶？", "Bạn có uống trà không?"],
    "咖啡": ["我要一杯咖啡。", "Tôi muốn một cốc cà phê."],
    "米饭": ["我吃米饭。", "Tôi ăn cơm."],
    "菜": ["这个菜很好吃。", "Món này rất ngon."],
    "水果": ["我喜欢吃水果。", "Tôi thích ăn trái cây."],
    "牛奶": ["他每天早上喝牛奶。", "Anh ấy uống sữa mỗi sáng."],
    "蛋糕": ["这个蛋糕很好吃。", "Cái bánh này rất ngon."],

    # Time
    "今天": ["今天天气很好。", "Hôm nay thời tiết rất đẹp."],
    "明天": ["明天我要去学校。", "Ngày mai tôi phải đi học."],
    "昨天": ["昨天我去了商店。", "Hôm qua tôi đã đi cửa hàng."],
    "早上": ["早上好！", "Chào buổi sáng!"],
    "中午": ["我们中午见面。", "Chúng ta gặp nhau buổi trưa."],
    "晚上": ["晚上好！", "Chào buổi tối!"],
    "现在": ["现在几点了？", "Bây giờ là mấy giờ?"],
    "年": ["我今年二十五岁。", "Tôi năm nay 25 tuổi."],
    "月": ["这个月很忙。", "Tháng này rất bận."],
    "星期": ["今天是星期一。", "Hôm nay là thứ Hai."],
    "时间": ["我没有时间。", "Tôi không có thời gian."],
    "时候": ["你什么时候来？", "Khi nào bạn đến?"],

    # Adjectives
    "好": ["这本书很好。", "Quyển sách này rất hay."],
    "大": ["这个房间很大。", "Căn phòng này rất lớn."],
    "小": ["这只猫很小。", "Con mèo này rất nhỏ."],
    "多": ["这里人很多。", "Ở đây có rất nhiều người."],
    "少": ["今天人很少。", "Hôm nay có rất ít người."],
    "高": ["他很高。", "Anh ấy rất cao."],
    "冷": ["今天很冷。", "Hôm nay rất lạnh."],
    "热": ["夏天很热。", "Mùa hè rất nóng."],
    "漂亮": ["她真漂亮。", "Cô ấy thật đẹp."],
    "高兴": ["我很高兴认识你。", "Tôi rất vui được quen biết bạn."],
    "快乐": ["生日快乐！", "Chúc mừng sinh nhật!"],
    "忙": ["我很忙。", "Tôi rất bận."],
    "累": ["今天我很累。", "Hôm nay tôi rất mệt."],
    "饿": ["我饿了。", "Tôi đói rồi."],
    "渴": ["我渴了。", "Tôi khát rồi."],
    "对": ["你说得对。", "Bạn nói đúng."],
    "错": ["对不起，我错了。", "Xin lỗi, tôi sai rồi."],

    # Essentials
    "谢谢": ["谢谢你！", "Cảm ơn bạn!"],
    "不客气": ["不客气！", "Không có gì!"],
    "对不起": ["对不起！", "Xin lỗi!"],
    "没关系": ["没关系。", "Không sao đâu."],
    "再见": ["明天见，再见！", "Ngày mai gặp lại, tạm biệt!"],
    "可以": ["我可以进来吗？", "Tôi có thể vào không?"],
    "但是": ["我想去，但是没时间。", "Tôi muốn đi, nhưng không có thời gian."],
    "因为": ["因为下雨，我不去。", "Vì trời mưa, tôi không đi."],
    "所以": ["因为下雨，所以我不去。", "Vì trời mưa, nên tôi không đi."],
    "如果": ["如果你来，我会很高兴。", "Nếu bạn đến, tôi sẽ rất vui."],

    # HSK 2 additions
    "帮助": ["请帮助我。", "Làm ơn giúp tôi."],
    "发现": ["我发现了一个问题。", "Tôi phát hiện ra một vấn đề."],
    "告诉": ["请告诉我你的名字。", "Làm ơn nói cho tôi tên của bạn."],
    "决定": ["我决定学中文。", "Tôi quyết định học tiếng Trung."],
    "开始": ["我们开始上课吧。", "Chúng ta bắt đầu vào lớp nhé."],
    "跑步": ["我每天早上跑步。", "Tôi chạy bộ mỗi sáng."],
    "游泳": ["我喜欢游泳。", "Tôi thích bơi."],
    "旅行": ["我想去旅行。", "Tôi muốn đi du lịch."],
    "考试": ["明天有考试。", "Ngày mai có thi."],
    "电脑": ["我用电脑工作。", "Tôi dùng máy tính để làm việc."],
    "电话": ["这是我的电话号码。", "Đây là số điện thoại của tôi."],
    "电影": ["我们去看电影吧。", "Chúng ta đi xem phim nhé."],
    "手机": ["我的手机没电了。", "Điện thoại của tôi hết pin rồi."],
    "问题": ["我有一个问题。", "Tôi có một câu hỏi."],
    "运动": ["你喜欢什么运动？", "Bạn thích môn thể thao nào?"],
    "容易": ["这个考试很容易。", "Bài thi này rất dễ."],
    "重要": ["学习中文很重要。", "Học tiếng Trung rất quan trọng."],
    "努力": ["我会努力的。", "Tôi sẽ cố gắng."],
    "已经": ["他已经来了。", "Anh ấy đã đến rồi."],
    "经常": ["我经常去图书馆。", "Tôi thường xuyên đến thư viện."],
    "虽然": ["虽然很累，但是很高兴。", "Mặc dù rất mệt, nhưng rất vui."],
    "而且": ["他很高而且很帅。", "Anh ấy cao mà còn đẹp trai."],
    "或者": ["茶或者咖啡，你喜欢哪个？", "Trà hoặc cà phê, bạn thích cái nào?"],
    "然后": ["先吃饭，然后去上课。", "Ăn cơm trước, sau đó đi học."],
    "以前": ["我以前不会说中文。", "Trước đây tôi không biết nói tiếng Trung."],
    "以后": ["以后我们一起去。", "Sau này chúng ta cùng đi."],

    # Colors
    "红色": ["我喜欢红色的花。", "Tôi thích hoa màu đỏ."],
    "白色": ["她穿着白色衣服。", "Cô ấy mặc quần áo trắng."],
    "黑色": ["他的车是黑色的。", "Xe của anh ấy màu đen."],
    "蓝色": ["天空是蓝色的。", "Bầu trời màu xanh lam."],
    "绿色": ["草是绿色的。", "Cỏ màu xanh lá."],
    "黄色": ["我有黄色的书包。", "Tôi có cặp sách màu vàng."],
}

# ========== SINO-VIETNAMESE MAPPING ==========
SINO_VIET_MAP = {
    "我": "ngã", "你": "nhĩ", "他": "tha", "她": "tha", "它": "tha",
    "我们": "ngã môn", "你们": "nhĩ môn", "他们": "tha môn", "大家": "đại gia",
    "一": "nhất", "二": "nhị", "三": "tam", "四": "tứ", "五": "ngũ",
    "六": "lục", "七": "thất", "八": "bát", "九": "cửu", "十": "thập",
    "零": "linh", "百": "bách", "千": "thiên", "半": "bán",
    "几": "kỷ", "多少": "đa thiểu", "很多": "ngận đa",
    "是": "thị", "有": "hữu", "在": "tại", "吃": "khiết",
    "喝": "khát", "看": "khán", "听": "thính", "说": "thuyết",
    "读": "độc", "写": "tả", "去": "khứ", "来": "lai",
    "做": "tố", "买": "mãi", "卖": "mại", "叫": "khiếu",
    "会": "hội", "能": "năng", "想": "tưởng", "要": "yếu",
    "喜欢": "hỉ hoan", "爱": "ái", "学习": "học tập",
    "工作": "công tác", "睡觉": "thụy giác", "起床": "khởi sàng",
    "上课": "thượng khóa", "回家": "hồi gia", "知道": "tri đạo",
    "认识": "nhận thức", "人": "nhân", "男人": "nam nhân",
    "女人": "nữ nhân", "孩子": "hài tử", "朋友": "bằng hữu",
    "名字": "danh tự", "水": "thủy", "茶": "trà",
    "咖啡": "ca phê", "米饭": "mễ phạn", "菜": "thái",
    "水果": "thủy quả", "书": "thư", "书包": "thư bao",
    "笔": "bút", "桌子": "trác tử", "椅子": "ỷ tử",
    "房间": "phòng gian", "学校": "học hiệu", "医院": "y viện",
    "商店": "thương điếm", "家": "gia", "钱": "tiền",
    "时间": "thời gian", "今天": "kim thiên", "明天": "minh thiên",
    "昨天": "tạc thiên", "早上": "tảo thượng", "中午": "trung ngọ",
    "晚上": "vãn thượng", "现在": "hiện tại", "星期": "tinh kỳ",
    "年": "niên", "月": "nguyệt", "日": "nhật",
    "号": "hiệu", "点": "điểm", "分钟": "phân chung",
    "衣服": "y phục", "天气": "thiên khí", "汉语": "Hán ngữ",
    "中文": "Trung văn", "好": "hảo", "大": "đại",
    "小": "tiểu", "多": "đa", "少": "thiểu",
    "高": "cao", "矮": "ải", "冷": "lãnh",
    "热": "nhiệt", "漂亮": "phiếu lượng", "好看": "hảo khán",
    "快乐": "khoái lạc", "高兴": "cao hưng", "忙": "mang",
    "累": "lụy", "饿": "ngã", "渴": "khát",
    "对": "đối", "错": "thác", "新": "tân",
    "老": "lão", "什么": "thập ma", "谁": "thùy",
    "哪里": "ná lý", "怎么": "chẩm ma", "为什么": "vị thập ma",
    "什么时候": "thập ma thời hầu", "的": "đích", "了": "liễu",
    "吗": "ma", "呢": "ni", "不": "bất",
    "很": "ngận", "也": "dã", "都": "đô",
    "和": "hòa", "还": "hoàn", "太": "thái",
    "最": "tối", "真": "chân", "请": "thỉnh",
    "谢谢": "tạ tạ", "不客气": "bất khách khí",
    "对不起": "đối bất khởi", "没关系": "một quan hệ",
    "再见": "tái kiến", "可以": "khả dĩ",
    "但是": "đãn thị", "非常": "phi thường",
    "一共": "nhất cộng", "红色": "hồng sắc",
    "白色": "bạch sắc", "黑色": "hắc sắc",
    "蓝色": "lam sắc", "绿色": "lục sắc",
    "黄色": "hoàng sắc",
    # HSK 2
    "帮助": "bang trợ", "变成": "biến thành",
    "出现": "xuất hiện", "打扫": "đả tảo",
    "打算": "đả toán", "带": "đới",
    "担心": "đam tâm", "发现": "phát hiện",
    "告诉": "cáo tố", "害怕": "hại phạ",
    "检查": "kiểm tra", "教": "giáo",
    "决定": "quyết định", "开": "khai",
    "开始": "khai thủy", "哭": "khốc",
    "离开": "ly khai", "练习": "luyện tập",
    "旅行": "lữ hành", "拿": "ná",
    "跑步": "bào bộ", "请客": "thỉnh khách",
    "让": "nhượng", "送": "tống",
    "游泳": "du vĩnh", "用完": "dụng hoàn",
    "遇到": "ngộ đáo", "愿意": "nguyện ý",
    "办公室": "bán công thất", "报纸": "báo chỉ",
    "词典": "từ điển", "答案": "đáp án",
    "蛋糕": "đản cao", "地方": "địa phương",
    "电话": "điện thoại", "电脑": "điện não",
    "电影": "điện ảnh", "公司": "công ty",
    "公园": "công viên", "故事": "cố sự",
    "顾客": "cố khách", "关系": "quan hệ",
    "国家": "quốc gia", "海滩": "hải than",
    "黑板": "hắc bản", "机场": "cơ trường",
    "机会": "cơ hội", "礼物": "lễ vật",
    "邻居": "lân cư", "门": "môn",
    "密码": "mật mã", "内容": "nội dung",
    "年级": "niên cấp", "牛奶": "ngưu nãi",
    "身体": "thân thể", "生日": "sinh nhật",
    "声音": "thanh âm", "世界": "thế giới",
    "手机": "thủ cơ", "数字": "số tự",
    "太阳": "thái dương", "图书馆": "đồ thư quán",
    "外国人": "ngoại quốc nhân", "晚饭": "vãn phạn",
    "问题": "vấn đề", "习惯": "tập quán",
    "小心": "tiểu tâm", "笑话": "tiếu thoại",
    "信息": "tín tức", "眼睛": "nhãn tình",
    "颜色": "nhan sắc", "意思": "ý tứ",
    "因为": "nhân vị", "音乐": "âm nhạc",
    "时候": "thời hầu", "知识": "tri thức",
    "中间": "trung gian", "安静": "an tĩnh",
    "方便": "phương tiện", "放心": "phóng tâm",
    "干净": "can tịnh", "重要": "trọng yếu",
    "着急": "trứ cấp", "一样": "nhất dạng",
    "认真": "nhận chân", "清楚": "thanh sở",
    "容易": "dung dị", "舒服": "thư phục",
    "危险": "nguy hiểm", "有名": "hữu danh",
    "努力": "nỗ lực", "不但": "bất đãn",
    "而且": "nhi thả", "或者": "hoặc giả",
    "虽然": "tuy nhiên", "如果": "như quả",
    "然后": "nhiên hậu", "已经": "dĩ kinh",
    "以前": "dĩ tiền", "以后": "dĩ hậu",
    "经常": "kinh thường", "总是": "tổng thị",
    "特别": "đặc biệt", "可能": "khả năng",
    "踢足球": "đích túc cầu", "掉": "điệu",
    "动物园": "động vật viên", "风俗": "phong tục",
    "妻子": "thê tử", "网站": "võng trạm",
    "微信": "vi tín", "钥匙": "dược thi",
    "保护": "bảo hộ", "因为": "nhân vị",
}

_bulk_sino_viet_cache = None

def _bulk_sino_viet_map():
    global _bulk_sino_viet_cache
    if _bulk_sino_viet_cache is None:
        if os.path.exists(_BULK_VOCAB_PATH):
            with open(_BULK_VOCAB_PATH, encoding="utf-8") as f:
                data = json.load(f)
            _bulk_sino_viet_cache = {w["simplified"]: w["sino_viet"] for w in data}
        else:
            _bulk_sino_viet_cache = {}
    return _bulk_sino_viet_cache

def get_sino_viet(word):
    return SINO_VIET_MAP.get(word) or _bulk_sino_viet_map().get(word, "")

# ========== EXAMPLE SENTENCES ==========
# (data defined above at lines ~311-470)

from example_sentences_bulk import BULK_EXAMPLE_SENTENCES
EXAMPLE_SENTENCES.update(BULK_EXAMPLE_SENTENCES)

def get_sentence(word):
    return EXAMPLE_SENTENCES.get(word, None)

# ========== CONTEXT GRAMMAR NOTES ==========
CONTEXT_NOTES = {
    "的": "Trợ từ sở hữu: đặt sau danh từ/đại từ → 'của'. VD: 我的书 (sách của tôi).",
    "了": "Trợ từ hoàn thành: đặt cuối câu → 'rồi'. VD: 我吃了 (tôi ăn rồi).",
    "吗": "Trợ từ nghi vấn: đặt cuối câu → thành câu hỏi. VD: 你好吗？",
    "不": "Phủ định: đặt trước động từ/tính từ. VD: 我不去. Riêng 有 phải dùng 没有.",
    "很": "Rất. 很 + tính từ. Thường dùng ngay cả khi không có nghĩa 'rất'.",
    "也": "Cũng: đặt trước động từ. VD: 我也是学生.",
    "都": "Đều: đặt trước động từ, sau chủ ngữ số nhiều. VD: 他们都是.",
    "和": "Và: nối 2 danh từ. KHÔNG dùng để nối 2 câu.",
    "还": "Còn/vẫn: đặt trước động từ. VD: 我还要吃.",
    "太": "Quá: 太 + tính từ + 了 = quá... VD: 太好了！",
    "在": "1) Giới từ 'ở': 我在家. 2) Đang: 我在吃饭.",
    "想": "1) Muốn: 我想去. 2) Nghĩ: 我想一想.",
    "会": "1) Biết (làm): 我会说. 2) Sẽ: 我会来的.",
    "能": "Có thể (khả năng hoặc được phép). VD: 我能进来吗？",
    "可以": "Được phép/có thể. VD: 可以进来吗？",
    "但是": "Nhưng: nối 2 vế tương phản. VD: 想去但是没时间.",
    "因为": "Bởi vì: 因为 + lý do. VD: 因为下雨我不去.",
    "如果": "Nếu: 如果 + điều kiện. VD: 如果你来，我会很高兴.",
    "吧": "Trợ từ đề nghị. VD: 走吧！(Đi thôi!).",
    "一下": "Làm một chút (nhẹ giọng). VD: 我看一下.",
    "怎么": "Thế nào? Hỏi cách thức. VD: 怎么去？",
    "为什么": "Tại sao? VD: 为什么不去？",
}

def get_context_note(word):
    return CONTEXT_NOTES.get(word, None)

# ========== DIALOGUES (Hội thoại thực tế) ==========
DIALOGUES = {
    "greeting_first": {
        "title": "Chào hỏi lần đầu",
        "context": "Hai người gặp lần đầu, tự giới thiệu.",
        "hsk_level": 1,
        "lines": [
            ("A", "你好！我叫小明，你叫什么名字？", "Nǐ hǎo! Wǒ jiào Xiǎo Míng, nǐ jiào shénme míngzì?", "Chào bạn! Tôi là Tiểu Minh, bạn tên là gì?"),
            ("B", "你好，我叫李红。认识你很高兴！", "Nǐ hǎo, wǒ jiào Lǐ Hóng. Rènshi nǐ hěn gāoxìng!", "Chào bạn, tôi là Lý Hồng. Rất vui được biết bạn!"),
            ("A", "我也是！你是中国人吗？", "Wǒ yě shì! Nǐ shì Zhōngguó rén ma?", "Tôi cũng vậy! Bạn là người Trung Quốc à?"),
            ("B", "是，我是中国人。你呢？", "Shì, wǒ shì Zhōngguó rén. Nǐ ne?", "Vâng, tôi là người Trung Quốc. Còn bạn?"),
            ("A", "我是越南人。我在学汉语。", "Wǒ shì Yuènán rén. Wǒ zài xué Hànyǔ.", "Tôi là người Việt Nam. Tôi đang học tiếng Trung."),
            ("B", "你的汉语很好！", "Nǐ de Hànyǔ hěn hǎo!", "Tiếng Trung của bạn rất tốt!"),
        ]
    },
    "ordering_food": {
        "title": "Gọi món ăn",
        "context": "Vào nhà hàng Trung Quốc gọi món.",
        "hsk_level": 1,
        "lines": [
            ("B", "欢迎光临！你们几位？", "Huānyíng guānglín! Nǐmen jǐ wèi?", "Chào mừng! Mấy người ạ?"),
            ("A", "两位。", "Liǎng wèi.", "Hai người."),
            ("B", "请这边坐。要喝什么？", "Qǐng zhè biān zuò. Yào hē shénme?", "Mời ngồi. Uống gì ạ?"),
            ("A", "我要一杯茶，他要咖啡。", "Wǒ yào yì bēi chá, tā yào kāfēi.", "Tôi muốn trà, anh ấy cà phê."),
            ("B", "好的，想吃什么？", "Hǎo de, xiǎng chī shénme?", "Vâng, ăn gì ạ?"),
            ("A", "这个菜是什么？好吃吗？", "Zhège cài shì shénme? Hǎochī ma?", "Món này là gì? Ngon không?"),
            ("B", "很好吃！这是我们的特色菜。", "Hěn hǎochī! Zhè shì wǒmen de tèsè cài.", "Rất ngon! Đây là món đặc sắc."),
            ("A", "好，我要这个。一共多少钱？", "Hǎo, wǒ yào zhège. Yígòng duōshao qián?", "Được, lấy món này. Tổng cộng bao nhiêu?"),
        ]
    },
    "shopping": {
        "title": "Mua sắm",
        "context": "Mua quần áo ở cửa hàng.",
        "hsk_level": 2,
        "lines": [
            ("A", "你好，我想买一件衣服。", "Nǐ hǎo, wǒ xiǎng mǎi yí jiàn yīfu.", "Chào, tôi muốn mua một cái áo."),
            ("B", "你喜欢什么颜色的？", "Nǐ xǐhuān shénme yánsè de?", "Bạn thích màu gì?"),
            ("A", "我喜欢红色的。有大的吗？", "Wǒ xǐhuān hóngsè de. Yǒu dà de ma?", "Tôi thích màu đỏ. Có size lớn không?"),
            ("B", "有。你试试这件。", "Yǒu. Nǐ shìshi zhè jiàn.", "Có. Bạn thử cái này."),
            ("A", "很好，很漂亮。多少钱？", "Hěn hǎo, hěn piàoliang. Duōshao qián?", "Đẹp. Bao nhiêu tiền?"),
            ("B", "一百五十块。", "Yì bǎi wǔshí kuài.", "150 tệ."),
            ("A", "太贵了！能不能便宜点儿？", "Tài guì le! Néng bù néng piányi diǎnr?", "Đắt quá! Có rẻ hơn không?"),
            ("B", "好吧，一百二十块。", "Hǎo ba, yì bǎi èrshí kuài.", "Thôi được, 120 tệ."),
            ("A", "好的，我要了。谢谢！", "Hǎo de, wǒ yào le. Xièxie!", "Được, tôi lấy. Cảm ơn!"),
        ]
    },
    "asking_directions": {
        "title": "Hỏi đường",
        "context": "Hỏi đường đến bệnh viện.",
        "hsk_level": 2,
        "lines": [
            ("A", "请问，医院怎么走？", "Qǐngwèn, yīyuàn zěnme zǒu?", "Xin hỏi, bệnh viện đi thế nào?"),
            ("B", "往前走，在路口左转。", "Wǎng qián zǒu, zài lùkǒu zuǒ zhuǎn.", "Đi thẳng, đến ngã rẽ rẽ trái."),
            ("A", "远不远？", "Yuǎn bù yuǎn?", "Xa không?"),
            ("B", "不远，走路五分钟。", "Bù yuǎn, zǒulù wǔ fēnzhōng.", "Không xa, đi bộ 5 phút."),
            ("A", "谢谢您！", "Xièxie nín!", "Cảm ơn!"),
            ("B", "不客气。", "Bú kèqi.", "Không có gì."),
        ]
    },
    "daily_routine": {
        "title": "Sinh hoạt hàng ngày",
        "context": "Nói về thói quen một ngày.",
        "hsk_level": 2,
        "lines": [
            ("A", "你每天几点起床？", "Nǐ měi tiān jǐ diǎn qǐchuáng?", "Mỗi ngày bạn dậy mấy giờ?"),
            ("B", "我每天六点半起床。", "Wǒ měi tiān liù diǎn bàn qǐchuáng.", "Tôi dậy lúc 6 giờ rưỡi."),
            ("A", "真早！你吃早饭吗？", "Zhēn zǎo! Nǐ chī zǎofàn ma?", "Sớm thật! Ăn sáng không?"),
            ("B", "吃，我吃面包和牛奶。", "Chī, wǒ chī miànbāo hé niúnǎi.", "Có, tôi ăn bánh mì sữa."),
            ("A", "你几点上班？", "Nǐ jǐ diǎn shàngbān?", "Mấy giờ đi làm?"),
            ("B", "九点上班，五点下班。", "Jiǔ diǎn shàngbān, wǔ diǎn xiàbān.", "9 giờ đi làm, 5 giờ tan làm."),
            ("A", "晚上你做什么？", "Wǎnshang nǐ zuò shénme?", "Tối làm gì?"),
            ("B", "我看电视或者看书。十一点睡觉。", "Wǒ kàn diànshì huòzhě kàn shū. Shíyī diǎn shuìjiào.", "Xem tivi hoặc đọc sách. 11 giờ đi ngủ."),
        ]
    },
    "weather_chat": {
        "title": "Thời tiết",
        "context": "Hỏi và trả lời về thời tiết.",
        "hsk_level": 1,
        "lines": [
            ("A", "今天天气怎么样？", "Jīntiān tiānqì zěnme yàng?", "Hôm nay thời tiết thế nào?"),
            ("B", "今天很热，三十度。", "Jīntiān hěn rè, sānshí dù.", "Hôm nay rất nóng, 30 độ."),
            ("A", "明天呢？", "Míngtiān ne?", "Ngày mai?"),
            ("B", "明天会下雨，很冷。", "Míngtiān huì xià yǔ, hěn lěng.", "Ngày mai mưa, lạnh."),
            ("A", "那我明天不去了。", "Nà wǒ míngtiān bú qù le.", "Thế thì mai tôi không đi nữa."),
        ]
    },
    "phone_call": {
        "title": "Gọi điện hẹn bạn",
        "context": "Gọi điện hẹn gặp bạn đi chơi.",
        "hsk_level": 2,
        "lines": [
            ("A", "喂？", "Wèi?", "A lô?"),
            ("B", "喂，你好，请问是小王吗？", "Wèi, nǐ hǎo, qǐngwèn shì Xiǎo Wáng ma?", "A lô, xin hỏi có phải Tiểu Vương không?"),
            ("A", "是我。什么事？", "Shì wǒ. Shénme shì?", "Tôi đây. Có việc gì?"),
            ("B", "星期天你有时间吗？", "Xīngqítiān nǐ yǒu shíjiān ma?", "Chủ nhật bạn có thời gian không?"),
            ("A", "有。我们一起去公园？", "Yǒu. Wǒmen yìqǐ qù gōngyuán?", "Có. Cùng đi công viên nhé?"),
            ("B", "好啊！下午两点见。", "Hǎo a! Xiàwǔ liǎng diǎn jiàn.", "Hay quá! 2 giờ chiều gặp nhé."),
        ]
    },
    "making_friends": {
        "title": "Kết bạn",
        "context": "Giới thiệu về bản thân và hỏi sở thích.",
        "hsk_level": 2,
        "lines": [
            ("A", "你从哪儿来？", "Nǐ cóng nǎr lái?", "Bạn từ đâu đến?"),
            ("B", "我从越南来，我是河内人。", "Wǒ cóng Yuènán lái, wǒ shì Hénèi rén.", "Tôi đến từ Việt Nam, tôi là người Hà Nội."),
            ("A", "我是中国人。你在学什么？", "Wǒ shì Zhōngguó rén. Nǐ zài xué shénme?", "Tôi là người Trung Quốc. Bạn đang học gì?"),
            ("B", "我在学汉语，我喜欢中文。", "Wǒ zài xué Hànyǔ, wǒ xǐhuān Zhōngwén.", "Tôi đang học Hán ngữ, tôi thích tiếng Trung."),
            ("A", "你为什么学中文？", "Nǐ wèishénme xué Zhōngwén?", "Vì sao bạn học tiếng Trung?"),
            ("B", "因为中文很有意思，而且我想去中国工作。", "Yīnwèi Zhōngwén hěn yǒuyìsi, érqiě wǒ xiǎng qù Zhōngguó gōngzuò.", "Vì tiếng Trung rất thú vị, hơn nữa tôi muốn sang Trung Quốc làm việc."),
            ("A", "加油！你会学得很好的。", "Jiāyóu! Nǐ huì xué dé hěn hǎo de.", "Cố lên! Bạn sẽ học tốt thôi."),
        ]
    },
    "at_hospital": {
        "title": "Ở bệnh viện",
        "context": "Đi khám bệnh nói triệu chứng.",
        "hsk_level": 2,
        "lines": [
            ("A", "医生，我不舒服。", "Yīshēng, wǒ bù shūfu.", "Bác sĩ, tôi không khỏe."),
            ("B", "哪里不舒服？", "Nǎlǐ bù shūfu?", "Đau chỗ nào?"),
            ("A", "我头疼，也有一点儿发烧。", "Wǒ tóu téng, yě yǒu yìdiǎnr fāshāo.", "Đau đầu, hơi sốt."),
            ("B", "三十八度。要多喝水，好好休息。", "Sānshíbā dù. Yào duō hē shuǐ, hǎohao xiūxi.", "38 độ. Cần uống nhiều nước, nghỉ ngơi cho tốt."),
            ("A", "好的，谢谢医生！", "Hǎo de, xièxie yīshēng!", "Vâng, cảm ơn bác sĩ!"),
        ]
    },
    # HSK 3-9: mỗi cấp 1 hội thoại, chủ đề/độ khó tăng dần theo cấp — trước
    # đây "Hội thoại" chỉ có nội dung HSK 1-2 (9 bài ở trên).
    "watch_movie": {
        "title": "Hẹn đi xem phim",
        "context": "Rủ bạn đi xem phim cuối tuần.",
        "hsk_level": 3,
        "lines": [
            ("A", "你好，周末你有时间吗？我们一起去看电影吧。", "Nǐ hǎo, zhōumò nǐ yǒu shíjiān ma? Wǒmen yìqǐ qù kàn diànyǐng ba.", "Chào bạn, cuối tuần bạn có rảnh không? Chúng ta cùng đi xem phim nhé."),
            ("B", "好啊！你想看什么电影？", "Hǎo a! Nǐ xiǎng kàn shénme diànyǐng?", "Được đó! Bạn muốn xem phim gì?"),
            ("A", "我觉得那部新电影很好看，很多人都说不错。", "Wǒ juéde nà bù xīn diànyǐng hěn hǎokàn, hěn duō rén dōu shuō búcuò.", "Tôi thấy bộ phim mới đó khá hay, nhiều người nói không tệ."),
            ("B", "好，那我们几点见面？", "Hǎo, nà wǒmen jǐ diǎn jiànmiàn?", "Được, vậy mấy giờ chúng ta gặp nhau?"),
            ("A", "下午两点，在电影院门口怎么样？", "Xiàwǔ liǎng diǎn, zài diànyǐngyuàn ménkǒu zěnmeyàng?", "2 giờ chiều, ở cửa rạp chiếu phim được không?"),
            ("B", "没问题。我坐地铁过去，大概二十分钟。", "Méi wèntí. Wǒ zuò dìtiě guòqù, dàgài èrshí fēnzhōng.", "Không vấn đề gì. Tôi đi tàu điện ngầm, khoảng 20 phút."),
            ("A", "好，那我们两点在门口见！", "Hǎo, nà wǒmen liǎng diǎn zài ménkǒu jiàn!", "Được, vậy 2 giờ gặp nhau ở cửa nhé!"),
        ]
    },
    "exercise_habit": {
        "title": "Thói quen tập thể dục",
        "context": "Trò chuyện về việc rèn luyện sức khỏe hằng ngày.",
        "hsk_level": 4,
        "lines": [
            ("A", "你平时怎么锻炼身体？", "Nǐ píngshí zěnme duànliàn shēntǐ?", "Bình thường bạn tập thể dục thế nào?"),
            ("B", "我每天早上跑步，大概三十分钟。", "Wǒ měitiān zǎoshang pǎobù, dàgài sānshí fēnzhōng.", "Mỗi sáng tôi chạy bộ khoảng 30 phút."),
            ("A", "真了不起！我一直坚持不下来。", "Zhēn liǎobuqǐ! Wǒ yìzhí jiānchí bú xiàlái.", "Giỏi thật! Tôi cứ không kiên trì được."),
            ("B", "其实一开始也很难，但是习惯了就好了。", "Qíshí yì kāishǐ yě hěn nán, dànshì xíguàn le jiù hǎo le.", "Thực ra lúc đầu cũng khó, nhưng quen rồi thì ổn."),
            ("A", "除了跑步，你还做别的运动吗？", "Chúle pǎobù, nǐ hái zuò bié de yùndòng ma?", "Ngoài chạy bộ, bạn còn tập môn gì khác không?"),
            ("B", "周末我常常打篮球，或者去游泳。", "Zhōumò wǒ chángcháng dǎ lánqiú, huòzhě qù yóuyǒng.", "Cuối tuần tôi hay chơi bóng rổ, hoặc đi bơi."),
            ("A", "听起来很健康。我也应该开始运动了。", "Tīng qǐlái hěn jiànkāng. Wǒ yě yīnggāi kāishǐ yùndòng le.", "Nghe có vẻ khoẻ mạnh đấy. Tôi cũng nên bắt đầu tập thể dục thôi."),
        ]
    },
    "job_interview": {
        "title": "Phỏng vấn xin việc",
        "context": "Trả lời phỏng vấn xin việc tại một công ty.",
        "hsk_level": 5,
        "lines": [
            ("A", "你好，请介绍一下你自己。", "Nǐ hǎo, qǐng jièshào yíxià nǐ zìjǐ.", "Chào bạn, hãy giới thiệu một chút về bản thân."),
            ("B", "您好，我叫王芳，毕业于北京大学，学的是市场营销专业。", "Nín hǎo, wǒ jiào Wáng Fāng, bìyè yú Běijīng Dàxué, xué de shì shìchǎng yíngxiāo zhuānyè.", "Chào ông/bà, tôi tên Vương Phương, tốt nghiệp Đại học Bắc Kinh, chuyên ngành marketing."),
            ("A", "你为什么想应聘我们公司这个职位？", "Nǐ wèishénme xiǎng yìngpìn wǒmen gōngsī zhège zhíwèi?", "Vì sao bạn muốn ứng tuyển vị trí này ở công ty chúng tôi?"),
            ("B", "我对贵公司的产品很感兴趣，也相信自己的能力能胜任这份工作。", "Wǒ duì guì gōngsī de chǎnpǐn hěn gǎn xìngqù, yě xiāngxìn zìjǐ de nénglì néng shèngrèn zhè fèn gōngzuò.", "Tôi rất quan tâm đến sản phẩm của quý công ty, và tin rằng năng lực của mình có thể đảm nhận công việc này."),
            ("A", "你有相关的工作经验吗？", "Nǐ yǒu xiāngguān de gōngzuò jīngyàn ma?", "Bạn có kinh nghiệm làm việc liên quan không?"),
            ("B", "有，我实习过一年，负责过市场推广和数据分析。", "Yǒu, wǒ shíxí guò yì nián, fùzé guò shìchǎng tuīguǎng hé shùjù fēnxī.", "Có, tôi từng thực tập một năm, phụ trách quảng bá thị trường và phân tích dữ liệu."),
            ("A", "好的，我们会尽快通知你结果。", "Hǎo de, wǒmen huì jǐnkuài tōngzhī nǐ jiéguǒ.", "Được, chúng tôi sẽ sớm thông báo kết quả cho bạn."),
        ]
    },
    "social_media_debate": {
        "title": "Tranh luận về mạng xã hội",
        "context": "Thảo luận ảnh hưởng hai mặt của mạng xã hội với giới trẻ.",
        "hsk_level": 6,
        "lines": [
            ("A", "你觉得社交媒体对年轻人的影响是好是坏？", "Nǐ juéde shèjiāo méitǐ duì niánqīngrén de yǐngxiǎng shì hǎo shì huài?", "Bạn nghĩ mạng xã hội ảnh hưởng đến giới trẻ là tốt hay xấu?"),
            ("B", "这很难一概而论。它既能拉近人与人的距离，也可能让人更孤独。", "Zhè hěn nán yígài ér lùn. Tā jì néng lājìn rén yǔ rén de jùlí, yě kěnéng ràng rén gèng gūdú.", "Cái này khó nói chung được. Nó vừa có thể kéo gần khoảng cách giữa người với người, cũng có thể khiến người ta cô đơn hơn."),
            ("A", "我同意。不过我担心大家越来越依赖手机，忽略了现实生活。", "Wǒ tóngyì. Búguò wǒ dānxīn dàjiā yuèláiyuè yīlài shǒujī, hūlüè le xiànshí shēnghuó.", "Tôi đồng ý. Nhưng tôi lo mọi người ngày càng phụ thuộc điện thoại, bỏ qua cuộc sống thực."),
            ("B", "关键还是要看怎么使用吧，凡事都有两面性。", "Guānjiàn háishi yào kàn zěnme shǐyòng ba, fánshì dōu yǒu liǎngmiànxìng.", "Then chốt vẫn là xem sử dụng thế nào thôi, cái gì cũng có hai mặt."),
            ("A", "说得有道理。合理安排使用时间应该是解决办法之一。", "Shuō de yǒu dàolǐ. Hélǐ ānpái shǐyòng shíjiān yīnggāi shì jiějué bànfǎ zhī yī.", "Nói cũng có lý. Sắp xếp thời gian sử dụng hợp lý chắc là một trong những cách giải quyết."),
            ("B", "对，我们不能因噎废食，完全拒绝社交媒体也不现实。", "Duì, wǒmen bùnéng yīnyēfèishí, wánquán jùjué shèjiāo méitǐ yě bù xiànshí.", "Đúng, chúng ta không thể vì nghẹn mà bỏ ăn, hoàn toàn từ chối mạng xã hội cũng không thực tế."),
            ("A", "没错，找到平衡点才是最重要的。", "Méi cuò, zhǎodào pínghéngdiǎn cái shì zuì zhòngyào de.", "Đúng vậy, tìm được điểm cân bằng mới là quan trọng nhất."),
        ]
    },
    "climate_change": {
        "title": "Bàn về bảo vệ môi trường",
        "context": "Thảo luận về biến đổi khí hậu và trách nhiệm mỗi bên.",
        "hsk_level": 7,
        "lines": [
            ("A", "近年来极端天气频发，你怎么看待气候变化这个问题？", "Jìnnián lái jíduān tiānqì pínfā, nǐ zěnme kàndài qìhòu biànhuà zhège wèntí?", "Những năm gần đây thời tiết cực đoan xảy ra thường xuyên, bạn nhìn nhận vấn đề biến đổi khí hậu thế nào?"),
            ("B", "我认为这不仅是环境问题，更是关系到人类未来生存的重大议题。", "Wǒ rènwéi zhè bùjǐn shì huánjìng wèntí, gèng shì guānxì dào rénlèi wèilái shēngcún de zhòngdà yìtí.", "Tôi cho rằng đây không chỉ là vấn đề môi trường, mà còn là vấn đề trọng đại liên quan đến sự sinh tồn tương lai của nhân loại."),
            ("A", "那你觉得普通人可以从哪些方面做出改变？", "Nà nǐ juéde pǔtōng rén kěyǐ cóng nǎxiē fāngmiàn zuòchū gǎibiàn?", "Vậy bạn nghĩ người bình thường có thể thay đổi từ những phương diện nào?"),
            ("B", "比如减少一次性用品的使用，尽量选择公共交通，从生活细节做起。", "Bǐrú jiǎnshǎo yícìxìng yòngpǐn de shǐyòng, jǐnliàng xuǎnzé gōnggòng jiāotōng, cóng shēnghuó xìjié zuò qǐ.", "Ví dụ giảm sử dụng đồ dùng một lần, cố gắng chọn giao thông công cộng, bắt đầu từ những chi tiết nhỏ trong cuộc sống."),
            ("A", "除了个人努力，政府和企业是不是应该承担更多责任？", "Chúle gèrén nǔlì, zhèngfǔ hé qǐyè shìbùshì yīnggāi chéngdān gèng duō zérèn?", "Ngoài nỗ lực cá nhân, chính phủ và doanh nghiệp có nên gánh vác nhiều trách nhiệm hơn không?"),
            ("B", "当然，政策的推动和企业的转型往往比个人行为更有影响力。", "Dāngrán, zhèngcè de tuīdòng hé qǐyè de zhuǎnxíng wǎngwǎng bǐ gèrén xíngwéi gèng yǒu yǐngxiǎnglì.", "Đương nhiên, việc thúc đẩy chính sách và chuyển đổi của doanh nghiệp thường có sức ảnh hưởng lớn hơn hành vi cá nhân."),
        ]
    },
    "ai_debate": {
        "title": "Tranh luận về trí tuệ nhân tạo",
        "context": "Bàn về tác động của AI đến việc làm và năng lực cốt lõi của con người.",
        "hsk_level": 8,
        "lines": [
            ("A", "人工智能的迅猛发展让很多人担忧会取代人类的工作，你怎么看？", "Réngōng zhìnéng de xùnměng fāzhǎn ràng hěnduō rén dānyōu huì qǔdài rénlèi de gōngzuò, nǐ zěnme kàn?", "Sự phát triển vũ bão của trí tuệ nhân tạo khiến nhiều người lo ngại sẽ thay thế công việc của con người, bạn nghĩ sao?"),
            ("B", "这种担忧不无道理，但历史上每次技术革命都伴随着新职业的诞生。", "Zhè zhǒng dānyōu bùwú dàolǐ, dàn lìshǐ shàng měicì jìshù gémìng dōu bànsuízhe xīn zhíyè de dànshēng.", "Nỗi lo này không phải không có lý, nhưng trong lịch sử mỗi lần cách mạng công nghệ đều đi kèm sự ra đời của nghề nghiệp mới."),
            ("A", "可是这一次的变革速度似乎比以往任何时候都快得多。", "Kěshì zhè yícì de biàngé sùdù sìhū bǐ yǐwǎng rènhé shíhòu dōu kuài de duō.", "Nhưng lần biến đổi này tốc độ dường như nhanh hơn bất kỳ thời điểm nào trước đây rất nhiều."),
            ("B", "确实如此，这也正是为什么我们需要提前思考教育体系和社会保障的转型。", "Quèshí rúcǐ, zhè yě zhèngshì wèishénme wǒmen xūyào tíqián sīkǎo jiàoyù tǐxì hé shèhuì bǎozhàng de zhuǎnxíng.", "Đúng là vậy, đây cũng chính là lý do tại sao chúng ta cần suy nghĩ trước về việc chuyển đổi hệ thống giáo dục và an sinh xã hội."),
            ("A", "那你认为人类不可取代的核心竞争力是什么？", "Nà nǐ rènwéi rénlèi bùkě qǔdài de héxīn jìngzhēnglì shì shénme?", "Vậy bạn cho rằng năng lực cạnh tranh cốt lõi không thể thay thế của con người là gì?"),
            ("B", "我想是创造力、同理心，以及应对复杂伦理困境的判断力。", "Wǒ xiǎng shì chuàngzàolì, tónglǐxīn, yǐjí yìngduì fùzá lúnlǐ kùnjìng de pànduànlì.", "Tôi nghĩ là sức sáng tạo, sự đồng cảm, và khả năng phán đoán khi đối mặt với những tình huống đạo đức phức tạp."),
        ]
    },
    "traditional_culture": {
        "title": "Trao đổi học thuật về văn hoá truyền thống",
        "context": "Thảo luận cách văn hoá truyền thống giữ bản sắc trong thời toàn cầu hoá.",
        "hsk_level": 9,
        "lines": [
            ("A", "在全球化的浪潮下，你认为传统文化该如何保持其独特性？", "Zài quánqiúhuà de làngcháo xià, nǐ rènwéi chuántǒng wénhuà gāi rúhé bǎochí qí dútèxìng?", "Trong làn sóng toàn cầu hoá, bạn cho rằng văn hoá truyền thống nên giữ gìn tính độc đáo của mình như thế nào?"),
            ("B", "我觉得关键在于创造性转化，而不是一味地固守成规。", "Wǒ juéde guānjiàn zàiyú chuàngzàoxìng zhuǎnhuà, ér búshì yíwèi de gùshǒu chéngguī.", "Tôi cho rằng then chốt là ở sự chuyển hoá mang tính sáng tạo, chứ không phải cứ khư khư bám giữ lề lối cũ."),
            ("A", "能不能举一个具体的例子来说明这种转化？", "Néng bùnéng jǔ yí gè jùtǐ de lìzi lái shuōmíng zhè zhǒng zhuǎnhuà?", "Bạn có thể nêu một ví dụ cụ thể để minh hoạ cho sự chuyển hoá này không?"),
            ("B", "比如说，传统戏曲融入现代舞台技术，既保留了精髓，又吸引了年轻观众。", "Bǐrú shuō, chuántǒng xìqǔ róngrù xiàndài wǔtái jìshù, jì bǎoliúle jīngsuǐ, yòu xīyǐnle niánqīng guānzhòng.", "Ví dụ như, hí kịch truyền thống hoà nhập vào kỹ thuật sân khấu hiện đại, vừa giữ được tinh tuý, vừa thu hút được khán giả trẻ."),
            ("A", "这确实是个很好的思路。但会不会因此失去一些原汁原味的东西？", "Zhè quèshí shì gè hěn hǎo de sīlù. Dàn huì bú huì yīncǐ shīqù yìxiē yuánzhīyuánwèi de dōngxi?", "Đây quả thực là một hướng đi hay. Nhưng liệu có vì thế mà mất đi một số điều nguyên bản không?"),
            ("B", "这是个值得深思的问题，任何变革都需要在传承与创新之间找到平衡。", "Zhè shì gè zhídé shēnsī de wèntí, rènhé biàngé dōu xūyào zài chuánchéng yǔ chuàngxīn zhījiān zhǎodào pínghéng.", "Đây là vấn đề đáng suy nghĩ sâu sắc, bất kỳ sự biến đổi nào cũng cần tìm được sự cân bằng giữa kế thừa và đổi mới."),
        ]
    },
}

def get_dialogues():
    return DIALOGUES

# ========== THEMES ==========
THEMES = {
    "greetings": {
        "name": "Chào hỏi", "icon": "👋", "desc": "Học cách chào hỏi cơ bản",
        "words": ["你好", "您好", "谢谢", "不客气", "对不起", "没关系", "再见", "请", "早上好", "晚上好", "请问"]
    },
    "family": {
        "name": "Gia đình", "icon": "👨‍👩‍👧‍👦", "desc": "Từ vựng về gia đình và người thân",
        "words": ["人", "男人", "女人", "孩子", "朋友", "名字", "大家", "他们", "我们", "你们", "他", "她", "它", "你", "我"]
    },
    "numbers": {
        "name": "Số đếm", "icon": "🔢", "desc": "Học đếm số và lượng",
        "words": ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "零", "百", "千", "半", "几", "多少", "很多"]
    },
    "food": {
        "name": "Đồ ăn", "icon": "🍜", "desc": "Từ vựng về ăn uống và ẩm thực",
        "words": ["吃", "喝", "水", "茶", "咖啡", "米饭", "菜", "水果", "牛奶", "蛋糕", "饿", "渴"]
    },
    "time": {
        "name": "Thời gian", "icon": "⏰", "desc": "Cách nói về thời gian và ngày tháng",
        "words": ["今天", "明天", "昨天", "早上", "中午", "晚上", "现在", "年", "月", "日", "号", "点", "分钟", "星期", "时间", "时候"]
    },
    "study": {
        "name": "Học tập", "icon": "📚", "desc": "Từ vựng về học tập và trường lớp",
        "words": ["学习", "读书", "写", "上课", "学校", "老师", "书", "书包", "笔", "桌子", "椅子", "汉字", "中文", "汉语", "考试"]
    },
    "shopping": {
        "name": "Mua sắm", "icon": "🛒", "desc": "Từ vựng mua bán và thương mại",
        "words": ["买", "卖", "钱", "商店", "多少", "贵", "便宜", "手机", "电脑", "电话", "颜色"]
    },
    "actions": {
        "name": "Hành động", "icon": "🏃", "desc": "Các động từ thường dùng hàng ngày",
        "words": ["去", "来", "做", "看", "听", "说", "读", "写", "叫", "会", "能", "想", "要", "喜欢", "爱", "知道", "认识"]
    },
    "travel": {
        "name": "Du lịch", "icon": "✈️", "desc": "Từ vựng khi đi du lịch và di chuyển",
        "words": ["去", "来", "回家", "机场", "火车站", "旅馆", "房间", "旅行", "游泳", "海滩"]
    },
    "colors": {
        "name": "Màu sắc", "icon": "🎨", "desc": "Tên các màu sắc cơ bản",
        "words": ["红色", "白色", "黑色", "蓝色", "绿色", "黄色", "颜色"]
    },
    # HSK 3-9 mở rộng nhiều vào từ vựng trừu tượng/chuyên ngành mà 10 chủ đề
    # gốc (vốn thiên về đời sống cơ bản HSK1-2) không phủ tới — các chủ đề
    # dưới đây không có danh sách tay, được lấp đầy hoàn toàn bằng
    # auto_categorize_theme_words() theo từ khoá trong THEME_KEYWORDS.
    "work": {
        "name": "Công việc", "icon": "💼", "desc": "Từ vựng công sở, nghề nghiệp, kinh doanh",
        "words": []
    },
    "emotions": {
        "name": "Cảm xúc & tính cách", "icon": "😊", "desc": "Diễn tả cảm xúc, tâm trạng và tính cách",
        "words": []
    },
    "health": {
        "name": "Sức khỏe", "icon": "🏥", "desc": "Cơ thể, bệnh tật, khám chữa bệnh",
        "words": []
    },
    "society": {
        "name": "Xã hội & thời sự", "icon": "📰", "desc": "Chính trị, pháp luật, kinh tế, tin tức",
        "words": []
    },
    "nature": {
        "name": "Thiên nhiên & môi trường", "icon": "🌳", "desc": "Cây cối, thời tiết, động vật, môi trường",
        "words": []
    },
    "tech": {
        "name": "Công nghệ & khoa học", "icon": "💻", "desc": "Máy tính, internet, khoa học kỹ thuật",
        "words": []
    },
}

# Từ khoá tiếng Việt (khớp trên trường `meanings`) dùng để tự động gán chủ đề
# cho toàn bộ từ vựng HSK 1-9 — bù cho việc 10 chủ đề gốc chỉ được biên soạn
# tay cho ~118 từ HSK1/2. Chạy bởi auto_categorize_theme_words(), idempotent.
THEME_KEYWORDS = {
    "greetings": ["chào", "cảm ơn", "xin lỗi", "tạm biệt", "làm ơn", "xin phép", "hân hạnh", "kính chào"],
    "family": ["bố", "cha", "mẹ", "con trai", "con gái", "anh", "chị", "em", "ông", "bà", "cháu", "vợ", "chồng",
               "gia đình", "họ hàng", "cô", "bác", "dì", "cậu", "cô chú", "người thân", "gia tộc"],
    "numbers": ["một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười", "trăm", "nghìn", "vạn",
                "triệu", "số lượng", "đếm", "phần trăm", "tỷ lệ", "con số", "số thứ tự"],
    "food": ["ăn", "uống", "món ăn", "cơm", "canh", "thịt", "cá", "rau", "trái cây", "hoa quả", "nước", "trà",
             "cà phê", "sữa", "bánh", "đói", "khát", "hương vị", "vị giác", "ngon", "nấu", "nhà bếp",
             "thực phẩm", "dinh dưỡng", "gia vị", "nhà hàng", "quán ăn", "đồ uống", "rượu", "bữa"],
    "time": ["hôm nay", "ngày mai", "hôm qua", "buổi sáng", "buổi trưa", "buổi chiều", "buổi tối", "ban đêm",
             "giờ", "phút", "giây", "tuần", "tháng", "thời gian", "lịch", "sớm", "muộn", "hiện tại", "quá khứ",
             "tương lai", "thời điểm", "thời kỳ", "kỳ hạn", "thời hạn", "lúc"],
    "study": ["học", "đọc", "viết", "trường", "lớp học", "giáo viên", "học sinh", "sinh viên", "sách", "bút",
              "bài tập", "thi", "kiểm tra", "kiến thức", "nghiên cứu", "giáo dục", "đại học", "chữ hán",
              "tiếng trung", "môn học", "giáo trình", "bằng cấp", "học vị", "luận văn", "giảng dạy"],
    "shopping": ["mua", "bán", "tiền", "giá cả", "đắt", "rẻ", "cửa hàng", "siêu thị", "chợ", "hàng hóa",
                 "thanh toán", "giảm giá", "khuyến mãi", "hóa đơn", "mặc cả", "sản phẩm", "kinh doanh",
                 "thương mại", "tiêu dùng", "khách hàng"],
    "actions": ["đi", "đến", "chạy", "nhảy", "đứng", "ngồi", "nằm", "mở", "đóng", "cầm", "mang", "đưa", "lấy",
                "đặt", "ném", "kéo", "đẩy", "leo", "bò", "bay"],
    "travel": ["du lịch", "đi chơi", "máy bay", "sân bay", "tàu hỏa", "xe lửa", "khách sạn", "hộ chiếu", "vé",
               "hành lý", "bãi biển", "phong cảnh", "tham quan", "chuyến đi", "nghỉ mát", "visa", "hướng dẫn viên"],
    "colors": ["màu", "đỏ", "trắng", "đen", "xanh", "vàng", "tím", "hồng", "nâu", "xám", "cam"],
    "work": ["công việc", "làm việc", "công ty", "nhân viên", "giám đốc", "sếp", "đồng nghiệp", "lương",
             "nghề nghiệp", "chức vụ", "hợp đồng", "cuộc họp", "dự án", "văn phòng", "nghỉ việc", "tuyển dụng",
             "phỏng vấn", "kỹ năng", "chuyên môn", "quản lý", "nhân sự", "xí nghiệp", "doanh nghiệp", "cấp trên",
             "cấp dưới", "báo cáo", "nghỉ phép"],
    "emotions": ["vui", "buồn", "giận", "sợ hãi", "lo lắng", "hạnh phúc", "tức giận", "yêu thương", "ghét",
                 "cảm động", "ngạc nhiên", "hồi hộp", "thất vọng", "hài lòng", "tự hào", "xấu hổ", "cô đơn",
                 "tính cách", "tình cảm", "cảm xúc", "cảm giác", "tâm trạng", "kiên nhẫn", "khiêm tốn", "tự tin"],
    "health": ["bệnh", "ốm", "đau", "sức khỏe", "bác sĩ", "bệnh viện", "thuốc", "khám bệnh", "chữa bệnh",
               "cơ thể", "sốt", "ho", "cảm cúm", "y tá", "phẫu thuật", "dinh dưỡng", "thể dục", "tập luyện",
               "mệt mỏi", "khỏe mạnh", "tiêm", "vắc xin", "sức khoẻ"],
    "society": ["xã hội", "chính phủ", "pháp luật", "kinh tế", "chính trị", "tin tức", "báo chí", "sự kiện",
                "quốc gia", "chính sách", "cộng đồng", "dân số", "quyền lợi", "an ninh", "luật pháp", "tòa án",
                "bầu cử", "quốc hội", "công dân", "quốc tế"],
    "nature": ["cây", "hoa", "núi", "sông", "biển", "bầu trời", "mưa", "nắng", "gió", "tuyết", "động vật",
               "thiên nhiên", "môi trường", "sinh vật", "rừng", "khí hậu", "trái đất", "vũ trụ", "mặt trời",
               "mặt trăng", "sinh thái", "ô nhiễm", "hồ", "đảo"],
    "tech": ["máy tính", "điện thoại", "internet", "công nghệ", "khoa học", "kỹ thuật", "phần mềm",
             "mạng lưới", "trên mạng", "lên mạng", "cư dân mạng", "dữ liệu", "thiết bị", "phát minh",
             "trí tuệ nhân tạo", "robot", "kỹ sư", "hệ thống", "ứng dụng", "lập trình", "số hóa", "điện tử"],
}

# Known collisions where a single-syllable keyword (highly reusable in
# Vietnamese) shows up inside an unrelated compound gloss — caught by manual
# spot-checking auto_categorize_theme_words() output. "mạng" was dropped
# entirely from THEME_KEYWORDS above (bare "mạng" hits life/fate/revolution
# far more than network: cách mạng, tính mạng, sứ mạng, liều mạng...) in
# favor of multi-word phrases; "hoa" and "cây" stay bare (mostly accurate)
# with their specific bad hits excluded here. Extend as more surface.
THEME_KEYWORD_EXCLUDE = {
    ("nature", "hoa"): [
        "chữ hoa", "trung hoa", "hoa kiều", "người hoa", "tiếng hoa",  # Hoa = Chinese, not flower
        "sa hoa", "xa hoa", "ba hoa", "tài hoa", "phồn hoa", "hoa lệ", "tinh hoa",  # idioms
        "hoa tai",  # earring
    ],
    ("nature", "cây"): ["cây số"],  # km marker, not a tree
    ("time", "lịch"): ["lịch sử", "lịch sự", "lịch lãm", "lý lịch"],
    ("food", "nước"): [
        "nước ngoài", "nhà nước", "đất nước", "cả nước", "trong nước", "về nước", "yêu nước", "toàn quốc",
        "việc nước", "ngoại quốc", "quốc gia",
    ],  # nước = country/state here, not water
    ("shopping", "tiền"): [
        "tiền bối", "tiền lệ", "tiền nhiệm", "tiền tuyến", "tiền đề", "tiền sử", "tiền phong",
    ],  # tiền = "pre-/former" here, not money
    ("family", "cô"): ["cô ấy", "của cô", "cô đơn", "cô độc", "thầy cô", "cô lập", "cô gái"],
    ("family", "bác"): ["bác sĩ", "bác bỏ", "đại bác", "bác học"],
}


def _keyword_in_meanings(meanings_lower: str, keyword: str, theme_id: str) -> bool:
    """Multi-word keywords (contain a space) match as a substring; single-word
    keywords must match a whole gloss token, to avoid accidental substring
    hits inside unrelated Vietnamese words. THEME_KEYWORD_EXCLUDE vetoes
    specific known-bad (theme, keyword) collisions regardless of match type."""
    exclusions = THEME_KEYWORD_EXCLUDE.get((theme_id, keyword))
    if exclusions and any(bad in meanings_lower for bad in exclusions):
        return False
    if " " in keyword:
        return keyword in meanings_lower
    return any(keyword in gloss.strip().split() for gloss in meanings_lower.split(","))


def auto_categorize_theme_words(conn):
    """Rule-based topic tagging for every word in the DB (mainly HSK 3-9,
    which has no hand-curated theme list): matches each word's Vietnamese
    `meanings` against THEME_KEYWORDS and links matches into theme_words.
    Idempotent — skips (theme, word) pairs already linked, so it's safe to
    call on every startup as the vocab set grows."""
    existing_pairs = {
        (r["theme_id"], r["word_id"])
        for r in conn.execute("SELECT theme_id, word_id FROM theme_words").fetchall()
    }
    next_sort = {}
    for r in conn.execute("SELECT theme_id, MAX(sort_order) m FROM theme_words GROUP BY theme_id").fetchall():
        next_sort[r["theme_id"]] = (r["m"] or 0) + 1

    words = conn.execute("SELECT id, meanings FROM words").fetchall()
    inserted = 0
    for theme_id, keywords in THEME_KEYWORDS.items():
        for w in words:
            key = (theme_id, w["id"])
            if key in existing_pairs:
                continue
            meanings_lower = w["meanings"].lower()
            if any(_keyword_in_meanings(meanings_lower, kw, theme_id) for kw in keywords):
                order = next_sort.get(theme_id, 0)
                conn.execute(
                    "INSERT INTO theme_words (theme_id, word_id, sort_order) VALUES (?, ?, ?)",
                    (theme_id, w["id"], order)
                )
                next_sort[theme_id] = order + 1
                existing_pairs.add(key)
                inserted += 1
    conn.commit()
    if inserted:
        print(f"Auto-categorized {inserted} theme_word links")


def get_theme_words(theme_id):
    """Get list of word simplified characters for a theme"""
    theme = THEMES.get(theme_id)
    if not theme:
        return []
    return theme["words"]

# ========== BADGES (huy hiệu) ==========
BADGES = {
    "streak_3":    {"name": "3 ngày liên tiếp",       "icon": "🔥", "desc": "Học 3 ngày liên tục"},
    "streak_7":    {"name": "Một tuần bền bỉ",        "icon": "🔥", "desc": "Học 7 ngày liên tục"},
    "streak_30":   {"name": "Một tháng kiên trì",     "icon": "🏆", "desc": "Học 30 ngày liên tục"},
    "words_50":    {"name": "50 từ thuộc lòng",       "icon": "📖", "desc": "Thuộc 50 từ vựng"},
    "words_150":   {"name": "Bậc thầy từ vựng",       "icon": "🎓", "desc": "Thuộc 150 từ vựng"},
    "reviews_100": {"name": "Ôn tập chăm chỉ",        "icon": "💪", "desc": "Hoàn thành 100 lượt ôn tập"},
    "writer_10":   {"name": "Tập viết chữ",           "icon": "✍️", "desc": "Luyện viết 10 chữ Hán"},
    "writer_50":   {"name": "Cao thủ viết chữ",       "icon": "🖌️", "desc": "Luyện viết 50 chữ Hán"},
    "xp_500":      {"name": "500 điểm kinh nghiệm",   "icon": "⭐", "desc": "Đạt 500 XP"},
    "xp_2000":     {"name": "2000 điểm kinh nghiệm",  "icon": "🌟", "desc": "Đạt 2000 XP"},
    "exam_first_pass":    {"name": "Thi thử đầu tiên",   "icon": "📝", "desc": "Đạt một bài thi thử"},
    "exam_tier_so_cap":   {"name": "Vượt qua Sơ cấp",    "icon": "🥉", "desc": "Đạt bài thi thử HSK 1-3"},
    "exam_tier_trung_cap":{"name": "Vượt qua Trung cấp", "icon": "🥈", "desc": "Đạt bài thi thử HSK 4-6"},
    "exam_tier_cao_cap":  {"name": "Vượt qua Cao cấp",   "icon": "🥇", "desc": "Đạt bài thi thử HSK 7-9"},
}

def get_badges():
    return BADGES
