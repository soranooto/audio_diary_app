from django.shortcuts import render, redirect, get_object_or_404
from .models import AudioDiary, Profile
from .forms import AudioDiaryForm, ProfileForm


# 🎧 日記一覧
def diary_list(request):
    order = request.GET.get('order', 'new')
    mood_filter = request.GET.get('mood')

    diaries = AudioDiary.objects.all()

    if mood_filter:
        diaries = diaries.filter(mood=mood_filter)

    if order == 'old':
        diaries = diaries.order_by('created_at')
    else:
        diaries = diaries.order_by('-created_at')

    return render(request, 'diary/diary_list.html', {
        'diaries': diaries,
        'order': order,
        'mood_filter': mood_filter,
        'diary_model': AudioDiary,
    })


# ✏️ 新しい音声日記作成
def diary_create(request):
    print("✅ diary_create が呼ばれました")
    print("📄 使用中テンプレート: diary/diary_create.html")  # ← この行を追加！

    from .models import Profile  # ← 念のため明示的にインポート

    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'username': request.user.username or 'ゲスト'}
        )
    else:
        profile = Profile(username="ゲスト")

    if request.method == 'POST':
        form = AudioDiaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('diary:diary_list')
    else:
        form = AudioDiaryForm()

    print("💡 渡しているprofile:", profile.username)  # ←これを追加

    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'diary/diary_create.html', context)



    




# 📖 日記詳細
def diary_detail(request, pk):
    diary = get_object_or_404(AudioDiary, pk=pk)
    return render(request, 'diary/diary_detail.html', {'diary': diary})


# 🧸 マイページ表示
def mypage(request):
    user = request.user  # ← ログイン中のユーザーを取得

    # ログインしていない場合はゲスト扱い
    if not user.is_authenticated:
        return render(request, 'diary/mypage.html', {
            'profile': None,
            'guest': True,
        })

    # プロフィールがまだなければ作成
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={'username': user.username or 'ゲスト', 'status_message': 'ようこそ！'}
    )

    return render(request, 'diary/mypage.html', {'profile': profile})



# 🪞 プロフィール編集ビュー
def edit_profile(request):
    profile = Profile.objects.first()  # ← 修正

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # ← 修正
        if form.is_valid():
            form.save()
            return redirect('diary:mypage')
    else:
        form = ProfileForm(instance=profile)  # ← 修正

    return render(request, 'diary/edit_profile.html', {'form': form})


# 🤖💬 chatbot
def sticker_page(request):
    return render(request, 'diary/sticker_page.html')

def settings_page(request):
    return render(request, 'diary/settings.html')

def chatbot_page(request):
    return render(request, 'diary/chatbot.html')

from django.shortcuts import render
from django.http import JsonResponse
import json

# 💬 Chatbotページ表示
def chatbot_page(request):
    # 👤 プロフィールを取得（ログイン中かどうかで分岐）
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'username': request.user.username or 'ゲスト'}
        )
    else:
        # 未ログインの場合は、仮のプロフィールを表示
        profile = Profile(username="ゲスト")

    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()
        reply = generate_music_reply(user_message)
        return JsonResponse({"reply": reply})

    # 👇 ここで profile をテンプレートに渡す！
    return render(request, "diary/chatbot.html", {"profile": profile})



# 🎵 Django内ロジックで返答を作る関数（改良版）
def generate_music_reply(message):
    message = message.lower()  # 英語対応用（例: happy, sad）

    # 🌧️ 悲しい・寂しい系
    if any(word in message for word in ["悲しい", "さみしい", "失恋", "泣きたい", "落ち込む", "lonely", "sad"]):
        return "🌧️ そんな時はAimerの『Ref:rain』や優里の『ドライフラワー』を聴いてみて。そっと寄り添ってくれる曲だよ。"

    # 😄 明るい・楽しい・ハッピー系
    elif any(word in message for word in ["楽しい", "ハッピー", "うれしい", "笑顔", "happy", "わくわく"]):
        return "☀️ いいね！YOASOBIの『ハルカ』やback numberの『アイラブユー』なんかも気分が上がるよ！"

    # 💡 曲のおすすめを聞かれた時
    elif any(word in message for word in ["おすすめ", "何聴けば", "曲教えて", "いい曲", "リコメンド", "suggest"]):
        return "💡 最近話題なのは藤井風の『grace』とadoの『Value』！どっちも心に響くよ。"

    # 😴 眠い・リラックス系
    elif any(word in message for word in ["眠い", "ねむ", "リラックス", "落ち着きたい", "まったり", "chill", "sleep"]):
        return "🌙 Lo-Fi Beatsやピアノジャズが合いそう。Spotifyの『夜の読書』プレイリストもおすすめ。"

    # 🔥 元気・テンション上げたい系
    elif any(word in message for word in ["元気", "テンション", "盛り上がる", "ノリノリ", "energy", "頑張りたい"]):
        return "🔥 King Gnuの『SPECIALZ』やMrs. GREEN APPLEの『ダンスホール』でテンション爆上がり！"

    # 💔 失恋・別れ
    elif any(word in message for word in ["失恋", "別れた", "会いたい", "恋", "ラブソング"]):
        return "💔 心が痛いね…。ヨルシカの『ただ君に晴れ』やback numberの『ハッピーエンド』が心に沁みるよ。"

    # 🌸 春・季節・自然
    elif any(word in message for word in ["春", "桜", "花見", "春っぽい", "春の曲"]):
        return "🌸 春ならスピッツの『チェリー』やいきものがかりの『SAKURA』がぴったり！"

    # ☀️ 夏っぽい
    elif any(word in message for word in ["夏", "海", "暑い", "サマー", "祭り"]):
        return "🏖️ 夏にはPerfumeの『ポリリズム』やあいみょんの『マリーゴールド』が合うよ！"

    # 🍁 秋・冬
    elif any(word in message for word in ["秋", "冬", "寒い", "雪", "紅葉"]):
        return "🍂 秋冬には宇多田ヒカルの『First Love』やレミオロメンの『粉雪』がしっとりくるね。"

    # 💗「好き」や感謝
    elif "好き" in message:
        return "💗 素敵！そのアーティストのどの曲が一番好き？語ろう🎶"
    elif "ありがとう" in message or "感謝" in message:
        return "😊 どういたしまして！また音楽の話をしようね🎵"

    # 🎧 勉強・作業中
    elif any(word in message for word in ["勉強", "集中", "作業", "仕事", "study", "work"]):
        return "📚 作業中なら、YOASOBIの『たぶん』とか、Lo-Fi HipHopが集中力UPにおすすめ！"

    # 🚗 移動・ドライブ
    elif any(word in message for word in ["ドライブ", "車", "旅", "出かける", "お出かけ"]):
        return "🚗 ドライブには、Official髭男dismの『I LOVE...』やback numberの『高嶺の花子さん』が合うよ！"

    # 🌧️ 雨の日
    elif any(word in message for word in ["雨", "梅雨", "しとしと", "rainy"]):
        return "☔ 雨の日は秦基博の『Rain』やスキマスイッチの『奏』を聴きながらのんびりしてみて。"
    
    # 🎻 クラシック作曲家関連
    elif any(word in message for word in [
        "ベートーヴェン", "モーツァルト", "ショパン", "バッハ", "ドビュッシー", "ラヴェル",
        "リスト", "シューベルト", "ブラームス", "メンデルスゾーン", "ハイドン",
        "チャイコフスキー", "ラフマニノフ", "プロコフィエフ", "ストラヴィンスキー",
        "シューマン", "サティ", "マーラー", "ブルックナー", "ワーグナー", "ヴィヴァルディ",
        "パッヘルベル", "ホルスト", "サン＝サーンス", "グリーグ", "ドヴォルザーク",
        "ラフマニノフ", "フォーレ", "プッチーニ", "ヴェルディ", "ビゼー", "ヘンデル"
    ]):
        composers = {
            "バッハ": "🎻 ヨハン・セバスチャン・バッハは『音楽の父』。対位法の達人で『G線上のアリア』や『平均律クラヴィーア曲集』が有名！",
            "ヘンデル": "🎺 ヘンデルは同時代の作曲家で、荘厳な『ハレルヤ』が有名。オラトリオの巨匠だよ。",
            "ハイドン": "🎶 ハイドンは『交響曲の父』。モーツァルトやベートーヴェンにも影響を与えたよ。",
            "モーツァルト": "🎹 モーツァルトは天才作曲家。軽やかで完璧なバランスの曲が特徴。『魔笛』や『トルコ行進曲』が人気！",
            "ベートーヴェン": "🎼 ベートーヴェンは情熱の人。『運命』や『第九』で知られ、古典派とロマン派の架け橋的存在。",
            "シューベルト": "🎵 シューベルトは歌曲の王様。『魔王』や『野ばら』など、人の感情を美しく描いたよ。",
            "シューマン": "🎹 シューマンは詩的なロマン派作曲家。『子供の情景』や『トロイメライ』が有名。",
            "ブラームス": "🎻 ブラームスはロマン派後期の巨匠。『交響曲第1番』や『子守唄』で知られてるよ。",
            "メンデルスゾーン": "🌿 メンデルスゾーンは爽やかで優雅な作風。『真夏の夜の夢』の“結婚行進曲”は有名だね。",
            "リスト": "🔥 リストはピアノの超絶技巧王！『ラ・カンパネラ』や『愛の夢』は必聴。",
            "ショパン": "🎵 ショパンはピアノの詩人。ノクターン、ワルツ、エチュードなど、どれも感情豊か。",
            "チャイコフスキー": "🎠 チャイコフスキーはロシアの巨匠。『白鳥の湖』『くるみ割り人形』などバレエ音楽が有名！",
            "ラフマニノフ": "🎹 ラフマニノフはロマン派の終焉を飾る作曲家。『ピアノ協奏曲第2番』は映画でもよく使われるね。",
            "ドビュッシー": "🌊 ドビュッシーは印象派の作曲家。『月の光』や『海』は音の絵画のよう。",
            "ラヴェル": "🎠 ラヴェルはフランス印象派。『ボレロ』や『亡き王女のためのパヴァーヌ』が有名。",
            "サティ": "🕯️ サティは不思議な雰囲気の作曲家。『ジムノペディ』の静けさが心地いいね。",
            "マーラー": "🌌 マーラーは壮大な交響曲作家。『交響曲第5番』の“アダージェット”は美しすぎる名曲。",
            "ブルックナー": "⛪ ブルックナーは荘厳な交響曲で知られる。教会音楽のような神聖さが魅力。",
            "ワーグナー": "⚔️ ワーグナーはオペラの革命児。『ニーベルングの指環』など壮大な作品が多いよ。",
            "ヴィヴァルディ": "🎻 ヴィヴァルディはバロック期の作曲家。『四季』は誰もが一度は聴いたことある名曲！",
            "パッヘルベル": "🎼 パッヘルベルの『カノン』は結婚式の定番。和声の美しさが永遠。",
            "ホルスト": "🪐 ホルストは『惑星』で知られる。特に“木星”は壮大で感動的！",
            "サン＝サーンス": "🦁 サン＝サーンスはフランスの作曲家。『動物の謝肉祭』や『白鳥』が親しまれているよ。",
            "グリーグ": "🌲 グリーグは北欧の作曲家。『ペール・ギュント』の“朝”が特に有名。",
            "ドヴォルザーク": "🌍 ドヴォルザークはチェコ出身。『新世界より』は世界中で愛される名曲！",
            "フォーレ": "🌙 フォーレはフランスの作曲家で『夢のあとに』や『レクイエム』が有名。",
            "プッチーニ": "🎭 プッチーニはオペラ作曲家。『トスカ』や『蝶々夫人』は感動的な名作！",
            "ヴェルディ": "🎬 ヴェルディはオペラの巨匠。『アイーダ』『椿姫』など劇的で情熱的！",
            "ビゼー": "💃 ビゼーは『カルメン』で知られる作曲家。情熱的でリズミカルな音楽が魅力！",
            "プロコフィエフ": "🎭 プロコフィエフは20世紀ロシアの作曲家。『ロメオとジュリエット』や『ピーターと狼』が有名！",
            "ストラヴィンスキー": "🔥 ストラヴィンスキーは『春の祭典』で音楽界に革命を起こしたね！",
        }
        for name, text in composers.items():
            if name in message:
                return text
        return "🎶 クラシック作曲家の話かな？バッハ、ショパン、ラヴェル、チャイコフスキーなど、誰が気になる？"


    # 🎼 音楽記号・理論系
    elif any(word in message for word in [
        "forte", "piano", "crescendo", "diminuendo", "decrescendo", "アレグロ", "モデラート", "アンダンテ", "アダージョ", "プレスト",
        "rit", "リタルダンド", "accel", "アッチェレランド", "スタッカート", "レガート", "テヌート",
        "♯", "♭", "♮", "トリル", "フェルマータ", "ダ・カーポ", "D.C.", "D.S.", "コーダ", "セーニョ",
        "メゾフォルテ", "メゾピアノ", "スフォルツァンド", "fp", "sf", "拍子", "4/4", "3/4", "2/4", "拍", "テンポ"
    ]):
        if "forte" in message or "f" in message:
            return "🎺 forte（フォルテ）は『強く』の意味。対になるのはpiano（弱く）！"
        elif "piano" in message or "p" in message:
            return "🎹 piano（ピアノ）は『弱く』の意味。楽器名としても使われるけど、記号では音量を表すんだ。"
        elif "mezzo" in message or "メゾフォルテ" in message or "メゾピアノ" in message:
            return "🎵 mezzo（メゾ）は『やや』という意味。mezzo-forteは『やや強く』、mezzo-pianoは『やや弱く』だよ。"
        elif "sf" in message or "スフォルツァンド" in message:
            return "💥 sforzando（スフォルツァンド）は『その音を特に強く』というアクセント記号！"
        elif "fp" in message:
            return "🎺 fp（フォルテピアノ）は『強く弾いてすぐ弱く』。古典派の音楽に多い表現だよ。"
        elif "crescendo" in message:
            return "🎶 crescendo（クレッシェンド）は『だんだん強く』。< の形で表すよ。"
        elif "diminuendo" in message or "decrescendo" in message:
            return "🎵 diminuendo（ディミヌエンド）は『だんだん弱く』。> の形で書かれるね。"
        elif "アレグロ" in message or "allegro" in message:
            return "🏃 Allegro（アレグロ）は『速く・快活に』というテンポ記号。生き生きとした演奏を意味するよ。"
        elif "モデラート" in message or "moderato" in message:
            return "🚶 Moderato（モデラート）は『中くらいの速さで』という意味。穏やかなテンポ。"
        elif "アンダンテ" in message or "andante" in message:
            return "🚶‍♀️ Andante（アンダンテ）は『歩くような速さで』というテンポ記号。穏やかな印象だよ。"
        elif "アダージョ" in message or "adagio" in message:
            return "🌙 Adagio（アダージョ）は『ゆっくりと』。静かで落ち着いた雰囲気の曲に使われるよ。"
        elif "プレスト" in message or "presto" in message:
            return "⚡ Presto（プレスト）は『とても速く』。エネルギッシュな終盤などでよく出てくるね。"
        elif "rit" in message or "リタルダンド" in message:
            return "⏳ rit.（リタルダンド）は『だんだん遅く』。曲の締めくくりに多い表現。"
        elif "accel" in message or "アッチェレランド" in message:
            return "🏃‍♂️ accel.（アッチェレランド）は『だんだん速く』。クレッシェンドと組み合わせて盛り上げることもあるよ。"
        elif "スタッカート" in message or "staccato" in message:
            return "🎈 Staccato（スタッカート）は『音を短く切って』。点のような記号で表すよ。"
        elif "レガート" in message or "legato" in message:
            return "🎵 Legato（レガート）は『なめらかに』音をつなげて弾くこと。スラーで表すよ。"
        elif "テヌート" in message or "tenuto" in message:
            return "🎻 Tenuto（テヌート）は『音を十分に保って』。線（―）で示されることが多いね。"
        elif "トリル" in message or "trill" in message:
            return "✨ Trill（トリル）は『主音とその隣の音を細かく交互に演奏する』装飾音。バロック音楽でよく使われるよ。"
        elif "フェルマータ" in message or "fermata" in message:
            return "⏸️ フェルマータは『音を伸ばす』記号。上に弧と点がついたマークだよ。"
        elif "ダ・カーポ" in message or "D.C." in message:
            return "🔁 D.C.（ダ・カーポ）は『最初に戻る』の意味。反復記号の一種だよ。"
        elif "D.S." in message or "セーニョ" in message:
            return "🔁 D.S.（ダル・セーニョ）は『セーニョ記号まで戻る』。スコア内で繰り返す時に使うよ。"
        elif "コーダ" in message or "coda" in message:
            return "🎯 Coda（コーダ）は『曲の終結部』を意味する。D.S.やD.C.とセットで使われるね。"
        elif "♯" in message:
            return "♯（シャープ）は音を半音上げる記号だよ。例えばC♯はCより半音高い音。"
        elif "♭" in message:
            return "♭（フラット）は音を半音下げる記号。B♭などは吹奏楽でもよく見るね。"
        elif "♮" in message:
            return "♮（ナチュラル）は『元の音に戻す』記号。♯や♭を一時的に解除するよ。"
        elif "拍子" in message or "4/4" in message or "3/4" in message or "2/4" in message:
            return "🕐 拍子はリズムの基本単位。4/4拍子は『1小節に4拍で、4分音符が1拍』を意味するよ。"
        elif "拍" in message:
            return "🥁 拍（はく）は音楽のリズムを刻む最小単位。メトロノームの『カチッ』が1拍だよ。"
        elif "テンポ" in message:
            return "🎵 テンポは曲の速さのこと。BPM（Beats Per Minute）で数値化されるよ。"
        else:
            return "🎼 音楽記号の話だね。例えば『crescendo（だんだん強く）』や『rit.（だんだん遅く）』など、色んな表現があるよ。"

    # 🎶 コード進行・調性・和声理論系
    elif any(word in message for word in [
        "コード", "進行", "和音", "ドミナント", "トニック", "サブドミナント", 
        "Ⅰ", "Ⅳ", "Ⅴ", "ⅱ", "Ⅵ", "Ⅲ", "Ⅶ",
        "メジャー", "マイナー", "長調", "短調", "調性", "転調", "モード",
        "ハーモニー", "分散和音", "アルペジオ", "カデンツァ", "終止", "解決"
    ]):
        if "トニック" in message or "Ⅰ" in message:
            return "🎵 トニック（Ⅰ）は『主和音』。曲の中心になる安定した和音で、ド・ミ・ソ（Cメジャー）などが代表だよ。"
        elif "サブドミナント" in message or "Ⅳ" in message:
            return "🎶 サブドミナント（Ⅳ）は『下属和音』。少し柔らかく広がる印象で、トニックに向かう途中に使われるよ。"
        elif "ドミナント" in message or "Ⅴ" in message:
            return "🔥 ドミナント（Ⅴ）は『属和音』。トニックに戻る力が強く、音楽に緊張と解決を生むよ。"
        elif "ⅱ" in message:
            return "🎻 Ⅱ（ツー）は『下属調の代理』としてよく使われるコード。Ⅱ→Ⅴ→Ⅰの進行は「ツー・ファイブ・ワン進行」！"
        elif "Ⅵ" in message or "Ⅵm" in message:
            return "🎹 Ⅵ（シックス）は『トニックの代理』としてよく登場。切なさや安定感を出せるコードだよ。"
        elif "Ⅲ" in message:
            return "🎼 Ⅲはメジャーだと明るく上昇感を出すコード、マイナーだと哀愁を感じさせる響き。"
        elif "Ⅶ" in message:
            return "🎶 Ⅶは導音を含む和音で、トニックへの解決を強く促すコードだよ。"
        elif "コード進行" in message or "進行" in message:
            return "🎸 コード進行は和音の流れのこと。Ⅰ→Ⅳ→Ⅴ→Ⅰ や Ⅵ→Ⅳ→Ⅰ→Ⅴ（王道進行）などが有名だね！"
        elif "和音" in message:
            return "🎵 和音（コード）は複数の音を同時に鳴らしたもの。3つなら三和音（トライアド）、4つなら四和音（セブンスコード）だよ。"
        elif "ハーモニー" in message:
            return "🎶 ハーモニーは和音の響き全体のこと。旋律と合わせて曲の表情を作る大切な要素だよ。"
        elif "アルペジオ" in message or "分散和音" in message:
            return "🎹 アルペジオ（分散和音）は和音の音を順番に弾く奏法。ピアノやギターでよく使われるね。"
        elif "カデンツァ" in message or "終止" in message:
            return "🎼 カデンツァ（終止）はフレーズの締め方のこと。Ⅴ→Ⅰ（ドミナント終止）が最も強い解決感を持つよ。"
        elif "解決" in message:
            return "✨ 和声における『解決』は、不安定な和音（Ⅴなど）が安定した和音（Ⅰ）に進むことを指すよ。"
        elif "転調" in message:
            return "🔁 転調は曲の途中で調（キー）を変えること。雰囲気を変えたり盛り上げたりする効果があるよ。"
        elif "メジャー" in message or "長調" in message:
            return "🌞 メジャー（長調）は明るい響きが特徴。Cメジャーはピアノの白鍵だけで弾ける基本のスケールだよ。"
        elif "マイナー" in message or "短調" in message:
            return "🌙 マイナー（短調）は少し悲しげで切ない響き。AマイナーはCメジャーと同じ音階を使うんだ。"
        elif "モード" in message:
            return "🌀 モードとは『旋法』のこと。ドリアンやリディアンなど、スケールごとに独特の雰囲気があるよ。"
        elif "調性" in message:
            return "🎼 調性は『どの音を基準にした曲か』を表す。Cメジャーならハ長調、Aマイナーならイ短調だよ。"
        else:
            return "🎵 和声理論の話かな？トニック・サブドミナント・ドミナントの関係を知ると、曲作りが一気に楽しくなるよ！"

    # 🎧 音楽ジャンル・スタイル系
    elif any(word in message for word in [
        "ジャズ", "ボサノヴァ", "ロック", "ポップス", "クラシック", "バロック", "ルネサンス",
        "ヒップホップ", "ラップ", "r&b", "ソウル", "ブルース", "メタル", "パンク",
        "オルタナ", "フォーク", "カントリー", "テクノ", "ハウス", "トランス", "エレクトロ",
        "ローファイ", "レゲエ", "サンバ", "タンゴ", "ワルツ", "オペラ"
    ]):
        if "ジャズ" in message:
            return "🎷 ジャズは即興演奏が魅力のジャンル。ブルーノートやスウィング感が特徴だよ。ビル・エヴァンスやマイルス・デイヴィスは必聴！"
        elif "ボサノヴァ" in message:
            return "🌴 ボサノヴァはブラジル発祥の音楽で、サンバとジャズを融合させたおしゃれなリズムが特徴。『イパネマの娘』が代表曲だよ。"
        elif "ロック" in message:
            return "🎸 ロックはエレキギターを中心としたエネルギッシュな音楽。ビートルズやクイーン、B'zなど多彩なスタイルがあるよ。"
        elif "ポップス" in message:
            return "🎤 ポップスは親しみやすいメロディと歌詞が特徴。時代や国によってスタイルがどんどん変化してるよ。"
        elif "クラシック" in message:
            return "🎻 クラシック音楽は西洋音楽の伝統。バロック・古典派・ロマン派・近代などの時代ごとに特徴があるよ。"
        elif "バロック" in message:
            return "🏛️ バロック音楽は1600〜1750年頃の音楽。バッハやヘンデルが代表で、対位法や装飾音が多いのが特徴！"
        elif "ルネサンス" in message:
            return "🕊️ ルネサンス音楽は多声音楽が発展した時代。パレストリーナやジョスカン・デ・プレが有名だよ。"

    # 🧪 ネットスラング辞書
    net_slang = {
        "草不可避": "草不可避ｗ",
        "草生える": "wwwww",
        "草枯れる": "枯れたｗ",
        "大草原": "草ァ！",
        "草野郎": "草野郎ｗ",
        "草ァ！": "草ァｗｗ",
        "草ァ": "草ァ！！",
        "草": "www",
        "ぬるぽ": "ｶﾞｯ"
    }

    # 追加スラングもupdate
    net_slang.update({
        "既視感": "デジャヴ…？",
        "初見": "初見さんいらっしゃい！",
        "仕様": "仕様です（白目）",
        "草原": "大草原ｗ",
        "ぐうかわ": "ぐうの音も出ないほどかわいい",
        "ぐう聖": "ぐう聖…まじ尊敬",
        "ぐう畜": "ぐう畜ｗｗｗ",
        "はぇ〜": "はぇ〜すっごい…",
        "ほーん": "ほーん、それで？",
        "なるほど": "なるほどな〜",
        "ま？": "まじ？",
        "マ？": "マ？草",
        "マジ？": "マジか…！",
        "せやかて": "せやかて工藤",
        "あざす": "あざっす！",
        "ありがと": "ありがと〜！",
        "ありがとう": "ありがとうやで！",
        "ぶっちゃけ": "ぶっちゃけすぎｗ",
        "正直": "正直わかる",
        "ワイ": "ワイもやで",
        "ぼく": "ぼくも〜",
        "俺": "俺もそう思うわ",
        "にゃん": "にゃ〜ん🐱",
        "草ァァ": "草ァァァ！！！",
        "尊死": "尊死……わかる……",
        "てえてぇ": "てえてぇ……尊い……",
        "卍": "卍って感じやな",
        "激寒": "激寒やんｗ",
        "きも": "きもいってｗ",
        "は？": "は？？？？？",
        "おこ": "おこなの？ｗ",
        "ぷん": "ぷんぷん！",
        "ずるい": "ずるいわそれ…",
        "ねむ": "寝ろｗ",
        "だる": "だるすぎｗ",
        "ひま": "暇なん？ｗ",
        "わら": "わらったｗ",
        "おもろ": "おもろｗ",
        "今北産業": "まとめてくれてありがとうｗ",
        "kwsk": "詳しく！",
        "乙": "乙！",
        "ワクテカ": "ワクテカワクテカｗ",
        "ワクワク": "楽しみすぎるｗ"
    })

    # メッセージにスラングが含まれていれば返す
    for slang, reply in net_slang.items():
        if slang in message:
            return reply

    # 🎧 その他（デフォルト）
    else:
        return "🎵 音楽って不思議だよね。クラシックの話もポップスの話もできるよ。気になる曲や作曲家を教えて！"

