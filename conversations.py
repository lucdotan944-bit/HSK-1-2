"""Hội thoại phân nhánh (scripted branching dialogue) để luyện phản xạ giao tiếp.

Thay thế "hội thoại mô phỏng với AI" bằng cây hội thoại viết sẵn — không gọi
LLM/API trả phí. Học viên chọn (hoặc nói) câu trả lời, cây tiến tới nhánh
tương ứng. Dữ liệu tĩnh, cùng dạng với bảng `dialogues` trong seed_data.py.
"""

CONVERSATIONS = {
    "order_food": {
        "title": "Gọi món ở quán ăn",
        "hsk_level": 1,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "你好！你要吃什么？", "pinyin": "nǐ hǎo! nǐ yào chī shén me?", "vi": "Chào bạn! Bạn muốn ăn gì?"},
                "choices": [
                    {"id": "a", "cn": "我要一个米饭。", "pinyin": "wǒ yào yí gè mǐfàn.", "vi": "Tôi muốn một phần cơm.", "next": "n2"},
                    {"id": "b", "cn": "我想看看菜单。", "pinyin": "wǒ xiǎng kàn kan càidān.", "vi": "Tôi muốn xem thực đơn.", "next": "n2b"},
                ],
            },
            "n2b": {
                "npc": {"cn": "好的，这是菜单。", "pinyin": "hǎo de, zhè shì càidān.", "vi": "Được, đây là thực đơn."},
                "choices": [
                    {"id": "a", "cn": "我要一个米饭。", "pinyin": "wǒ yào yí gè mǐfàn.", "vi": "Tôi muốn một phần cơm.", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "你要喝什么？", "pinyin": "nǐ yào hē shén me?", "vi": "Bạn muốn uống gì?"},
                "choices": [
                    {"id": "a", "cn": "我要喝茶。", "pinyin": "wǒ yào hē chá.", "vi": "Tôi muốn uống trà.", "next": "n3"},
                    {"id": "b", "cn": "我要喝水。", "pinyin": "wǒ yào hē shuǐ.", "vi": "Tôi muốn uống nước.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "好，请等一下。", "pinyin": "hǎo, qǐng děng yí xià.", "vi": "Được, xin chờ một chút."},
                "choices": [
                    {"id": "a", "cn": "谢谢！", "pinyin": "xiè xie!", "vi": "Cảm ơn!", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!"},
                "choices": [],
            },
        },
    },
    "ask_direction": {
        "title": "Hỏi đường",
        "hsk_level": 1,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "请问，医院在哪儿？", "pinyin": "qǐng wèn, yīyuàn zài nǎr?", "vi": "Xin hỏi, bệnh viện ở đâu?"},
                "choices": [
                    {"id": "a", "cn": "对不起，我不知道。", "pinyin": "duì bu qǐ, wǒ bù zhī dào.", "vi": "Xin lỗi, tôi không biết.", "next": "end_unknown"},
                    {"id": "b", "cn": "医院在前面。", "pinyin": "yīyuàn zài qián miàn.", "vi": "Bệnh viện ở phía trước.", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "谢谢你！很远吗？", "pinyin": "xiè xie nǐ! hěn yuǎn ma?", "vi": "Cảm ơn bạn! Có xa không?"},
                "choices": [
                    {"id": "a", "cn": "不远，走五分钟。", "pinyin": "bù yuǎn, zǒu wǔ fēn zhōng.", "vi": "Không xa, đi bộ năm phút.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "太好了，谢谢！", "pinyin": "tài hǎo le, xiè xie!", "vi": "Tuyệt quá, cảm ơn!"},
                "choices": [],
            },
            "end_unknown": {
                "npc": {"cn": "没关系，谢谢。", "pinyin": "méi guān xi, xiè xie.", "vi": "Không sao, cảm ơn."},
                "choices": [],
            },
        },
    },
    "shopping": {
        "title": "Mua sắm",
        "hsk_level": 2,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "欢迎光临！你想买什么？", "pinyin": "huān yíng guāng lín! nǐ xiǎng mǎi shén me?", "vi": "Chào mừng! Bạn muốn mua gì?"},
                "choices": [
                    {"id": "a", "cn": "这件衣服多少钱？", "pinyin": "zhè jiàn yī fu duō shǎo qián?", "vi": "Cái áo này bao nhiêu tiền?", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "一百块。", "pinyin": "yì bǎi kuài.", "vi": "Một trăm tệ."},
                "choices": [
                    {"id": "a", "cn": "太贵了，便宜一点吧。", "pinyin": "tài guì le, pián yi yì diǎn ba.", "vi": "Đắt quá, rẻ hơn chút đi.", "next": "n3"},
                    {"id": "b", "cn": "好，我要买。", "pinyin": "hǎo, wǒ yào mǎi.", "vi": "Được, tôi mua.", "next": "end"},
                ],
            },
            "n3": {
                "npc": {"cn": "好吧，八十块。", "pinyin": "hǎo ba, bā shí kuài.", "vi": "Được rồi, tám mươi tệ."},
                "choices": [
                    {"id": "a", "cn": "谢谢，我要买。", "pinyin": "xiè xie, wǒ yào mǎi.", "vi": "Cảm ơn, tôi mua.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "谢谢惠顾！", "pinyin": "xiè xie huì gù!", "vi": "Cảm ơn đã mua hàng!"},
                "choices": [],
            },
        },
    },
    # HSK 3-9: mỗi cấp 1 kịch bản phân nhánh, chủ đề/độ khó tăng dần theo cấp
    # — trước đây chỉ có 3 kịch bản, toàn bộ HSK 1-2.
    "book_hotel": {
        "title": "Đặt phòng khách sạn",
        "hsk_level": 3,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "您好，请问需要帮忙吗？", "pinyin": "nín hǎo, qǐng wèn xūyào bāngmáng ma?", "vi": "Xin chào, anh/chị cần giúp gì không?"},
                "choices": [
                    {"id": "a", "cn": "我想订一个房间。", "pinyin": "wǒ xiǎng dìng yí gè fángjiān.", "vi": "Tôi muốn đặt một phòng.", "next": "n2"},
                    {"id": "b", "cn": "请问还有空房间吗？", "pinyin": "qǐngwèn hái yǒu kòng fángjiān ma?", "vi": "Xin hỏi còn phòng trống không?", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "有的，您想要什么样的房间？", "pinyin": "yǒu de, nín xiǎng yào shénme yàng de fángjiān?", "vi": "Có ạ, anh/chị muốn phòng như thế nào?"},
                "choices": [
                    {"id": "a", "cn": "我要一个单人房间。", "pinyin": "wǒ yào yí gè dānrén fángjiān.", "vi": "Tôi muốn một phòng đơn.", "next": "n3"},
                    {"id": "b", "cn": "我要一个双人房间。", "pinyin": "wǒ yào yí gè shuāngrén fángjiān.", "vi": "Tôi muốn một phòng đôi.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "好的，一晚三百块，您住几天？", "pinyin": "hǎo de, yì wǎn sānbǎi kuài, nín zhù jǐ tiān?", "vi": "Được, một đêm 300 tệ, anh/chị ở mấy ngày?"},
                "choices": [
                    {"id": "a", "cn": "我住两天。", "pinyin": "wǒ zhù liǎng tiān.", "vi": "Tôi ở hai ngày.", "next": "n4"},
                    {"id": "b", "cn": "太贵了，能不能便宜点儿？", "pinyin": "tài guì le, néng bùnéng piányi diǎnr?", "vi": "Đắt quá, có rẻ hơn được không?", "next": "n4b"},
                ],
            },
            "n4b": {
                "npc": {"cn": "好吧，给您打九折。", "pinyin": "hǎo ba, gěi nín dǎ jiǔ zhé.", "vi": "Được, giảm 10% cho anh/chị."},
                "choices": [
                    {"id": "a", "cn": "谢谢，我住两天。", "pinyin": "xièxie, wǒ zhù liǎng tiān.", "vi": "Cảm ơn, tôi ở hai ngày.", "next": "n4"},
                ],
            },
            "n4": {
                "npc": {"cn": "好的，请给我看一下您的护照。", "pinyin": "hǎo de, qǐng gěi wǒ kàn yíxià nín de hùzhào.", "vi": "Được, cho tôi xem hộ chiếu của anh/chị."},
                "choices": [
                    {"id": "a", "cn": "给你。", "pinyin": "gěi nǐ.", "vi": "Đây ạ.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "谢谢，祝您入住愉快！", "pinyin": "xièxie, zhù nín rùzhù yúkuài!", "vi": "Cảm ơn, chúc anh/chị ở lại vui vẻ!"},
                "choices": [],
            },
        },
    },
    "return_item": {
        "title": "Đổi trả hàng",
        "hsk_level": 4,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "您好，请问有什么可以帮您？", "pinyin": "nín hǎo, qǐngwèn yǒu shénme kěyǐ bāng nín?", "vi": "Xin chào, tôi có thể giúp gì ạ?"},
                "choices": [
                    {"id": "a", "cn": "这件衣服有点问题，我想退货。", "pinyin": "zhè jiàn yīfu yǒudiǎn wèntí, wǒ xiǎng tuìhuò.", "vi": "Cái áo này có vấn đề, tôi muốn trả hàng.", "next": "n2"},
                    {"id": "b", "cn": "这个不合适，我想换一下。", "pinyin": "zhège bù héshì, wǒ xiǎng huàn yíxià.", "vi": "Cái này không hợp, tôi muốn đổi.", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "请问是什么问题呢？", "pinyin": "qǐngwèn shì shénme wèntí ne?", "vi": "Xin hỏi vấn đề là gì ạ?"},
                "choices": [
                    {"id": "a", "cn": "尺寸不对，太小了。", "pinyin": "chǐcùn bú duì, tài xiǎo le.", "vi": "Kích cỡ không đúng, nhỏ quá.", "next": "n3"},
                    {"id": "b", "cn": "颜色跟图片不一样。", "pinyin": "yánsè gēn túpiàn bù yíyàng.", "vi": "Màu sắc không giống hình.", "next": "n3"},
                ],
            },
            "n2b": {
                "npc": {"cn": "好的，您想换成什么？", "pinyin": "hǎo de, nín xiǎng huàn chéng shénme?", "vi": "Được, anh/chị muốn đổi thành gì?"},
                "choices": [
                    {"id": "a", "cn": "我想换大一号的。", "pinyin": "wǒ xiǎng huàn dà yí hào de.", "vi": "Tôi muốn đổi cỡ lớn hơn.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "没问题，您有购物小票吗？", "pinyin": "méi wèntí, nín yǒu gòuwù xiǎopiào ma?", "vi": "Không vấn đề gì, anh/chị có hóa đơn không?"},
                "choices": [
                    {"id": "a", "cn": "有，给你。", "pinyin": "yǒu, gěi nǐ.", "vi": "Có, đây ạ.", "next": "end"},
                    {"id": "b", "cn": "不好意思，我找不到了。", "pinyin": "bù hǎoyìsi, wǒ zhǎo bú dào le.", "vi": "Xin lỗi, tôi không tìm thấy.", "next": "end_no_receipt"},
                ],
            },
            "end": {
                "npc": {"cn": "好的，已经帮您处理好了。", "pinyin": "hǎo de, yǐjīng bāng nín chǔlǐ hǎo le.", "vi": "Được, tôi đã xử lý xong cho anh/chị."},
                "choices": [],
            },
            "end_no_receipt": {
                "npc": {"cn": "没有小票的话，可能需要一点时间处理，麻烦您稍等。", "pinyin": "méiyǒu xiǎopiào dehuà, kěnéng xūyào yìdiǎn shíjiān chǔlǐ, máfan nín shāo děng.", "vi": "Không có hóa đơn thì có thể cần chút thời gian xử lý, phiền anh/chị đợi một chút."},
                "choices": [],
            },
        },
    },
    "apartment_rental": {
        "title": "Thuê nhà",
        "hsk_level": 5,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "你好，你是来看房子的吧？", "pinyin": "nǐ hǎo, nǐ shì lái kàn fángzi de ba?", "vi": "Chào bạn, bạn đến xem nhà phải không?"},
                "choices": [
                    {"id": "a", "cn": "对，请问这套房子月租多少钱？", "pinyin": "duì, qǐngwèn zhè tào fángzi yuèzū duōshao qián?", "vi": "Đúng vậy, xin hỏi căn này giá thuê tháng bao nhiêu?", "next": "n2"},
                    {"id": "b", "cn": "是的，附近方便吗？", "pinyin": "shì de, fùjìn fāngbiàn ma?", "vi": "Vâng, khu này có tiện không?", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "月租三千五，还包水电。", "pinyin": "yuèzū sānqiān wǔ, hái bāo shuǐdiàn.", "vi": "Giá thuê 3500 tệ/tháng, đã bao gồm điện nước."},
                "choices": [
                    {"id": "a", "cn": "有点贵，能不能商量一下？", "pinyin": "yǒudiǎn guì, néng bùnéng shāngliang yíxià?", "vi": "Hơi đắt, thương lượng chút được không?", "next": "n3"},
                    {"id": "b", "cn": "好的，我很满意，可以签合同吗？", "pinyin": "hǎo de, wǒ hěn mǎnyì, kěyǐ qiān hétong ma?", "vi": "Được, tôi rất hài lòng, ký hợp đồng được chứ?", "next": "n4"},
                ],
            },
            "n2b": {
                "npc": {"cn": "很方便，附近有地铁站和超市。", "pinyin": "hěn fāngbiàn, fùjìn yǒu dìtiězhàn hé chāoshì.", "vi": "Rất tiện, gần đó có ga tàu điện ngầm và siêu thị."},
                "choices": [
                    {"id": "a", "cn": "听起来不错，月租多少？", "pinyin": "tīng qǐlái búcuò, yuèzū duōshao?", "vi": "Nghe cũng ổn, giá thuê tháng bao nhiêu?", "next": "n2"},
                ],
            },
            "n3": {
                "npc": {"cn": "那这样吧，三千二，怎么样？", "pinyin": "nà zhèyàng ba, sānqiān èr, zěnmeyàng?", "vi": "Vậy thế này, 3200 tệ, được không?"},
                "choices": [
                    {"id": "a", "cn": "好，就这个价格吧。", "pinyin": "hǎo, jiù zhège jiàgé ba.", "vi": "Được, vậy giá này nhé.", "next": "n4"},
                ],
            },
            "n4": {
                "npc": {"cn": "好的，那我们签合同吧，押一付三。", "pinyin": "hǎo de, nà wǒmen qiān hétong ba, yā yī fù sān.", "vi": "Được, vậy ta ký hợp đồng nhé, đặt cọc 1 tháng trả trước 3 tháng."},
                "choices": [
                    {"id": "a", "cn": "没问题。", "pinyin": "méi wèntí.", "vi": "Không vấn đề gì.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "欢迎入住！", "pinyin": "huānyíng rùzhù!", "vi": "Chào mừng bạn đến ở!"},
                "choices": [],
            },
        },
    },
    "customer_complaint": {
        "title": "Khiếu nại dịch vụ khách sạn",
        "hsk_level": 6,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "您好，请问需要什么帮助？", "pinyin": "nín hǎo, qǐngwèn xūyào shénme bāngzhù?", "vi": "Xin chào, anh/chị cần giúp gì ạ?"},
                "choices": [
                    {"id": "a", "cn": "我们房间的空调坏了，一直不制冷。", "pinyin": "wǒmen fángjiān de kōngtiáo huài le, yìzhí bú zhìlěng.", "vi": "Điều hòa phòng chúng tôi hỏng, không mát được.", "next": "n2"},
                    {"id": "b", "cn": "楼上太吵了，我们完全没办法休息。", "pinyin": "lóushàng tài chǎo le, wǒmen wánquán méi bànfǎ xiūxi.", "vi": "Trên lầu ồn quá, chúng tôi hoàn toàn không nghỉ ngơi được.", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "非常抱歉给您带来不便，我马上安排人来检修。", "pinyin": "fēicháng bàoqiàn gěi nín dàilái búbiàn, wǒ mǎshàng ānpái rén lái jiǎnxiū.", "vi": "Rất xin lỗi vì sự bất tiện này, tôi sẽ cho người đến sửa ngay."},
                "choices": [
                    {"id": "a", "cn": "谢谢，希望能尽快解决。", "pinyin": "xièxie, xīwàng néng jǐnkuài jiějué.", "vi": "Cảm ơn, mong sớm giải quyết.", "next": "n3"},
                ],
            },
            "n2b": {
                "npc": {"cn": "十分抱歉，我们会立刻联系楼上客人，请他们注意音量。", "pinyin": "shífēn bàoqiàn, wǒmen huì lìkè liánxì lóushàng kèrén, qǐng tāmen zhùyì yīnliàng.", "vi": "Rất xin lỗi, chúng tôi sẽ liên hệ ngay với khách trên lầu, nhắc họ chú ý âm lượng."},
                "choices": [
                    {"id": "a", "cn": "谢谢你的处理。", "pinyin": "xièxie nǐ de chǔlǐ.", "vi": "Cảm ơn bạn đã xử lý.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "为了表示歉意，我们可以为您免除今晚的房费，您看可以吗？", "pinyin": "wèile biǎoshì qiànyì, wǒmen kěyǐ wèi nín miǎnchú jīnwǎn de fángfèi, nín kàn kěyǐ ma?", "vi": "Để tỏ lòng xin lỗi, chúng tôi có thể miễn phí tiền phòng tối nay, anh/chị thấy được không?"},
                "choices": [
                    {"id": "a", "cn": "那太好了，谢谢你们的诚意。", "pinyin": "nà tài hǎo le, xièxie nǐmen de chéngyì.", "vi": "Vậy tốt quá, cảm ơn sự chân thành của các bạn.", "next": "end"},
                    {"id": "b", "cn": "没关系，只要问题解决就行。", "pinyin": "méi guānxi, zhǐyào wèntí jiějué jiùxíng.", "vi": "Không sao, chỉ cần giải quyết được vấn đề là được.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "再次为给您带来的不便道歉，祝您入住愉快！", "pinyin": "zàicì wèi gěi nín dàilái de búbiàn dàoqiàn, zhù nín rùzhù yúkuài!", "vi": "Một lần nữa xin lỗi vì sự bất tiện, chúc anh/chị ở lại vui vẻ!"},
                "choices": [],
            },
        },
    },
    "environment_choice": {
        "title": "Thảo luận chọn phương án bảo vệ môi trường",
        "hsk_level": 7,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "针对社区垃圾分类的问题，你觉得我们应该优先推广哪种方案？", "pinyin": "zhēnduì shèqū lājī fēnlèi de wèntí, nǐ juéde wǒmen yīnggāi yōuxiān tuīguǎng nǎ zhǒng fāng'àn?", "vi": "Về vấn đề phân loại rác trong khu dân cư, bạn nghĩ chúng ta nên ưu tiên triển khai phương án nào?"},
                "choices": [
                    {"id": "a", "cn": "我认为应该先从教育入手，提高居民的环保意识。", "pinyin": "wǒ rènwéi yīnggāi xiān cóng jiàoyù rùshǒu, tígāo jūmín de huánbǎo yìshí.", "vi": "Tôi nghĩ nên bắt đầu từ giáo dục, nâng cao ý thức bảo vệ môi trường của người dân.", "next": "n2"},
                    {"id": "b", "cn": "我觉得应该先制定强制性的分类规定，效果更直接。", "pinyin": "wǒ juéde yīnggāi xiān zhìdìng qiángzhìxìng de fēnlèi guīdìng, xiàoguǒ gèng zhíjiē.", "vi": "Tôi nghĩ nên ban hành quy định bắt buộc phân loại trước, hiệu quả trực tiếp hơn.", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "教育确实重要，但见效可能比较慢，你觉得该怎么加快这个过程？", "pinyin": "jiàoyù quèshí zhòngyào, dàn jiànxiào kěnéng bǐjiào màn, nǐ juéde gāi zěnme jiākuài zhège guòchéng?", "vi": "Giáo dục đúng là quan trọng, nhưng hiệu quả có thể chậm, bạn nghĩ nên đẩy nhanh quá trình này thế nào?"},
                "choices": [
                    {"id": "a", "cn": "可以结合社区活动和奖励机制，鼓励大家参与。", "pinyin": "kěyǐ jiéhé shèqū huódòng hé jiǎnglì jīzhì, gǔlì dàjiā cānyù.", "vi": "Có thể kết hợp hoạt động cộng đồng và cơ chế khen thưởng để khuyến khích mọi người tham gia.", "next": "n3"},
                ],
            },
            "n2b": {
                "npc": {"cn": "强制规定确实立竿见影，但推行初期可能会遇到居民的抵触，你怎么看？", "pinyin": "qiángzhì guīdìng quèshí lìgānjiànyǐng, dàn tuīxíng chūqī kěnéng huì yùdào jūmín de dǐchù, nǐ zěnme kàn?", "vi": "Quy định bắt buộc đúng là hiệu quả tức thì, nhưng giai đoạn đầu triển khai có thể gặp phản ứng từ người dân, bạn nghĩ sao?"},
                "choices": [
                    {"id": "a", "cn": "可以先试点，再逐步推广到全社区。", "pinyin": "kěyǐ xiān shìdiǎn, zài zhúbù tuīguǎng dào quán shèqū.", "vi": "Có thể thí điểm trước, rồi từng bước mở rộng ra toàn khu dân cư.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "你的想法很有建设性，那我们就把它写进这次的提案里吧。", "pinyin": "nǐ de xiǎngfǎ hěn yǒu jiànshèxìng, nà wǒmen jiù bǎ tā xiě jìn zhè cì de tí'àn lǐ ba.", "vi": "Ý kiến của bạn rất mang tính xây dựng, vậy chúng ta đưa nó vào đề án lần này nhé."},
                "choices": [
                    {"id": "a", "cn": "好的，希望这个方案真的能落实下去。", "pinyin": "hǎo de, xīwàng zhège fāng'àn zhēnde néng luòshí xiàqù.", "vi": "Được, hy vọng phương án này thực sự được triển khai.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "谢谢你的参与，这次讨论很有价值。", "pinyin": "xièxie nǐ de cānyù, zhè cì tǎolùn hěn yǒu jiàzhí.", "vi": "Cảm ơn bạn đã tham gia, buổi thảo luận lần này rất có giá trị."},
                "choices": [],
            },
        },
    },
    "business_negotiation": {
        "title": "Đàm phán hợp đồng kinh doanh",
        "hsk_level": 8,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "关于这次合作的价格，贵方的报价似乎比市场行情高出不少。", "pinyin": "guānyú zhè cì hézuò de jiàgé, guì fāng de bàojià sìhū bǐ shìchǎng xíngqíng gāo chū bùshǎo.", "vi": "Về giá hợp tác lần này, mức giá phía quý công ty đưa ra dường như cao hơn khá nhiều so với mặt bằng thị trường."},
                "choices": [
                    {"id": "a", "cn": "我们的产品在品质和售后服务上更有保障，这也是成本的一部分。", "pinyin": "wǒmen de chǎnpǐn zài pǐnzhì hé shòuhòu fúwù shàng gèng yǒu bǎozhàng, zhè yě shì chéngběn de yíbùfen.", "vi": "Sản phẩm của chúng tôi được đảm bảo hơn về chất lượng và hậu mãi, đây cũng là một phần chi phí.", "next": "n2"},
                    {"id": "b", "cn": "如果贵公司能签订长期合同，我们可以考虑调整价格。", "pinyin": "rúguǒ guì gōngsī néng qiāndìng chángqī hétong, wǒmen kěyǐ kǎolǜ tiáozhěng jiàgé.", "vi": "Nếu quý công ty ký hợp đồng dài hạn, chúng tôi có thể cân nhắc điều chỉnh giá.", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "品质我们认可，但预算方面确实有限，能不能在其他方面做出让步？", "pinyin": "pǐnzhì wǒmen rènkě, dàn yùsuàn fāngmiàn quèshí yǒuxiàn, néng bùnéng zài qítā fāngmiàn zuòchū ràngbù?", "vi": "Chất lượng chúng tôi công nhận, nhưng ngân sách thực sự có hạn, có thể nhượng bộ ở khía cạnh khác không?"},
                "choices": [
                    {"id": "a", "cn": "我们可以延长账期，或者提供额外的技术支持。", "pinyin": "wǒmen kěyǐ yáncháng zhàngqī, huòzhě tígōng éwài de jìshù zhīchí.", "vi": "Chúng tôi có thể kéo dài kỳ hạn thanh toán, hoặc cung cấp hỗ trợ kỹ thuật thêm.", "next": "n3"},
                ],
            },
            "n2b": {
                "npc": {"cn": "长期合作对我们来说也是希望的，那具体能优惠多少？", "pinyin": "chángqī hézuò duì wǒmen láishuō yěshì xīwàng de, nà jùtǐ néng yōuhuì duōshao?", "vi": "Hợp tác dài hạn cũng là điều chúng tôi mong muốn, vậy cụ thể có thể ưu đãi bao nhiêu?"},
                "choices": [
                    {"id": "a", "cn": "如果签订三年合同，我们可以给出百分之十的折扣。", "pinyin": "rúguǒ qiāndìng sān nián hétong, wǒmen kěyǐ gěichū bǎifēnzhī shí de zhékòu.", "vi": "Nếu ký hợp đồng ba năm, chúng tôi có thể chiết khấu 10%.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "这个方案听起来可以接受，我需要向上级汇报一下。", "pinyin": "zhège fāng'àn tīng qǐlái kěyǐ jiēshòu, wǒ xūyào xiàng shàngjí huìbào yíxià.", "vi": "Phương án này nghe có vẻ chấp nhận được, tôi cần báo cáo lại với cấp trên."},
                "choices": [
                    {"id": "a", "cn": "好的，期待贵方的回复，我们随时可以进一步沟通。", "pinyin": "hǎo de, qídài guì fāng de huífù, wǒmen suíshí kěyǐ jìnyíbù gōutōng.", "vi": "Được, mong chờ phản hồi từ quý công ty, chúng tôi có thể trao đổi thêm bất cứ lúc nào.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "感谢贵方的诚意，希望这次合作能顺利达成。", "pinyin": "gǎnxiè guì fāng de chéngyì, xīwàng zhè cì hézuò néng shùnlì dáchéng.", "vi": "Cảm ơn thiện chí của quý công ty, hy vọng lần hợp tác này sẽ thành công tốt đẹp."},
                "choices": [],
            },
        },
    },
    "academic_discussion": {
        "title": "Bảo vệ luận văn học thuật",
        "hsk_level": 9,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "你的研究假设是否考虑过样本量不足可能带来的偏差？", "pinyin": "nǐ de yánjiū jiǎshè shìfǒu kǎolǜguò yàngběnliàng bùzú kěnéng dàilái de piānchā?", "vi": "Giả thuyết nghiên cứu của bạn đã cân nhắc đến sai lệch có thể xảy ra do mẫu không đủ lớn chưa?"},
                "choices": [
                    {"id": "a", "cn": "确实存在这个局限，我们在讨论部分已经做了说明，并建议后续研究扩大样本。", "pinyin": "quèshí cúnzài zhège júxiàn, wǒmen zài tǎolùn bùfen yǐjīng zuò le shuōmíng, bìng jiànyì hòuxù yánjiū kuòdà yàngběn.", "vi": "Đúng là có hạn chế này, chúng tôi đã nêu rõ trong phần thảo luận, và đề xuất nghiên cứu sau nên mở rộng mẫu.", "next": "n2"},
                    {"id": "b", "cn": "我们通过统计方法对样本进行了加权处理，尽量减少了偏差的影响。", "pinyin": "wǒmen tōngguò tǒngjì fāngfǎ duì yàngběn jìnxíngle jiāquán chǔlǐ, jǐnliàng jiǎnshǎole piānchā de yǐngxiǎng.", "vi": "Chúng tôi đã dùng phương pháp thống kê để xử lý trọng số mẫu, cố gắng giảm thiểu ảnh hưởng của sai lệch.", "next": "n2b"},
                ],
            },
            "n2": {
                "npc": {"cn": "那你认为这个局限会在多大程度上影响结论的普遍性？", "pinyin": "nà nǐ rènwéi zhège júxiàn huì zài duōdà chéngdù shàng yǐngxiǎng jiélùn de pǔbiànxìng?", "vi": "Vậy bạn cho rằng hạn chế này ảnh hưởng đến mức độ khái quát của kết luận đến đâu?"},
                "choices": [
                    {"id": "a", "cn": "在一定范围内结论仍然成立，但推广到更大群体时需要谨慎。", "pinyin": "zài yídìng fànwéi nèi jiélùn réngrán chénglì, dàn tuīguǎng dào gèng dà qúntǐ shí xūyào jǐnshèn.", "vi": "Trong một phạm vi nhất định kết luận vẫn đúng, nhưng khi mở rộng ra nhóm lớn hơn cần thận trọng.", "next": "n3"},
                ],
            },
            "n2b": {
                "npc": {"cn": "加权处理是个不错的方法，但你如何验证加权模型本身的合理性？", "pinyin": "jiāquán chǔlǐ shì gè búcuò de fāngfǎ, dàn nǐ rúhé yànzhèng jiāquán móxíng běnshēn de hélǐxìng?", "vi": "Xử lý trọng số là một phương pháp tốt, nhưng bạn kiểm chứng tính hợp lý của bản thân mô hình trọng số thế nào?"},
                "choices": [
                    {"id": "a", "cn": "我们用了交叉验证和敏感性分析来检验模型的稳健性。", "pinyin": "wǒmen yòngle jiāochā yànzhèng hé mǐngǎnxìng fēnxī lái jiǎnyàn móxíng de wěnjiànxìng.", "vi": "Chúng tôi dùng kiểm định chéo và phân tích độ nhạy để kiểm tra độ vững chắc của mô hình.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "这个回答比较严谨，我对你的研究方法基本认可。", "pinyin": "zhège huídá bǐjiào yánjǐn, wǒ duì nǐ de yánjiū fāngfǎ jīběn rènkě.", "vi": "Câu trả lời khá chặt chẽ, tôi cơ bản công nhận phương pháp nghiên cứu của bạn."},
                "choices": [
                    {"id": "a", "cn": "谢谢老师的指导，我会在最终稿中进一步完善这部分论述。", "pinyin": "xièxie lǎoshī de zhǐdǎo, wǒ huì zài zuìzhōng gǎo zhōng jìnyíbù wánshàn zhè bùfen lùnshù.", "vi": "Cảm ơn thầy/cô đã chỉ dẫn, em sẽ hoàn thiện thêm phần lập luận này trong bản cuối.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "很好，期待你完善后的论文。", "pinyin": "hěn hǎo, qídài nǐ wánshàn hòu de lùnwén.", "vi": "Tốt lắm, mong chờ bản luận văn đã hoàn thiện của em."},
                "choices": [],
            },
        },
    },
}
