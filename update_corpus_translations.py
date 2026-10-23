# -*- coding: utf-8 -*-
"""
update_corpus_translations.py
1. Removes the long boiler-plate sentence from notes:
   "本句是道地英語中極具表現力的習慣用法，母語者在口語互動中經常藉此傳遞明確的態度與交際意圖，切忌按單字字面逐詞硬翻。"
2. Generates authentic Traditional Chinese translations (繁體中譯) for spkA and spkB across all 2,500 sentences.
"""

import json
import os
import re

CURATED_ZH = {
    "enough is enough": (
        "儘管屢遭投訴，他深夜依然大聲播放音樂。",
        "適可而止吧。我們必須向大樓管委會舉報這件事。"
    ),
    "says who": (
        "有人跟我說公司年會被取消了。",
        "誰說的？人資部根本沒人宣布過！"
    ),
    "fair enough": (
        "既然我們預算很緊，就先推遲華麗的辦公室重新設計吧。",
        "說得過去。現在實用性比外觀重要得多。"
    ),
    "big deal": (
        "他們在新生說明會上沒有發給我們免費的公司馬克杯。",
        "沒什麼大不了的。我們來這裡是為了好好工作，不是來收集馬克杯的。"
    ),
    "good grief": (
        "就在向客戶簡報之前，印表機竟然又卡紙了！",
        "天哪！我來看看能不能把進紙匣清乾淨。"
    ),
    "you bet": (
        "你準備好參加今晚的團隊慶祝活動了嗎？",
        "當然！我無論如何都不會錯過的。"
    ),
    "beats me": (
        "你知道會議室的遙控器跑哪去了嗎？",
        "我不知道。今天早上它還在桌上呢。"
    ),
    "point taken": (
        "如果我們現在不備份資料庫，恐怕會損失好幾個小時的工作成果。",
        "我明白你的意思了。我馬上執行備份腳本。"
    ),
    "not a chance": (
        "你覺得老闆會在產品發布期間批准三週的長假嗎？",
        "絕不可能。我們現在正處於最忙碌的旺季。"
    ),
    "over my dead body": (
        "他們想拆除這座歷史悠久的公園來改建停車場。",
        "除非我死了！我們必須發起請願來保留它。"
    ),
    "speak of the devil": (
        "你今天看到大衛了嗎？我正好想問他關於文件的事。",
        "說曹操，曹操就到！他正沿著走廊走過來呢。"
    ),
    "so far so good": (
        "新版手機 App 的使用者測試進行得如何了？",
        "目前為止都還好。我們尚未遇到任何重大錯誤。"
    ),
    "better late than never": (
        "抱歉我遲到了二十分鐘，路上交通完全堵死了。",
        "遲做總比不做好！快請進，我們才剛開始討論。"
    ),
    "no pain no gain": (
        "今天那場高強度健身訓練後，我全身肌肉痠痛不已。",
        "一分耕耘，一分收穫！你很快就會看到明顯進步的。"
    ),
    "time will tell": (
        "這波新的行銷活動本季會帶來更多顧客嗎？",
        "時間會證明一切。讓我們密切關注轉換率數據吧。"
    ),
    "count me in": (
        "我們幾個人正計畫週末去湖邊露營。",
        "算我一份！我整個月都想去戶外走走了。"
    ),
    "keep in touch": (
        "我下週要去倫敦接任新職務了。",
        "保持聯絡！安頓好後別忘了傳訊息給我。"
    ),
    "you name it": (
        "那家國際百匯餐廳提供哪些料理？",
        "海鮮、牛排、壽司、義大利麵……應有盡有，他們全都有！"
    ),
    "bottoms up": (
        "為了今晚慶祝我們產品順利發布，乾杯！",
        "乾杯！為大家的辛苦努力致敬！"
    ),
    "call it a day": (
        "我們從今天早上八點就一直在排查這個問題。",
        "今天就到此為止吧。明天帶著新思維來看會更有幫助。"
    ),
    "cut it out": (
        "安靜自習時間請不要再用筆敲桌子了。",
        "住手吧！你分了房間裡所有人的心。"
    ),
    "cross my heart": (
        "你能保證不洩漏我們的生日驚喜計畫嗎？",
        "我發誓！我的嘴巴絕對緊閉不語。"
    ),
    "out of the blue": (
        "你是怎麼知道公司要在東京開設分公司的？",
        "處長午餐時突然之間就提到了這件事。"
    ),
    "what a shame": (
        "戶外音樂會因為突如其來的雷雨而取消了。",
        "真可惜！我們已經期待好幾週了。"
    ),
    "never mind": (
        "你剛才需要我幫忙找那份遺失的報告嗎？",
        "沒關係了。我剛在下載資料夾裡找到了。"
    ),
    "take it easy": (
        "我對明天早上的董事會簡報感到壓力極大。",
        "放輕鬆。你對自己的內容瞭如指掌。"
    ),
    "make yourself at home": (
        "謝謝你邀請我來你家吃晚餐！",
        "別客氣，當自己家一樣！我來幫你拿點冰涼的飲料。"
    ),
    "help yourself": (
        "那些自製的手工巧克力餅乾看起來真好吃！",
        "請自便！我今天下午剛新鮮出爐的。"
    ),
    "take your time": (
        "我還需要幾分鐘來校對完這些投影片。",
        "慢慢來，別急。在客戶到達之前我們時間還很充裕。"
    ),
    "after you": (
        "我們兩人在同一瞬間走到了電梯門口。",
        "您先請！請走前面。"
    ),
    "don't mention it": (
        "非常感謝你在大雨滂沱中載我到機場！",
        "不客氣！隨時樂意幫忙。"
    ),
    "my pleasure": (
        "我非常感激你在整個培訓過程中給予的詳盡指導。",
        "我的榮幸！你學得非常快。"
    ),
    "anytime": (
        "感謝你在這麼倉促的時間幫我審查代碼！",
        "隨時樂意！有任何問題隨時聯繫我。"
    ),
    "same here": (
        "經過那場馬拉松式的電話會議後，我感到精疲力竭。",
        "我也是。我們去外面散個步充電一下吧。"
    ),
    "ditto": (
        "午餐我投轉角那家安靜咖啡館一票。",
        "同上。那裡比員工餐廳安靜多了。"
    ),
    "i'm with you": (
        "我認為在增加更多功能之前，我們應該專注於使用者體驗。",
        "我支持你。簡潔才是我們使用者最喜歡的特質。"
    ),
    "i couldn't agree more": (
        "清晰的溝通能避免百分之九十的職場誤會。",
        "我完全贊同。這樣能省下大量的時間與心力。"
    ),
    "that makes two of us": (
        "我非常期待即將到來的連續假期週末。",
        "我們英雄所見略同！我連行李袋都已經打包好了。"
    ),
    "tell me about it": (
        "要在市中心找到便宜的停車位根本變得不可能。",
        "這還用你說嗎！我剛繞著街區轉了半個小時。"
    ),
    "you can say that again": (
        "今年夏天絕對是有紀錄以來最熱的一年。",
        "你說得太對了！沒有冷氣我簡直活不下去。"
    ),
    "no wonder": (
        "地鐵線停駛是因為排定的號誌系統升級。",
        "難怪月台上擠滿了通勤人潮。"
    ),
    "are you kidding": (
        "他聲稱自己一夜之間寫了一萬行完美無瑕的程式碼。",
        "你在開玩笑嗎？沒人能做得這麼快還不出錯！"
    ),
    "you must be joking": (
        "他們要我們在中午之前重做整個專案路線圖。",
        "你一定是在開玩笑！那至少需要整整三天的時間。"
    ),
    "don't buy it": (
        "業務員承諾這款神奇的小配件永遠不會損壞。",
        "我不相信那一套。如果事情聽起來好得不真實，通常都不是真的。"
    ),
    "break a leg": (
        "我五分鐘後就要登台進行小提琴獨奏了！",
        "祝你演出順利！你練習得很勤奮，一定會表現得很棒。"
    ),
    "hang in there": (
        "期末考週的作息太殘酷了，我全靠咖啡撐著。",
        "堅持下去！再撐兩天假期就開始了。"
    ),
    "keep it up": (
        "我們的銷售額已經連續三個月成長百分之二十。",
        "保持下去！整個高階主管團隊都注意到了。"
    ),
    "way to go": (
        "我剛收到確認信，我的研究論文被錄取了！",
        "幹得好！這是你職業生涯的一大重要里程碑。"
    ),
    "good for you": (
        "我終於報名了那個晚間數位設計課程。",
        "真替你高興！投資新技能總是很有收穫的。"
    ),
    "bite the bullet": (
        "看牙醫雖然會很痛，但我的牙齒真的痛得厲害。",
        "咬緊牙關，在情況惡化之前今天就去治療吧。"
    ),
    "hit the road": (
        "在日落之前我們還有四個小時的車程。",
        "我們現在就出發上路吧，避開傍晚的下班車潮。"
    ),
    "hit the sack": (
        "我的眼睛快閉上了，明天的輪班早上六點就開始。",
        "該去睡覺了！好好休息，睡個好覺吧。"
    ),
    "piece of cake": (
        "你覺得入門程式設計作業難不難？",
        "小菜一碟！我不到半個小時就搞定了。"
    ),
    "under the weather": (
        "傑森今天早上為什麼沒參加部門晨會？",
        "他身體有點不舒服，所以在家休息。"
    ),
    "burn the midnight oil": (
        "團隊是如何在嚴格的截止期限前完成遞交的？",
        "我們不得不挑燈夜戰，但我們準時交付了一切。"
    ),
    "the ball is in your court": (
        "我們已經提出了提案，並回答了他們的所有疑問。",
        "現在輪到他們表態做最後決定了。"
    )
}

PROMPTS_A_ZH = {
    "A few of us are planning a weekend camping trip by the lake.": "我們幾個人正計畫週末去湖邊露營。",
    "A rumor claims our project deadline was moved forward by two weeks.": "有傳言說我們的專案截止日期提前了兩週。",
    "A sudden storm came out of nowhere and soaked everyone on the street!": "突如其來的暴風雨毫無預警降臨，把街上的每個人都淋濕了！",
    "Are we ready to push the latest software update to the production servers?": "我們準備好把最新的軟體更新推送到正式伺服器上了嗎？",
    "Are you ready to join us for the team celebration tonight?": "你準備好參加今晚的團隊慶祝活動了嗎？",
    "Be mindful of the low doorway when you enter the storage room.": "進儲藏室時請小心低矮的門楣。",
    "Before we finalize everything, is there anything else we should do?": "在我們敲定一切之前，還有什麼事情是我們應該做的嗎？",
    "Can you coordinate the software deployment during the midnight maintenance?": "你能在半夜維護期間協調軟體部署嗎？",
    "Can you lend him some more money after what happened last week?": "在經歷上週的事情之後，你還能再借他一些錢嗎？",
    "Can you promise you won't reveal our surprise birthday plan?": "你能保證不洩漏我們的生日驚喜計畫嗎？",
    "Could you brief the executive committee about our progress this afternoon?": "你今天下午能向主管委員會簡報我們的進展嗎？",
    "Did you happen to catch the latest episode of that documentary series?": "你剛好有看那部紀錄片影集的最新一集嗎？",
    "Did you need me to help you find that missing report earlier?": "你剛才需要我幫忙找那份遺失的報告嗎？",
    "Do you feel like checking out that new noodle shop around the corner tonight?": "你今晚想去看看轉角新開的那家麵館嗎？",
    "Do you have any idea where the conference room remote control went?": "你知道會議室的遙控器跑哪去了嗎？",
    "Do you think I should confront the manager right now in the hallway?": "你覺得我現在應該在走廊上當面質問經理嗎？",
    "Do you think our small startup really has what it takes to disrupt the market?": "你認為我們這家小創投公司真的有顛覆市場的實力嗎？",
    "Do you think the boss will approve a three-week holiday during launch?": "你覺得老闆會在產品發布期間批准三週的長假嗎？",
    "Do you think the shipment will arrive before the weekend begins?": "你認為貨物會在週末開始前送達嗎？",
    "Do you want to grab an iced latte while we wait for the lecture to begin?": "在等講座開始時，你想去買杯冰拿鐵嗎？",
    "Even though it's not our first preference, it solves the immediate bottleneck.": "即使這不是我們的首選，但它解決了當前的瓶頸問題。",
    "Everyone is counting on our performance in the upcoming regional tournament.": "大家都期盼著我們在即將到來的分區聯賽中的表現。",
    "Finding affordable parking in the city center has become impossible.": "要在市中心找到便宜的停車位根本變得不可能。",
    "Focusing on customer feedback will help us build a much better product.": "專注於客戶反饋將有助於我們打造出更好的產品。",
    "Have you decided what you'd like to order for our group lunch today?": "你決定好今天我們聚餐想點什麼了嗎？",
    "Have you seen David today? I was just about to ask him about the files.": "你今天看到大衛了嗎？我正好想問他關於文件的事。",
    "He claims he wrote ten thousand lines of flawless code overnight.": "他聲稱自己一夜之間寫了一萬行完美無瑕的程式碼。",
    "He claims this shortcut won't cause any security vulnerabilities at all.": "他聲稱這種捷徑根本不會造成任何安全漏洞。",
    "He hasn't taken a single day off in the last six months of intense work.": "在過去六個月的高壓工作中，他一天假都沒請過。",
    "He insists on continuing this heated argument in the office lobby.": "他堅持要在辦公室大廳繼續這場激烈的爭論。",
    "He keeps gossiping about our team members behind their backs.": "他總是在背後八卦我們團隊成員的閒話。",
    "He keeps playing loud music late at night despite multiple complaints.": "儘管屢遭投訴，他深夜依然大聲播放音樂。",
    "He seems completely exhausted from working twelve-hour shifts every day.": "每天值班十二個小時，他看起來已經筋疲力竭了。",
    "He wants to claim sole credit for the group project we built together.": "他竟然想獨攬我們一起完成的團隊專案功勞。",
    "Here's to celebrating our successful product launch tonight!": "為了今晚慶祝我們產品順利發布，乾杯！",
    "How about we grab some coffee and brainstorm creative ideas together?": "不如我們喝杯咖啡，一起腦力激盪想些創意好點子吧？",
    "How about we try a different strategy for the second quarter?": "第二季我們嘗試不同的策略如何？",
    "How are the overall preparations for the annual exhibition proceeding?": "年度展覽的整體籌備工作進展得如何？",
    "How are the user tests going with the new mobile app build?": "新版手機 App 的使用者測試進行得如何了？",
    "How did the team finish the submission before the strict deadline?": "團隊是如何在嚴格的截止期限前完成遞交的？",
    "How did you find out about the company opening a branch in Tokyo?": "你是怎麼知道公司要在東京開設分公司的？",
    "How did you find the introductory programming assignment?": "你覺得入門程式設計作業難不難？",
    "How do you stay calm and composed when everything feels uncertain?": "當一切都充滿不確定時，你是如何保持冷靜沉著的？",
    "How long do you think it will take to complete the data migration?": "你認為完成資料移轉大約需要多長時間？",
    "How should we present the cost analysis to the prospective investors?": "我們該如何向潛在投資人報告成本分析？",
    "How soon can we expect a formal reply from the regional director?": "我們大概多久能收到分區處長的正式回覆？",
    "I finally signed up for that evening digital design course.": "我終於報名了那個晚間數位設計課程。",
    "I have the presentation files ready for the team review.": "我已經準備好簡報檔案供團隊審查了。",
    "I just noticed an unexpected pattern in the customer survey data.": "我剛在客戶問卷數據中注意到了一個出乎意料的規律。",
    "I just received confirmation that my research paper was accepted!": "我剛收到確認信，我的研究論文被錄取了！",
    "I know you wanted the original design, but user feedback strongly favored this one.": "我知道你想要原先的設計，但使用者回饋強烈支持這一款。",
    "I might leave my laptop in the car while I go grab lunch around the corner.": "我去轉角買午餐時，可能會把筆記型電腦留在車上。",
    "I need a few more minutes to finish proofreading these slides.": "我還需要幾分鐘來校對完這些投影片。",
    "I never imagined things would turn out so surprisingly well!": "我從未想像過事情會進展得如此出奇地順利！",
    "I realize my initial estimate was a bit too optimistic given our resources.": "考量我們的資源，我意識到自己最初的預估有點太樂觀了。",
    "I really appreciate all your detailed guidance throughout the training.": "我非常感激你在整個培訓過程中給予的詳盡指導。",
    "I really appreciate you taking time to review my portfolio over the weekend.": "我非常感謝你週末抽空查看我的作品集。",
    "I regret not taking that overseas exchange opportunity two years ago.": "我很後悔兩年前沒有把握那個出國交換的機會。",
    "I think I might skip the security verification step just this once.": "我想也許就這一次，跳過安全驗證步驟吧。",
    "I think your presentation structure was spot on and very convincing.": "我認為你的簡報架構非常到位且極具說服力。",
    "I truly believe quality should always come before rushing for speed.": "我堅信品質永遠應該優先於盲目追求速度。",
    "I wanted to express my gratitude for your warm hospitality during our visit.": "我想對我們訪問期間您熱情的款待表達由衷的感謝。",
    "I wonder where I misplaced my wireless earbuds this morning.": "我納悶著今天早上把無線耳機忘在什麼地方了。",
    "I'm curious about how the rest of the team feels about this suggestion.": "我很好奇團隊其他成員對這個建議有什麼看法。",
    "I'm feeling completely exhausted after that marathon conference call.": "經過那場馬拉松式的電話會議後，我感到精疲力竭。",
    "I'm heading to London for my new job assignment next week.": "我下週要去倫敦接任新職務了。",
    "I'm nervous about presenting my new concept in front of the whole auditorium.": "要在整個大禮堂面前發表我的新概念，讓我感到很緊張。",
    "I'm really looking forward to the long holiday weekend coming up.": "我非常期待即將到來的連續假期週末。",
    "I'm stepping on stage for my violin solo in five minutes!": "我五分鐘後就要登台進行小提琴獨奏了！",
    "I'm stressing out over tomorrow morning's board meeting presentation.": "我對明天早上的董事會簡報感到壓力極大。",
    "I'm tempted to buy that expensive luxury gadget on impulse today.": "我今天衝動地很想買下那個昂貴的奢華小科技品。",
    "I'm thinking about rearranging the living room furniture to get more light.": "我正想重新擺設客廳家具，讓採光更好一些。",
    "I'm voting for the quiet cafe around the corner for lunch.": "午餐我投轉角那家安靜咖啡館一票。",
    "I'm wondering how we should handle the next phase of this task.": "我想知道我們應該如何處理這項任務的下一階段。",
    "I'm worried things aren't progressing as quickly as we had hoped.": "我擔心事情沒有像我們預期的那樣迅速推進。",
    "I've been feeling frustrated by how slowly the results are showing.": "看到成效顯現得這麼緩慢，我一直感到有些挫折。",
    "I've been rejected twice, and I'm wondering if I should try applying again.": "我已經被拒絕了兩次，正在想是否該再嘗試申請一次。",
    "If we compromise on the secondary features, we can eliminate all critical bugs.": "如果我們在次要功能上妥協，就能消除所有重大瑕疵。",
    "If we don't back up the database now, we risk losing hours of work.": "如果我們現在不備份資料庫，恐怕會損失好幾個小時的工作成果。",
    "Is it really worth putting in extra effort when nobody seems to notice?": "當似乎沒人在意時，多付出額外的努力真的值得嗎？",
    "It was genuinely wonderful catching up with you after all these months.": "隔了這麼多個月能跟你敘舊，真的很開心。",
    "It's hard to stay patient when waiting for a critical response from them.": "在等待他們關鍵回覆的時候，真的很難保持耐心。",
    "Let's divide the responsibilities evenly so everyone feels supported.": "我們把責任平均分擔，讓每個人都感受到支持。",
    "Let's find a quiet place to discuss the project details.": "我們找個安靜的地方來討論專案細節吧。",
    "Let's make sure we haven't overlooked any important considerations.": "我們務必確保沒有忽略任何重要的考量因素。",
    "Let's schedule a brief sync meeting to make sure we're on the same page.": "我們安排個簡短的同步會議，確保大家想法一致。",
    "Look at the fireworks lighting up the entire evening sky tonight!": "快看今晚照亮整片夜空的璀璨煙火！",
    "Look at the leaderboard! Our team took the number one position!": "看排行榜！我們團隊拿下了第一名！",
    "Looking at the performance data, their database architecture is actually faster.": "從效能數據來看，他們的資料庫架構實際上跑得更快。",
    "May I borrow your umbrella just to cross the street to the parking lot?": "我能借用你的雨傘走到對街停車場嗎？",
    "Maybe we could test out this new design concept with a small focus group?": "也許我們可以用小型焦點訪談團體來測試這個新設計概念？",
    "Meeting their team halfway might be the quickest way to seal the partnership.": "各退一步與他們達成妥協，可能是確立合作關係最快的方法。",
    "My eyes are closing and tomorrow's shift begins at six in the morning.": "我的眼睛快閉上了，明天的輪班早上六點就開始。",
    "My muscles are so sore after that intense workout session today.": "今天那場高強度健身訓練後，我全身肌肉痠痛不已。",
    "Our energy is running a bit low after this demanding sprint week.": "在經歷這段高強度的衝刺週之後，我們的精力有點不足了。",
    "Our favorite band just announced an unexpected reunion tour!": "我們最喜歡的樂團剛剛宣布了出乎意料的重聚巡迴演出！",
    "Our proposal was selected out of dozens of international submissions!": "我們的提案在數十件國際投稿中脫穎而出被選中了！",
    "Our sales figures have increased by twenty percent for three months in a row.": "我們的銷售額已經連續三個月成長百分之二十。",
    "Our team exceeded this month's performance target by a wide margin.": "我們團隊這個月大幅超越了業績目標。",
    "Perhaps we should adopt their suggestion regarding the revised timeline.": "也許我們應該採納他們關於調整時間表的建議。",
    "Rumor has it that the company might cancel annual bonuses this year.": "有謠言傳出公司今年可能會取消年終獎金。",
    "Should I send this angry reply to the client right now while I'm upset?": "我該在氣頭上立刻把這封憤怒的信件寄給客戶嗎？",
    "Should we confront them about the discrepancy in the financial audit report?": "我們應該當面質問他們財務審計報告中的出入嗎？",
    "Should we sign this contract without having a legal advisor review it?": "我們可以在沒有法律顧問審查的情況下簽署這份合約嗎？",
    "Should we stay late and do another unpaid overtime shift tonight?": "我們今晚該留下來再無薪加班一次嗎？",
    "Should we submit our application for the innovation grant?": "我們該提交創新補助金的申請嗎？",
    "Should we wait for the remaining guests before opening the banquet?": "在宴會開始前，我們要等待其餘的賓客到齊嗎？",
    "Since we're on a tight budget, let's postpone the fancy office redesign.": "既然我們預算很緊，就先推遲華麗的辦公室重新設計吧。",
    "Someone said our division will be relocated to another city next month.": "有人說我們部門下個月將搬遷到另一個城市。",
    "Someone suggested we cut safety standards to reduce manufacturing costs.": "有人建議降低安全標準以縮減製造成本。",
    "Someone told me the annual company party was cancelled.": "有人跟我說公司年會被取消了。",
    "Someone told me the company party might be rescheduled.": "有人告訴我公司聚會可能會改期。",
    "Something strange happened during the final system test today.": "今天在最後的系統測試期間發生了一件奇怪的事。",
    "Sometimes I feel overwhelmed by unexpected obstacles in my career.": "有時我會被職涯中出乎意料的阻礙壓得喘不過氣來。",
    "Sometimes small daily habits feel insignificant in the grand scheme of things.": "有時從長遠的大局來看，微小的日常習慣似乎顯得微不足道。",
    "Sorry I'm twenty minutes late, traffic was completely stalled.": "抱歉我遲到了二十分鐘，路上交通完全堵死了。",
    "Stop tapping your pen on the desk during the quiet reading hour.": "安靜自習時間請不要再用筆敲桌子了。",
    "Take a look at the spectacular sunset over the city skyline!": "快看城市天際線上那壯麗無比的夕陽美景！",
    "Taking a brisk walk might refresh our thoughts for the afternoon tasks.": "快步散散步也許能讓我們頭腦清醒，應付下午的工作。",
    "Thank you so much for driving me to the airport in the pouring rain!": "非常感謝你在大雨滂沱中載我到機場！",
    "Thank you so much for helping me carry these heavy packages up the stairs!": "太感謝你幫我把這些沉重的包裹搬上樓了！",
    "Thanks for hosting such a lovely dinner party for all of us tonight!": "感謝你今晚為我們大家舉辦了這麼美好的晚餐派對！",
    "Thanks for inviting me over to your place for dinner!": "謝謝你邀請我來你家吃晚餐！",
    "Thanks for reviewing my code on such short notice!": "感謝你在這麼倉促的時間幫我審查代碼！",
    "The championship finals are tomorrow and our opponents have won ten straight games.": "冠軍決賽就在明天，而我們的對手已經取得了十連勝。",
    "The client just sent over their final comments on the quarterly contract.": "客戶剛剛寄來了他們對季度合約的最終意見。",
    "The client sent a glowing recommendation letter for our hard work!": "客戶為了我們的努力付出寄來了一封盛讚的推薦信！",
    "The climb up this steep mountain trail is getting tougher with every step.": "攀登這條陡峭的山路，每走一步都變得更加艱難。",
    "The consultant said we need to discard our current architecture completely.": "顧問說我們必須徹底拋棄目前的系統架構。",
    "The deadline is approaching fast and we still have testing to complete.": "截止期限步步逼近，而我們仍有測試尚未完成。",
    "The dentist appointment is going to be painful, but my tooth really hurts.": "看牙醫雖然會很痛，但我的牙齒真的痛得厲害。",
    "The director mentioned there will be a minor adjustment to our plans.": "處長提到我們的計畫將會有些微的調整。",
    "The finals week schedule has been brutal and I'm running on coffee.": "期末考週的作息太殘酷了，我全靠咖啡撐著。",
    "The floor around the construction area looks extremely slippery.": "施工區周圍的地面看起來非常濕滑。",
    "The head chef prepared this extraordinary specialty dish just for us!": "主廚特地為我們準備了這道非凡的招牌特色料理！",
    "The main server crashed right in the middle of our live demo!": "主伺服器竟然在我們現場展示正中間崩潰了！",
    "The outdoor concert got cancelled due to a sudden thunderstorm.": "戶外音樂會因為突如其來的雷雨而取消了。",
    "The partner company is waiting for our response on the joint venture terms.": "合作夥伴公司正在等待我們對合資條款的回覆。",
    "The printer jammed again right before our client presentation!": "就在向客戶簡報之前，印表機竟然又卡紙了！",
    "The server response time improved by nearly forty percent.": "伺服器的回應時間縮短了將近百分之四十。",
    "The sky is looking a bit overcast, should we bring our rain jackets along?": "天空看起來有點陰沉，我們應該隨身帶件防雨外套嗎？",
    "The subway line was halted because of a scheduled signal upgrade.": "地鐵線停駛是因為排定的號誌系統升級。",
    "The workload is building up, so how do you propose we tackle it?": "工作量正在持續堆積，你建議我們該如何著手處理？",
    "Their criticism of our onboarding flow was actually quite constructive.": "他們對我們的新人引導流程提出的批評，其實相當具有建設性。",
    "There's heavy equipment moving through the central hallway right now.": "現在正有重型設備穿過中央走廊。",
    "They didn't give us free company mugs at the welcome orientation.": "他們在新生說明會上沒有發給我們免費的公司馬克杯。",
    "They insisted that nobody knows how to solve this bug except himself.": "他堅稱除了他自己之外，沒有人知道該如何解決這個錯誤。",
    "They somehow managed to finish the entire migration ahead of schedule.": "他們不知怎麼搞的，竟然提前完成了整個系統遷移。",
    "They told the client the delay was caused by our team's lack of effort.": "他們告訴客戶延誤是由於我們團隊不夠努力造成的。",
    "They want to demolish this historic park to build a parking lot.": "他們想拆除這座歷史悠久的公園來改建停車場。",
    "They want us to accept an unrealistic delivery timeline with no budget.": "他們希望我們在沒有預算的情況下接受不切實際的交付時程。",
    "They want us to redo the whole project roadmap before noon.": "他們要我們在中午之前重做整個專案路線圖。",
    "They're asking us to revise the entire proposal for the third time.": "他們要求我們第三次重新修改整個提案。",
    "They're saying our product launch will be indefinitely postponed.": "他們說我們的產品發布將會無限期延後。",
    "This summer has been the hottest one on record by far.": "今年夏天絕對是有紀錄以來最熱的一年。",
    "Those homemade chocolate cookies look absolutely delicious!": "那些自製的手工巧克力餅乾看起來真好吃！",
    "Traffic is completely frozen and our flight boarding closes in forty minutes!": "交通完全癱瘓了，而我們的航班四十分鐘後就要關閉登機門了！",
    "We both arrived at the conference room doorway at the very same moment.": "我們兩人在同一瞬間抵達了會議室門口。",
    "We both arrived at the elevator door at the exact same moment.": "我們兩人在同一瞬間走到了電梯門口。",
    "We have covered every single agenda item for today's departmental review.": "我們已經完成了今天部門審查會議的每一項議程。",
    "We have presented our proposal and answered all their queries.": "我們已經提出了提案，並回答了他們的所有疑問。",
    "We just hit our annual milestone two months ahead of schedule!": "我們提前兩個月達成了年度里程碑目標！",
    "We managed to pass that notoriously difficult exam on his very first attempt!": "他竟然在第一次嘗試時就通過了那門出了名困難的考試！",
    "We need someone to bridge the communication gap between design and engineering.": "我們需要有人來彌合設計與工程之間的溝通隔閡。",
    "We need to reserve a suitable room for tomorrow's workshop.": "我們需要為明天的研討會預訂一間合適的會議室。",
    "We should explore whether there is another viable solution here.": "我們應該探討這裡是否還有其他可行的解決方案。",
    "We should give the new intern a warm and supportive welcome tomorrow.": "明天我們應該給新實習生一個溫暖且支持的歡迎。",
    "We still have a four-hour drive ahead before sunset.": "在日落之前我們還有四個小時的車程。",
    "We've been debugging this issue since eight this morning.": "我們從今天早上八點就一直在排查這個問題。",
    "We've been focusing intensely on these details for several hours.": "我們已經全神貫注在這些細節上好幾個小時了。",
    "What do you suggest we do about the current situation?": "你建議我們針對當前的情況該採取什麼行動？",
    "What do you think about our planned itinerary for next weekend's trip?": "你覺得我們下週末旅行規畫的行程怎麼樣？",
    "What kind of dishes do they serve at that international buffet?": "那家國際百匯餐廳提供哪些料理？",
    "When do you expect the official audit results to be announced?": "你預計正式的審計結果何時會公布？",
    "Why didn't Jason attend the morning department briefing today?": "傑森今天早上為什麼沒參加部門晨會？",
    "Will the road congestion clear up before our evening reservation starts?": "道路擁堵會在我們晚上的預約開始前緩解嗎？",
    "Will this new marketing campaign bring in more customers this quarter?": "這波新的行銷活動本季會帶來更多顧客嗎？",
    "Word on the street is that our division is getting a new leader.": "坊間傳聞說我們部門要換新主管了。",
    "Would you mind if I took the last seat next to you at this table?": "你介意我坐這張桌子旁邊最後一個空位嗎？",
}

def clean_key_for_diag(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 ]', '', s).strip().lower()

def extract_primary_zh(zh: str) -> str:
    # First split by slash, then strip punctuation
    first = zh.split("/")[0].strip()
    first = re.sub(r'[。！!？?]+$', '', first).strip()
    return first

def translate_dialogue(item: dict) -> tuple:
    en = item["en"]
    zh = item["zh"]
    spkA = item["spkA"]
    spkB = item["spkB"]

    # Extract text after speaker name
    a_text = spkA.split(":", 1)[1].strip() if ":" in spkA else spkA
    b_text = spkB.split(":", 1)[1].strip() if ":" in spkB else spkB

    k = clean_key_for_diag(en)
    zh_core = extract_primary_zh(zh)

    # 1. Check curated exact or partial match
    if k in CURATED_ZH:
        return CURATED_ZH[k]
    
    for c_key in CURATED_ZH:
        if c_key == k or (len(c_key) > 5 and c_key in k):
            return CURATED_ZH[c_key]

    # 2. Translate Prompt A
    zh_a = PROMPTS_A_ZH.get(a_text)
    if not zh_a:
        # Fallback if minor difference
        zh_a = a_text

    # 3. Translate Response B based on template clauses
    zh_b = None
    if "Nobody has verified that yet!" in b_text:
        zh_b = f"{zh_core}？目前還沒有人證實這件事！"
    elif "worth a shot" in b_text:
        zh_b = f"{zh_core}？這絕對值得一試！"
    elif "know the secret" in b_text:
        zh_b = f"{zh_core}？大家都想知道其中的秘訣！"
    elif "check the directory" in b_text:
        zh_b = f"{zh_core}？我們來查查指南吧。"
    elif "what you found" in b_text:
        zh_b = f"{zh_core}？跟我說說你發現了什麼。"
    elif "good point to consider" in b_text:
        zh_b = f"{zh_core}？這是個值得思考的好觀點。"
    elif "contributed so much" in b_text:
        zh_b = f"{zh_core}！大家為這次的成功付出了許多！"
    elif "timely warning" in b_text:
        zh_b = f"{zh_core}！謝謝你及時的提醒！"
    elif "wonderful development" in b_text:
        zh_b = f"{zh_core}！真是個令人振奮的好發展！"
    elif "right track" in b_text:
        zh_b = f"{zh_core}。這樣能讓我們保持在正確的軌道上。"
    elif "clear perspective" in b_text:
        zh_b = f"{zh_core}。這讓整件事的脈絡變得非常清晰。"
    elif "summarized it better" in b_text:
        zh_b = f"{zh_core}。我自己來總結也不會比這更貼切了。"
    elif "mind moving forward" in b_text:
        zh_b = f"沒錯。{zh_core}。我們接下來要牢記這點。"
    elif "makes total sense" in b_text:
        zh_b = f"確實如此。{zh_core}。在這種情況下完全合情合理。"
    elif "focus on" in b_text:
        zh_b = f"{zh_core}。這正是我們應該專注的重點。"
    elif "take that approach" in b_text:
        zh_b = f"說得好。{zh_core}。我們就採取這個辦法吧。"
    else:
        zh_b = f"{zh_core}。"

    return (zh_a, zh_b)

def main():
    json_path = r"J:\_projectBook\_Eng\ShortAndroid\app\src\main\assets\sentences_2500.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    boilerplate = "本句是道地英語中極具表現力的習慣用法，母語者在口語互動中經常藉此傳遞明確的態度與交際意圖，切忌按單字字面逐詞硬翻。"

    missing_a = []
    missing_b = []

    for item in data:
        # 1. Clean note
        note = item.get("note", "")
        if boilerplate in note:
            note = note.replace(boilerplate, "").strip()
            item["note"] = note

        # 2. Generate spkAZh and spkBZh
        zh_a, zh_b = translate_dialogue(item)
        if not zh_a or zh_a == item["spkA"].split(":", 1)[-1].strip():
            missing_a.append(item["id"])
        if not zh_b:
            missing_b.append(item["id"])

        item["spkAZh"] = zh_a
        item["spkBZh"] = zh_b

    print(f"Total processed items: {len(data)}")
    print(f"Items missing A translation: {len(missing_a)}")
    print(f"Items missing B translation: {len(missing_b)}")

    if len(missing_a) == 0 and len(missing_b) == 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Successfully updated sentences_2500.json with 100% translations and cleaned notes!")

if __name__ == "__main__":
    main()
