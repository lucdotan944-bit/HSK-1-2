# -*- coding: utf-8 -*-
"""Ngữ pháp hệ thống theo 9 cấp HSK 3.0 — soạn cho người Việt.

Mỗi điểm ngữ pháp: cấu trúc, giải thích tiếng Việt, ví dụ (chữ Hán + pinyin +
âm Hán-Việt + nghĩa). Âm Hán-Việt là "neo nhớ" đặc trưng của Hán Ngữ+ —
đọc âm Hán-Việt của cả câu giúp người Việt nhận ra từ gốc Hán quen thuộc.

Nội dung đối chiếu theo giáo trình HSK Standard Course và đề cương
《国际中文教育中文水平等级标准》(chuẩn HSK 3.0/2021).
"""

GRAMMAR = {
    1: [
        {
            "id": "hsk1-shi",
            "title": "Câu khẳng định với 是 (thị)",
            "pattern": "A + 是 + B",
            "explanation": "是 nối chủ ngữ với danh từ để nói 'A là B'. Khác tiếng Việt: KHÔNG dùng 是 trước tính từ (không nói 我是高 mà nói 我很高).",
            "examples": [
                {"cn": "我是越南人。", "pinyin": "Wǒ shì Yuènán rén.", "hv": "ngã thị Việt Nam nhân", "vi": "Tôi là người Việt Nam."},
                {"cn": "他是老师。", "pinyin": "Tā shì lǎoshī.", "hv": "tha thị lão sư", "vi": "Anh ấy là giáo viên."},
            ],
        },
        {
            "id": "hsk1-bu",
            "title": "Phủ định với 不 (bất)",
            "pattern": "Chủ ngữ + 不 + động từ/tính từ",
            "explanation": "不 đặt trước động từ hoặc tính từ để phủ định — giống 'không' tiếng Việt. Nhớ: 不 dùng cho hiện tại/tương lai và thói quen; việc đã xảy ra dùng 没 (một).",
            "examples": [
                {"cn": "我不喝咖啡。", "pinyin": "Wǒ bù hē kāfēi.", "hv": "ngã bất hát ca phê", "vi": "Tôi không uống cà phê."},
                {"cn": "今天不冷。", "pinyin": "Jīntiān bù lěng.", "hv": "kim thiên bất lãnh", "vi": "Hôm nay không lạnh."},
            ],
        },
        {
            "id": "hsk1-ma",
            "title": "Câu hỏi với 吗 (ma)",
            "pattern": "Câu trần thuật + 吗？",
            "explanation": "Thêm 吗 vào cuối câu để biến thành câu hỏi có/không — như '... phải không?' của tiếng Việt. Không đổi trật tự từ.",
            "examples": [
                {"cn": "你是学生吗？", "pinyin": "Nǐ shì xuéshēng ma?", "hv": "nhĩ thị học sinh ma", "vi": "Bạn là học sinh phải không?"},
                {"cn": "你喜欢中国菜吗？", "pinyin": "Nǐ xǐhuan Zhōngguó cài ma?", "hv": "nhĩ hỉ hoan Trung Quốc thái ma", "vi": "Bạn thích món Trung Quốc không?"},
            ],
        },
        {
            "id": "hsk1-de",
            "title": "Sở hữu với 的 (đích)",
            "pattern": "A + 的 + B  (= B của A)",
            "explanation": "的 nối người sở hữu với vật — NGƯỢC trật tự tiếng Việt: 我的书 = 'sách của tôi' (chứ không phải 'tôi của sách'). Với người thân/quan hệ gần có thể bỏ 的: 我妈妈.",
            "examples": [
                {"cn": "这是我的手机。", "pinyin": "Zhè shì wǒ de shǒujī.", "hv": "giá thị ngã đích thủ cơ", "vi": "Đây là điện thoại của tôi."},
                {"cn": "她是我的朋友。", "pinyin": "Tā shì wǒ de péngyou.", "hv": "tha thị ngã đích bằng hữu", "vi": "Cô ấy là bạn của tôi."},
            ],
        },
        {
            "id": "hsk1-hen",
            "title": "Tính từ với 很 (ngận)",
            "pattern": "Chủ ngữ + 很 + tính từ",
            "explanation": "Câu tả tính chất KHÔNG dùng 是; trước tính từ thường có 很 (nghĩa gốc 'rất' nhưng ở đây gần như bắt buộc, nghĩa nhạt). Nói 我很忙 chứ không nói 我是忙.",
            "examples": [
                {"cn": "我很忙。", "pinyin": "Wǒ hěn máng.", "hv": "ngã ngận mang", "vi": "Tôi (rất) bận."},
                {"cn": "汉语很有意思。", "pinyin": "Hànyǔ hěn yǒu yìsi.", "hv": "Hán ngữ ngận hữu ý tứ", "vi": "Tiếng Trung rất thú vị."},
            ],
        },
        {
            "id": "hsk1-you",
            "title": "有 (hữu) và phủ định 没有",
            "pattern": "Chủ ngữ + 有/没有 + danh từ",
            "explanation": "有 = 'có'. Phủ định của 有 luôn là 没有 (một hữu), KHÔNG bao giờ nói 不有.",
            "examples": [
                {"cn": "我有两个哥哥。", "pinyin": "Wǒ yǒu liǎng ge gēge.", "hv": "ngã hữu lưỡng cá ca ca", "vi": "Tôi có hai anh trai."},
                {"cn": "他没有时间。", "pinyin": "Tā méiyǒu shíjiān.", "hv": "tha một hữu thời gian", "vi": "Anh ấy không có thời gian."},
            ],
        },
        {
            "id": "hsk1-zai",
            "title": "Vị trí với 在 (tại)",
            "pattern": "A + 在 + địa điểm",
            "explanation": "在 chỉ vị trí 'ở/tại' — giống chữ 'tại' Hán-Việt (hiện tại, tại chỗ). Địa điểm luôn đứng SAU 在.",
            "examples": [
                {"cn": "我在家。", "pinyin": "Wǒ zài jiā.", "hv": "ngã tại gia", "vi": "Tôi ở nhà."},
                {"cn": "他在学校工作。", "pinyin": "Tā zài xuéxiào gōngzuò.", "hv": "tha tại học hiệu công tác", "vi": "Anh ấy làm việc ở trường."},
            ],
        },
        {
            "id": "hsk1-question-words",
            "title": "Từ hỏi 什么 / 谁 / 哪儿",
            "pattern": "Từ hỏi đứng NGUYÊN vị trí của từ được hỏi",
            "explanation": "什么 (thập ma) = gì; 谁 (thuỳ) = ai; 哪儿 = ở đâu. Khác tiếng Anh: không đảo từ hỏi lên đầu câu — hỏi ở đâu thì để từ hỏi ngay đó.",
            "examples": [
                {"cn": "这是什么？", "pinyin": "Zhè shì shénme?", "hv": "giá thị thập ma", "vi": "Đây là cái gì?"},
                {"cn": "你去哪儿？", "pinyin": "Nǐ qù nǎr?", "hv": "nhĩ khứ ná nhi", "vi": "Bạn đi đâu?"},
            ],
        },
        {
            "id": "hsk1-measure",
            "title": "Lượng từ 个 (cá)",
            "pattern": "Số + 个 + danh từ",
            "explanation": "Giữa số đếm và danh từ phải có lượng từ, như 'cái/con/quyển' tiếng Việt. 个 là lượng từ vạn năng cho người và nhiều vật.",
            "examples": [
                {"cn": "三个人", "pinyin": "sān ge rén", "hv": "tam cá nhân", "vi": "ba người"},
                {"cn": "我买一个面包。", "pinyin": "Wǒ mǎi yí ge miànbāo.", "hv": "ngã mãi nhất cá diện bao", "vi": "Tôi mua một cái bánh mì."},
            ],
        },
        {
            "id": "hsk1-le-completed",
            "title": "了 (liễu) — việc đã hoàn thành",
            "pattern": "Động từ + 了",
            "explanation": "了 sau động từ cho biết hành động đã xảy ra/hoàn thành — gần với 'đã/rồi' tiếng Việt. Phủ định dùng 没(有) và BỎ 了: 我没吃 (không nói 我没吃了).",
            "examples": [
                {"cn": "我吃了早饭。", "pinyin": "Wǒ chī le zǎofàn.", "hv": "ngã cật liễu tảo phạn", "vi": "Tôi đã ăn sáng rồi."},
                {"cn": "他买了一本书。", "pinyin": "Tā mǎi le yì běn shū.", "hv": "tha mãi liễu nhất bản thư", "vi": "Anh ấy đã mua một quyển sách."},
            ],
        },
        {
            "id": "hsk1-dou-ye",
            "title": "都 (đô) và 也 (dã)",
            "pattern": "Chủ ngữ + 都/也 + động từ",
            "explanation": "都 = 'đều', 也 = 'cũng'. Cả hai LUÔN đứng trước động từ, sau chủ ngữ — không đứng cuối câu như tiếng Việt ('tôi cũng vậy' → 我也是).",
            "examples": [
                {"cn": "我们都是学生。", "pinyin": "Wǒmen dōu shì xuéshēng.", "hv": "ngã môn đô thị học sinh", "vi": "Chúng tôi đều là học sinh."},
                {"cn": "我也喜欢。", "pinyin": "Wǒ yě xǐhuan.", "hv": "ngã dã hỉ hoan", "vi": "Tôi cũng thích."},
            ],
        },
        {
            "id": "hsk1-ne",
            "title": "Câu hỏi ngắn với 呢 (ni)",
            "pattern": "Danh từ/đại từ + 呢？",
            "explanation": "呢 hỏi ngược lại chủ đề vừa nói — như 'còn ... thì sao?'. Tiết kiệm cả câu hỏi dài.",
            "examples": [
                {"cn": "我很好，你呢？", "pinyin": "Wǒ hěn hǎo, nǐ ne?", "hv": "ngã ngận hảo, nhĩ ni", "vi": "Tôi khoẻ, còn bạn thì sao?"},
                {"cn": "我的书呢？", "pinyin": "Wǒ de shū ne?", "hv": "ngã đích thư ni", "vi": "Sách của tôi đâu rồi?"},
            ],
        },
    ],
    2: [
        {
            "id": "hsk2-le-change",
            "title": "了 (liễu) — thay đổi trạng thái",
            "pattern": "Câu + 了 (cuối câu)",
            "explanation": "了 cuối câu báo hiệu tình huống ĐÃ THAY ĐỔI: 下雨了 = '(bắt đầu) mưa rồi'. Khác 了 sau động từ (hoàn thành hành động).",
            "examples": [
                {"cn": "下雨了。", "pinyin": "Xià yǔ le.", "hv": "hạ vũ liễu", "vi": "Trời mưa rồi."},
                {"cn": "他二十岁了。", "pinyin": "Tā èrshí suì le.", "hv": "tha nhị thập tuế liễu", "vi": "Anh ấy đã 20 tuổi rồi."},
            ],
        },
        {
            "id": "hsk2-guo",
            "title": "过 (quá) — kinh nghiệm từng trải",
            "pattern": "Động từ + 过",
            "explanation": "过 = 'từng/đã từng'. Nhấn mạnh KINH NGHIỆM (ít nhất một lần trong đời), khác 了 nói về một lần cụ thể. Phủ định: 没…过.",
            "examples": [
                {"cn": "我去过中国。", "pinyin": "Wǒ qù guo Zhōngguó.", "hv": "ngã khứ quá Trung Quốc", "vi": "Tôi từng đi Trung Quốc."},
                {"cn": "他没吃过越南菜。", "pinyin": "Tā méi chī guo Yuènán cài.", "hv": "tha một cật quá Việt Nam thái", "vi": "Anh ấy chưa từng ăn món Việt."},
            ],
        },
        {
            "id": "hsk2-zhengzai",
            "title": "正在 / 在 + động từ — đang làm gì",
            "pattern": "Chủ ngữ + (正)在 + động từ",
            "explanation": "在 hoặc 正在 (chính tại) trước động từ = 'đang'. Có thể thêm 呢 cuối câu tăng ý đang tiếp diễn.",
            "examples": [
                {"cn": "我正在学习汉语。", "pinyin": "Wǒ zhèngzài xuéxí Hànyǔ.", "hv": "ngã chính tại học tập Hán ngữ", "vi": "Tôi đang học tiếng Trung."},
                {"cn": "他在打电话呢。", "pinyin": "Tā zài dǎ diànhuà ne.", "hv": "tha tại đả điện thoại ni", "vi": "Anh ấy đang gọi điện."},
            ],
        },
        {
            "id": "hsk2-bi",
            "title": "So sánh với 比 (tỉ)",
            "pattern": "A + 比 + B + tính từ",
            "explanation": "比 (tỉ — như 'tỉ lệ, so tỉ') so sánh hơn: A 比 B 高 = A cao hơn B. KHÔNG thêm 很 trước tính từ; muốn nói hơn nhiều thì thêm 多了 cuối: 高多了.",
            "examples": [
                {"cn": "今天比昨天热。", "pinyin": "Jīntiān bǐ zuótiān rè.", "hv": "kim thiên tỉ tạc thiên nhiệt", "vi": "Hôm nay nóng hơn hôm qua."},
                {"cn": "他比我大三岁。", "pinyin": "Tā bǐ wǒ dà sān suì.", "hv": "tha tỉ ngã đại tam tuế", "vi": "Anh ấy lớn hơn tôi ba tuổi."},
            ],
        },
        {
            "id": "hsk2-de-degree",
            "title": "Bổ ngữ mức độ với 得 (đắc)",
            "pattern": "Động từ + 得 + tính từ",
            "explanation": "得 nối động từ với nhận xét về mức độ: 说得很好 = 'nói rất giỏi'. Nếu có tân ngữ phải lặp động từ: 说汉语说得很好.",
            "examples": [
                {"cn": "你说得很好。", "pinyin": "Nǐ shuō de hěn hǎo.", "hv": "nhĩ thuyết đắc ngận hảo", "vi": "Bạn nói rất hay."},
                {"cn": "他跑得很快。", "pinyin": "Tā pǎo de hěn kuài.", "hv": "tha bào đắc ngận khoái", "vi": "Anh ấy chạy rất nhanh."},
            ],
        },
        {
            "id": "hsk2-yao-le",
            "title": "要…了 — sắp xảy ra",
            "pattern": "(快/就)要 + động từ + 了",
            "explanation": "Diễn tả việc SẮP xảy ra: 要下雨了 = 'sắp mưa rồi'. 快要…了 gấp hơn; 就要…了 hay đi với mốc thời gian cụ thể.",
            "examples": [
                {"cn": "火车快要开了。", "pinyin": "Huǒchē kuàiyào kāi le.", "hv": "hoả xa khoái yếu khai liễu", "vi": "Tàu sắp chạy rồi."},
                {"cn": "我们明天就要考试了。", "pinyin": "Wǒmen míngtiān jiù yào kǎoshì le.", "hv": "ngã môn minh thiên tựu yếu khảo thí liễu", "vi": "Ngày mai chúng tôi thi rồi."},
            ],
        },
        {
            "id": "hsk2-yinwei-suoyi",
            "title": "因为…所以… (nhân vị… sở dĩ…)",
            "pattern": "因为 + lý do, 所以 + kết quả",
            "explanation": "Cặp 'vì… nên…'. Tiếng Trung thường dùng CẢ HAI vế (tiếng Việt hay bỏ một): 因为下雨，所以我没去.",
            "examples": [
                {"cn": "因为下雨，所以我没去。", "pinyin": "Yīnwèi xià yǔ, suǒyǐ wǒ méi qù.", "hv": "nhân vị hạ vũ, sở dĩ ngã một khứ", "vi": "Vì trời mưa nên tôi không đi."},
                {"cn": "因为他病了，所以没来上课。", "pinyin": "Yīnwèi tā bìng le, suǒyǐ méi lái shàngkè.", "hv": "nhân vị tha bệnh liễu, sở dĩ một lai thượng khoá", "vi": "Vì anh ấy ốm nên không đến lớp."},
            ],
        },
        {
            "id": "hsk2-suiran-danshi",
            "title": "虽然…但是… (tuy nhiên… đãn thị…)",
            "pattern": "虽然 + A, 但是 + B",
            "explanation": "'Tuy… nhưng…'. 虽然 chính là 'tuy nhiên' Hán-Việt. Hai vế đều phải có từ nối, khác tiếng Anh chỉ dùng một.",
            "examples": [
                {"cn": "虽然很累，但是我很高兴。", "pinyin": "Suīrán hěn lèi, dànshì wǒ hěn gāoxìng.", "hv": "tuy nhiên ngận luỵ, đãn thị ngã ngận cao hứng", "vi": "Tuy mệt nhưng tôi rất vui."},
                {"cn": "虽然贵，但是质量好。", "pinyin": "Suīrán guì, dànshì zhìliàng hǎo.", "hv": "tuy nhiên quý, đãn thị chất lượng hảo", "vi": "Tuy đắt nhưng chất lượng tốt."},
            ],
        },
        {
            "id": "hsk2-cong-dao",
            "title": "从…到… (tòng… đáo…)",
            "pattern": "从 + A + 到 + B",
            "explanation": "'Từ A đến B' — dùng cho cả thời gian lẫn nơi chốn. 从 (tòng) = từ, 到 (đáo) = đến (như 'đáo hạn').",
            "examples": [
                {"cn": "我从八点到十二点上课。", "pinyin": "Wǒ cóng bā diǎn dào shí'èr diǎn shàngkè.", "hv": "ngã tòng bát điểm đáo thập nhị điểm thượng khoá", "vi": "Tôi học từ 8 giờ đến 12 giờ."},
                {"cn": "从河内到北京", "pinyin": "cóng Hénèi dào Běijīng", "hv": "tòng Hà Nội đáo Bắc Kinh", "vi": "từ Hà Nội đến Bắc Kinh"},
            ],
        },
        {
            "id": "hsk2-yixia",
            "title": "Động từ + 一下 (nhất hạ)",
            "pattern": "Động từ + 一下",
            "explanation": "一下 làm nhẹ hành động — 'một chút/thử xem', lịch sự hơn mệnh lệnh trần: 等一下 = 'đợi chút'.",
            "examples": [
                {"cn": "请等一下。", "pinyin": "Qǐng děng yíxià.", "hv": "thỉnh đẳng nhất hạ", "vi": "Xin đợi một chút."},
                {"cn": "我看一下可以吗？", "pinyin": "Wǒ kàn yíxià kěyǐ ma?", "hv": "ngã khán nhất hạ khả dĩ ma", "vi": "Tôi xem một chút được không?"},
            ],
        },
        {
            "id": "hsk2-bie",
            "title": "Cấm/khuyên với 别 (biệt)",
            "pattern": "别 + động từ (+ 了)",
            "explanation": "别 = 'đừng'. Thêm 了 cuối khi bảo ai dừng việc ĐANG làm: 别说了 = 'đừng nói nữa'.",
            "examples": [
                {"cn": "别担心！", "pinyin": "Bié dānxīn!", "hv": "biệt đảm tâm", "vi": "Đừng lo lắng!"},
                {"cn": "别忘了带护照。", "pinyin": "Bié wàng le dài hùzhào.", "hv": "biệt vong liễu đái hộ chiếu", "vi": "Đừng quên mang hộ chiếu."},
            ],
        },
        {
            "id": "hsk2-li",
            "title": "Khoảng cách với 离 (ly)",
            "pattern": "A + 离 + B + 近/远",
            "explanation": "离 (ly — 'ly biệt, cách ly') đo khoảng cách giữa hai điểm: A 离 B 很近 = 'A cách B rất gần'.",
            "examples": [
                {"cn": "我家离公司很近。", "pinyin": "Wǒ jiā lí gōngsī hěn jìn.", "hv": "ngã gia ly công ty ngận cận", "vi": "Nhà tôi cách công ty rất gần."},
                {"cn": "机场离市区有点儿远。", "pinyin": "Jīchǎng lí shìqū yǒudiǎnr yuǎn.", "hv": "cơ trường ly thị khu hữu điểm nhi viễn", "vi": "Sân bay cách trung tâm hơi xa."},
            ],
        },
    ],
    3: [
        {
            "id": "hsk3-ba",
            "title": "Câu chữ 把 (bả)",
            "pattern": "Chủ ngữ + 把 + tân ngữ + động từ + thành phần khác",
            "explanation": "把 kéo tân ngữ lên TRƯỚC động từ để nhấn mạnh việc 'xử lý' nó ra sao. Động từ không được đứng trơ — phải kèm 了/bổ ngữ: 把门关上 chứ không nói 把门关.",
            "examples": [
                {"cn": "请把门关上。", "pinyin": "Qǐng bǎ mén guān shang.", "hv": "thỉnh bả môn quan thượng", "vi": "Xin đóng cửa lại."},
                {"cn": "我把作业做完了。", "pinyin": "Wǒ bǎ zuòyè zuò wán le.", "hv": "ngã bả tác nghiệp tố hoàn liễu", "vi": "Tôi làm xong bài tập rồi."},
            ],
        },
        {
            "id": "hsk3-bei",
            "title": "Câu bị động với 被 (bị)",
            "pattern": "A + 被 + (B) + động từ + kết quả",
            "explanation": "被 chính là 'bị' Hán-Việt — dễ nhớ nhất cho người Việt! 手机被偷了 = 'điện thoại bị trộm rồi'. Thường mang sắc thái không may.",
            "examples": [
                {"cn": "我的手机被偷了。", "pinyin": "Wǒ de shǒujī bèi tōu le.", "hv": "ngã đích thủ cơ bị thâu liễu", "vi": "Điện thoại của tôi bị trộm rồi."},
                {"cn": "蛋糕被他吃完了。", "pinyin": "Dàngāo bèi tā chī wán le.", "hv": "đản cao bị tha cật hoàn liễu", "vi": "Bánh kem bị anh ấy ăn hết rồi."},
            ],
        },
        {
            "id": "hsk3-yuelaiyue",
            "title": "越来越 (việt lai việt) — ngày càng",
            "pattern": "越来越 + tính từ",
            "explanation": "'Ngày càng…': 越来越贵 = ngày càng đắt. Biến thể 越 A 越 B = 'càng A càng B': 越多越好.",
            "examples": [
                {"cn": "天气越来越热。", "pinyin": "Tiānqì yuèláiyuè rè.", "hv": "thiên khí việt lai việt nhiệt", "vi": "Thời tiết ngày càng nóng."},
                {"cn": "他汉语说得越来越好。", "pinyin": "Tā Hànyǔ shuō de yuèláiyuè hǎo.", "hv": "tha Hán ngữ thuyết đắc việt lai việt hảo", "vi": "Anh ấy nói tiếng Trung ngày càng giỏi."},
            ],
        },
        {
            "id": "hsk3-youyou",
            "title": "又…又… (hựu… hựu…)",
            "pattern": "又 + A + 又 + B",
            "explanation": "'Vừa A vừa B' — hai tính chất cùng lúc: 又便宜又好吃. So sánh: 一边…一边 dùng cho hai HÀNH ĐỘNG song song.",
            "examples": [
                {"cn": "这个菜又便宜又好吃。", "pinyin": "Zhège cài yòu piányi yòu hǎochī.", "hv": "giá cá thái hựu tiện nghi hựu hảo cật", "vi": "Món này vừa rẻ vừa ngon."},
                {"cn": "她又聪明又努力。", "pinyin": "Tā yòu cōngming yòu nǔlì.", "hv": "tha hựu thông minh hựu nỗ lực", "vi": "Cô ấy vừa thông minh vừa chăm chỉ."},
            ],
        },
        {
            "id": "hsk3-yibian",
            "title": "一边…一边… (nhất biên…)",
            "pattern": "一边 + động từ A + 一边 + động từ B",
            "explanation": "Hai hành động diễn ra CÙNG LÚC: 一边吃饭一边看电视 = 'vừa ăn vừa xem TV'.",
            "examples": [
                {"cn": "他一边走一边打电话。", "pinyin": "Tā yìbiān zǒu yìbiān dǎ diànhuà.", "hv": "tha nhất biên tẩu nhất biên đả điện thoại", "vi": "Anh ấy vừa đi vừa gọi điện."},
                {"cn": "我喜欢一边听音乐一边学习。", "pinyin": "Wǒ xǐhuan yìbiān tīng yīnyuè yìbiān xuéxí.", "hv": "ngã hỉ hoan nhất biên thính âm nhạc nhất biên học tập", "vi": "Tôi thích vừa nghe nhạc vừa học."},
            ],
        },
        {
            "id": "hsk3-ruguo",
            "title": "如果…就… (như quả… tựu…)",
            "pattern": "如果 + điều kiện, (chủ ngữ) 就 + kết quả",
            "explanation": "'Nếu… thì…'. 就 đứng SAU chủ ngữ vế hai: 如果你去，我就去 (không nói 就我去).",
            "examples": [
                {"cn": "如果明天下雨，我们就不去了。", "pinyin": "Rúguǒ míngtiān xià yǔ, wǒmen jiù bú qù le.", "hv": "như quả minh thiên hạ vũ, ngã môn tựu bất khứ liễu", "vi": "Nếu mai mưa thì chúng ta không đi nữa."},
                {"cn": "如果有问题，就问我。", "pinyin": "Rúguǒ yǒu wèntí, jiù wèn wǒ.", "hv": "như quả hữu vấn đề, tựu vấn ngã", "vi": "Nếu có vấn đề thì hỏi tôi."},
            ],
        },
        {
            "id": "hsk3-budan-erqie",
            "title": "不但…而且… (bất đãn… nhi thả…)",
            "pattern": "不但 + A, 而且 + B",
            "explanation": "'Không những… mà còn…'. Nếu hai vế cùng chủ ngữ, chủ ngữ đứng trước 不但.",
            "examples": [
                {"cn": "他不但会说汉语，而且说得很好。", "pinyin": "Tā búdàn huì shuō Hànyǔ, érqiě shuō de hěn hǎo.", "hv": "tha bất đãn hội thuyết Hán ngữ, nhi thả thuyết đắc ngận hảo", "vi": "Anh ấy không những biết nói tiếng Trung mà còn nói rất giỏi."},
                {"cn": "这里不但便宜，而且东西很多。", "pinyin": "Zhèlǐ búdàn piányi, érqiě dōngxi hěn duō.", "hv": "giá lý bất đãn tiện nghi, nhi thả đông tây ngận đa", "vi": "Ở đây không những rẻ mà đồ còn rất nhiều."},
            ],
        },
        {
            "id": "hsk3-result-complement",
            "title": "Bổ ngữ kết quả 完 / 到 / 见 / 好",
            "pattern": "Động từ + 完/到/见/好",
            "explanation": "Gắn sau động từ để nói KẾT QUẢ: 吃完 (ăn xong), 找到 (tìm thấy), 听见 (nghe thấy), 做好 (làm xong/tốt). Phủ định quá khứ: 没 + động từ + bổ ngữ.",
            "examples": [
                {"cn": "我找到工作了！", "pinyin": "Wǒ zhǎo dào gōngzuò le!", "hv": "ngã trảo đáo công tác liễu", "vi": "Tôi tìm được việc rồi!"},
                {"cn": "作业还没做完。", "pinyin": "Zuòyè hái méi zuò wán.", "hv": "tác nghiệp hài một tố hoàn", "vi": "Bài tập vẫn chưa làm xong."},
            ],
        },
        {
            "id": "hsk3-cai-jiu",
            "title": "才 (tài) và 就 (tựu) — muộn và sớm",
            "pattern": "Thời gian + 才/就 + động từ",
            "explanation": "Cùng mốc thời gian: 才 hàm ý MUỘN/chậm ('mãi mới'), 就 hàm ý SỚM/nhanh ('đã'). 十点才起床 = mãi 10 giờ mới dậy; 六点就起床了 = mới 6 giờ đã dậy.",
            "examples": [
                {"cn": "他十点才来。", "pinyin": "Tā shí diǎn cái lái.", "hv": "tha thập điểm tài lai", "vi": "Mãi 10 giờ anh ấy mới đến."},
                {"cn": "她六点就到了。", "pinyin": "Tā liù diǎn jiù dào le.", "hv": "tha lục điểm tựu đáo liễu", "vi": "Mới 6 giờ cô ấy đã đến rồi."},
            ],
        },
        {
            "id": "hsk3-huozhe-haishi",
            "title": "或者 (hoặc giả) và 还是 (hài thị)",
            "pattern": "A 或者 B (trần thuật) · A 还是 B (câu hỏi)",
            "explanation": "Cả hai nghĩa 'hoặc', nhưng 还是 dùng trong CÂU HỎI lựa chọn, 或者 trong câu kể: 你喝茶还是咖啡？ / 我喝茶或者咖啡都行.",
            "examples": [
                {"cn": "你想喝茶还是咖啡？", "pinyin": "Nǐ xiǎng hē chá háishi kāfēi?", "hv": "nhĩ tưởng hát trà hài thị ca phê", "vi": "Bạn muốn uống trà hay cà phê?"},
                {"cn": "周六或者周日都可以。", "pinyin": "Zhōuliù huòzhě zhōurì dōu kěyǐ.", "hv": "chu lục hoặc giả chu nhật đô khả dĩ", "vi": "Thứ Bảy hoặc Chủ nhật đều được."},
            ],
        },
        {
            "id": "hsk3-chule",
            "title": "除了…以外 (trừ liễu… dĩ ngoại)",
            "pattern": "除了 A 以外，还/都…",
            "explanation": "Đi với 还/也 = 'ngoài A ra còn…' (bao gồm A); đi với 都 = 'trừ A ra thì…' (loại A). Chữ 除 chính là 'trừ' Hán-Việt.",
            "examples": [
                {"cn": "除了汉语以外，他还会说英语。", "pinyin": "Chúle Hànyǔ yǐwài, tā hái huì shuō Yīngyǔ.", "hv": "trừ liễu Hán ngữ dĩ ngoại, tha hài hội thuyết Anh ngữ", "vi": "Ngoài tiếng Trung, anh ấy còn biết nói tiếng Anh."},
                {"cn": "除了他以外，我们都去。", "pinyin": "Chúle tā yǐwài, wǒmen dōu qù.", "hv": "trừ liễu tha dĩ ngoại, ngã môn đô khứ", "vi": "Trừ anh ấy ra, chúng tôi đều đi."},
            ],
        },
        {
            "id": "hsk3-gen-yiyang",
            "title": "A 跟 B 一样 (nhất dạng)",
            "pattern": "A + 跟 + B + 一样 (+ tính từ)",
            "explanation": "So sánh bằng: 'A giống B / A … như B'. Phủ định: A 跟 B 不一样.",
            "examples": [
                {"cn": "我的手机跟你的一样。", "pinyin": "Wǒ de shǒujī gēn nǐ de yíyàng.", "hv": "ngã đích thủ cơ cân nhĩ đích nhất dạng", "vi": "Điện thoại của tôi giống của bạn."},
                {"cn": "他跟我一样高。", "pinyin": "Tā gēn wǒ yíyàng gāo.", "hv": "tha cân ngã nhất dạng cao", "vi": "Anh ấy cao bằng tôi."},
            ],
        },
    ],
    4: [
        {
            "id": "hsk4-lian-dou",
            "title": "连…都/也… (liên… đô…)",
            "pattern": "连 + X + 都/也 + động từ",
            "explanation": "'Đến cả X cũng…' — nhấn mạnh trường hợp cực端: 连小孩都知道 = 'đến trẻ con cũng biết'.",
            "examples": [
                {"cn": "这个字连老师都不认识。", "pinyin": "Zhège zì lián lǎoshī dōu bú rènshi.", "hv": "giá cá tự liên lão sư đô bất nhận thức", "vi": "Chữ này đến giáo viên cũng không biết."},
                {"cn": "他忙得连饭都没时间吃。", "pinyin": "Tā máng de lián fàn dōu méi shíjiān chī.", "hv": "tha mang đắc liên phạn đô một thời gian cật", "vi": "Anh ấy bận đến mức cơm cũng không có thời gian ăn."},
            ],
        },
        {
            "id": "hsk4-buguan",
            "title": "不管…都… (bất quản… đô…)",
            "pattern": "不管 + mọi trường hợp, 都 + kết quả",
            "explanation": "'Bất kể/dù… đều…'. Sau 不管 phải là dạng câu hỏi hoặc lựa chọn (谁/什么/多…还是…): 不管多难，我都要学.",
            "examples": [
                {"cn": "不管多忙，他都坚持学习。", "pinyin": "Bùguǎn duō máng, tā dōu jiānchí xuéxí.", "hv": "bất quản đa mang, tha đô kiên trì học tập", "vi": "Dù bận đến đâu, anh ấy đều kiên trì học."},
                {"cn": "不管你去不去，我都去。", "pinyin": "Bùguǎn nǐ qù bu qù, wǒ dōu qù.", "hv": "bất quản nhĩ khứ bất khứ, ngã đô khứ", "vi": "Bất kể bạn đi hay không, tôi vẫn đi."},
            ],
        },
        {
            "id": "hsk4-jishi",
            "title": "即使…也… (tức sử… dã…)",
            "pattern": "即使 + giả thiết, 也 + kết quả",
            "explanation": "'Cho dù… cũng…' — giả thiết CHƯA/không chắc xảy ra, khác 虽然 (việc đã thật). 即使失败，也要试试.",
            "examples": [
                {"cn": "即使下大雨，比赛也不会取消。", "pinyin": "Jíshǐ xià dà yǔ, bǐsài yě bú huì qǔxiāo.", "hv": "tức sử hạ đại vũ, tỉ tái dã bất hội thủ tiêu", "vi": "Cho dù mưa to, trận đấu cũng sẽ không bị huỷ."},
                {"cn": "即使没人支持，我也要坚持。", "pinyin": "Jíshǐ méi rén zhīchí, wǒ yě yào jiānchí.", "hv": "tức sử một nhân chi trì, ngã dã yếu kiên trì", "vi": "Cho dù không ai ủng hộ, tôi vẫn sẽ kiên trì."},
            ],
        },
        {
            "id": "hsk4-jiran",
            "title": "既然…就… (ký nhiên… tựu…)",
            "pattern": "既然 + sự thật, 就 + kết luận",
            "explanation": "'Đã… thì…' — vế đầu là việc ĐÃ RÕ, vế sau là kết luận hợp lý: 既然你不舒服，就回家吧.",
            "examples": [
                {"cn": "既然大家都同意，就这么决定吧。", "pinyin": "Jìrán dàjiā dōu tóngyì, jiù zhème juédìng ba.", "hv": "ký nhiên đại gia đô đồng ý, tựu giá ma quyết định ba", "vi": "Mọi người đã đồng ý thì quyết định vậy nhé."},
                {"cn": "既然来了，就多住几天。", "pinyin": "Jìrán lái le, jiù duō zhù jǐ tiān.", "hv": "ký nhiên lai liễu, tựu đa trú kỷ thiên", "vi": "Đã đến rồi thì ở thêm vài hôm."},
            ],
        },
        {
            "id": "hsk4-zhiyao",
            "title": "只要…就… (chỉ yếu… tựu…)",
            "pattern": "只要 + điều kiện đủ, 就 + kết quả",
            "explanation": "'Chỉ cần… là…' — điều kiện ĐỦ. Phân biệt 只有…才 (điều kiện DUY NHẤT, 'chỉ có… mới…').",
            "examples": [
                {"cn": "只要努力，就会成功。", "pinyin": "Zhǐyào nǔlì, jiù huì chénggōng.", "hv": "chỉ yếu nỗ lực, tựu hội thành công", "vi": "Chỉ cần nỗ lực là sẽ thành công."},
                {"cn": "只要你来，我就高兴。", "pinyin": "Zhǐyào nǐ lái, wǒ jiù gāoxìng.", "hv": "chỉ yếu nhĩ lai, ngã tựu cao hứng", "vi": "Chỉ cần bạn đến là tôi vui rồi."},
            ],
        },
        {
            "id": "hsk4-zhiyou-cai",
            "title": "只有…才… (chỉ hữu… tài…)",
            "pattern": "只有 + điều kiện duy nhất, 才 + kết quả",
            "explanation": "'Chỉ có… mới…' — điều kiện BẮT BUỘC: 只有多练习，才能说好 = chỉ có luyện nhiều mới nói giỏi được.",
            "examples": [
                {"cn": "只有多听多说，才能学好汉语。", "pinyin": "Zhǐyǒu duō tīng duō shuō, cáinéng xué hǎo Hànyǔ.", "hv": "chỉ hữu đa thính đa thuyết, tài năng học hảo Hán ngữ", "vi": "Chỉ có nghe nhiều nói nhiều mới học giỏi tiếng Trung được."},
                {"cn": "只有他才知道答案。", "pinyin": "Zhǐyǒu tā cái zhīdào dá'àn.", "hv": "chỉ hữu tha tài tri đạo đáp án", "vi": "Chỉ có anh ấy mới biết đáp án."},
            ],
        },
        {
            "id": "hsk4-qilai",
            "title": "V + 起来 (khởi lai) — bắt đầu / nhận xét",
            "pattern": "Động từ/tính từ + 起来",
            "explanation": "Hai nghĩa chính: (1) bắt đầu hành động: 笑起来 = bật cười; (2) nhận xét khi thử: 看起来很好吃 = 'trông có vẻ ngon'.",
            "examples": [
                {"cn": "听了这话，大家都笑起来。", "pinyin": "Tīng le zhè huà, dàjiā dōu xiào qilai.", "hv": "thính liễu giá thoại, đại gia đô tiếu khởi lai", "vi": "Nghe câu đó, mọi người đều bật cười."},
                {"cn": "这个菜看起来很好吃。", "pinyin": "Zhège cài kàn qilai hěn hǎochī.", "hv": "giá cá thái khán khởi lai ngận hảo cật", "vi": "Món này trông có vẻ rất ngon."},
            ],
        },
        {
            "id": "hsk4-bushi-ershi",
            "title": "不是…而是… (bất thị… nhi thị…)",
            "pattern": "不是 + A, 而是 + B",
            "explanation": "'Không phải A mà là B' — phủ định A để khẳng định B: 他不是不想去，而是没时间.",
            "examples": [
                {"cn": "他不是老师，而是学生。", "pinyin": "Tā bú shì lǎoshī, ér shì xuéshēng.", "hv": "tha bất thị lão sư, nhi thị học sinh", "vi": "Anh ấy không phải giáo viên mà là học sinh."},
                {"cn": "问题不是钱，而是时间。", "pinyin": "Wèntí bú shì qián, ér shì shíjiān.", "hv": "vấn đề bất thị tiền, nhi thị thời gian", "vi": "Vấn đề không phải tiền mà là thời gian."},
            ],
        },
        {
            "id": "hsk4-que",
            "title": "却 (khước) — 'lại/thế mà'",
            "pattern": "Chủ ngữ + 却 + động từ",
            "explanation": "Diễn tả sự trái ngược bất ngờ, đứng SAU chủ ngữ (khác 但是 đứng đầu vế): 我等了他两个小时，他却没来.",
            "examples": [
                {"cn": "东西很贵，质量却不好。", "pinyin": "Dōngxi hěn guì, zhìliàng què bù hǎo.", "hv": "đông tây ngận quý, chất lượng khước bất hảo", "vi": "Đồ rất đắt, thế mà chất lượng lại không tốt."},
                {"cn": "他答应了，却没做到。", "pinyin": "Tā dāying le, què méi zuòdào.", "hv": "tha đáp ứng liễu, khước một tố đáo", "vi": "Anh ấy nhận lời rồi mà lại không làm được."},
            ],
        },
        {
            "id": "hsk4-jingran",
            "title": "竟然 (cánh nhiên) — không ngờ",
            "pattern": "Chủ ngữ + 竟然 + động từ",
            "explanation": "Bày tỏ NGẠC NHIÊN vì ngoài dự đoán: 他竟然赢了 = 'không ngờ anh ấy thắng'.",
            "examples": [
                {"cn": "这么难的题，他竟然做出来了。", "pinyin": "Zhème nán de tí, tā jìngrán zuò chulai le.", "hv": "giá ma nan đích đề, tha cánh nhiên tố xuất lai liễu", "vi": "Đề khó thế mà không ngờ anh ấy làm ra được."},
                {"cn": "他竟然忘了我的生日。", "pinyin": "Tā jìngrán wàng le wǒ de shēngrì.", "hv": "tha cánh nhiên vong liễu ngã đích sinh nhật", "vi": "Không ngờ anh ấy quên sinh nhật tôi."},
            ],
        },
    ],
    5: [
        {
            "id": "hsk5-shi-ling",
            "title": "使 / 令 (sử / lệnh) — khiến cho",
            "pattern": "A + 使/令 + B + tính từ/động từ",
            "explanation": "Văn viết trang trọng của 让: 这个消息使大家很高兴. 令 thường đi cảm xúc mạnh: 令人感动 (khiến người ta cảm động).",
            "examples": [
                {"cn": "这个消息使我们非常激动。", "pinyin": "Zhège xiāoxi shǐ wǒmen fēicháng jīdòng.", "hv": "giá cá tiêu tức sử ngã môn phi thường kích động", "vi": "Tin này khiến chúng tôi vô cùng phấn khích."},
                {"cn": "他的故事令人感动。", "pinyin": "Tā de gùshi lìng rén gǎndòng.", "hv": "tha đích cố sự lệnh nhân cảm động", "vi": "Câu chuyện của anh ấy khiến người ta cảm động."},
            ],
        },
        {
            "id": "hsk5-duiyu-guanyu",
            "title": "对于 / 关于 (đối vu / quan vu)",
            "pattern": "对于/关于 + đối tượng, câu",
            "explanation": "对于 = 'đối với' (thái độ/quan hệ với đối tượng); 关于 = 'về/liên quan đến' (phạm vi nội dung, hay đứng đầu câu hoặc trước danh từ).",
            "examples": [
                {"cn": "对于这个问题，大家有不同的看法。", "pinyin": "Duìyú zhège wèntí, dàjiā yǒu bùtóng de kànfǎ.", "hv": "đối vu giá cá vấn đề, đại gia hữu bất đồng đích khán pháp", "vi": "Đối với vấn đề này, mọi người có cách nhìn khác nhau."},
                {"cn": "这是一本关于中国历史的书。", "pinyin": "Zhè shì yì běn guānyú Zhōngguó lìshǐ de shū.", "hv": "giá thị nhất bản quan vu Trung Quốc lịch sử đích thư", "vi": "Đây là một cuốn sách về lịch sử Trung Quốc."},
            ],
        },
        {
            "id": "hsk5-yudan",
            "title": "一旦…就… (nhất đán… tựu…)",
            "pattern": "一旦 + tình huống, 就 + hệ quả",
            "explanation": "'Một khi… là…' — nhấn mạnh hệ quả tất yếu ngay khi điều kiện xảy ra: 一旦开始，就不能停.",
            "examples": [
                {"cn": "一旦决定了，就不要后悔。", "pinyin": "Yídàn juédìng le, jiù bú yào hòuhuǐ.", "hv": "nhất đán quyết định liễu, tựu bất yếu hậu hối", "vi": "Một khi đã quyết định thì đừng hối hận."},
                {"cn": "机会一旦错过，就很难再有。", "pinyin": "Jīhuì yídàn cuòguò, jiù hěn nán zài yǒu.", "hv": "cơ hội nhất đán thác quá, tựu ngận nan tái hữu", "vi": "Cơ hội một khi bỏ lỡ thì rất khó có lại."},
            ],
        },
        {
            "id": "hsk5-yuqi-buru",
            "title": "与其…不如… (dữ kỳ… bất như…)",
            "pattern": "与其 + A, 不如 + B",
            "explanation": "'Thay vì A chi bằng B' — so sánh hai phương án và chọn B: 与其等他，不如自己做.",
            "examples": [
                {"cn": "与其在家等，不如出去找他。", "pinyin": "Yǔqí zài jiā děng, bùrú chūqu zhǎo tā.", "hv": "dữ kỳ tại gia đẳng, bất như xuất khứ trảo tha", "vi": "Thay vì ở nhà đợi, chi bằng ra ngoài tìm anh ấy."},
                {"cn": "与其抱怨，不如改变自己。", "pinyin": "Yǔqí bàoyuàn, bùrú gǎibiàn zìjǐ.", "hv": "dữ kỳ bão oán, bất như cải biến tự kỷ", "vi": "Thay vì oán trách, chi bằng thay đổi chính mình."},
            ],
        },
        {
            "id": "hsk5-ningke",
            "title": "宁可…也不… (ninh khả… dã bất…)",
            "pattern": "宁可 + A, 也不 + B",
            "explanation": "'Thà A chứ không B' — chấp nhận thiệt để tránh điều tệ hơn: 宁可累一点，也不放弃.",
            "examples": [
                {"cn": "我宁可走路，也不坐他的车。", "pinyin": "Wǒ nìngkě zǒulù, yě bú zuò tā de chē.", "hv": "ngã ninh khả tẩu lộ, dã bất toạ tha đích xa", "vi": "Tôi thà đi bộ chứ không ngồi xe anh ta."},
                {"cn": "宁可少赚钱，也不做坏事。", "pinyin": "Nìngkě shǎo zhuànqián, yě bú zuò huàishì.", "hv": "ninh khả thiểu trám tiền, dã bất tố hoại sự", "vi": "Thà kiếm ít tiền chứ không làm việc xấu."},
            ],
        },
        {
            "id": "hsk5-fan-er",
            "title": "反而 (phản nhi) — trái lại",
            "pattern": "…, (chủ ngữ) 反而 + động từ",
            "explanation": "Kết quả NGƯỢC hẳn mong đợi: 吃了药，病反而更重了 = 'uống thuốc rồi bệnh trái lại còn nặng hơn'.",
            "examples": [
                {"cn": "我安慰他，他反而更生气了。", "pinyin": "Wǒ ānwèi tā, tā fǎn'ér gèng shēngqì le.", "hv": "ngã an uỷ tha, tha phản nhi cánh sinh khí liễu", "vi": "Tôi an ủi anh ấy, anh ấy trái lại càng tức giận."},
                {"cn": "雨不但没停，反而下得更大了。", "pinyin": "Yǔ búdàn méi tíng, fǎn'ér xià de gèng dà le.", "hv": "vũ bất đãn một đình, phản nhi hạ đắc cánh đại liễu", "vi": "Mưa không những không tạnh mà trái lại còn to hơn."},
            ],
        },
        {
            "id": "hsk5-chufei",
            "title": "除非…否则… (trừ phi… phủ tắc…)",
            "pattern": "除非 + điều kiện, 否则 + hậu quả",
            "explanation": "除非 chính là 'trừ phi' Hán-Việt! 'Trừ phi… nếu không thì…': 除非你去，否则我不去.",
            "examples": [
                {"cn": "除非下雨，否则我们一定去爬山。", "pinyin": "Chúfēi xià yǔ, fǒuzé wǒmen yídìng qù páshān.", "hv": "trừ phi hạ vũ, phủ tắc ngã môn nhất định khứ ba sơn", "vi": "Trừ phi trời mưa, nếu không chúng tôi nhất định đi leo núi."},
                {"cn": "除非他道歉，否则我不会原谅他。", "pinyin": "Chúfēi tā dàoqiàn, fǒuzé wǒ bú huì yuánliàng tā.", "hv": "trừ phi tha đạo khiểm, phủ tắc ngã bất hội nguyên lượng tha", "vi": "Trừ phi anh ấy xin lỗi, nếu không tôi sẽ không tha thứ."},
            ],
        },
        {
            "id": "hsk5-zhisuoyi",
            "title": "之所以…是因为… (chi sở dĩ…)",
            "pattern": "A 之所以 + kết quả, 是因为 + nguyên nhân",
            "explanation": "Đảo kết quả lên trước để nhấn mạnh nguyên nhân: 他之所以成功，是因为他努力 = 'sở dĩ anh ấy thành công là vì anh ấy nỗ lực'. 'Sở dĩ' Hán-Việt dùng y hệt!",
            "examples": [
                {"cn": "他之所以迟到，是因为堵车。", "pinyin": "Tā zhīsuǒyǐ chídào, shì yīnwèi dǔchē.", "hv": "tha chi sở dĩ trì đáo, thị nhân vị đổ xa", "vi": "Sở dĩ anh ấy đến muộn là vì tắc đường."},
                {"cn": "我之所以学汉语，是因为想去中国工作。", "pinyin": "Wǒ zhīsuǒyǐ xué Hànyǔ, shì yīnwèi xiǎng qù Zhōngguó gōngzuò.", "hv": "ngã chi sở dĩ học Hán ngữ, thị nhân vị tưởng khứ Trung Quốc công tác", "vi": "Sở dĩ tôi học tiếng Trung là vì muốn sang Trung Quốc làm việc."},
            ],
        },
        {
            "id": "hsk5-yi-wei",
            "title": "以…为… (dĩ… vi…)",
            "pattern": "以 + A + 为 + B",
            "explanation": "Cấu trúc văn viết 'lấy A làm B': 以学生为中心 = 'lấy học sinh làm trung tâm'. Gặp nhiều trong báo chí, văn kiện.",
            "examples": [
                {"cn": "我们要以健康为重。", "pinyin": "Wǒmen yào yǐ jiànkāng wéi zhòng.", "hv": "ngã môn yếu dĩ kiện khang vi trọng", "vi": "Chúng ta phải lấy sức khoẻ làm trọng."},
                {"cn": "这家公司以质量为第一。", "pinyin": "Zhè jiā gōngsī yǐ zhìliàng wéi dì-yī.", "hv": "giá gia công ty dĩ chất lượng vi đệ nhất", "vi": "Công ty này lấy chất lượng làm hàng đầu."},
            ],
        },
        {
            "id": "hsk5-hekuang",
            "title": "何况 (hà huống) — huống chi",
            "pattern": "…, 何况 + trường hợp mạnh hơn",
            "explanation": "'Huống chi/huống hồ' — y hệt Hán-Việt: 大人都做不到，何况孩子 = 'người lớn còn không làm được, huống chi trẻ con'.",
            "examples": [
                {"cn": "这个问题连专家都难回答，何况我们。", "pinyin": "Zhège wèntí lián zhuānjiā dōu nán huídá, hékuàng wǒmen.", "hv": "giá cá vấn đề liên chuyên gia đô nan hồi đáp, hà huống ngã môn", "vi": "Vấn đề này chuyên gia còn khó trả lời, huống chi chúng ta."},
                {"cn": "他平时都很忙，何况现在是年底。", "pinyin": "Tā píngshí dōu hěn máng, hékuàng xiànzài shì niándǐ.", "hv": "tha bình thời đô ngận mang, hà huống hiện tại thị niên để", "vi": "Bình thường anh ấy đã bận, huống chi bây giờ là cuối năm."},
            ],
        },
    ],
    6: [
        {
            "id": "hsk6-guran",
            "title": "固然 (cố nhiên) — cố nhiên là",
            "pattern": "A 固然 + đúng, 但/却 + B",
            "explanation": "'Cố nhiên' Hán-Việt dùng y hệt: thừa nhận A đúng rồi chuyển sang ý quan trọng hơn: 钱固然重要，但健康更重要.",
            "examples": [
                {"cn": "钱固然重要，但不是一切。", "pinyin": "Qián gùrán zhòngyào, dàn bú shì yíqiè.", "hv": "tiền cố nhiên trọng yếu, đãn bất thị nhất thiết", "vi": "Tiền cố nhiên quan trọng, nhưng không phải là tất cả."},
                {"cn": "成功固然好，失败也是经验。", "pinyin": "Chénggōng gùrán hǎo, shībài yě shì jīngyàn.", "hv": "thành công cố nhiên hảo, thất bại dã thị kinh nghiệm", "vi": "Thành công cố nhiên tốt, thất bại cũng là kinh nghiệm."},
            ],
        },
        {
            "id": "hsk6-bufang",
            "title": "不妨 (bất phương) — chẳng ngại gì",
            "pattern": "不妨 + động từ",
            "explanation": "Gợi ý nhẹ nhàng 'cứ thử… xem sao, không hại gì': 你不妨试试 = 'bạn cứ thử xem'.",
            "examples": [
                {"cn": "有问题不妨直接问老师。", "pinyin": "Yǒu wèntí bùfáng zhíjiē wèn lǎoshī.", "hv": "hữu vấn đề bất phương trực tiếp vấn lão sư", "vi": "Có vấn đề cứ hỏi thẳng giáo viên, chẳng ngại gì."},
                {"cn": "周末不妨去郊外走走。", "pinyin": "Zhōumò bùfáng qù jiāowài zǒuzou.", "hv": "chu mạt bất phương khứ giao ngoại tẩu tẩu", "vi": "Cuối tuần cứ thử ra ngoại ô dạo chơi xem."},
            ],
        },
        {
            "id": "hsk6-nanmian",
            "title": "难免 (nan miễn) — khó tránh khỏi",
            "pattern": "…难免 + động từ/tình huống",
            "explanation": "'Khó tránh khỏi' — việc không mong muốn nhưng dễ hiểu: 第一次上台，难免紧张. So với 未免 (vị miễn): 未免 là NHẬN XÉT 'e rằng hơi quá'.",
            "examples": [
                {"cn": "刚开始工作，难免会犯错误。", "pinyin": "Gāng kāishǐ gōngzuò, nánmiǎn huì fàn cuòwù.", "hv": "cương khai thuỷ công tác, nan miễn hội phạm thác ngộ", "vi": "Mới đi làm, khó tránh khỏi mắc lỗi."},
                {"cn": "你这样说，未免太不客气了。", "pinyin": "Nǐ zhèyàng shuō, wèimiǎn tài bú kèqi le.", "hv": "nhĩ giá dạng thuyết, vị miễn thái bất khách khí liễu", "vi": "Bạn nói vậy e rằng hơi thiếu lịch sự."},
            ],
        },
        {
            "id": "hsk6-wufei",
            "title": "无非 (vô phi) — chẳng qua là",
            "pattern": "…无非 (是) + nội dung",
            "explanation": "'Chẳng qua chỉ là' — thu hẹp vấn đề, coi nhẹ: 他无非是想多赚点钱.",
            "examples": [
                {"cn": "他说这些，无非是想让你放心。", "pinyin": "Tā shuō zhèxiē, wúfēi shì xiǎng ràng nǐ fàngxīn.", "hv": "tha thuyết giá ta, vô phi thị tưởng nhượng nhĩ phóng tâm", "vi": "Anh ấy nói vậy chẳng qua là muốn bạn yên tâm."},
                {"cn": "成功的秘诀无非是坚持。", "pinyin": "Chénggōng de mìjué wúfēi shì jiānchí.", "hv": "thành công đích bí quyết vô phi thị kiên trì", "vi": "Bí quyết thành công chẳng qua là kiên trì."},
            ],
        },
        {
            "id": "hsk6-yiwei",
            "title": "一味 (nhất vị) — một mực",
            "pattern": "一味 (地) + động từ",
            "explanation": "'Một mực/khăng khăng' làm gì đó bất chấp — sắc thái phê phán: 一味追求利润 = 'một mực chạy theo lợi nhuận'.",
            "examples": [
                {"cn": "不能一味地批评孩子。", "pinyin": "Bù néng yíwèi de pīpíng háizi.", "hv": "bất năng nhất vị địa phê bình hài tử", "vi": "Không thể một mực phê bình con trẻ."},
                {"cn": "他一味地工作，不注意身体。", "pinyin": "Tā yíwèi de gōngzuò, bú zhùyì shēntǐ.", "hv": "tha nhất vị địa công tác, bất chú ý thân thể", "vi": "Anh ấy một mực làm việc, không chú ý sức khoẻ."},
            ],
        },
        {
            "id": "hsk6-fei-buke",
            "title": "非…不可 (phi… bất khả)",
            "pattern": "非 + động từ + 不可",
            "explanation": "Phủ định kép = khẳng định mạnh 'nhất định phải': 这件事非你去不可 = 'việc này nhất định phải bạn đi mới được'.",
            "examples": [
                {"cn": "这个会议很重要，你非参加不可。", "pinyin": "Zhège huìyì hěn zhòngyào, nǐ fēi cānjiā bùkě.", "hv": "giá cá hội nghị ngận trọng yếu, nhĩ phi tham gia bất khả", "vi": "Cuộc họp này rất quan trọng, bạn nhất định phải tham gia."},
                {"cn": "要学好汉语，非下功夫不可。", "pinyin": "Yào xué hǎo Hànyǔ, fēi xià gōngfu bùkě.", "hv": "yếu học hảo Hán ngữ, phi hạ công phu bất khả", "vi": "Muốn học giỏi tiếng Trung, nhất định phải bỏ công sức."},
            ],
        },
        {
            "id": "hsk6-dabuliao",
            "title": "大不了 (đại bất liễu) — cùng lắm thì",
            "pattern": "大不了 + phương án xấu nhất",
            "explanation": "'Cùng lắm thì…' — trấn an rằng hậu quả xấu nhất cũng chấp nhận được: 大不了重新开始.",
            "examples": [
                {"cn": "别怕，大不了我们从头再来。", "pinyin": "Bié pà, dàbuliǎo wǒmen cóngtóu zài lái.", "hv": "biệt phạ, đại bất liễu ngã môn tòng đầu tái lai", "vi": "Đừng sợ, cùng lắm thì chúng ta làm lại từ đầu."},
                {"cn": "试试吧，大不了失败一次。", "pinyin": "Shìshi ba, dàbuliǎo shībài yí cì.", "hv": "thí thí ba, đại bất liễu thất bại nhất thứ", "vi": "Thử đi, cùng lắm thì thất bại một lần."},
            ],
        },
        {
            "id": "hsk6-qi",
            "title": "岂 (khởi) — há lẽ nào",
            "pattern": "岂 + 不/能/是…",
            "explanation": "Câu hỏi tu từ văn viết: 岂不是 = 'há chẳng phải', 岂能 = 'há có thể'. Người Việt gặp trong truyện cổ: 'há lẽ nào'.",
            "examples": [
                {"cn": "这样做岂不是更好？", "pinyin": "Zhèyàng zuò qǐ bú shì gèng hǎo?", "hv": "giá dạng tố khởi bất thị cánh hảo", "vi": "Làm vậy há chẳng phải tốt hơn sao?"},
                {"cn": "答应了的事，岂能不做？", "pinyin": "Dāying le de shì, qǐ néng bú zuò?", "hv": "đáp ứng liễu đích sự, khởi năng bất tố", "vi": "Việc đã nhận lời, há có thể không làm?"},
            ],
        },
    ],
    7: [
        {
            "id": "hsk7-jianyu",
            "title": "鉴于 (giám vu) — xét thấy",
            "pattern": "鉴于 + tình hình, kết luận",
            "explanation": "Mở đầu trang trọng trong văn bản/báo cáo: 'xét thấy/căn cứ tình hình': 鉴于天气原因，航班取消.",
            "examples": [
                {"cn": "鉴于目前的情况，会议推迟举行。", "pinyin": "Jiànyú mùqián de qíngkuàng, huìyì tuīchí jǔxíng.", "hv": "giám vu mục tiền đích tình huống, hội nghị suy trì cử hành", "vi": "Xét tình hình hiện tại, hội nghị hoãn tổ chức."},
                {"cn": "鉴于他的贡献，公司决定给他升职。", "pinyin": "Jiànyú tā de gòngxiàn, gōngsī juédìng gěi tā shēngzhí.", "hv": "giám vu tha đích cống hiến, công ty quyết định cấp tha thăng chức", "vi": "Xét đóng góp của anh ấy, công ty quyết định thăng chức."},
            ],
        },
        {
            "id": "hsk7-yimian",
            "title": "以免 (dĩ miễn) — để tránh",
            "pattern": "Hành động, 以免 + hậu quả xấu",
            "explanation": "'Để tránh/kẻo': 早点出发，以免堵车. Đối lập 以便 (dĩ tiện) = 'để tiện cho' (mục đích tốt).",
            "examples": [
                {"cn": "请记好密码，以免忘记。", "pinyin": "Qǐng jì hǎo mìmǎ, yǐmiǎn wàngjì.", "hv": "thỉnh ký hảo mật mã, dĩ miễn vong ký", "vi": "Hãy ghi nhớ mật khẩu để tránh quên."},
                {"cn": "请留下电话，以便联系。", "pinyin": "Qǐng liúxià diànhuà, yǐbiàn liánxì.", "hv": "thỉnh lưu hạ điện thoại, dĩ tiện liên hệ", "vi": "Xin để lại số điện thoại để tiện liên hệ."},
            ],
        },
        {
            "id": "hsk7-tangruo",
            "title": "倘若 / 假使 (thảng nhược / giả sử)",
            "pattern": "倘若 + giả thiết, …",
            "explanation": "Bản văn viết của 如果. 假使 chính là 'giả sử' Hán-Việt: 倘若有机会，我一定去.",
            "examples": [
                {"cn": "倘若明天天气好，我们就出发。", "pinyin": "Tǎngruò míngtiān tiānqì hǎo, wǒmen jiù chūfā.", "hv": "thảng nhược minh thiên thiên khí hảo, ngã môn tựu xuất phát", "vi": "Nếu như mai thời tiết đẹp, chúng ta sẽ xuất phát."},
                {"cn": "假使当时你在场，你会怎么做？", "pinyin": "Jiǎshǐ dāngshí nǐ zàichǎng, nǐ huì zěnme zuò?", "hv": "giả sử đương thời nhĩ tại trường, nhĩ hội chẩm ma tố", "vi": "Giả sử lúc đó bạn có mặt, bạn sẽ làm thế nào?"},
            ],
        },
        {
            "id": "hsk7-zhuru",
            "title": "诸如 (chư như) — chẳng hạn như",
            "pattern": "…, 诸如 + ví dụ liệt kê",
            "explanation": "Liệt kê trang trọng 'như là/chẳng hạn': 诸如此类 = 'những thứ đại loại như vậy'.",
            "examples": [
                {"cn": "他会很多乐器，诸如钢琴、吉他等。", "pinyin": "Tā huì hěn duō yuèqì, zhūrú gāngqín, jítā děng.", "hv": "tha hội ngận đa nhạc khí, chư như cương cầm, cát tha đẳng", "vi": "Anh ấy chơi được nhiều nhạc cụ, chẳng hạn piano, guitar."},
                {"cn": "网上有很多骗局，诸如此类，要小心。", "pinyin": "Wǎngshàng yǒu hěn duō piànjú, zhūrú cǐ lèi, yào xiǎoxīn.", "hv": "võng thượng hữu ngận đa phiến cục, chư như thử loại, yếu tiểu tâm", "vi": "Trên mạng có nhiều trò lừa đảo đại loại như vậy, phải cẩn thận."},
            ],
        },
        {
            "id": "hsk7-jiu-eryan",
            "title": "就…而言 (tựu… nhi ngôn)",
            "pattern": "就 + phương diện + 而言",
            "explanation": "'Xét về mặt…mà nói': 就质量而言，这是最好的 = 'xét về chất lượng mà nói, đây là tốt nhất'.",
            "examples": [
                {"cn": "就发音而言，越南人学汉语有优势。", "pinyin": "Jiù fāyīn ér yán, Yuènán rén xué Hànyǔ yǒu yōushì.", "hv": "tựu phát âm nhi ngôn, Việt Nam nhân học Hán ngữ hữu ưu thế", "vi": "Xét về phát âm mà nói, người Việt học tiếng Trung có lợi thế."},
                {"cn": "就价格而言，这家店最便宜。", "pinyin": "Jiù jiàgé ér yán, zhè jiā diàn zuì piányi.", "hv": "tựu giá cách nhi ngôn, giá gia điếm tối tiện nghi", "vi": "Xét về giá cả mà nói, cửa hàng này rẻ nhất."},
            ],
        },
        {
            "id": "hsk7-shibi",
            "title": "势必 (thế tất) — ắt sẽ",
            "pattern": "…势必 + kết quả tất yếu",
            "explanation": "'Thế tất/ắt phải' — suy đoán chắc chắn dựa trên xu thế: 这样下去，势必失败.",
            "examples": [
                {"cn": "长期熬夜，势必影响健康。", "pinyin": "Chángqī áoyè, shìbì yǐngxiǎng jiànkāng.", "hv": "trường kỳ ngao dạ, thế tất ảnh hưởng kiện khang", "vi": "Thức khuya lâu dài ắt sẽ ảnh hưởng sức khoẻ."},
                {"cn": "油价上涨，物价势必上升。", "pinyin": "Yóujià shàngzhǎng, wùjià shìbì shàngshēng.", "hv": "du giá thượng trướng, vật giá thế tất thượng thăng", "vi": "Giá xăng tăng, vật giá ắt sẽ tăng theo."},
            ],
        },
        {
            "id": "hsk7-youdaiyu",
            "title": "有待于 (hữu đãi vu) — còn chờ",
            "pattern": "…有待(于) + động từ",
            "explanation": "'Còn phải chờ/cần được…' — văn viết: 这个问题有待研究 = 'vấn đề này còn cần nghiên cứu thêm'.",
            "examples": [
                {"cn": "这个方案有待于进一步讨论。", "pinyin": "Zhège fāng'àn yǒudàiyú jìnyíbù tǎolùn.", "hv": "giá cá phương án hữu đãi vu tiến nhất bộ thảo luận", "vi": "Phương án này còn cần thảo luận thêm."},
                {"cn": "他的能力有待提高。", "pinyin": "Tā de nénglì yǒudài tígāo.", "hv": "tha đích năng lực hữu đãi đề cao", "vi": "Năng lực của anh ấy còn cần nâng cao."},
            ],
        },
    ],
    8: [
        {
            "id": "hsk8-weiyou-fangneng",
            "title": "唯有…方能… (duy hữu… phương năng…)",
            "pattern": "唯有 + điều kiện, 方能 + kết quả",
            "explanation": "Bản văn ngôn của 只有…才能: 'duy chỉ có… mới có thể'. Xuất hiện trong diễn văn, bài luận.",
            "examples": [
                {"cn": "唯有坚持，方能成功。", "pinyin": "Wéiyǒu jiānchí, fāng néng chénggōng.", "hv": "duy hữu kiên trì, phương năng thành công", "vi": "Duy chỉ có kiên trì mới có thể thành công."},
                {"cn": "唯有合作，方能共赢。", "pinyin": "Wéiyǒu hézuò, fāng néng gòngyíng.", "hv": "duy hữu hợp tác, phương năng cộng doanh", "vi": "Duy chỉ có hợp tác mới có thể cùng thắng."},
            ],
        },
        {
            "id": "hsk8-wubu",
            "title": "无不 / 无一不 (vô bất) — không ai không",
            "pattern": "Chủ ngữ + 无不 + động từ",
            "explanation": "Phủ định kép văn viết = 'tất cả đều': 听者无不感动 = 'người nghe không ai không cảm động'.",
            "examples": [
                {"cn": "在场的人无不为他鼓掌。", "pinyin": "Zàichǎng de rén wúbù wèi tā gǔzhǎng.", "hv": "tại trường đích nhân vô bất vị tha cổ chưởng", "vi": "Người có mặt không ai không vỗ tay vì anh ấy."},
                {"cn": "游客无一不称赞这里的风景。", "pinyin": "Yóukè wú yī bù chēngzàn zhèlǐ de fēngjǐng.", "hv": "du khách vô nhất bất xưng tán giá lý đích phong cảnh", "vi": "Du khách không một ai không khen phong cảnh nơi này."},
            ],
        },
        {
            "id": "hsk8-bujin",
            "title": "不禁 (bất cấm) — không kìm được",
            "pattern": "Chủ ngữ + 不禁 + động từ cảm xúc",
            "explanation": "'Không kìm/nhịn được' phản ứng cảm xúc: 不禁笑了起来 = 'không nhịn được bật cười'.",
            "examples": [
                {"cn": "看到老照片，她不禁流下眼泪。", "pinyin": "Kàndào lǎo zhàopiàn, tā bùjīn liúxià yǎnlèi.", "hv": "khán đáo lão chiếu phiến, tha bất cấm lưu hạ nhãn lệ", "vi": "Nhìn ảnh cũ, cô ấy không kìm được rơi nước mắt."},
                {"cn": "听到这个笑话，大家不禁大笑。", "pinyin": "Tīngdào zhège xiàohua, dàjiā bùjīn dà xiào.", "hv": "thính đáo giá cá tiếu thoại, đại gia bất cấm đại tiếu", "vi": "Nghe câu chuyện cười, mọi người không nhịn được cười to."},
            ],
        },
        {
            "id": "hsk8-burong",
            "title": "不容 (bất dung) — không cho phép",
            "pattern": "…不容 + động từ",
            "explanation": "'Không thể/không cho phép' — khẳng định mạnh, văn viết: 不容忽视 = 'không thể xem nhẹ', 不容置疑 = 'không thể nghi ngờ'.",
            "examples": [
                {"cn": "环境问题不容忽视。", "pinyin": "Huánjìng wèntí bùróng hūshì.", "hv": "hoàn cảnh vấn đề bất dung hốt thị", "vi": "Vấn đề môi trường không thể xem nhẹ."},
                {"cn": "他的实力不容置疑。", "pinyin": "Tā de shílì bùróng zhìyí.", "hv": "tha đích thực lực bất dung trí nghi", "vi": "Thực lực của anh ấy không thể nghi ngờ."},
            ],
        },
        {
            "id": "hsk8-zhiji",
            "title": "…之际 (chi tế) — nhân dịp/vào lúc",
            "pattern": "Sự kiện + 之际",
            "explanation": "Trang trọng 'vào lúc/nhân dịp': 新年之际 = 'nhân dịp năm mới'. Hay mở đầu thư từ, diễn văn.",
            "examples": [
                {"cn": "值此新年之际，祝大家身体健康。", "pinyin": "Zhí cǐ xīnnián zhī jì, zhù dàjiā shēntǐ jiànkāng.", "hv": "trị thử tân niên chi tế, chúc đại gia thân thể kiện khang", "vi": "Nhân dịp năm mới, chúc mọi người sức khoẻ."},
                {"cn": "毕业之际，同学们都很不舍。", "pinyin": "Bìyè zhī jì, tóngxuémen dōu hěn bùshě.", "hv": "tất nghiệp chi tế, đồng học môn đô ngận bất xả", "vi": "Vào lúc tốt nghiệp, các bạn học đều lưu luyến."},
            ],
        },
        {
            "id": "hsk8-guqie",
            "title": "姑且 (cô thả) — tạm thời cứ",
            "pattern": "姑且 + động từ",
            "explanation": "'Tạm cứ/hẵng cứ' làm gì trong khi chưa có phương án tốt hơn: 姑且试试看.",
            "examples": [
                {"cn": "我们姑且按原计划进行。", "pinyin": "Wǒmen gūqiě àn yuán jìhuà jìnxíng.", "hv": "ngã môn cô thả án nguyên kế hoạch tiến hành", "vi": "Chúng ta tạm cứ tiến hành theo kế hoạch cũ."},
                {"cn": "真假姑且不论，先听他说完。", "pinyin": "Zhēnjiǎ gūqiě bú lùn, xiān tīng tā shuō wán.", "hv": "chân giả cô thả bất luận, tiên thính tha thuyết hoàn", "vi": "Thật giả tạm chưa bàn, trước hết nghe anh ấy nói hết đã."},
            ],
        },
        {
            "id": "hsk8-yushi-jubian",
            "title": "与日俱增 (dữ nhật câu tăng)",
            "pattern": "Danh từ + 与日俱增",
            "explanation": "Thành ngữ 'tăng lên từng ngày' — dùng như vị ngữ: 压力与日俱增. Nhiều thành ngữ 4 chữ đọc âm Hán-Việt là hiểu ngay.",
            "examples": [
                {"cn": "学汉语的人数与日俱增。", "pinyin": "Xué Hànyǔ de rénshù yǔrìjùzēng.", "hv": "học Hán ngữ đích nhân số dữ nhật câu tăng", "vi": "Số người học tiếng Trung tăng lên từng ngày."},
                {"cn": "两国的合作与日俱增。", "pinyin": "Liǎng guó de hézuò yǔrìjùzēng.", "hv": "lưỡng quốc đích hợp tác dữ nhật câu tăng", "vi": "Hợp tác hai nước ngày một tăng."},
            ],
        },
    ],
    9: [
        {
            "id": "hsk9-zongshangsuoshu",
            "title": "综上所述 (tổng thượng sở thuật)",
            "pattern": "综上所述，+ kết luận",
            "explanation": "'Tổng hợp những điều đã trình bày ở trên' — câu mở đoạn kết trong bài luận, báo cáo. Bắt buộc phải biết khi viết luận HSK cấp cao.",
            "examples": [
                {"cn": "综上所述，这个方案是可行的。", "pinyin": "Zōng shàng suǒ shù, zhège fāng'àn shì kěxíng de.", "hv": "tổng thượng sở thuật, giá cá phương án thị khả hành đích", "vi": "Tổng kết những điều trên, phương án này là khả thi."},
                {"cn": "综上所述，环保应从每个人做起。", "pinyin": "Zōng shàng suǒ shù, huánbǎo yīng cóng měi ge rén zuòqǐ.", "hv": "tổng thượng sở thuật, hoàn bảo ưng tòng mỗi cá nhân tố khởi", "vi": "Tóm lại, bảo vệ môi trường nên bắt đầu từ mỗi người."},
            ],
        },
        {
            "id": "hsk9-ruoefei",
            "title": "若非 (nhược phi) — nếu không phải",
            "pattern": "若非 + A, B (giả định ngược)",
            "explanation": "Văn ngôn 'nếu không nhờ/nếu chẳng phải': 若非你帮忙，我早就失败了.",
            "examples": [
                {"cn": "若非亲眼所见，我真不敢相信。", "pinyin": "Ruòfēi qīnyǎn suǒ jiàn, wǒ zhēn bù gǎn xiāngxìn.", "hv": "nhược phi thân nhãn sở kiến, ngã chân bất cảm tương tín", "vi": "Nếu không tận mắt thấy, tôi thật không dám tin."},
                {"cn": "若非大家支持，项目不可能完成。", "pinyin": "Ruòfēi dàjiā zhīchí, xiàngmù bù kěnéng wánchéng.", "hv": "nhược phi đại gia chi trì, hạng mục bất khả năng hoàn thành", "vi": "Nếu không nhờ mọi người ủng hộ, dự án không thể hoàn thành."},
            ],
        },
        {
            "id": "hsk9-cong-jiaodu",
            "title": "从…的角度来看 (giác độ)",
            "pattern": "从 + góc nhìn + 的角度来看",
            "explanation": "'Nhìn từ góc độ…' — 角度 chính là 'giác độ'. Khung câu chuẩn cho văn nghị luận: 从经济的角度来看….",
            "examples": [
                {"cn": "从教育的角度来看，这个政策很有意义。", "pinyin": "Cóng jiàoyù de jiǎodù lái kàn, zhège zhèngcè hěn yǒu yìyì.", "hv": "tòng giáo dục đích giác độ lai khán, giá cá chính sách ngận hữu ý nghĩa", "vi": "Nhìn từ góc độ giáo dục, chính sách này rất có ý nghĩa."},
                {"cn": "从长远的角度来看，投资教育最划算。", "pinyin": "Cóng chángyuǎn de jiǎodù lái kàn, tóuzī jiàoyù zuì huásuàn.", "hv": "tòng trường viễn đích giác độ lai khán, đầu tư giáo dục tối hoạch toán", "vi": "Nhìn về lâu dài, đầu tư giáo dục là đáng nhất."},
            ],
        },
        {
            "id": "hsk9-buyan-eryu",
            "title": "不言而喻 (bất ngôn nhi dụ)",
            "pattern": "…是不言而喻的 / …不言而喻",
            "explanation": "Thành ngữ 'không nói cũng hiểu/hiển nhiên' — dùng khẳng định điều ai cũng thấy rõ trong văn luận.",
            "examples": [
                {"cn": "健康的重要性不言而喻。", "pinyin": "Jiànkāng de zhòngyàoxìng bùyán'éryù.", "hv": "kiện khang đích trọng yếu tính bất ngôn nhi dụ", "vi": "Tầm quan trọng của sức khoẻ là hiển nhiên không cần nói."},
                {"cn": "父母对孩子的爱不言而喻。", "pinyin": "Fùmǔ duì háizi de ài bùyán'éryù.", "hv": "phụ mẫu đối hài tử đích ái bất ngôn nhi dụ", "vi": "Tình yêu cha mẹ dành cho con cái không nói cũng hiểu."},
            ],
        },
        {
            "id": "hsk9-shufang",
            "title": "毋庸置疑 (vô dung trí nghi)",
            "pattern": "毋庸置疑，… / …毋庸置疑",
            "explanation": "'Không cần bàn cãi' — mức khẳng định cao nhất trong văn viết, thay cho 当然 khẩu ngữ.",
            "examples": [
                {"cn": "毋庸置疑，科技改变了我们的生活。", "pinyin": "Wúyōng zhìyí, kējì gǎibiàn le wǒmen de shēnghuó.", "hv": "vô dung trí nghi, khoa kỹ cải biến liễu ngã môn đích sinh hoạt", "vi": "Không cần bàn cãi, khoa học kỹ thuật đã thay đổi cuộc sống chúng ta."},
                {"cn": "他的专业水平毋庸置疑。", "pinyin": "Tā de zhuānyè shuǐpíng wúyōng zhìyí.", "hv": "tha đích chuyên nghiệp thuỷ bình vô dung trí nghi", "vi": "Trình độ chuyên môn của anh ấy là không phải bàn."},
            ],
        },
        {
            "id": "hsk9-jinguan-ruci",
            "title": "尽管如此 (tận quản như thử)",
            "pattern": "…。尽管如此，…",
            "explanation": "'Dù vậy/mặc dù thế' — từ nối liên đoạn trong văn luận, chuyển ý ngược sau khi đã trình bày: 尽管如此，我们仍要努力.",
            "examples": [
                {"cn": "任务很难。尽管如此，我们仍然完成了。", "pinyin": "Rènwu hěn nán. Jǐnguǎn rúcǐ, wǒmen réngrán wánchéng le.", "hv": "nhiệm vụ ngận nan. tận quản như thử, ngã môn nhưng nhiên hoàn thành liễu", "vi": "Nhiệm vụ rất khó. Dù vậy, chúng tôi vẫn hoàn thành."},
                {"cn": "天气恶劣。尽管如此，比赛照常进行。", "pinyin": "Tiānqì èliè. Jǐnguǎn rúcǐ, bǐsài zhàocháng jìnxíng.", "hv": "thiên khí ác liệt. tận quản như thử, tỉ tái chiếu thường tiến hành", "vi": "Thời tiết khắc nghiệt. Dù vậy, trận đấu vẫn diễn ra bình thường."},
            ],
        },
    ],
}


def get_grammar_levels():
    """Tóm tắt số điểm ngữ pháp mỗi cấp."""
    return [
        {"level": level, "count": len(points)}
        for level, points in sorted(GRAMMAR.items())
    ]


def get_grammar_points(level):
    return GRAMMAR.get(level, [])
